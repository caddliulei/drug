# coding=utf-8
import re
import os
import math
import cPickle
import multiprocessing as mp
import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.DataStructs import TanimotoSimilarity
from celery import shared_task
from works.models import AutoDock, AutoDock2, VirtualScreen, VirtualScreen2, Screen
from drug.settings import BASE_DIR, vina_path, TARGET_FOLDER_BASE, drugdb

# from perform import gen_user_db_qt_smiles

FP_PARAM = {
    'topological_hashed': {
        "mean": 0.000026936641120031898,
        "sd": 0.00398734520007183,
        "sd_exp": 0.5145149536573593,
        "tc": 0.66,
        "fp_func": lambda m: AllChem.GetHashedTopologicalTorsionFingerprint(m)
    },
    'atompair_hashed': {
        "mean": 0.00002541280101763038,
        "sd": 0.003864080986890242,
        "sd_exp": 0.5118760617288712,
        "tc": 0.61,
        "fp_func": lambda m: AllChem.GetHashedAtomPairFingerprint(m)
    },
    'maccs': {
        "mean": 0.00003686608558399457,
        "sd": 0.00484043909504593,
        "sd_exp": 0.5199608769322853,
        "tc": 0.88,
        "fp_func": lambda m: AllChem.GetMACCSKeysFingerprint(m)
    },
    'morgan_hashed': {
        "mean": 0.00002318732496154415,
        "sd": 0.003829515743309366,
        "sd_exp": 0.5101931872278405,
        "tc": 0.65,
        "fp_func": lambda m: AllChem.GetHashedMorganFingerprint(m, 2)
    }
}


def raw_score(target_mol_pkl, mol_fp, cutoff):
    # try:
    sim_list = list()
    for el_fp in target_mol_pkl:
        sim = TanimotoSimilarity(mol_fp, el_fp)
        if sim >= cutoff:
            sim_list.append(sim)
    rawscore = sum(sim_list)
    if rawscore > 0:
        return round(rawscore, 3)
    return None


def z_score(rs, size, mean, sd, sd_exp):
    return (rs - size * mean) / (sd * size ** sd_exp)


def p_value(z):
    x = -math.exp(-z * math.pi / math.sqrt(6) - 0.577215665)
    if z > 28:
        return -(x + x ** 2 / 2 + x ** 3 / 6)
    else:
        return 1 - math.exp(x)


def pred(smiles, target_list):
    result = list()
    try:
        mol = Chem.MolFromSmiles(smiles)
    except:
        # todo: invalid rdkit molecule
        print 'invalid smiles'
        return None
    # for fp_name, fp_parm in FP_PARAM.iteritems():
    #     mol_fp = fp_parm['fp_func'](mol)
    #     print fp_name
    #     fp_result = dict()
    fp_dict = dict()
    for fp_name, fp_param in FP_PARAM.iteritems():
       fp_dict[fp_name] = fp_param['fp_func'](mol)

    for idx, chembl_id in enumerate(target_list):
        # print idx
        target_result = dict()
        for fp_name, fp_param in FP_PARAM.iteritems():
            mol_fp = fp_dict[fp_name]
            target_mol_pkl = cPickle.load(open(os.path.join(TARGET_FOLDER_BASE, fp_name, chembl_id), 'r'))
            rs = raw_score(target_mol_pkl, mol_fp, fp_param['tc'])
            if rs:
                zscore = z_score(rs, len(target_mol_pkl), fp_param['mean'], fp_param['sd'], fp_param['sd_exp'])
                pvalue = p_value(zscore)
                target_result[fp_name] = pvalue

        if target_result:
            target_result['chembl_id'] = chembl_id
            result.append(target_result)
    return result


def dock_status(work_name, status):
    work = AutoDock.objects.get(work_name=work_name)
    work.status = status
    work.save()


def dock_out(work_name, out_path):
    work = AutoDock.objects.get(work_name=work_name)
    work.out_path = out_path
    work.save()


