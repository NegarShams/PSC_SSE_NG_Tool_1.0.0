"""
#######################################################################################################################
###											Example DataFrame Processing											###
###																													###
###		Code developed by Negar Shams (negar.shams@PSCconsulting.com, +44 7436 544893) as part of PSC 		 		###
###		project JK7938 - SHEPD - studies and automation																###
###																													###
#######################################################################################################################
"""
import SSE_NG
import SSE_NG.GSP_assigner_function as GSP_assigner_function
import SSE_NG.BB_assigner_function as BB_assigner_function
import SSE_NG.aggregator_function as aggregator_function

# section for input excel files names:
DFES_dataset_excel_name = '11kV DFES output dataset - SHEPD - v6 - data -modified.xlsx'
GSP_NRN_excel_name = 'GSP_NRN lookup.xlsx'
SHEPD_load_estimates_excel_name = '2019-20 SHEPD Load Estimates - v6.xlsx'
missing_substations_excel_name = 'missing_substations.xlsx'
DFES_final_submission_excel_name = 'DFES 2020 Final Submission to ESO_Updated_Map.xlsx'

# section for inputs which are typically left unchanged:
# input excel files sheets names
DFES_dataset_sheet_name = 'Database'
GSP_NRN_sheet_name = 'GSP List'
SHEPD_load_estimates_sheet_name_1 = 'SubstationLoad_Max_Primaries'
SHEPD_load_estimates_sheet_name_2 = 'GSP List'
missing_substations_sheet_name = 'GSP'
DFES_final_submission_sheet_name = 'Maping to BBs'

# output excel files names
excel_final_output_name = 'Final_Results.xlsx'
excel_no_match_substations_name = 'no_match_substations.xlsx'
excel_no_match_gen_load_types_name = 'no_match_gen_load_types.xlsx'

# output excel files sheets names
no_match_substation_sheet_name = 'no_match_substations'
zero_GSP_substation_sheet_name = 'zero_GSP_substations'
no_data_type_match_sheet_name = 'data_type_no_match'
grouped_final_data_sheet_name = 'grouped_final_data'
ungrouped_final_data_sheet_name = 'ungrouped_final_data'

input_list = [DFES_dataset_excel_name, GSP_NRN_excel_name, SHEPD_load_estimates_excel_name, \
              SHEPD_load_estimates_excel_name, missing_substations_excel_name, DFES_final_submission_excel_name]

sheet_list = [DFES_dataset_sheet_name, GSP_NRN_sheet_name, SHEPD_load_estimates_sheet_name_1, \
              SHEPD_load_estimates_sheet_name_2, missing_substations_sheet_name, DFES_final_submission_sheet_name]


# main functions
print('main code successfully started running')
df_SHEPD, Substations, Substations_with_0_GSP_names = GSP_assigner_function.GSP_assigner(input_list=input_list, \
                                                                                         sheet_list=sheet_list,
                                                                                         excel_check_data_name=excel_no_match_substations_name, \
                                                                                         no_match_substation_sheet_name=no_match_substation_sheet_name, \
                                                                                         zero_GSP_substation_sheet_name=zero_GSP_substation_sheet_name)
print('GSP assignment has successfully finished')
df_SHEPD, data_type_not_mapped = BB_assigner_function.BB_assigner(
    excel_check_data_name=excel_no_match_gen_load_types_name, output_sheet_name=no_data_type_match_sheet_name)
print('NG Building Block assignment has successfully finished')
df_grouped_final, df_ungrouped_final = aggregator_function.aggregator(excel_output_name=excel_final_output_name,
                                                                      grouped_final_data_sheet_name=grouped_final_data_sheet_name, \
                                                                      ungrouped_final_data_sheet_name=ungrouped_final_data_sheet_name)
print('total code has successfully finished')

k = 1
