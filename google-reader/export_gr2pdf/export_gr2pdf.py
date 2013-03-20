# -*- coding: utf-8 -*-

import codecs, json, sys, logging 
import xhtml2pdf, xhtml2pdf.pisa
import cStringIO

FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
logging.basicConfig(format='%(message)s', level=logging.DEBUG)

def export_pdf(source_file, target_file):
    logging.info('* Loading source: %s', source_file)
    src_file = codecs.open(source_file, 'r', encoding='utf-8')
    tmp_file = cStringIO.StringIO()
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

    logging.info('Converting to pdf: %s', target_file)
    out_file = codecs.open(target_file, 'wb', encoding='utf-8')

    pdf = xhtml2pdf.pisa.CreatePDF(tmp_file, out_file, encoding='utf-8')
    if not pdf.err:
        logging.info('PDF successfull created.')
    else:
        logging.error(pdf.err)
    
    out_file.close()


if __name__ == '__main__':
    TMP_FILE = 'temp.html'
    SYS_ENCODING = sys.getdefaultencoding()
    
    import argparse
    parser = argparse.ArgumentParser(description='Export google reader to pdf.')
    parser.add_argument('-f', dest='source', required=True, help='Source file to export. starred.json')
    parser.add_argument('-o', dest='target', required=True, help='PDF file to export. export.pdf')
    args = parser.parse_args()

    export_pdf(args.source, args.target)

