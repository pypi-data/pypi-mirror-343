#! env python
#
import argparse
import json
import os
import sys
import time
import xml


class BEAQueryH():
    def __init__(self):

        self.bsurl = 'https://apps.bea.gov/api/signup/'
        self.bdurl = 'https://apps.bea.gov/api/data/'
        if 'BEA_API_KEY' in os.environ:
                self.api_key = os.environ['BEA_API_KEY']
        else:
            print('BEA api_key required: %s' % (self.bsurl), file=sys.stderr)
            print('assign this key to BEA_API_KEY env variable',
                              file=sys.stderr)
            sys.exit()

        self.burl = '%s?&UserID=%s' % (self.bdurl, self.api_key)

    def getfixedassetdata(self, tbl, yr, fmt):
        pass

    def getnipatbls(self, dsn, fq, yr, fmt):
        if fq == None:
            fq = 'MQA'
        if yr == None:
            yr='X'
        params = ('&method=GetParameterValue&'
                  'DatasetName=NIPA&'
                  'ParameterName=%s&'
                  'ResultFormat=%s' %
                  (dsn, prm, fmt) )
        url = self.burl % params

    def getparamvals(self, dsn, prm, fmt):
        params = ('&method=GetParameterValue&'
                  'DatasetName=%s&'
                  'ParameterName=%s&'
                  'ResultFormat=%s' %
                  (dsn, prm, fmt) )
        url = self.burl % params

    def getparams(self, dsn, fmt):
        params = ('&method=getparameterlist&'
                  'DatasetName=%s&'
                  'ResultFormat=%s' %
                  (dsn, fmt) )
        url = self.burl % params

    def getdatasets(self, fmt):
        params = ('&method=GETDATASETLIST&'
                  'ResultFormat=%s' % fmt)
        url = self.burl % params
#
def main():
    argp = argparse.ArgumentParser(description='explore BEA structure')

    argp.add_argument('--dataset', help='specify the dataset',
                      choices=['NIPA', 'NIUnderlyingDetail', 'MNE',
                      'FixedAssets', 'ITA', 'IIP', 'InputOutpus',
                      'IntlServTrade', 'GDPbyIndustry', 'Regional',
                      'UnderlyingGDPbyIndustry', 'APIDatasetMetaData'])

    argp.add_argument('--format', help='result format',
                      choices=['json', 'XML'])
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

    BQ = BEAQueryH()

    argp.print_help()




if __name__ == '__main__':
    main()
