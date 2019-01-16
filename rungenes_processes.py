import subprocess
from bs4 import BeautifulSoup as Soup
import os
import pandas as pd

f_reference = "gwas_reference_toadd"
csvfile = pd.read_csv(f_reference)
codes = csvfile['code']

outdir = 'genes_chromosomes'
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
          '<p>This is a chromosome view to visualize gene-wise associations ' +
          'for a selected phenotype. ' +
          'Gene-wise associations ' +
          'were derived from SNP-phenotype association statistics '
          'obtained from genome-wide ' +
          'association studies ' +
          '(GWAS) using ' +
          '<a href="https://ctg.cncr.nl/software/magma">MAGMA</a>; ' +
          'associations in tissues were computed using ' +
          '<a href="https://github.com/hakyimlab/MetaXcan">S-PrediXcan</a>. '
          'Only genes with p-value &le; 0.005 in MAGMA or S-PrediXcan ' +
          'are shown on this plot. '
          'Gene associations are significant if p-value &le; 0.05/20000. ' +
          'Clicking on a specific gene will lead to its tissue profile. ' +
          'If a chromosome is "empty", it has no gene with '
          'p-value &le; 0.005 in MAGMA or S-PrediXcan, or the GWAS did not ' +
          'include the chromosome (the latter can only happen for X and Y).' +
          'Clicking on MAGMA sig. and S-PrediXcan sig. options will show ' +
          'or hide genes significant in MAGMA and S-PrediXcan. ' +
          '<br><br>The following symbols indicate in which analyses ' +
          'genes were found to be significant:<br>' +
          '&#9679;: significant in MAGMA and S-PrediXcan analyses<br>' +
	      '&#9632;: significant in S-PrediXcan analyses only<br>' +
          '&#9650;: significant in MAGMA only <br>'+
          '&#10010;: not significant <br>' +
          '</p>' +
          '</div>')

for i in codes:
    phenotype = csvfile[csvfile['code']==i]['phenotype'].iloc[0]
    cmd = ['python', 'navigome_vis6_chrom_pathways_filtered.py',
           'genes_chromosomes_data/'+str(i)+'_fusion_targetor',
           phenotype + ' (' + str(i) + ')',
           'genes_chromosomes/'+str(i)+'.geneschromosomes']
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    (output, err) = process.communicate()
    p_status = process.wait()
    head = newheader + '<title>' + "Genes: " + str(i) + '</title>'
    print(str(i))
    with open('genes_chromosomes/'+str(i)+'.geneschromosomes'+'.html','r') as f:
        html = f.read()
        soup = Soup(html,features="html.parser")
        soup.head.contents = Soup(head,
                                  features="html.parser")
        soup.div.insert_after(Soup(adddiv,features="html.parser"))
        soup = str(soup).replace('embedOpt = {"mode": "vega-lite"};',
                                 'embedOpt = {"mode": "vega-lite", "loader": vega.loader({target: \'_blank\'})};')
    with open('genes_chromosomes/'+str(i)+'.geneschromosomes'+'.html','w') as fout:
        fout.write(str(soup))
