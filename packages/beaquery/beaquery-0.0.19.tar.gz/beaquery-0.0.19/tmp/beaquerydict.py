#! env python
#
import os
import sys
import json
import time
import argparse
import pandas as pd
import webbrowser

import beaapi


class BEAQueryDict():
    def __init__(self):

        # BEA
        self.burl = 'https://apps.bea.gov/api/signup/'
        if 'BEA_API_KEY' in os.environ:
                self.api_key = os.environ['BEA_API_KEY']
        else:
            print('BEA api_key required: %s' % (self.burl), file=sys.stderr)
            print('assign this key to BEA_API_KEY env variable',
                              file=sys.stderr)
            sys.exit()

        self.delay = 2

        # pandas
        pd.set_option('display.max_colwidth', None)
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)

    def dsparamvals(self, dataset_name, parameter_name):
        """ dsparamvals(dataset_name, parameter_name)
        dataset_name - name of the dataset
        parameter_name - name of the parameter
        return pandas dataframe for the values of the dataset parameter
        """
        print('Values for dataset %s parameter %s' % (dataset_name,
                          parameter_name), file=sys.stderr)
        try:
            pvalframe = beaapi.get_parameter_values(self.api_key,
                            dataset_name,
                            parameter_name)
        except Exception as e:
            print('dsparamvals get_parameter_values %s' % e)
            sys.exit()

        time.sleep(self.delay)
        return pvalframe


    def dsparams(self, dataset_name):
        """ dsparams(dataset_name)
        dataset_name = name of the dataset
        return pandas frame for the parameters of a dataset
        """
        print('Parameters for %s dataset' % dataset_name,
        file=sys.stderr)
        try:
            paramframe = beaapi.get_parameter_list(self.api_key,
                                                       dataset_name)
        except Exception as e:
            print('dsparams get_parameter_list %s' % e)
            sys.exit()

        time.sleep(self.delay)
        return paramframe

    def datasets(self):
        """ datasets()
        return pandas frame for BEA datasets
        """
        try:
            datasetsframe = beaapi.get_data_set_list(self.api_key)
        except Exception as e:
            print('hierarchy get_data_set_list %s' % e)
            sys.exit()

        time.sleep(self.delay)
        return datasetsframe

    def aa2table(self, cap, aa):
       """ aa2table(aa)

       convert array of arrays to an html table
       aa - array of arrays
       """
       tbla = []
       # table
       tbla.append('<table border="1">')
       # table header
       hdra = aa[0]
       hdr = '</th><th>'.join(hdra)
       tbla.append('<tr><th scope="col">%s</th></tr>' % (hdr) )
       cap = '<caption>%s</caption>' % cap
       tbla.append(cap)
       # table rows
       for i in range(1, len(aa) ):
           rowa = aa[i]
           for j in range(len(rowa)):
               if rowa[j] == None:
                   rowa[j] = ''
               elif type(rowa[j]) == type(1):
                   rowa[j] = '%d' % rowa[j]
           row = '</td><td>'.join(rowa)
           tbla.append('<tr><td>%s</td></tr>' % (row) )

       # close
       tbla.append('</table>')
       return tbla

    def datasetparametervaluestables(self, ds, dict):
        """ datasetparametervaluestables(ds, param, dict)
        ds - dataset name
        param - parameter name
        dict - dictionary containing schema for values of a parameter of a dataset
        return an html table rendering for the values of the parameter
        """
        for p in  dict['ParameterValues'].keys():
            pa = dict['ParameterValues'][p]
            cap = 'Parameter Values for Dataset %s Parameter %s' % (ds, p)
            tbla = self.aa2table(cap, pa)
        return tbla

    def datasetparameterstable(self, ds, dict):
        """ datasetparameterstable(ds, dict)
        ds - dataset name
        dict - dict containing data model for a dataset
        return an html table rendering for the parameters of a dataset
        """
        cap = 'BEA Dataset %s Parameters' % ds
        pa = dict['Parameters']
        tbla = self.aa2table(cap, pa)
        return tbla


    def datasethierarchytables(self, dict):
        """ datasethierarchytables(dict)
        render BEA dataset names parameters and values to html tables
        dict = dictionary containing model data for datasets
        return array containing an table renderings
        """

        cap = 'BEA Datasets'
        aa = []
        aa.append(['DatasetName', 'DatasetDescription'])
        ka = [k for k in dict['datasets'].keys()]
        for k in ka:
            d = dict['datasets'][k]['DatasetDescription']
            ra = [k, d]
            aa.append(ra)
        tbls = self.aa2table(cap, aa)
        for k in ka:
            tbls.append('<h3>Parameters for %s</h3>' % k)
            ht = self.datasetparameterstable(k, dict['datasets'][k])
            if ht != None:
                tbls.extend(ht)
            tbls.append('<h3>Parameter Values for %s</h3>' % k)
            ht = self.datasetparametervaluestables(k, dict['datasets'][k])
            if ht != None:
                tbls.extend(ht)

        return tbls

    def datasethierarchyhtml(self, dict):
        """ datasethierarchyhtml(dict)
        render BEA dataset hierarchy to an html page
        dict - dictionary containing data model for datasets
        return array containing the html rendering
        """
        htmla = []
        htmla.append('<html>')
        ttl = 'BEA Dataset Data Hierarchy'
        htmla.append('<head><h1>%s</h1></head>' % (ttl) )

        tbls = self.datasethierarchytables(dict)
        htmla.extend(tbls)

        htmla.append('</html>')

        return htmla


    def datasethierarchyshow(self, dict):
        """ datasethierarchyshow(dict)
        display the html page depicting BEA dataset model to a browser
        dict - dictionary containing data model for datasets
        """
        htmla = self.datasethierarchyhtml(dict)
        fn = '/tmp/beahierarchy.html'
        with open(fn, 'w') as fp:
            fp.write(''.join(htmla))
        webbrowser.open('file://%s' % fn)

    def datasetparamvaldict(self, i, pvdict):
        """ datasetparamvaldict(i, pvdict)
        make a python dictionary for values at index i
        i - index into pvdict
        pvdict - parameter values dictionary for a dataset
        return the dictionary
        """
        pvd = {}
        for k in pvdict.keys():
            pvd[k] = pvdict[k][i]
        return pvd

    def datasetparamvalsdict(self, dsdict, dn):
        """ datasetparamvalsdict(dsdict, dn)
        make a dictionary for parameter values for a dataset
        dsdict - dataset hierarchy dictionary
        dn - dataset name
        store result in the dataset hierarchy dictionary
        """
        dsdict['datasets'][dn]['ParameterValues'] = {}
        for i in range(1, len(dsdict['datasets'][dn]['Parameters'])):
            pn = dsdict['datasets'][dn]['Parameters'][1][0]
            pvalframe = self.dsparamvals(dn, pn)
            pvalsdict = pvalframe.to_dict()
            ks = [k for k in pvalsdict.keys()]
            ix = [i for i in pvalsdict[ks[0]].keys()]
            rows = []
            rows.append(ks)
            for i in ix:
                rw = [pvalsdict[k][i] for k in ks]
                rows.append(rw)
            dsdict['datasets'][dn]['ParameterValues'][pn]=rows

        return

    def datasetparamsdict(self, dsdict, dn):
        """ datasetparamsdict(dsdict, dn)
        make a dictionary for parameters for a dataset
        dsdict - dataset hierarchy dictionary
        dn - dataset name
        store result in the dataset hierarchy dictionary
        """
        paramsframe = self.dsparams(dn)
        paramsdict = paramsframe.to_dict()
        ks = [k for k in paramsdict.keys()]
        ix = [i for i in paramsdict[ks[0]].keys()]
        rows = []
        rows.append(ks)
        for i in ix:
            rw = [paramsdict[k][i] for k in ks]
            rows.append(rw)
        dsdict['datasets'][dn]['Parameters'] = rows
        return

    def initdatasetdict(self, dsf):
        """ initdatasetsict(dsf)
        initialize the dataset hierarchy dictionary
        dsf - pandas fræme representing the dataset
        return the dataset dict
        """
        dsr = dsf.to_dict()
        dsdict = {}
        dsdict['datasets'] = {}
        for i in dsr['DatasetName'].keys():
            n = dsr['DatasetName'][i]
            d = dsr['DatasetDescription'][i]
            dsdict['datasets'][n] = {}
            dsdict['datasets'][n]['DatasetDescription'] = d
        return dsdict

    def datasethierarchydict(self):
        """ datasethierarchydict()
        populate the BEA dataset hierarchy model
        return a python dictionary representing the hierarchy
        """
        datasetsframe = self.datasets()
        dsdict = self.initdatasetdict(datasetsframe)

        # datasetsframe.to_excel('beahierarchy.xlsx', sheet_name='datasets')

        for n in dsdict['datasets'].keys():
            self.datasetparamsdict(dsdict, n)
            self.datasetparamvalsdict(dsdict, n)

        return dsdict
