#! /user/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('./')

import os
import cgi

# use Django 1.2
from google.appengine.dist import use_library
use_library('django', '1.2')

# Google App Engine Libraries
from google.appengine.api import memcache
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from django.utils import simplejson as json

import pktools


class BuildResult(object):

    def getData(self):
        import codecs
        
        get = memcache.get('getData')
        if get is not None:
            return get

        f = codecs.open("./resources/data.csv", "r", "utf-8")
        data = []
        csv = [i.split(',') for i in f]
        for i in csv:
            d = {'no': i[0].strip(),
                 'name': i[1].strip(),
                 'types': [i[2].strip(), i[3].strip()],
                 'traits': [j.strip() for j in i[4:-2]],
                 'evo': int(i[-2].strip()),
                 'gen': int(i[-1].strip())}
            data.append(d)
        f.close()
        get = data

        memcache.add('getData', get, time=21600)
        return get

    def getResult(self, queries, evo=0, gen=None, trt=0, or_=0):
        if gen == None:
            gen = ['after', 1]
        queryString = str(queries) + str(evo) + str(gen) + str(trt) + str(or_)

        result = memcache.get(queryString)
        if result is not None:
            return result

        calc = pktools.Effect()
        data = self.getData()
        result = []

        def getResultWithoutTrait(d):
            for q in queries:
                if not calc.isConform(q[0], q[1], d['types'], q[2]):
                    break
            else:
                if isCompliedWithOptions(d):
                    return {'name': d['name'],
                            'types': d['types']}
            return False
        def getResultWithTrait(d):
            for t in [trait for trait in d['traits']
                      if calc.isEffectiveTrait(trait)]:
                for q in queries:
                    if not calc.isConform(q[0], q[1], d['types'], q[2], t):
                        break
                else:
                    if isCompliedWithOptions(d):
                        return {'name': d['name'],
                                'types': d['types'],
                                'trait': t}
            return False
        def getResultWithoutTraitByOr(d):
            for q in queries:
                if (calc.isConform(q[0], q[1], d['types'], q[2]) and
                    isCompliedWithOptions(d)):
                    return {'name': d['name'],
                            'types': d['types']}
        def getResultWithTraitByOr(d):
            for t in [trait for trait in d['traits']
                      if calc.isEffectiveTrait(trait)]:
                for q in queries:
                    if (calc.isConform(q[0], q[1], d['types'], q[2], t) and
                        isCompliedWithOptions(d)):
                        return {'name': d['name'],
                                'types': d['types'],
                                'trait': t}
        def isCompliedWithOptions(d):
            if (evo <= d['evo'] and
                ((gen[0] == 'after' and gen[1] <= d['gen']) or
                 (gen[0] == 'before' and gen[1] >= d['gen']))):
                return True
            return False

        for i in data:
            if or_:
                without_trait = getResultWithoutTraitByOr(i)
                with_trait = getResultWithTraitByOr(i)
            else:
                without_trait = getResultWithoutTrait(i)
                with_trait = getResultWithTrait(i)
            
            if (not trt and len(i['traits']) == 1 and
                calc.isEffectiveTrait(i['traits'][0])):
                if without_trait and not with_trait:
                    continue
                    
            if without_trait:
                result.append(without_trait)
            elif with_trait and not trt:
                result.append(with_trait)

        memcache.add(queryString, result, time=3600)
        return result

    def getHtml(self):
        template_values = {"title": u"ポケモン耐性検索"}
        path = os.path.join(os.path.dirname(__file__),
                            './resources/base.html')
        return template.render(path, template_values).encode('utf-8')

    def getStaticResultsHtml(self, query):
        from cgi import parse_qs

        trans = pktools.Translate().typeEintoJ
        WORDS_DIC = {'4.0': u'4倍', '2.0': u'2倍', '1.0': u'等倍',
                     '0.5': u'1/2', '0.25': u'1/4', '0.0': u'無効',
                     'less': u'以下', 'more': u'以上', 'equal': '',
                     'nor': u'ノーマル', 'fir': u'炎',
                     'wat': u'水', 'ele': u'電気',
                     'gra': u'草', 'ice': u'氷',
                     'fig': u'格闘', 'poi': u'毒',
                     'gro': u'地面', 'fly': u'飛行',
                     'psy': u'エスパー', 'bug': u'虫',
                     'roc': u'岩', 'gho': u'ゴースト',
                     'dra': u'ドラゴン', 'dar': u'悪',
                     'ste': u'鋼'}
        TYPES = ['nor', 'fir', 'wat', 'ele', 'gra', 'ice',
                 'fig', 'poi', 'gro', 'fly', 'psy', 'bug',
                 'roc', 'gho', 'dra', 'dar', 'ste']

        keys = query.keys()

        queries = []
        for type_ in TYPES:
            if type_ in keys:
                comparison, effect = query[type_][0].split('_')
                effect = float(effect)
                if effect != -1:
                    queries.append([type_, effect, comparison])

        if 'evo' in keys:
            evo = int(query['evo'][0])
        else:
            evo = 0
        if 'gen' in keys:
            gen = query['gen'][0].split('_')
            gen[1] = int(gen[1])
        else:
            gen = ['after', 1]
        if 'trt' in keys:
            trt = int(query['trt'][0])
        else:
            trt = 0
        if 'or' in keys:
            or_ = int(query['or'][0])
        else:
            or_ = 0

        result = BuildResult().getResult(queries,
                                         evo=evo, gen=gen, trt=trt, or_=or_)

        result_list = []
        for r in result:
            d = {}
            d['name'] = r['name']
            d['types'] = [{'en': r['types'][0],
                           'ja': trans(r['types'][0])}]
            if len(r['types']) == 2:
                d['types'].append({'en': r['types'][1],
                                   'ja': trans(r['types'][1])})
            if 'trait' in r.keys():
                d['trait'] = r['trait']

            result_list.append(d)

        title_str_list = []
        for q in queries:
            s = ''.join([WORDS_DIC[str(i)] for i in q])
            title_str_list.append(s)
        if title_str_list:
            title_str = u'%sのポケモン一覧 - ポケモン耐性検索' % \
                        u'・'.join(title_str_list)
        else:
            title_str = u'ポケモン耐性検索'

        template_values = {"count": len(result),
                           "title": title_str,
                           "result_list": result_list}
        path = os.path.join(os.path.dirname(__file__),
                            './resources/result.html')
        return template.render(path, template_values).encode('utf-8')


