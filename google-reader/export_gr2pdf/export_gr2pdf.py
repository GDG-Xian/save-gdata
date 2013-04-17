# -*- coding: utf-8 -*-

import codecs, json, sys, logging 
import xhtml2pdf, xhtml2pdf.pisa
import cStringIO

FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
logging.basicConfig(format='%(message)s', level=logging.DEBUG)

def export_pdf(source_file, target_file):
    logging.info('Loading source: %s', source_file)
    src_file = codecs.open(source_file, 'r', encoding='utf-8')
    tmp_file = codecs.open(TMP_FILE, 'w', encoding='utf-8')
    data = json.load(src_file, encoding='utf-8')
    count = len(data['items'])
      
    logging.info('  Title: %s', data['title'])
    logging.info('  Total %d entries', count)
    logging.info('  Converting entries to html...')
    tmp_file.write('''<!DOCTYPE html>
    <html>
        <head>
            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
            <!-- <link rel="stylesheet" type="text/css" href="style.css" />  -->
            <style type="text/css">
            @font-face {
                font-family: simsun;
                src: url(/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc);
            }
            body{
                font-family: simsun;
            }

            .article { margin-bottom: 30px; width: 210mm; }

            @page {
             margin: 1cm;
             margin-bottom: 2.5cm;
             font-family: simhei;
             @frame footer {
               -pdf-frame-content: footerContent;
               bottom: 2cm;
               margin-left: 1cm;
               margin-right: 1cm;
               height: 1cm;
               font-family: simhei;
             }
            }
            </style>
        </head>
        <body>''')
    tmp_file.write('<h1 style="text-align:center;">%s</h1>\n' % data['title'])

    for i, item in enumerate(data['items']):
        logging.info(u'  [%%%dd/%%d] %%s' % len(str(count)) % (i + 1, count, item['title']))
        tmp_file.write('<div style="article">\n')
        tmp_file.write('<h2 style="background: #EEE;">%s</h2>\n' % item['title'])
        content = item.get('content', item.get('summary', { 'content': '' }))
        tmp_file.write('<p>%s</p>\n' % content['content'])
        tmp_file.write('</div>\n')
    tmp_file.write('</body></html>\n')
    tmp_file.close()
    src_file.close()

    logging.info('Converting to pdf: %s', target_file)
    out_file = open(target_file, 'wb')
    tmp_file = open(TMP_FILE, 'rb')
    # css_text = codecs.open(CSS_FILE, 'r').read()

    pdf = xhtml2pdf.pisa.CreatePDF(tmp_file, out_file, link_callback=False)
    if not pdf.err:
        logging.info('PDF successfull created.')
    else:
        logging.error(pdf.err)
    
    out_file.close()


if __name__ == '__main__':
    TMP_FILE = 'temp.html'
    SYS_ENCODING = sys.getdefaultencoding()
    CSS_FILE = 'style.css'

    import argparse
    parser = argparse.ArgumentParser(description='Export google reader to pdf.')
    parser.add_argument('-f', dest='source', required=True, help='Source file to export. starred.json')
    parser.add_argument('-o', dest='target', required=True, help='PDF file to export. export.pdf')
    args = parser.parse_args()

    export_pdf(args.source, args.target)