def dock_affinity(work_name, affinity):
    work = AutoDock.objects.get(work_name=work_name)
    work.affinity = affinity
    work.save()


def dock2_status(work_name, status):
    work = AutoDock2.objects.get(work_name=work_name)
    work.status = status
    work.save()


def dock2_out(work_name, out_path):
    work = AutoDock2.objects.get(work_name=work_name)
    work.out_path = out_path
    work.save()


def dock2_affinity(work_name, affinity):
    work = AutoDock2.objects.get(work_name=work_name)
    work.affinity = affinity
    work.save()


def screen_status(work_name, status):
    work = VirtualScreen.objects.get(work_name=work_name)
    work.status = status
    work.save()


def screen2_status(work_name, status):
    work = VirtualScreen2.objects.get(work_name=work_name)
    work.status = status
    work.save()


def gen_user_db_qt_smiles(input_file, output_path):
    """
    处理用户上传的数据库
    :param input_file:
    :param output_path:
    :return:
    """
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    sdf = Chem.SDMolSupplier(input_file.encode('utf-8'))
    sdf = [n for n in sdf if n is not None]
    smiles = []
    for mol in sdf:
        name = mol.GetProp('_Name'.encode('utf-8'))
        name = name + '.pdb'.encode('utf-8')
        mol_path = os.path.join(output_path, name)
        Chem.MolToPDBFile(mol=mol, filename=mol_path.encode('utf-8'))
        smile = Chem.MolToSmiles(mol)
        smiles.append([name, smile])
    df = pd.DataFrame(smiles)
    smiles_file = os.path.join(output_path, 'smiles.csv')
    df.to_csv(smiles_file, index=False, header=False, encoding='utf-8')

    pdblst = os.listdir(output_path)
    pdblst = [pdb for pdb in pdblst if pdb.endswith('.pdb')]
    for pdb in pdblst:
        pdb_path = os.path.join(output_path, pdb)
        os.system("python %s/extra_apps/vina/prepare_ligand4.py -l %s -v" % (BASE_DIR, pdb_path))
        pdbqt = pdb.split('.')[0] + '.pdbqt'
        if os.path.exists(pdbqt):
            os.system("mv %s %s" % (pdbqt, output_path))


