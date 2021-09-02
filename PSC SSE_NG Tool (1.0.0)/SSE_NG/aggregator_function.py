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
import os
#import Levenshtein as lev
import collections

# Meta Data
__author__ = 'Negar Shams'
__version__ = '0.0.1'
__email__ = 'negar.shams@PSCconsulting.com'
__phone__ = '++44 7436 544893'
__status__ = 'In Development - Beta'




def aggregator(excel_output_name,grouped_final_data_sheet_name,ungrouped_final_data_sheet_name):
    """

    :param list
    :return list
    """
    # todo: add the description

    # Coming from GUI:
    # TODO: update from GUI with constants
    input_variable_list=['df_SHEPD_GSP_BB_added']
    input_dill_file_list= ['{}.dill'.format(x) for x in input_variable_list]
    output_variable_list=['df_grouped_final','df_ungrouped_final']
    output_dill_file_list= ['{}.dill'.format(x) for x in output_variable_list]

    variable_path_dict = collections.OrderedDict()
    variable_dict=collections.OrderedDict()


    for b in input_dill_file_list:
        b_no_dill=b.replace('.dill','')
        variable_path_dict[b_no_dill]=common.get_local_file_path_withfolder(file_name=b,folder_name=common.folder_file_names.dill_folder)

    for n in input_variable_list:
        with open(variable_path_dict[n], 'rb') as file:
            variable_dict[n] = dill.load(file)

    df_SHEPD_GSP_BB_added = variable_dict['df_SHEPD_GSP_BB_added']

    headers_list=list(df_SHEPD_GSP_BB_added.columns)
    year_columns=[e for e in headers_list if isinstance(e, int)]

    required_headers_noyears=['NG_BB','Units','Scenario','GSP','Substation','Baseline']
    required_headers=required_headers_noyears+year_columns

    df=df_SHEPD_GSP_BB_added[required_headers]
    list_y=['Baseline']
    load_columns=list_y+year_columns

    df_grouped=df.groupby(['Scenario','GSP','NG_BB','Units'])[load_columns].sum().reset_index()

    df_grouped['DNO License Area']='SEPD'
    df_grouped_column_sorted=df_grouped.loc[:,['NG_BB','Units','DNO License Area','Scenario','GSP']+load_columns]

    df_grouped_final=df_grouped_column_sorted
    df_ungrouped_final=df
    variable_dict['df_grouped_final'] = df_grouped_final
    variable_dict['df_ungrouped_final'] = df_ungrouped_final


    for b in output_dill_file_list:
        b_no_dill=b.replace('.dill','')
        variable_path_dict[b_no_dill]=common.get_local_file_path_withfolder(file_name=b,folder_name=common.folder_file_names.dill_folder)
        local_dir = os.path.dirname(os.path.realpath(__file__))
        dill_folder = os.path.join(local_dir, common.folder_file_names.dill_folder)

        if not os.path.exists(dill_folder):
            os.mkdir(dill_folder)

        with open(variable_path_dict[b_no_dill], 'wb') as f:
            dill.dump(variable_dict[b_no_dill], f)


    local_dir = os.path.dirname(os.path.realpath(__file__))
    excel_folder = os.path.join(local_dir, common.folder_file_names.excel_output_folder) #

    if not os.path.exists(excel_folder):
        os.mkdir(excel_folder)

    excel_file_pth = os.path.join(excel_folder,excel_output_name)

    with pd.ExcelWriter(excel_file_pth) as writer:
        df_grouped_final.to_excel(writer,sheet_name=grouped_final_data_sheet_name)  #
        df_ungrouped_final.to_excel(writer, sheet_name=ungrouped_final_data_sheet_name)
        # constants.XlFileConstants.amend_data.to_excel(writer, sheet_name=constants.XlFileConstants.sheet3)
        worksheet1 = writer.sheets['grouped_final_data']
        worksheet1.set_tab_color('green')
        worksheet1 = writer.sheets['ungrouped_final_data']
        worksheet1.set_tab_color('yellow')


    return df_grouped_final,df_ungrouped_final


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
    grouped_final_data_sheet_name='grouped_final_data'
    ungrouped_final_data_sheet_name='ungrouped_final_data'

    df_grouped_final_1, df_ungrouped_final_1 = aggregator(excel_output_name,grouped_final_data_sheet_name=grouped_final_data_sheet_name,\
                                                          ungrouped_final_data_sheet_name=ungrouped_final_data_sheet_name)








