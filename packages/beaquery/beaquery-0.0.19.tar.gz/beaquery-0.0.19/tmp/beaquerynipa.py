#! env python
#
import argparse
import json
import os
import sys
import time
import xml

try:
    import beaquery.ebquery
except Exception as e:
    import ebquery


class BEAQueryNIPA():
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

        self.trurl = 'https://apps.bea.gov/national/Release/TXT/TablesRegister.txt'

        self.uq = ebquery._EBURLQuery()

    def gettableregister(self):
        resp = self.uq.query(self.trurl)
        rstr = resp.read().decode('utf-8')
        return rstr

    def gettable(self, ds, tn, fq, yr, fmt):
        params = ('&method=GetData&'
                  'DatasetName=%s&'
                  'TableName=%s&'
                  'Frequency=%s&'
                  'Year=%s&'
                  'ResultFormat=%s' %
                  (ds, tn, fq, yr, fmt) )
        url = self.burl + params
        resp = self.uq.query(url)
        rstr = resp.read().decode('utf-8')
        return rstr

#
def main():
    argp = argparse.ArgumentParser(description='get NIPA data')

    argp.add_argument('--dataset', default='NIPA',
                      choices=['NIPA', 'NIUnderlyingDetail'], help='result format')
    argp.add_argument('--table', help='specify tablename ')
    argp.add_argument('--tableregister',
                      action='store_true', default=False,
                      help='get table register ')
    argp.add_argument('--freq', default = 'A',
                     help='frequency M, Q, A ')
    argp.add_argument('--yr', default = 'X',
                      help='year 1929-2025 or X ')
    argp.add_argument('--format', default='json',
                      choices=['json', 'XML'], help='result format')

    args=argp.parse_args()

    BN = BEAQueryNIPA()

    if args.tableregister:
       txt = BN.gettableregister()
       print(txt)
    elif args.table:
        tbl = BN.gettable(args.dataset, args.table,
                          args.freq, args.yr, args.format)
        print(tbl)
    else:
        argp.print_help()
        sys.exit()




if __name__ == '__main__':
    main()