@shared_task
def perform_screen(work_name, center_x, center_y, center_z, size_x, size_y, size_z, mol_db, pdb_path, res_path):
    """
    用户指定筛选中心以及盒子大小
    :param work_name:
    :param center_x:
    :param center_y:
    :param center_z:
    :param size_x:
    :param size_y:
    :param size_z:
    :param mol_db:
    :param pdb_path:
    :param res_path:
    :return:
    """
    screen_status(work_name, status='computing')

    screen_out = 'screen_out.csv'
    res = os.path.join(res_path, 'res')

    if not os.path.exists(res):
        os.mkdir(res)

    ligand_db = os.path.join(drugdb, mol_db)

    os.system("python %s/extra_apps/vina/prepare_receptor4.py -r %s"
              " -A checkhydrogens " % (BASE_DIR, pdb_path))
    pdbqt = pdb_path.split('/')[-1].split('.')[0] + '.pdbqt'
    os.system("mv %s %s" % (pdbqt, res_path))

    target_list = os.listdir(os.path.join(TARGET_FOLDER_BASE, 'maccs'))
    smile_file = os.path.join(ligand_db, 'smiles.csv')
    df = pd.read_csv(smile_file, header=None, encoding='utf-8')
    smile_data = df.values.tolist()
    curr_proc = mp.current_process()
    curr_proc.daemon = False
    p = mp.Pool(processes=mp.cpu_count())
    curr_proc.daemon = True
    pool_lst = []
    for ligand in smile_data:
        smiles = ligand[1]
        targets = p.apply_async(pred, args=(smiles, target_list))
        pool_lst.append([ligand[0], targets])
    p.close()
    p.join()
    pool_lst = [[n[0], n[1].get()] for n in pool_lst]
    for target in pool_lst:
        if target[1]:
            ligand = target[0].split('.')[0] + '.pdbqt'
            ligand_path = ligand_db + '/' + ligand
            os.system("%s --receptor %s/%s --ligand %s --center_x %s --center_y %s"
                      " --center_z %s --size_x %s --size_y %s --size_z %s" % (vina_path, res_path, pdbqt,
                                                                              ligand_path, center_x, center_y, center_z,
                                                                              size_x, size_y, size_z))
            os.system("mv %s %s" % (ligand_path.split('.')[0]+'_out.pdbqt', res))
            os.system("python %s/extra_apps/vina/pdbqt_to_pdb.py -f %s -v" % (BASE_DIR, os.path.join(res,
                                                    ligand_path.split('/')[-1].split('.')[0]+'_out.pdbqt')))

    res_lst = os.listdir(res)
    reg = 'REMARK VINA RESULT:(.*?)\n'
    re_reg = re.compile(reg)
    screen_res = []
    insert_lst = []
    for out in res_lst[:]:
        out_path = os.path.join(res, out)
        with open(out_path, 'r') as f:
            data = f.read()
        out_lst = re_reg.findall(data)
        if out_lst:
            med = []
            for model in out_lst:
                med.append(float(model.split()[0]))
            file_name = out.split('_out')[0]
            screen_res.append([file_name, min(med)])
            insert_lst.append(Screen(work_name=work_name, screen_cat='screen', affinity=min(med), path=os.path.join(res.split('media/')[1],
                                                                                               out[:-2])))
    Screen.objects.bulk_create(insert_lst)
    arr = np.array(screen_res)
    df = pd.DataFrame(arr, columns=['id', 'Affinity (kcal/mol)'])
    df = df.sort_values("Affinity (kcal/mol)", ascending=False)
    df.to_csv(screen_out, index=False)
    os.system("mv %s %s" % (screen_out, res))

    screen_status(work_name=work_name, status='completed')


