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
__phone__ = '+44 7449 315133'
__status__ = 'In Development - Beta'




def GSP_assigner(input_list,sheet_list,excel_check_data_name,no_match_substation_sheet_name,zero_GSP_substation_sheet_name):
	"""

	:param :
	:return :
	"""
	# todo: add the description

	# Coming from GUI:
	# TODO: update from GUI with constants

	variable_list = ['df_SHEPD', 'df_MAP_1', 'df_MAP_2', 'df_MAP_3', 'df_MAP_4', 'df_MAP_BB_1']
	variables_to_be_dilled = [True, True, True, True, True, True]


	GSP_map_list = ['df_MAP_1', 'df_MAP_2', 'df_MAP_3', 'df_MAP_4']

	# this is the list of headers in each of the map dataframes which corresponds to the primary substation column name
	# same size as GSP_map_list
	GSP_map_primary_header_list = ['Primary Name', 'PRIMARY', 'Primary Name', 'Primary Name']
	# this is the list of headers in each of the map dataframes which corresponds to the GSP column name
	# same size as GSP_map_list
	GSP_map_gsp_header_list = ['GSP Name', 'GSP', 'GSP Name', 'GSP']

	# output dill name of this process
	output_dill_name = 'df_SHEPD_GSP_added.dill'
	output_dill_name_no_dill = output_dill_name.replace('.dill', '')

	# using zip()
	# to convert two lists to a dictionary
	primary_headers_dictionary = dict(zip(GSP_map_list, GSP_map_primary_header_list))
	GSP_headers_dictionary = dict(zip(GSP_map_list, GSP_map_gsp_header_list))
	variable_to_be_dilled_dict = dict(zip(variable_list, variables_to_be_dilled))
	variable_excel_dict = dict(zip(variable_list, input_list))

	variable_dict = collections.OrderedDict()
	variable_path_dict = collections.OrderedDict()
	dill_file_list = ['{}.dill'.format(x) for x in variable_list]
	i = 0
	o = 0
	missing_variable_list = []
	for n in variables_to_be_dilled:
		if variables_to_be_dilled[i] == True:
			variable_path_dict[variable_list[i]] = common.get_local_file_path_withfolder(file_name=dill_file_list[i],
																						 folder_name=common.folder_file_names.dill_folder)
			local_dir = os.path.dirname(os.path.realpath(__file__))
			dill_folder = os.path.join(local_dir, common.folder_file_names.dill_folder)

			if not os.path.exists(dill_folder):
				os.mkdir(dill_folder)

			df = common.variable_dill_maker(input_name=input_list[i], sheet_name=sheet_list[i],
											variable_name=variable_list[i])
			variable_dict[variable_list[i]] = df
		elif variables_to_be_dilled[i] == False:
			local_dir = os.path.dirname(os.path.realpath(__file__))
			dill_folder = os.path.join(local_dir, common.folder_file_names.dill_folder)
			variable_path_dict[variable_list[i]] = common.get_local_file_path_withfolder(file_name=dill_file_list[i],
																						 folder_name=common.folder_file_names.dill_folder)
			if not os.path.exists(dill_folder):
				# print('The dill folder does not exist')
				message = 'The folder by the name of {} does not exist'.format(common.folder_file_names.dill_folder)
				sys.exit(message)
			elif not os.path.exists(variable_path_dict[variable_list[i]]):
				o = +1
				missing_variable_list = missing_variable_list.append(variable_list[i])
				print('The dill folder does not exist')
				sys.exit("The dill variable does not exist, try changing")
				# 'SAV case = {}'.format(os.path.basename(self.sav_case))
			elif os.path.exists(variable_path_dict[variable_list[i]]):
				with open(variable_path_dict[variable_list[i]], 'rb') as file:
					variable_dict[variable_list[i]] = dill.load(file)
		i += 1

	if len(missing_variable_list) > 0:
		print('The code stopped as the following dill variable does not exist:')
		print('\n'.join(map(str, missing_variable_list)))
		print('Try changing the false to true for the missing variables:')
		sys.exit()

	df_SHEPD = variable_dict['df_SHEPD']
	df_MAP_1 = variable_dict['df_MAP_1']
	df_MAP_2 = variable_dict['df_MAP_2']
	df_MAP_3 = variable_dict['df_MAP_3']
	df_MAP_4 = variable_dict['df_MAP_4']
	df_MAP_BB_1 = variable_dict['df_MAP_BB_1']

	headers_list = list(df_SHEPD.columns)
	year_columns = [e for e in headers_list if isinstance(e, int)]

	# this line sets the index of the map dfs to primary substation column
	df_MAP_1 = df_MAP_1.set_index(primary_headers_dictionary['df_MAP_1'])
	df_MAP_2 = df_MAP_2.set_index(primary_headers_dictionary['df_MAP_2'])
	df_MAP_3 = df_MAP_3.set_index(primary_headers_dictionary['df_MAP_3'])
	df_MAP_4 = df_MAP_4.set_index(primary_headers_dictionary['df_MAP_4'])

	# these lines are to remove duplicate indexes (as it's going to be used as a map to find the GSPs)
	Primary_List_1 = df_MAP_1.index
	is_duplicate_1 = Primary_List_1.duplicated(keep="first")
	not_duplicate = ~is_duplicate_1
	df_MAP_no_duplicate_1 = df_MAP_1[not_duplicate]

	Primary_List_2 = df_MAP_2.index
	is_duplicate_2 = Primary_List_2.duplicated(keep="first")
	not_duplicate_2 = ~is_duplicate_2
	df_MAP_no_duplicate_2 = df_MAP_2[not_duplicate_2]
	df_MAP_no_duplicate_2.index = df_MAP_no_duplicate_2.index.str.upper()  # this line is done to make the primary
	# substation names which are indexes upper case as in the data set (df_SHEPD) the data given as upper case

	Primary_List_3 = df_MAP_3.index
	is_duplicate_3 = Primary_List_3.duplicated(keep="first")
	not_duplicate_3 = ~is_duplicate_3
	df_MAP_no_duplicate_3 = df_MAP_3[not_duplicate_3]

	Primary_List_4 = df_MAP_4.index
	is_duplicate_4 = Primary_List_4.duplicated(keep="first")
	not_duplicate_4 = ~is_duplicate_4
	df_MAP_no_duplicate_4 = df_MAP_4[not_duplicate_4]

	df_SHEPD_to_be_mapped = df_SHEPD[common.Headers_SHEPD_NG.SHEPD_Substation]

	df_MAP_mapper_1 = df_MAP_no_duplicate_1[GSP_headers_dictionary['df_MAP_1']]

	df_MAP_mapper_1_dict = df_MAP_mapper_1.to_dict()

	GSP_Mapped_1 = df_SHEPD_to_be_mapped.map(df_MAP_mapper_1_dict)

	df_MAP_mapper_2 = df_MAP_no_duplicate_2[GSP_headers_dictionary['df_MAP_2']]

	df_MAP_mapper_2_dict = df_MAP_mapper_2.to_dict()

	GSP_Mapped_2 = df_SHEPD_to_be_mapped.map(df_MAP_mapper_2_dict)

	df_MAP_mapper_3 = df_MAP_no_duplicate_3[GSP_headers_dictionary['df_MAP_3']]

	df_MAP_mapper_3_dict = df_MAP_mapper_3.to_dict()

	GSP_Mapped_3 = df_SHEPD_to_be_mapped.map(df_MAP_mapper_3_dict)

	df_MAP_mapper_4 = df_MAP_no_duplicate_4[GSP_headers_dictionary['df_MAP_4']]

	df_MAP_mapper_4_dict = df_MAP_mapper_4.to_dict()

	GSP_Mapped_4 = df_SHEPD_to_be_mapped.map(df_MAP_mapper_4_dict)

	GSP_Mapped_1 = GSP_Mapped_1.to_frame()
	GSP_Mapped_1.columns = ['GSP']
	GSP_Mapped_2 = GSP_Mapped_2.to_frame()
	GSP_Mapped_2.columns = ['GSP']
	GSP_Mapped_3 = GSP_Mapped_3.to_frame()
	GSP_Mapped_3.columns = ['GSP']
	GSP_Mapped_4 = GSP_Mapped_4.to_frame()
	GSP_Mapped_4.columns = ['GSP']
	# GSP_Mapped[0].isna()

	idx = GSP_Mapped_1['GSP'].isna()
	GSP_Mapped_1.loc[idx, 'GSP'] = GSP_Mapped_2.loc[idx, 'GSP']
	idx = GSP_Mapped_2['GSP'].isna()
	GSP_Mapped_2.loc[idx, 'GSP'] = GSP_Mapped_1.loc[idx, 'GSP']
	idx = GSP_Mapped_1['GSP'].isna()
	GSP_Mapped_1.loc[idx, 'GSP'] = GSP_Mapped_3.loc[idx, 'GSP']
	idx = GSP_Mapped_1['GSP'].isna()
	GSP_Mapped_1.loc[idx, 'GSP'] = GSP_Mapped_4.loc[idx, 'GSP']

	df_SHEPD['GSP'] = GSP_Mapped_1['GSP']

	idx = df_SHEPD['GSP'].isna()

	df_SHEPD_missing_GSP = df_SHEPD.loc[idx, :]
	Substations = df_SHEPD_missing_GSP['Substation']

	is_duplicate = Substations.duplicated(keep="first")
	not_duplicate = ~is_duplicate
	Substations = Substations[not_duplicate]

	if len(Substations) > 0:
		print('Substations with no match for GSP:')
		print('\n'.join(map(str, Substations)))

	idx = df_SHEPD['GSP'].le(0)
	Substations_with_0_GSP = df_SHEPD.loc[idx, :]
	Substations_with_0_GSP_names = Substations_with_0_GSP['Substation']

	is_duplicate = Substations_with_0_GSP_names.duplicated(keep="first")
	not_duplicate = ~is_duplicate
	Substations_with_0_GSP_names = Substations_with_0_GSP_names[not_duplicate]

	if len(Substations_with_0_GSP_names) > 0:
		print('Substations with 0 GSPs are:')
		print('\n'.join(map(str, Substations_with_0_GSP_names)))

	df_SHEPD.loc[idx, 'GSP'] = df_SHEPD.loc[idx, 'GSP']

	df_SHEPD['GSP New'] = df_SHEPD['Substation'].apply(lambda x: "{}{}".format(x, ' GSP'))
	# add a temp column to make fake GSP names by adding GSP str at the beginning of the primary names
	df_SHEPD.loc[idx, 'GSP'] = df_SHEPD.loc[idx, 'GSP New']
	# this line replace the GSP value of all 0 GSP substation identified with (GSP Substation name)
	df_SHEPD.drop('GSP New', axis='columns', inplace=True)
	# removes the temp column

	variable_path_dict[output_dill_name_no_dill] = common.get_local_file_path_withfolder(file_name=output_dill_name,
																						 folder_name=common.folder_file_names.dill_folder)

	with open(variable_path_dict[output_dill_name_no_dill], 'wb') as f:
		dill.dump(df_SHEPD, f)

	local_dir = os.path.dirname(os.path.realpath(__file__))
	excel_folder = os.path.join(local_dir, common.folder_file_names.excel_output_folder)  #

	if not os.path.exists(excel_folder):
		os.mkdir(excel_folder)

	excel_file_pth = os.path.join(excel_folder, excel_check_data_name)


	with pd.ExcelWriter(excel_file_pth) as writer:
		Substations.to_excel(writer, sheet_name=no_match_substation_sheet_name)  #
		Substations_with_0_GSP_names.to_excel(writer, sheet_name=zero_GSP_substation_sheet_name)
		# constants.XlFileConstants.amend_data.to_excel(writer, sheet_name=constants.XlFileConstants.sheet3)
		worksheet1 = writer.sheets[no_match_substation_sheet_name]
		worksheet1.set_tab_color('red')
		worksheet1 = writer.sheets[zero_GSP_substation_sheet_name]
		worksheet1.set_tab_color('yellow')

	return df_SHEPD,Substations,Substations_with_0_GSP_names


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
	excel_check_data_name='no_match_data.xlsx'
	no_match_substation_sheet_name = 'no_match_substations'
	zero_GSP_substation_sheet_name = '0_GSP_substations'

	df_SHEPD, Substations, Substations_with_0_GSP_names = GSP_assigner(input_list=input_list,
																							 variables_to_be_dilled=variables_to_be_dilled,
																							 sheet_list=sheet_list,excel_check_data_name=excel_check_data_name, \
																	   no_match_substation_sheet_name=no_match_substation_sheet_name,\
																	   zero_GSP_substation_sheet_name=zero_GSP_substation_sheet_name )
