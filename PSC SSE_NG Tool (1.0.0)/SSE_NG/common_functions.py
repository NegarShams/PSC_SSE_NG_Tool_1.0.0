"""
#######################################################################################################################
###											Used for example of imports												###
###																													###
###		Code developed by David Mills (david.mills@PSCconsulting.com, +44 7899 984158) as part of PSC 		 		###
###		project JK7938 - SHEPD - studies and automation																###
###																													###
#######################################################################################################################
"""

# Generic Imports
import os
import re
import pandas as pd
import numpy as np
from scipy import interpolate
import collections
import dill

# Meta Data
__author__ = 'David Mills'
__version__ = '0.0.1'
__email__ = 'david.mills@PSCconsulting.com'
__phone__ = '+44 7899 984158'
__status__ = 'Alpha'

from pandas import DataFrame


def import_raw_load_estimates(pth_load_est, sheet_name='MASTER Based on SubstationLoad'):
	"""
		Function imports the raw load estimate into a DataFrame with no processing of the data
	:param str pth_load_est: Full path to file
	:param str sheet_name:  (optional) Name of worksheet in load estimate
	:return pd.DataFrame df_raw:
	"""

	# Read the raw excel worksheet
	df_raw = pd.read_excel(
		io=pth_load_est,			# Path to worksheet
		sheet_name=sheet_name,		# Name of worksheet to import
		skiprows=2,					# Skip first 2 rows since they do not contain anything useful
		header=0
	)

	# Remove any special characters from the column names (i.e. new line characters)
	df_raw.columns = df_raw.columns.str.replace('\n', '')

	return df_raw

def import_excel(pth_load_est, sheet_name='Sheet1'):
	"""
		Function imports an excel file with sheet1 as default sheet name - this is used for rereading the exported df to excel and continue codingn from \
		that section of the code
	:param str pth_load_est: Full path to file
	:param str sheet_name:  (optional) Name of worksheet
	:return pd.DataFrame df_raw:
	"""

	# Read the raw excel worksheet
	df_raw = pd.read_excel(
		io=pth_load_est,			# Path to worksheet
		sheet_name=sheet_name,		# Name of worksheet to import
		# skiprows=2,					# Skip first 2 rows since they do not contain anything useful
		header=0
	)

	# Remove any special characters from the column names (i.e. new line characters)
	#df_raw.columns = df_raw.columns.str.replace('\n', '')
	#df_raw.reset_index(drop=True, inplace=True)
	df_raw.set_index(df_raw.columns[0], inplace=True)
	return df_raw


def adjust_years(headers_list):
	"""
		Function will find the headers which contain the years associated with the forecast so that they can be
		duplicated for diversified and aggregate load
	:param list  headers_list:  List of all  headers
	:return list forecast_years:  List of headers now just for the forecast years
	"""

	# This is a Regex search string being compiled for matching, further details available here:
	# https://docs.python.org/3/library/re.html
	# Effectively:
	# r = Declares as a raw string
	#  (\d{4}) = 4 digits between 0-9 in a group
	#  \s* = 0 or more spaces
	#  [/] = / symbol
	r = re.compile(r'(\d{4})\s*[/]\s*(\d{4})')
	# The following extracts a list of all of the times the above is true
	forecast_years = filter(r.match, headers_list)

	return forecast_years


def get_local_file_path(file_name):
	"""
		Function returns the full path to a file which is stored in the same directory as this script
	:param str file_name:  Name of file
	:return str file_pth:  Full path to file assuming it exists in this folder
	"""
	local_dir = os.path.dirname(os.path.realpath(__file__))
	file_pth = os.path.join(local_dir, file_name)

	return file_pth

def get_local_file_path_withfolder(file_name,folder_name):
	"""
		Function returns the full path to a file (it gets the new folder as well) which is stored in the same directory as this script
	:param str file_name:  Name of file
	:return str file_pth:  Full path to file assuming it exists in this folder
	"""
	local_dir = os.path.dirname(os.path.realpath(__file__))
	file_pth = os.path.join(local_dir,folder_name, file_name)

	return file_pth



# The following statement is used by PyCharm to stop it being flagged as a potential error, should only be used when
# necessary
# noinspection PyClassHasNoInit
class Headers:
	"""
		Headers used as part of the DataFrame
	"""
	gsp = 'GSP'
	nrn = 'NRN'
	name = 'Name'
	voltage = 'Voltage Ratio'
	psse_1 = 'PSS/E Bus #1'
	spring_autumn = 'Spring/Autumn'
	summer = 'Summer'
	min_demand = 'Minimum Demand'

	# Columns to define attributes
	sub_gsp = 'Sub_GSP'
	sub_primary = 'Sub_Primary'
	diverse_factor = 'Divers_Factor'

	# Header adjustments
	aggregate = 'aggregate'
	percentage='percentage'
	estimate='estimate'
	sum_percentages='sum_percentages'