@shared_task
def perform_screen2(work_name, mol_db, pdb_path, resi_path, res_path):
    """
    用户指定几个残基进行筛选
    :param work_name:
    :param mol_db:
    :param pdb_path:
    :param lig_path:
    :param res_path:
    :return:
    """
    screen2_status(work_name=work_name, status='computing')

    with open(resi_path, 'r') as f:
        lines = f.readlines()
    lines = [n.rstrip() for n in lines if len(n) > 1]

    x, y, z = [], [], []
    for n in lines:
        x.append(float(n[30:38]))
        y.append(float(n[38:46]))
        z.append(float(n[46:54]))
    center_x = float('%.3f' % (sum(x)/len(x)))
    center_y = float('%.3f' % (sum(y)/len(y)))
    center_z = float('%.3f' % (sum(z)/len(z)))
    size_x = max(x) - min(x)
    size_y = max(y) - min(y)
    size_z = max(z) - min(z)

    screen_out = 'screen_out.csv'
    res = os.path.join(res_path, 'res')

    if not os.path.exists(res):
        os.mkdir(res)

    ligand_db = os.path.join(drugdb, mol_db)

    os.system("python %s/extra_apps/vina/prepare_receptor4.py -r /%s"
              " -A checkhydrogens " % (BASE_DIR, pdb_path))
    pdbqt = pdb_path.split('/')[-1].split('.')[0] + '.pdbqt'
    os.system("mv %s %s" % (pdbqt, res_path))

    target_list = os.listdir(os.path.join(TARGET_FOLDER_BASE, 'maccs'))
    smile_file = os.path.join(ligand_db, 'smiles.csv')
    df = pd.read_csv(smile_file, header=None, encoding='utf-8')
    smile_data = df.values.tolist()
    curr_proc = mp.current_process()
    curr_proc.daemon = False
    p = mp.Pool(processes=mp.cpu_count())
    curr_proc.daemon = True
    pool_lst = []
    for ligand in smile_data:
        smiles = ligand[1]
        targets = p.apply_async(pred, args=(smiles, target_list))
        pool_lst.append([ligand[0], targets])
    p.close()
    p.join()
    pool_lst = [[n[0], n[1].get()] for n in pool_lst]
    for target in pool_lst:
        if target[1]:
            ligand = target[0].split('.')[0] + '.pdbqt'
            ligand_path = ligand_db + '/' + ligand
            os.system("%s --receptor %s/%s --ligand %s --center_x %s --center_y %s"
                      " --center_z %s --size_x %s --size_y %s --size_z %s" % (vina_path, res_path, pdbqt,
                                                                              ligand_path, center_x, center_y, center_z,
                                                                              size_x, size_y, size_z))
            os.system("mv %s %s" % (ligand_path.split('.')[0]+'_out.pdbqt', res))
            os.system("python %s/extra_apps/vina/pdbqt_to_pdb.py -f %s -v" % (BASE_DIR, os.path.join(res,
                                                    ligand_path.split('/')[-1].split('.')[0]+'_out.pdbqt')))

    res_lst = os.listdir(res)
    reg = 'REMARK VINA RESULT:(.*?)\n'
    re_reg = re.compile(reg)
    screen_res = []
    insert_lst = []
    for out in res_lst[:]:
        out_path = os.path.join(res, out)
        with open(out_path, 'r') as f:
            data = f.read()
        out_lst = re_reg.findall(data)
        if out_lst:
            med = []
            for model in out_lst:
                med.append(float(model.split()[0]))
            file_name = out.split('_out')[0]
            screen_res.append([file_name, min(med)])
            insert_lst.append(Screen(work_name=work_name, screen_cat='screen2', affinity=min(med), path=os.path.join(res.split('media/')[1],
                                                                                               out[:-2])))
    Screen.objects.bulk_create(insert_lst)
    arr = np.array(screen_res)
    df = pd.DataFrame(arr, columns=['id', 'Affinity (kcal/mol)'])
    df = df.sort_values("Affinity (kcal/mol)", ascending=False)
    df.to_csv(screen_out, index=False)
    os.system("mv %s %s" % (screen_out, res))

    screen2_status(work_name=work_name, status='completed')