class WsgiUrlMapper(object):
    def __init__(self, table):
        paths = sorted(table, key=lambda x: len(x), reverse=True)
        table = [(x, table[x]) for x in paths]
        self.table = table

    def __call__(self, environ, start_response):
        NAME = 'SCRIPT_NAME'
        INFO = 'PATH_INFO'

        scriptname = environ.get(NAME, '')
        pathinfo = environ.get(INFO, '')

        for path, app in self.table:
            if path == '' or path == '/' and pathinfo.startswith(path):
                return app(environ, start_response)

            if pathinfo == path or pathinfo.startswith(path) and \
                   pathinfo[len(path)] == '/':
                scriptname = scriptname + path
                pathinfo = pathinfo[len(path):]

                environ[NAME] = scriptname
                environ[INFO] = pathinfo

                return app(environ, start_response)


class Applications(object):

    status = '200 OK'

    def main(self, environ, start_response):
        from cgi import parse_qs
        query = parse_qs(environ.get('QUERY_STRING'))

        if '_escaped_fragment_' in query.keys():
            unescaped_query = parse_qs(query['_escaped_fragment_'][0][1:])
            output = BuildResult().getStaticResultsHtml(unescaped_query)
        elif environ.get('REQUEST_METHOD') == 'POST':
            TYPES = ['nor', 'fir', 'wat', 'ele', 'gra', 'ice',
                     'fig', 'poi', 'gro', 'fly', 'psy', 'bug',
                     'roc', 'gho', 'dra', 'dar', 'ste']
            wsgi_input = environ['wsgi.input']
            query = parse_qs(wsgi_input.read())

            corrected_query = {}
            if 'evo' in query.keys():
                corrected_query['evo'] = query['evo']
            if 'trt' in query.keys():
                corrected_query['trt'] = query['trt']
            for t in TYPES:
                if t in query.keys():
                    corrected_query[t] = ['%s_%s' % (query[t + 'c'][0],
                                                     query[t][0])]
            output = BuildResult().getStaticResultsHtml(corrected_query)
        else:
            output = BuildResult().getHtml()

        response_headers = [('Content-Type', 'text/html'),
                            ('Content-Length', str(len(output)))]
        start_response(self.status, response_headers)

        return [output]

    def api(self, environ, start_response):
        from cgi import parse_qs

        TYPES = ['nor', 'fir', 'wat', 'ele', 'gra', 'ice',
                 'fig', 'poi', 'gro', 'fly', 'psy', 'bug',
                 'roc', 'gho', 'dra', 'dar', 'ste']

        query = parse_qs(environ.get('QUERY_STRING'))
        keys = query.keys()

        queries = []
        for type_ in TYPES:
            if type_ in keys:
                comparison, effect = query[type_][0].split('_')
                effect = float(effect)
                if effect != -1:
                    queries.append([type_, effect, comparison])

        # option that exclude pokemon that can't evolve
        # 0: disabled
        # 1: enabled
        if 'evo' in keys:
            evo = int(query['evo'][0])
        else:
            evo = 0
        # specify generation
        # ex.
        # 'after_1': 1st generation and after it
        # 'before_3': 3rd generation and before it
        if 'gen' in keys:
            gen = query['gen'][0].split('_')
            gen[1] = int(gen[1])
        else:
            gen = ['after', 1]
        # option that ignore trait
        # 0: disabled
        # 1: enabled
        if 'trt' in keys:
            trt = int(query['trt'][0])
        else:
            trt = 0
        # option that change from and-search to or-search
        # 0: disabled
        # 1: enabled
        if 'or' in keys:
            or_ = int(query['or'][0])
        else:
            or_ = 0

        result = BuildResult().getResult(queries,
                                         evo=evo, gen=gen, trt=trt, or_=or_)

        if 'callback' in keys:
            dumped_result = '%s(%s)' % (query['callback'][0],
                                        json.dumps(result))
            content_type = 'text/javascript'
        else:
            dumped_result = json.dumps(result)
            content_type = 'application/json'

        output = dumped_result
        response_headers = [('Content-Type', content_type),
                            ('Content-Length', str(len(output)))]
        start_response(self.status, response_headers)

        # debug
        # import time
        # time.sleep(3)

        return [output]


def main():
    app = Applications()
    url_map = {'/api': app.api,
               '/': app.main,
               '': app.main}
    application = WsgiUrlMapper(url_map)
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
