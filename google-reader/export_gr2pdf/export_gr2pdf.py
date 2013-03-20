# -*- coding: utf-8 -*-

import codecs, json, sys
import logging
FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
logging.basicConfig(format='%(message)s', level=logging.DEBUG)

def export_html(filename):
    logging.info('* Loading source: %s', filename)
    src_file = codecs.open(filename, 'r', encoding='utf-8')
    tmp_file = codecs.open(TMP_FILE, 'w', encoding='utf-8')
    data = json.load(src_file, encoding='utf-8')
    count = len(data['items'])
      
    logging.info('  Title: %s', data['title'])
    logging.info('  Total %d entries', count)
    logging.info('  Converting entries to html...')
    tmp_file.write('<h1 style="text-align:center;">%s</h1>\n' % data['title'])
    tmp_file.write('<div style="margin-bottom: 50px;">\n')
    for i, item in enumerate(data['items']):
        logging.info(u'  [%%%dd/%%d] %%s' % len(str(count)) % (i + 1, count, item['title']))
        tmp_file.write('<h2 style="background: #EEE;">%s</h2>\n' % item['title'])
        content = item.get('content', item.get('summary', { 'content': '' }))
        tmp_file.write('<div>%s</div>\n' % content['content'])
        tmp_file.write('</div>\n')
    tmp_file.close()
    src_file.close()

if __name__ == '__main__':
    TMP_FILE = 'temp.html'
    SYS_ENCODING = sys.getdefaultencoding()
    
    import argparse
    parser = argparse.ArgumentParser(description='Export google reader to pdf.')
    parser.add_argument('-f', dest='source', required=True, help='Source file to export. starred.json')
    parser.add_argument('-o', dest='target', required=True, help='PDF file to export. export.pdf')
    args = parser.parse_args()

    export_html(args.source)