#
def main():
    argp = argparse.ArgumentParser(description='explore BEA structure')

    argp.add_argument('--dataset', help='specify the dataset',
                      choices=['NIPA', 'NIUnderlyingDetail', 'MNE',
                      'FixedAssets', 'ITA', 'IIP', 'InputOutpus',
                      'IntlServTrade', 'GDPbyIndustry', 'Regional',
                      'UnderlyingGDPbyIndustry', 'APIDatasetMetaData'])
    argp.add_argument('--getdata', action='store_true', default=False,
        help='get data for a dataset')
    argp.add_argument('--table', help='table name')
    argp.add_argument('--freq', default = 'A',
                      choices = ['M','Q','A'],
                      help='frequency M,Q,A')
    argp.add_argument('--year', default = 'X',
                      help='year 1929-CY or X for all')

    argp.add_argument('--datasets', action='store_true', default=False,
        help='display datasets')
    argp.add_argument('--params', action='store_true', default=False,
        help='display parameters for a dataset')
    argp.add_argument('--paramvals', action='store_true', default=False,
              help='show values for a parameter of a dataset')
    argp.add_argument('--hierarchy', action='store_true', default=False,
        help='display BEA data organization hierarchy')

    argp.add_argument('--json', action='store_true', default=False,
        help='display json')
    argp.add_argument('--html', action='store_true', default=False,
        help='display html')
    argp.add_argument('--show', action='store_true', default=False,
        help='display hierarchy html in browser')
    args=argp.parse_args()

    BQ = BEAQueryDict()
    if args.hierarchy:
        dsdict = BQ.datasethierarchydict()
        if args.show:
            BQ.datasethierarchyshow(dsdict)
        elif args.html:
            htmla = BQ.datasethierarchytables(dsdict)
            print(''.join(htmla))
        elif args.json:
            dsjson = json.JSONEncoder().encode(dsdict)
            print(dsjson)
        else:
            print(dsdict)
    elif args.getdata:
        df = BQ.getdata(args.dataset, args.table,
                        args.freq, args.year)
        print(df)
    elif args.datasets:
        ds = BQ.datasets()
        if args.json:
            dsjson = json.JSONEncoder().encode(ds)
            print(dsjson)
        else:
            print(ds)
    elif args.params:
        if args.dataset == None:
            print('a dataset must be provided')
            argp.print_help()
            sys.exit()
        ps = BQ.dsparams(args.dataset)
        if args.json:
            psjson = json.JSONEncoder().encode(ps)
            print(psjson)
        else:
            print(ps)
    elif args.paramvals:
        if args.dataset == None or args.param == None:
            print('a dataset and parameter must be provided')
            argp.print_help()
            sys.exit()
        pvs = BQ.dsparamvals(args.dataset, args.param)
        print(pvs)
    else:
        argp.print_help()




if __name__ == '__main__':
    main()