class Seasons:
	"""
		Used for estimating the missing season load values
	"""
	spring_autumn_q = 75
	summer_q=75
	min_demand_q=25
	gsp_spring_autumn_val = float
	gsp_summer_val = float
	gsp_min_demand_val = float
	primary_spring_autumn_val = float
	primary_summer_val = float
	primary_min_demand_val = float


def interpolator(t1):
	"""
	Function returns #  gets a dataframe with one column and number of indexes equal to the number of # years and the
	missing values as nan, then interpolates the missing values by using indexes as x and y. Where y is values in the
	dataframe, then gives out a df of interpolated values
	:param t1:  one column dataframe with nan values
	:return y_estimated_df:  a dataframe with the interpolated values
	"""

	idx_t1 = t1[t1.columns[0]].isna()

	x = idx_t1[idx_t1 == False].index

	y = t1.loc[x, t1.columns[0]]

	x_to_estimate = idx_t1[idx_t1 == True].index
	y_list = y.values.tolist()

	f = interpolate.interp1d(x, y_list, fill_value='extrapolate')

	y_estimated = f(x_to_estimate)
	y_estimated_df = pd.DataFrame(y_estimated)

	return y_estimated_df

def variable_dill_maker(input_name,sheet_name,variable_name):
	"""
	Function returns #  gets an excel file name with.xlsx (input_name), the sheet_name, and the variable name which it would be dilled by that name (variable_name+.dill)
	:param t1:
	:return y_estimated_df:  a dataframe of the read excel file, also saves the dataframe as a dill
	"""

	file_pth_input = get_local_file_path(file_name=input_name)
	df = import_excel(pth_load_est=file_pth_input, sheet_name=sheet_name)

	df = df.reset_index()
	variable_name_list = [variable_name]

	dill_file_list = ['{}.dill'.format(x) for x in variable_name_list]

	i = 0
	for n in variable_name_list:
		with open(get_local_file_path_withfolder(
			file_name=dill_file_list[i], folder_name=folder_file_names.dill_folder), 'wb') as f:
			dill.dump(df, f)
		i += 1

	return df


class folder_file_names:
	"""
		Folder names to save data
	"""
	dill_folder = 'dills'
	excel_output_folder = 'excel_output_results'
	# excel_check_data_name='no_match_data.xlsx'
	# excel_check_data_name_2='gen_type_no_match.xlsx'
	# excel_final_output_name='Final_Results.xlsx'
	variable_path_dict = collections.OrderedDict()
	variable_dict = collections.OrderedDict()


class Headers_SHEPD_NG:
	"""
		Headers of interest for SHEPD and NG data
	"""
	SHEPD_Type='Type'
	SHEPD_Technology='Technology'
	SHEPD_sub_technology='sub-technology'
	SHEPD_OpenNetwork_BB='Open Netwrok Building Block'
	SHEPD_Substation='Substation'
	SHEPD_Scenario='Scenario'
	# Map_GSP='GSP Name'
	# Map_Primary='Primary Name'
	#
	# Map_2_GSP='GSP'
	# Map_2_Primary='PRIMARY'
	#
	# Map_3_GSP = 'GSP Name'
	# Map_3_Primary = 'Primary Name'
	#
	# Map_4_GSP='GSP'
	# Map_4_Primary='New Name'

class input_excel_files:
	"""

		"""
	variable_list = ['df_SHEPD', 'df_MAP_1', 'df_MAP_2', 'df_MAP_3', 'df_MAP_4', 'df_MAP_BB_1']
	variables_to_be_dilled = [False, False, False, False, True, False]
	sheet_list = ['Database', 'GSP List', 'SubstationLoad_Max_Primaries', 'GSP List', 'GSP', 'Maping to BBs']
	input_list = ['11kV DFES output dataset - SHEPD - v6 - data -modified.xlsx', 'GSP_NRN lookup.xlsx', \
		              '2019-20 SHEPD Load Estimates - v6.xlsx', '2019-20 SHEPD Load Estimates - v6.xlsx',
	              'missing_substations.xlsx',\
	              'DFES 2020 Final Submission to ESO_Updated_Map.xlsx']

class output_excel_files:
	excel_output_name = 'Final_Results.xlsx'
	excel_check_data_name='no_match_data.xlsx'
	excel_check_data_name_2 = 'gen_type_no_match.xlsx'
