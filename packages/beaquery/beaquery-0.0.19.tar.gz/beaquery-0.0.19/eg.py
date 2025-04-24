
import os
import sys
import beaapi
import pandas as pd
pd.set_option('display.max_colwidth', None)

beakey = os.environ['BEA_API_KEY']

# https://us-bea.github.io/beaapi/api.html
# https://us-bea.github.io/beaapi/iTables_to_api.html
#
def main():

    # Get some basic Meta-data. What are the table names?
    datasets_info = beaapi.get_data_set_list(beakey)
    dataset_names = list(datasets_info['DatasetName'])
    param_infos = {dataset_name: beaapi.get_parameter_list(beakey, dataset_name) for dataset_name in dataset_names}

    tbl = beaapi.get_data(beakey, "NIPA", TableName=table_param_val, Frequency=freq, Year=year)
    tbl.head()

    tbl = beaapi.get_data(beakey, "NIUnderlyingDetail", TableName=table_param_val, Frequency=freq, Year=year)
    tbl.head()

# Tools to help lookup table IDs from table descriptions
table_var = {'NIPA':'TableName',
    'NIUnderlyingDetail':'TableName',
    'MNE':None,
    'FixedAssets': 'TableName',
    'ITA':None,
    'IIP':None,
    'InputOutput':"TableID",
    'IntlServTrade':None,
    'GDPbyIndustry':"TableID",
    'Regional': "TableName",
    'UnderlyingGDPbyIndustry':"TableID"}
table_param_desc = {'NIPA':'Description',
    'NIUnderlyingDetail':'Description',
    'MNE':None,
    'FixedAssets': 'Description',
    'ITA':None,
    'IIP':None,
    'InputOutput':"Desc",
    'IntlServTrade':None,
    'GDPbyIndustry':"Desc",
    'Regional': "Desc",
    'UnderlyingGDPbyIndustry':"Desc"}
table_names = {}
for dataset_name, table_var_name in table_var.items():
    if table_var_name is not None:
        table_names[dataset_name] = beaapi.get_parameter_values(beakey, dataset_name, table_var_name)

def get_table_param_from_desc(dataset_name, desc):
    mask = table_names[dataset_name][table_param_desc[dataset_name]].str.contains(desc)
    results = table_names[dataset_name][mask]
    table_var_name = table_var[dataset_name]
    return table_var_name, results


main()
