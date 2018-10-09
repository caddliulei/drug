# coding=utf-8
import xadmin

from .models import Banner, Product, AutoDuck, VirtualScreen, VsBlast, ReverseVirtualScreen, Dynamic, Admet


class BannerAdmin(object):
    list_display = ['image', 'index', 'add_time']
    search_fields = ['image', 'index', 'add_time']
    list_filter = ['image', 'index', 'add_time']


class ProductAdmin(object):
    list_display = ['name', 'add_time']
    search_fields = ['name', 'add_time']
    list_filter = ['name', 'add_time']


class AutoDuctAdmin(object):
    list_display = ['name', 'work_name', 'work_decs', 'mol_db', 'size_x', 'size_y', 'size_z',
                    'center_x', 'center_y', 'center_z', 'pdb_file', 'add_time']
    search_fields = ['name', 'work_name', 'work_decs', 'mol_db', 'size_x', 'size_y', 'size_z',
                     'center_x', 'center_y', 'center_z', 'pdb_file', 'add_time']
    list_filter = ['name', 'work_name', 'work_decs', 'mol_db', 'size_x', 'size_y', 'size_z',
                   'center_x', 'center_y', 'center_z', 'pdb_file', 'add_time']


class VirtualScreenAdmin(object):
    list_display = ['name', 'work_name', 'work_decs', 'mol_db', 'size_x', 'size_y', 'size_z',
                    'center_x', 'center_y', 'center_z', 'pdb_file', 'add_time']
    search_fields = ['name', 'work_name', 'work_decs', 'mol_db', 'size_x', 'size_y', 'size_z','center_x', 'center_y',
                     'center_z', 'pdb_file', 'add_time']
    list_filter = ['name', 'work_name', 'work_decs', 'mol_db', 'size_x', 'size_y', 'size_z', 'center_x', 'center_y',
                   'center_z', 'pdb_file', 'add_time']


class VsBlastAdmin(object):
    list_display = ['name', 'work_name', 'work_decs', 'sequence', 'protein_db', 'e_value', 'out_format', 'add_time']
    search_fields = ['name', 'work_name', 'work_decs', 'sequence', 'protein_db', 'e_value', 'out_format', 'add_time']
    list_filter = ['name', 'work_name', 'work_decs', 'sequence', 'protein_db', 'e_value', 'out_format', 'add_time']


class ReverseVirtualScreenAdmin(object):
    list_display = ['name', 'work_name', 'work_decs', 'target_db', 'mol_file', 'top_n', 'add_time']
    search_fields = ['name', 'work_name', 'work_decs', 'target_db', 'mol_file', 'top_n', 'add_time']
    list_filter = ['name', 'work_name', 'work_decs', 'target_db', 'mol_file', 'top_n', 'add_time']


class DynamicAdmin(object):
    list_display = ['name', 'work_name', 'work_decs', 'conf_info', 'protein_file', 'mol_file', 'conf_project',
                    's_file', 'lig_file', 'frcmod_file', 'res_num', 'add_time']
    search_fields = ['name', 'work_name', 'work_decs', 'conf_info', 'protein_file', 'mol_file', 'conf_project',
                     's_file', 'lig_file', 'frcmod_file', 'res_num', 'add_time']
    list_filter = ['name', 'work_name', 'work_decs', 'conf_info', 'protein_file', 'mol_file', 'conf_project',
                   's_file', 'lig_file', 'frcmod_file', 'res_num', 'add_time']


class AdmetAdmin(object):
    list_display = ['name', 'work_name', 'work_decs', 'mol_file', 'add_time']
    search_fields = ['name', 'work_name', 'work_decs', 'mol_file', 'add_time']
    list_filter = ['name', 'work_name', 'work_decs', 'mol_file', 'add_time']


xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(Product, ProductAdmin)
xadmin.site.register(AutoDuck, AutoDuctAdmin)
xadmin.site.register(VirtualScreen, VirtualScreenAdmin)
xadmin.site.register(VsBlast, VsBlastAdmin)
xadmin.site.register(ReverseVirtualScreen, ReverseVirtualScreenAdmin)
xadmin.site.register(Dynamic, DynamicAdmin)
xadmin.site.register(Admet, AdmetAdmin)
