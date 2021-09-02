"""
#######################################################################################################################
###											Example DataFrame Processing											###
###																													###
###		Code developed by Negar Shams (negar.shams@PSCconsulting.com, +44 7436 544893) as part of PSC 		 		###
###		project JK7938 - SHEPD - studies and automation																###
###																													###
#######################################################################################################################
"""

# Modules to be imported first
# Generic Imports
import pandas as pd
import numpy as np
import dill
# Unique imports
import common_functions as common
import re
# import Levenshtein as lev
import collections
import os
import sys

# Meta Data
__author__ = 'Negar Shams'
__version__ = '0.0.1'
__email__ = 'negar.shams@PSCconsulting.com'
__phone__ = '+44 7436 544893'
__status__ = 'In Development - Beta'


def BB_assigner(excel_check_data_name, output_sheet_name):
    """

    :param
    :return
    """
    # todo: add the description

    # Coming from GUI:
    # TODO: update from GUI with constants

    # this process have to be run after the GSP_assigner has been run and the dill files are made in the dill folder
    import collections
    variable_list = ['df_SHEPD_GSP_added', 'df_MAP_BB_1']
    dill_file_list = ['{}.dill'.format(x) for x in variable_list]  #
    variable_path_dict = collections.OrderedDict()
    variable_dict = collections.OrderedDict()
    output_dill_name = 'df_SHEPD_GSP_BB_added.dill'
    output_dill_name_no_dill = output_dill_name.replace('.dill', '')

    for b in dill_file_list:
        b_no_dill = b.replace('.dill', '')
        variable_path_dict[b_no_dill] = common.get_local_file_path_withfolder(file_name=b,
                                                                              folder_name=common.folder_file_names.dill_folder)

    for n in variable_list:
        with open(variable_path_dict[n], 'rb') as file:
            variable_dict[n] = dill.load(file)

    df_SHEPD = variable_dict['df_SHEPD_GSP_added']
    df_MAP_BB_1 = variable_dict['df_MAP_BB_1']

    headers_SHEPD = df_SHEPD.columns
    headers_MAP_BB = df_MAP_BB_1.columns
    Map_start = df_MAP_BB_1.loc[:, headers_MAP_BB[:3]]
    Map_updated = df_MAP_BB_1.loc[:, headers_MAP_BB[:5]]
    i = 5
    last_column_minus_1 = len(headers_MAP_BB) - 1

    for i in range(5, last_column_minus_1, 2):
        Map_sub = df_MAP_BB_1.loc[:, headers_MAP_BB[i:i + 2]]
        Map_section = pd.concat([Map_start, Map_sub], axis=1, join="inner")
        Map_section.columns = Map_updated.columns
        idx = (Map_section[headers_MAP_BB[3]].isna()) & (Map_section[headers_MAP_BB[4]].isna())
        Map_section = Map_section[~idx]
        Map_updated = pd.concat([Map_updated, Map_section], ignore_index=True, sort=False)

    Map_string_column = Map_updated[headers_MAP_BB[2]].astype(str) + '/' + Map_updated[headers_MAP_BB[3]].astype(
        str) + '/' + Map_updated[headers_MAP_BB[4]].astype(str)
    Map_updated['BB_String'] = Map_string_column
    Map_updated_index_changed = Map_updated.set_index('BB_String')

    mapper = Map_updated_index_changed[headers_MAP_BB[1]]

    To_be_mapped_string = df_SHEPD[headers_SHEPD[4]].astype(str) + '/' + df_SHEPD[headers_SHEPD[2]].astype(str) + '/' + \
                          df_SHEPD[headers_SHEPD[3]].astype(str)

    df_SHEPD['BB_String'] = To_be_mapped_string

    To_be_mapped_df = df_SHEPD['BB_String']

    mapper_dict = mapper.to_dict()

    mapped = To_be_mapped_df.map(mapper_dict)
    df_SHEPD['NG_BB'] = mapped

    idx = df_SHEPD['NG_BB'].isna()
    not_mapped = df_SHEPD[idx]
    not_mapped_BB_column = not_mapped['BB_String']

    is_duplicate = not_mapped_BB_column.duplicated(keep="first")
    not_duplicate = ~is_duplicate
    data_type_not_mapped = not_mapped[not_duplicate]

    if len(data_type_not_mapped) > 0:
        print('The generation/demand types that could not be matched:')
        print('\n'.join(map(str, data_type_not_mapped)))

    variable_path_dict[output_dill_name_no_dill] = common.get_local_file_path_withfolder(file_name=output_dill_name,
                                                                                         folder_name=common.folder_file_names.dill_folder)

    with open(variable_path_dict[output_dill_name_no_dill], 'wb') as f:
        dill.dump(df_SHEPD, f)

    local_dir = os.path.dirname(os.path.realpath(__file__))
    excel_folder = os.path.join(local_dir, common.folder_file_names.excel_output_folder)  #

    if not os.path.exists(excel_folder):
        os.mkdir(excel_folder)

    # excel_file_pth = os.path.join(excel_folder,common.folder_file_names.excel_check_data_name)
    excel_file_pth = os.path.join(excel_folder, excel_check_data_name)
    # sheet_name = 'data_type_not_mapped'

    with pd.ExcelWriter(excel_file_pth) as writer:
        data_type_not_mapped.to_excel(writer, sheet_name=output_sheet_name)  #
    # todo: make it write the data in an exisitng excel file withought using openpyxl

    return df_SHEPD, data_type_not_mapped


if __name__ == '__main__':
    """
        This is the main block of code that will be run if this script is run directly
    """

    sheet_list = ['Database', 'GSP List', 'SubstationLoad_Max_Primaries', 'GSP List', 'GSP', 'Maping to BBs']
    input_list = ['11kV DFES output dataset - SHEPD - v6 - data -modified.xlsx', 'GSP_NRN lookup.xlsx', \
                  '2019-20 SHEPD Load Estimates - v6.xlsx', '2019-20 SHEPD Load Estimates - v6.xlsx',
                  'missing_substations.xlsx', \
                  'DFES 2020 Final Submission to ESO_Updated_Map.xlsx']
    variable_list = ['df_SHEPD', 'df_MAP_1', 'df_MAP_2', 'df_MAP_3', 'df_MAP_4', 'df_MAP_BB_1']
    variables_to_be_dilled = [True, True, True, True, True, True]
    excel_output_name = 'Final_Results.xlsx'
    excel_check_data_name = 'no_match_data.xlsx'
    no_match_substation_sheet_name = 'no_match_substations'
    zero_GSP_substation_sheet_name = 'zero_GSP_substations'
    excel_check_data_name_2 = 'data_type_no_match.xlsx'
    no_data_type_match_sheet_name = 'data_type_no_match'

    df_SHEPD, data_type_not_mapped = BB_assigner(excel_check_data_name=excel_check_data_name_2,
                                             output_sheet_name=no_data_type_match_sheet_name)