@shared_task
def perform_screen_user(work_name, center_x, center_y, center_z, size_x, size_y, size_z, user_db_name, pdb_path, res_path):
    """
    用户提供数据库以及中心坐标和盒子大小进行筛选
    :param work_name:
    :param center_x:
    :param center_y:
    :param center_z:
    :param size_x:
    :param size_y:
    :param size_z:
    :param user_db_name:
    :param pdb_path:
    :param res_path:
    :return:
    """
    screen_status(work_name, status='computing')

    screen_out = 'screen_out.csv'
    user_db = os.path.join(res_path, 'userdb')
    res = os.path.join(res_path, 'res')

    if not os.path.exists(user_db):
        os.mkdir(user_db)

    if not os.path.exists(res):
        os.mkdir(res)

    input_file = os.path.join(res_path, user_db_name)
    gen_user_db_qt_smiles(input_file, user_db)

    os.system("python %s/extra_apps/vina/prepare_receptor4.py -r /%s"
              " -A checkhydrogens " % (BASE_DIR, pdb_path))
    pdbqt = pdb_path.split('/')[-1].split('.')[0] + '.pdbqt'
    os.system("mv %s %s" % (pdbqt, res_path))

    target_list = os.listdir(os.path.join(TARGET_FOLDER_BASE, 'maccs'))
    smile_file = os.path.join(user_db, 'smiles.csv')
    df = pd.read_csv(smile_file, header=None, encoding='utf-8')
    smile_data = df.values.tolist()
    curr_proc = mp.current_process()
    curr_proc.daemon = False
    p = mp.Pool(processes=mp.cpu_count())
    curr_proc.daemon = True
    pool_lst = []
    for ligand in smile_data:
        smiles = ligand[1]
        targets = p.apply_async(pred, args=(smiles, target_list))
        pool_lst.append([ligand[0], targets])
    p.close()
    p.join()
    pool_lst = [[n[0], n[1].get()] for n in pool_lst]
    for target in pool_lst:
        if target[1]:
            ligand = target[0].split('.')[0] + '.pdbqt'
            ligand_path = os.path.join(user_db, ligand)
            if os.path.exists(ligand_path):
                os.system("%s --receptor %s/%s --ligand %s --center_x %s --center_y %s"
                          " --center_z %s --size_x %s --size_y %s --size_z %s" % (vina_path, res_path, pdbqt,
                                                                                  ligand_path, center_x, center_y,
                                                                                  center_z, size_x, size_y, size_z))
                os.system("mv %s %s" % (ligand_path.split('.')[0] + '_out.pdbqt', res))
                os.system("python %s/extra_apps/vina/pdbqt_to_pdb.py -f %s -v" % (BASE_DIR, os.path.join(res,
                                                        ligand_path.split('/')[-1].split('.')[0] + '_out.pdbqt')))

    res_lst = os.listdir(res)
    reg = 'REMARK VINA RESULT:(.*?)\n'
    re_reg = re.compile(reg)
    screen_res = []
    insert_lst = []
    for out in res_lst[:]:
        out_path = os.path.join(res, out)
        with open(out_path, 'r') as f:
            data = f.read()
        out_lst = re_reg.findall(data)
        if out_lst:
            med = []
            for model in out_lst:
                med.append(float(model.split()[0]))
            file_name = out.split('_out')[0]
            screen_res.append([file_name, min(med)])
            insert_lst.append(Screen(work_name=work_name, screen_cat='screen', affinity=min(med),
                                     path=os.path.join(res.split('media/')[1],
                                                       out[:-2])))
    Screen.objects.bulk_create(insert_lst)
    arr = np.array(screen_res)
    df = pd.DataFrame(arr, columns=['id', 'Affinity (kcal/mol)'])
    df = df.sort_values("Affinity (kcal/mol)", ascending=False)
    df.to_csv(screen_out, index=False)
    os.system("mv %s %s" % (screen_out, res))

    screen_status(work_name, status='completed')


