import urllib
import json as simplejson

import time
import os

api_url = 'https://%s.wikipedia.org/w/api.php'

def _unicode_urlencode(params):
    """
    A unicode aware version of urllib.urlencode.
    Borrowed from pyfacebook :: http://github.com/sciyoshi/pyfacebook/
    """
    if isinstance(params, dict):
        params = params.items()
    return urllib.urlencode([(k, isinstance(v, unicode) and v.encode('utf-16') or v) for k, v in params])

def _run_query(args, language, retry=5, wait=5):
    """
    takes arguments and optional language argument and runs query on server
    if a socket error occurs, wait the specified seconds of time and retry for the specified number of times
    """
    url = api_url % (language)
    data = _unicode_urlencode(args)
    while True:
        try:
            search_results = urllib.urlopen(url, data=data)
            # print language +": " +args['titles'] +'\n'
            json = simplejson.loads(search_results.read())
        except Exception:
            if not retry:
                json = None
                break
            retry -= 1
            time.sleep(wait)
        else:
            break
    return json

def query_text_raw(title, language='en'):
    """
    action=query
    Fetches the article in wikimarkup form
    """
    query_args = {
        'action': 'query',
        'titles': title,
        'explaintext': True,
        'prop': 'extracts',
        'format': 'json',
        'redirects': ''
    }
    json = _run_query(query_args, language)
    if not json == None:
        for page_id in json['query']['pages']:
            if page_id != '-1' and 'missing' not in json['query']['pages'][page_id]:
                response = {
                    'text': json['query']['pages'][page_id]['extract']
                }
                return response
    return None

def create_lang_list(filename):
    f = open(filename, "r")
    lang = f.readline().strip("\r\n").split("\t")
    f.close()
    return lang

def write_content_to_file(name, article, language):
    filepath = "data/%s/%s.txt" %(language, name)
    d = os.path.dirname(filepath)

    if not os.path.exists(d):
        os.makedirs(d)

    f = open(filepath, "w")
    f.write(article.encode('utf-16'))
    f.close()

def read_file_by_line(filename, languages):
    f = open(filename, "r")
    for i, line in enumerate(f):
        # TODO read line as a list and then access the specific document name in the specific language
        if not i == 0:
            titles = line.strip("\r\n").split("\t")
            for index, lang in enumerate(languages):
                if not titles[index] == "":
                    article = query_text_raw(titles[index], lang)
                    if not article == None:
                        write_content_to_file("".join(titles[0].split()), article['text'], lang)


if __name__ == "__main__":
    # response = query_text_raw("Princess Charlotte of Cambridge")
    # print(response)
    # print(create_lang_list("test-sample"))
    languages = create_lang_list("test-sample")
    read_file_by_line("test-sample", languages)