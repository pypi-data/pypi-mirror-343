#! env python
#
import os
import sys
import time
import argparse
import beaapi
import pandas as pd

try:
    import beaquery.ebquery
except Exception as e:
    import ebquery


class BEAQuery():
    def __init__(self):

        self.burl = 'https://apps.bea.gov/api/signup/'
        if 'BEA_API_KEY' in os.environ:
                self.api_key = os.environ['BEA_API_KEY']
        else:
            print('BEA api_key required: %s' % (self.burl), file=sys.stderr)
            print('assign this key to BEA_API_KEY env variable',
                              file=sys.stderr)
            sys.exit()

        pd.set_option('display.max_colwidth', None)
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)

    def gettableregister(self):
        resp = self.uq.query(self.trurl)
        rstr = resp.read().decode('utf-8')
        return rstr

    def gettfydata(self, ds, tn, fq, yr):
        """ gettfydata(ds, parameter_name)
        ds - name of the dataset
        tn - table name
        fq = frequency M,Q,Y
        yr - year or X for all
        return pandas dataframe for the dataset parameter data
        """
        try:
            pvalframe = beaapi.get_data(self.api_key,
                               ds, tn,
                               Frequency=fq,
                               Year=yr)
        except Exception as e:
            print('dsparamvals gettfydata %s' % e)
            sys.exit()

        time.sleep(self.delay)
        return pvalframe

    def gettydata(self, ds, tn, fq, yr):
        """ gettfydata(ds, parameter_name)
        ds - name of the dataset
        tn - table name
        yr - year or X for all
        return pandas dataframe for the dataset parameter data
        """
        try:
            pvalframe = beaapi.get_data(self.api_key,
                               ds, tn,
                               Year=yr)
        except Exception as e:
            print('dsparamvals gettydata %s' % e)
            sys.exit()

        time.sleep(self.delay)
        return pvalframe

    def getdcydata(self, ds, doi, cl, yr):
        """ getdata(ds, parameter_name)
        ds - name of the dataset
        doi - direction of investment
        cl = classification
        yr - year or all
        return pandas dataframe for the dataset parameter data
        """
        try:
            pvalframe = beaapi.get_data(self.api_key,
                               ds, DirectionOfInvestment=doi,
                               Classification=cl,
                               Year=yr)
        except Exception as e:
            print('dsparamvals getdcydata %s' % e)
            sys.exit()

        time.sleep(self.delay)
        return pvalframe

    def dsparamvals(self, dataset_name, parameter_name):
        print('Values for dataset %s parameter %s' % (dataset_name,
                                                      parameter_name))
        try:
            param_vals = beaapi.get_parameter_values(self.api_key,
                                                     dataset_name,
                                                     parameter_name)
        except Exception as e:
            print('dsparamvale get_parameter_values %s' % e)
            sys.exit()

        print(param_vals)

    def dsparamhier(self, dataset_name):
        print('Parameters for %s dataset' % dataset_name)
        try:
            list_of_params = beaapi.get_parameter_list(self.api_key,
                                                       dataset_name)
        except Exception as e:
            print('dsparams get_parameter_list %s' % e)
            sys.exit()

        print(list_of_params)

        for parameter_name in list_of_params['ParameterName']:
            time.sleep(2)
            self.dsparamvals(dataset_name, parameter_name)

    def dsparams(self, dataset_name):
        print('Parameters for %s dataset' % dataset_name)
        try:
            list_of_params = beaapi.get_parameter_list(self.api_key,
                                                       dataset_name)
        except Exception as e:
            print('dsparams get_parameter_list %s' % e)
            sys.exit()

        print(list_of_params)

    def metadata(self):
        print('Metadata Search examples')
        try:
            grossdom = beaapi.search_metadata('Gross domestic',
            self.api_key)
        except Exception as e:
            print('metadata search_metadata  %s' % e)
            sys.exit()

        print(grossdom)

    def datasets(self):
        print('Dataset Names')
        try:
            datasets_info = beaapi.get_data_set_list(self.api_key)
        except Exception as e:
            print('hierarchy get_data_set_list %s' % e)
            sys.exit()

        print(datasets_info)
        return datasets_info


    def hierarchy(self):
        datasets_info = self.datasets()

        for dataset_name in datasets_info['DatasetName']:
            time.sleep(2)
            self.dsparamhier(dataset_name)

#
def main():
    argp = argparse.ArgumentParser(description='explore BEA structure')

    argp.add_argument('--dataset', help='specify the dataset',
                      choices=['NIPA', 'NIUnderlyingDetail', 'MNE',
                      'FixedAssets', 'ITA', 'IIP', 'InputOutpus',
                      'IntlServTrade', 'GDPbyIndustry', 'Regional',
                      'UnderlyingGDPbyIndustry', 'APIDatasetMetaData'])

    argp.add_argument('--param', help='specify a  parameter for a dataset')

    argp.add_argument('--hierarchy', action='store_true', default=False,
        help='display BEA data organization hierarchy')
    argp.add_argument('--datasets', action='store_true', default=False,
        help='display datasets')
    argp.add_argument('--params', action='store_true', default=False,
        help='display parameters for a dataset')
    argp.add_argument('--paramvals', action='store_true', default=False,
              help='show values for a parameter of a dataset')
    args=argp.parse_args()

    BQ = BEAQuery()
    if args.hierarchy:
        BQ.hierarchy()
    elif args.datasets:
        BQ.datasets()
    elif args.params:
        if args.dataset == None:
            print('a dataset must be provided')
            argp.print_help()
            sys.exit()
        BQ.dsparams(args.dataset)
    elif args.paramvals:
        if args.dataset == None and args.param == None:
            print('a dataset and parameter must be provided')
            argp.print_help()
            sys.exit()
        BQ.dsparamvals(args.dataset, args.param)




if __name__ == '__main__':
    main()