@shared_task
def perform_screen2_user(work_name, user_db_name, pdb_path, resi_path, res_path):
    """
    用户提供数据库以及残基进行筛选
    :param work_name:
    :param user_db_name:
    :param pdb_path:
    :param resi_path:
    :param res_path:
    :return:
    """
    screen2_status(work_name, status='computing')

    with open(resi_path, 'r') as f:
        lines = f.readlines()
    lines = [n.rstrip() for n in lines if len(n) > 1]

    x, y, z = [], [], []
    for n in lines:
        x.append(float(n[30:38]))
        y.append(float(n[38:46]))
        z.append(float(n[46:54]))
    center_x = float('%.3f' % (sum(x)/len(x)))
    center_y = float('%.3f' % (sum(y)/len(y)))
    center_z = float('%.3f' % (sum(z)/len(z)))
    size_x = max(x) - min(x)
    size_y = max(y) - min(y)
    size_z = max(z) - min(z)

    screen_out = 'screen_out.csv'
    user_db = os.path.join(res_path, 'userdb')
    res = os.path.join(res_path, 'res')

    if not os.path.exists(user_db):
        os.mkdir(user_db)

    if not os.path.exists(res):
        os.mkdir(res)
    input_file = os.path.join(res_path, user_db_name)
    gen_user_db_qt_smiles(input_file, user_db)

    os.system("python %s/extra_apps/vina/prepare_receptor4.py -r /%s"
              " -A checkhydrogens " % (BASE_DIR, pdb_path))
    pdbqt = pdb_path.split('/')[-1].split('.')[0] + '.pdbqt'
    os.system("mv %s %s" % (pdbqt, res_path))

    target_list = os.listdir(os.path.join(TARGET_FOLDER_BASE, 'maccs'))
    smile_file = os.path.join(user_db, 'smiles.csv')
    df = pd.read_csv(smile_file, header=None, encoding='utf-8')
    smile_data = df.values.tolist()
    curr_proc = mp.current_process()
    curr_proc.daemon = False
    p = mp.Pool(processes=mp.cpu_count())
    curr_proc.daemon = True
    pool_lst = []
    for ligand in smile_data:
        smiles = ligand[1]
        targets = p.apply_async(pred, args=(smiles, target_list))
        pool_lst.append([ligand[0], targets])
    p.close()
    p.join()
    pool_lst = [[n[0], n[1].get()] for n in pool_lst]
    for target in pool_lst:
        if target[1]:
            ligand = target[0].split('.')[0] + '.pdbqt'
            ligand_path = os.path.join(user_db, ligand)
            if os.path.exists(ligand_path):
                os.system("%s --receptor %s/%s --ligand %s --center_x %s --center_y %s"
                          " --center_z %s --size_x %s --size_y %s --size_z %s" % (vina_path, res_path, pdbqt,
                                                                                  ligand_path, center_x, center_y,
                                                                                  center_z, size_x, size_y, size_z))
                os.system("mv %s %s" % (ligand_path.split('.')[0] + '_out.pdbqt', res))
                os.system("python %s/extra_apps/vina/pdbqt_to_pdb.py -f %s -v" % (BASE_DIR, os.path.join(res,
                                                    ligand_path.split('/')[-1].split('.')[0]+'_out.pdbqt')))

    res_lst = os.listdir(res)
    reg = 'REMARK VINA RESULT:(.*?)\n'
    re_reg = re.compile(reg)
    screen_res = []
    insert_lst = []
    for out in res_lst[:]:
        out_path = os.path.join(res, out)
        with open(out_path, 'r') as f:
            data = f.read()
        out_lst = re_reg.findall(data)
        if out_lst:
            med = []
            for model in out_lst:
                med.append(float(model.split()[0]))
            file_name = out.split('_out')[0]
            screen_res.append([file_name, min(med)])
            insert_lst.append(Screen(work_name=work_name, screen_cat='screen2', affinity=min(med),
                                     path=os.path.join(res.split('media/')[1],
                                                       out[:-2])))
    Screen.objects.bulk_create(insert_lst)
    arr = np.array(screen_res)
    df = pd.DataFrame(arr, columns=['id', 'Affinity (kcal/mol)'])
    df = df.sort_values("Affinity (kcal/mol)", ascending=False)
    df.to_csv(screen_out, index=False)
    os.system("mv %s %s" % (screen_out, res))

    screen2_status(work_name, status='completed')


@shared_task
def perform_dock(work_name, center_x, center_y, center_z, size_x, size_y, size_z, pdb_path, lig_path, res_path):
    """
    用户指定对接中心以及盒子大小
    :param work_name:
    :param center_x:
    :param center_y:
    :param center_z:
    :param size_x:
    :param size_y:
    :param size_z:
    :param pdb_path:
    :param lig_path:
    :param res_path:
    :return:
    """
    dock_status(work_name=work_name, status='computing')

    res = os.path.join(res_path, 'res')
    if not os.path.exists(res):
        os.mkdir(res)

    os.system("python %s/extra_apps/vina/prepare_receptor4.py -r %s"
              " -A checkhydrogens " % (BASE_DIR, pdb_path))
    pdbqt = pdb_path.split('/')[-1].split('.')[0] + '.pdbqt'
    os.system("mv %s %s" % (pdbqt, res_path))

    os.system("python %s/extra_apps/vina/prepare_ligand4.py -l %s -v" % (BASE_DIR, lig_path))
    ligqt = lig_path.split('/')[-1].split('.')[0] + '.pdbqt'
    os.system("mv %s %s" % (ligqt, res_path))

    os.system("%s --receptor %s/%s --ligand %s/%s --center_x %s --center_y %s --center_z %s --size_x %s --size_y %s"
              " --size_z %s" % (vina_path, res_path, pdbqt, res_path, ligqt, center_x, center_y, center_z,
                                size_x, size_y, size_z))
    outqt = ligqt.split('.')[0]+'_out.pdbqt'
    outqt_path = os.path.join(res_path, outqt)
    if os.path.exists(outqt_path):
        reg = 'REMARK VINA RESULT:(.*?)\n'
        re_reg = re.compile(reg)
        with open(outqt_path, 'r') as f:
            data = f.read()
        out_lst = re_reg.findall(data)
        if out_lst:
            med = []
            for model in out_lst:
                med.append(float(model.split()[0]))
            affinity = str(min(med))
            dock_affinity(work_name=work_name, affinity=affinity)
        os.system("mv %s %s" % (outqt_path, res))
        os.system("python %s/extra_apps/vina/pdbqt_to_pdb.py -f %s -v" % (BASE_DIR, os.path.join(res, outqt)))
        out_path = os.path.join(res.split('media/')[1], outqt[:-2])
        dock_out(work_name=work_name, out_path=out_path)
    dock_status(work_name=work_name, status='completed')


