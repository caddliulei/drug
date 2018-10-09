# coding=utf-8
from __future__ import absolute_import, unicode_literals

import os
import re

import numpy as np
import pandas as pd
from celery import shared_task


@shared_task
def duck_perform(center_x, center_y, center_z, size_x, size_y, size_z, mol_db, receptor, file_path):
    """
    用户指定中心坐标以及盒子大小
    :param center_x:
    :param center_y:
    :param center_z:
    :param size_x:
    :param size_y:
    :param size_z:
    :param mol_db:
    :param receptor:
    :param file_path:
    :return:
    """
    res = '%s/res' % file_path
    if not os.path.exists(res):
        os.mkdir(res)
    ligand_file = '/home/jianping/pywork/drug/media/autoduck_db/%s' % mol_db
    os.system("python /home/jianping/pywork/drug/extra_apps/vina/prepare_receptor4.py -r %s/%s"
              " -A checkhydrogens " % (file_path, receptor))
    os.system("mv %s %s" % (receptor.split('.')[0]+'.pdbqt', file_path))
    ligand_lst = os.listdir(ligand_file)
    for ligand in ligand_lst:
        ligand_path = ligand_file + '/' + ligand
        os.system("/home/jianping/vina/bin/vina --receptor %s/%s --ligand %s --center_x %s --center_y %s"
                  " --center_z %s --size_x %s --size_y %s --size_z %s" % (file_path, receptor.split('.')[0]+'.pdbqt',
                                                                          ligand_path, center_x, center_y, center_z,
                                                                          size_x, size_y, size_z))

        os.system("mv %s %s" % (ligand_path.split('.')[0]+'_out.pdbqt', res))


@shared_task
def duck2_perform(mol_db, lig_file, receptor, file_path):
    """
    用户给定残基对接
    :param mol_db:
    :param lig_file:
    :param receptor:
    :param file_path:
    :return:
    """
    res = '%s/res' % file_path

    with open(lig_file, 'r') as f:
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

    if not os.path.exists(res):
        os.mkdir(res)
    ligand_file = '/home/jianping/pywork/drug/media/autoduck_db/%s' % mol_db
    os.system("python /home/jianping/pywork/drug/extra_apps/vina/prepare_receptor4.py -r %s/%s"
              " -A checkhydrogens " % (file_path, receptor))
    os.system("mv %s %s" % (receptor.split('.')[0]+'.pdbqt', file_path))
    ligand_lst = os.listdir(ligand_file)
    for ligand in ligand_lst:
        ligand_path = ligand_file + '/' + ligand
        os.system("/home/jianping/vina/bin/vina --receptor %s/%s --ligand %s --center_x %s --center_y %s"
                  " --center_z %s --size_x %s --size_y %s --size_z %s" % (file_path, receptor.split('.')[0]+'.pdbqt',
                                                                          ligand_path, center_x, center_y, center_z,
                                                                          size_x, size_y, size_z))

        os.system("mv %s %s" % (ligand_path.split('.')[0]+'_out.pdbqt', res))


@shared_task
def screen_perform(center_x, center_y, center_z, size_x, size_y, size_z, mol_db, receptor, file_path):
    """
    用户制定筛选的坐标以及盒子大小
    :param center_x:
    :param center_y:
    :param center_z:
    :param size_x:
    :param size_y:
    :param size_z:
    :param mol_db:
    :param receptor:
    :param file_path:
    :return:
    """
    screen_out = 'screen_out.csv'
    res = '%s/res' % file_path
    if not os.path.exists(res):
        os.mkdir(res)
    ligand_file = '/home/jianping/pywork/drug/media/autoduck_db/%s' % mol_db
    os.system("python /home/jianping/pywork/drug/extra_apps/vina/prepare_receptor4.py -r %s/%s"
              " -A checkhydrogens " % (file_path, receptor))
    os.system("mv %s %s" % (receptor.split('.')[0] + '.pdbqt', file_path))
    ligand_lst = os.listdir(ligand_file)
    for ligand in ligand_lst:
        ligand_path = ligand_file + '/' + ligand
        os.system("/home/jianping/vina/bin/vina --receptor %s/%s --ligand %s --center_x %s --center_y %s"
                  " --center_z %s --size_x %s --size_y %s --size_z %s" % (file_path, receptor.split('.')[0] + '.pdbqt',
                                                                          ligand_path, center_x, center_y, center_z,
                                                                          size_x, size_y, size_z))

        os.system("mv %s %s" % (ligand_path.split('.')[0] + '_out.pdbqt', res))
    res_lst = os.listdir(res)
    reg = 'REMARK VINA RESULT:(.*?)\n'
    re_reg = re.compile(reg)
    screen_res = []
    for out in res_lst[:]:
        res_path = '%s/%s' % (res, out)
        with open(res_path, 'r') as f:
            data = f.read()
        out_lst = re_reg.findall(data)
        if out_lst:
            med = []
            for model in out_lst:
                med.append(float(model.split()[0]))
            file_name = out.split('_')[0]
            screen_res.append([file_name, min(med)])
    arr = np.array(screen_res)
    df = pd.DataFrame(arr, columns=['id', 'Affinity (kcal/mol)'])
    df.sort_values("Affinity (kcal/mol)", inplace=True)
    df.to_csv(screen_out, index=False)
    os.system("mv %s %s" % (screen_out, res))


@shared_task
def screen2_perform(mol_db, lig_file, receptor, file_path):
    """
    用户指定几个残基进行筛选
    :param mol_db:
    :param lig_file:
    :param receptor:
    :param file_path:
    :return:
    """
    screen_out = 'screen_out.csv'
    res = '%s/res' % file_path

    with open(lig_file, 'r') as f:
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

    if not os.path.exists(res):
        os.mkdir(res)
    ligand_file = '/home/jianping/pywork/drug/media/autoduck_db/%s' % mol_db
    os.system("python /home/jianping/pywork/drug/extra_apps/vina/prepare_receptor4.py -r %s/%s"
              " -A checkhydrogens " % (file_path, receptor))
    os.system("mv %s %s" % (receptor.split('.')[0]+'.pdbqt', file_path))
    ligand_lst = os.listdir(ligand_file)
    for ligand in ligand_lst:
        ligand_path = ligand_file + '/' + ligand
        os.system("/home/jianping/vina/bin/vina --receptor %s/%s --ligand %s --center_x %s --center_y %s"
                  " --center_z %s --size_x %s --size_y %s --size_z %s" % (file_path, receptor.split('.')[0]+'.pdbqt',
                                                                          ligand_path, center_x, center_y, center_z,
                                                                          size_x, size_y, size_z))

        os.system("mv %s %s" % (ligand_path.split('.')[0]+'_out.pdbqt', res))

    res_lst = os.listdir(res)
    reg = 'REMARK VINA RESULT:(.*?)\n'
    re_reg = re.compile(reg)
    screen_res = []
    for out in res_lst[:]:
        res_path = '%s/%s' % (res, out)
        with open(res_path, 'r') as f:
            data = f.read()
        out_lst = re_reg.findall(data)
        if out_lst:
            med = []
            for model in out_lst:
                med.append(float(model.split()[0]))
            file_name = out.split('_')[0]
            screen_res.append([file_name, min(med)])
    arr = np.array(screen_res)
    df = pd.DataFrame(arr, columns=['id', 'Affinity (kcal/mol)'])
    df.sort_values("Affinity (kcal/mol)", inplace=True)
    df.to_csv(screen_out, index=False)
    os.system("mv %s %s" % (screen_out, res))


