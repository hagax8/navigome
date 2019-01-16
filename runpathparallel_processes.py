import subprocess
from bs4 import BeautifulSoup as Soup
import os
import pandas as pd


f_reference = "gwas_reference_toadd"
csvfile = pd.read_csv(f_reference)

f_pathways = "list_of_significant_pathways_toadd"
csvfilep = pd.read_csv(f_pathways)

codes = csvfile['code']

outdir = 'gene_content'
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
            '<script src="https://phenviz.navigome.com/js/bootstrap.js"></script>'


adddiv = ('<div class="col-lg-12 col-md-12 content-item content-item-1">' +
          '<p>This is a parallel coordinates visualization ' +
          'for per-tissue gene associations ' +
          'with the phenotype of interest. ' +
          'It shows which genes are significant for this phenotype ' +
          'and in which tissues, based on gene expression (eQTL) data. ' +
          'For many phenotypes, this visualization might be a bit "crowded". ' +
          'All genes (= lines) displayed are significant ' +
          '(p-value &le; 0.05/20000) in at least one tissue. ' +
          'Hover over any line (gene) ' +
          'to see the gene\'s associations across tissues. ' +
          'The association statistics ' +
          'were computed using ' +
          '<a href="https://github.com/hakyimlab/MetaXcan">S-PrediXcan</a>. ' +
          'Clicking on a specific gene will lead to ' +
          'its tissue profile across all Navigome phenotypes.' +
          '</p>' +
          '</div>')

for index, row in csvfilep.iterrows():
    phenotype = csvfile[csvfile['code']==row['code']]['phenotype'].iloc[0]

    cmd = ['python', 'navigome_vis7_parallel.py',
           'gene_content_magma_data/'+row['code']+'_'+row['pathway'],
           'gene_content/'+str(row['code'])+'_'+str(row['pathway'])]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    (output, err) = process.communicate()
    p_status = process.wait()
    head = newheader + '<title>' + str(row['code'])+'_'+str(row['pathway']) + '</title>'
    print(str(row['code'])+'_'+str(row['pathway']))
    with open('gene_content/'+str(row['code'])+'_'+str(row['pathway'])+'.html','r') as f:
        html = f.read()
        soup = Soup(html,features="html.parser")
        soup.head.contents = Soup(head,
                                  features="html.parser")
        soup.div.insert_before(Soup("<h3>Gene associations in tissues.</h3>" + '<h4>Phenotype: ' + phenotype + ' (' + str(row['code']) + ')</h4><h4>Pathway: ' + str(row['pathway']) + "</h2>",features="html.parser"))
        soup.div.insert_after(Soup(adddiv,features="html.parser"))
        soup = str(soup).replace('embedOpt = {"mode": "vega-lite"};',
                                 'embedOpt = {"mode": "vega-lite", "loader": vega.loader({target: \'_blank\'})};')
    with open('gene_content/'+str(row['code'])+'_'+str(row['pathway'])+'.html','w') as fout:
        fout.write(str(soup))
