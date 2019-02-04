import subprocess
from bs4 import BeautifulSoup as Soup
import os
import pandas as pd
from sys import argv

workdir = str(argv[1])
f_reference = workdir + '/input/' + "gwas_reference_toadd"
csvfile = pd.read_csv(f_reference, keep_default_na=False)
codes = csvfile['code']
outdir = workdir + '/output/' + 'pathways'
if not os.path.exists(outdir):
    os.makedirs(outdir)

# new headers and nav bars for html files
newheader = '<style>' \
            '.vega-actions a {' \
            'margin-right: 12px;' \
            'color: #757575;' \
            'font-weight: normal;' \
            'font-size: 13px;' \
            '}' \
            '.error {' \
            'color: red;' \
            '}' \
            '</style>' \
            '<script type="text/javascript" src="https://cdn.jsdelivr.net/npm//vega@4"></script>' \
            '<script type="text/javascript" src="https://cdn.jsdelivr.net/npm//vega-lite@2.6.0"></script>' \
            '<script type="text/javascript" src="https://cdn.jsdelivr.net/npm//vega-embed@3"></script>' \
            '<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />' \
            '<meta http-equiv="X-UA-Compatible" content="IE=edge">' \
            '<meta name="viewport" content="width=device-width, initial-scale=1">' \
            '<link href="https://fonts.googleapis.com/css?family=Open+Sans:300,400,600,700" rel="stylesheet" type="text/css">' \
            '<link rel="stylesheet" type="text/css" href="https://phenviz.navigome.com/static/Font-Awesome-4.7/css/font-awesome.min.css">' \
            '<link rel="stylesheet" type="text/css" href="https://phenviz.navigome.com/static/css/bootstrap.min.css">' \
            '<link rel="stylesheet" type="text/css" href="https://phenviz.navigome.com/static/css/bootstrap-theme.css">' \
            '<link rel="icon" type="image/png" href="https://phenviz.navigome.com/static/images/gnomic_icon.png">' \
            '<script src="https://phenviz.navigome.com/js/jquery.min.js"></script>' \
            '<script src="https://phenviz.navigome.com/js/bootstrap.js"></script>' \

for i in codes:
    phenotype = csvfile[csvfile['code'] == i]['phenotype'].iloc[0]
    cmd = ['python', workdir + '/scripts/' + 'navigome_vis8_pathways.py',
           workdir + '/input/' + 'pathways_per_phenotype/' + str(i), str(i),
           workdir + '/output/' + 'pathways/' + str(i) + '.pathways']
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    (output, err) = process.communicate()
    p_status = process.wait()
    print(str(i))
    with open(workdir + '/output/' + 'pathways/' + str(i) + '.pathways' + '.html', 'r') as f:
        head = newheader + '<title>' + "Pathways: " + str(i) + '</title>'
        html = f.read()
        soup = Soup(html, features="html.parser")
        soup.head.contents = Soup(head,
                                  features="html.parser")
        soup.div.insert_before(
            Soup(
                "<h4>Pathways: " +
                phenotype +
                ' (' +
                str(i) +
                ')' +
                "</h4>",
                features="html.parser"))
        soup = str(soup).replace(
            'embedOpt = {"mode": "vega-lite"};',
            'embedOpt = {"mode": "vega-lite", "loader": vega.loader({target: \'_blank\'})};')
    with open(workdir + '/output/' + 'pathways/' + str(i) + '.pathways' + '.html', 'w') as fout:
        fout.write(str(soup))