@shared_task
def perform_dock2(work_name, pdb_path, lig_path, resi_path, res_path):
    """
    用户指定几个残基对接
    :param work_name:
    :param pdb_path:
    :param lig_path:
    :param resi_path:
    :param res_path:
    :return:
    """
    dock2_status(work_name=work_name, status='computing')
    res = '%s/res' % res_path
    if not os.path.exists(res):
        os.mkdir(res)

    with open(resi_path, 'r') as f:
        lines = f.readlines()
    lines = [n.rstrip() for n in lines if len(n) > 1]

    x, y, z = [], [], []
    for n in lines:
        x.append(float(n[30:38]))
        y.append(float(n[38:46]))
        z.append(float(n[46:54]))
    center_x = float('%.3f' % (sum(x)/len(x)))
    center_y = float('%.3f' % (sum(y)/len(y)))
    center_z = float('%.3f' % (sum(z)/len(z)))
    size_x = max(x) - min(x)
    size_y = max(y) - min(y)
    size_z = max(z) - min(z)

    os.system("python %s/extra_apps/vina/prepare_receptor4.py -r %s"
              " -A checkhydrogens " % (BASE_DIR, pdb_path))
    pdbqt = pdb_path.split('/')[-1].split('.')[0] + '.pdbqt'
    os.system("mv %s %s" % (pdbqt, res_path))

    os.system("python %s/extra_apps/vina/prepare_ligand4.py -l %s -v" % (BASE_DIR, lig_path))
    ligqt = lig_path.split('/')[-1].split('.')[0] + '.pdbqt'
    os.system("mv %s %s" % (ligqt, res_path))

    os.system("%s --receptor %s/%s --ligand %s/%s --center_x %s --center_y %s --center_z %s --size_x %s --size_y %s"
              " --size_z %s" % (vina_path, res_path, pdbqt, res_path, ligqt, center_x, center_y, center_z,
                                size_x, size_y, size_z))
    outqt = ligqt.split('.')[0]+'_out.pdbqt'
    outqt_path = os.path.join(res_path, outqt)
    if os.path.exists(outqt_path):
        reg = 'REMARK VINA RESULT:(.*?)\n'
        re_reg = re.compile(reg)
        with open(outqt_path, 'r') as f:
            data = f.read()
        out_lst = re_reg.findall(data)
        if out_lst:
            med = []
            for model in out_lst:
                med.append(float(model.split()[0]))
            affinity = min(med)
            dock2_affinity(work_name=work_name, affinity=affinity)
        os.system("mv %s %s" % (outqt_path, res))
        os.system("python %s/extra_apps/vina/pdbqt_to_pdb.py -f %s -v" % (BASE_DIR, os.path.join(res, outqt)))
        out_path = os.path.join(res.split('media/')[1], outqt[:-2])
        dock2_out(work_name=work_name, out_path=out_path)
    dock2_status(work_name=work_name, status='completed')
