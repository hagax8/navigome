import subprocess
from bs4 import BeautifulSoup as Soup
import os
import pandas as pd
from sys import argv

workdir = str(argv[1])
f_reference = workdir + '/input/' + 'genes_to_update.csv'
csvfile = pd.read_csv(f_reference, keep_default_na=False)
codes = csvfile['ensembl']
gwas_reference = workdir + '/input/' + "gwas_reference"

# create output directory if does not exist
outdir = workdir + '/output/' + 'gene_phenotypes'
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

adddiv = (
    '<div class="col-lg-12 col-md-12 content-item content-item-1">' +
    '<p>This is a visualization of GWAS-derived gene associations  ' +
    'across Navigome phenotypes. ' +
    'Only phenotypes for which the gene has at least one significant ' +
    'association (p-value &le; 0.05/20000) ' +
    'in <a href="https://ctg.cncr.nl/software/magma">MAGMA</a> <b>and/or</b> ' +
    '<a href="https://github.com/hakyimlab/MetaXcan">S-PrediXcan</a> analyses are shown. ' +
    'The first panel is a visualization of gene-phenotype associations ' +
    'obtained using <a href="https://ctg.cncr.nl/software/magma">MAGMA</a> (-log10(p-value)). ' +
    'Hover over any bar to highlight the phenotype in the other panels. ' +
    'The other panels are parallel coordinates visualizations ' +
    'for tissue-wise associations (z-scores)'
    'computed using ' +
    '<a href="https://github.com/hakyimlab/MetaXcan">S-PrediXcan</a> ' +
    ' and eQTL expression data from GTEx and DGN. ' +
    'Significance thresholds are delineated ' +
    'with black lines. ' +
    'The parallel coordinates show which phenotypes ' +
    'have a significant association ' +
    'and in which tissues, based on gene expression data. ' +
    'Clicking on a specific phenotype will lead to ' +
    'the reference of the GWAS study.' +
    '</p>' +
    '</div>')

for i in codes:
    ensembl = i
    name = csvfile[csvfile['ensembl'] == i]['name'].iloc[0]
    if isinstance(name, str):
        gene = ensembl + ' (' + name + ')'
    else:
        gene = ensembl
    print(gene)
    cmd = [
        'python',
        workdir +
        '/scripts/' +
        'navigome_vis2_profile.py',
        workdir +
        '/input/' +
        'gene_phenotype_links/' +
        str(i),
        gwas_reference,
        workdir +
        '/output/' +
        'gene_phenotypes/' +
        str(i)]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    (output, err) = process.communicate()
    p_status = process.wait()
    head = newheader + '<title>' + \
        "Gene profile: " + str(i) + '</title>'
    with open(workdir + '/output/' + 'gene_phenotypes/' + str(i) + '.html', 'r') as f:
        html = f.read()
        soup = Soup(html, features="html.parser")
        soup.head.contents = Soup(head,
                                  features="html.parser")
        soup.div.insert_before(
            Soup(
                "<h4>Gene profile across phenotypes - " +
                gene +
                "</h2>",
                features="html.parser"))
        soup.div.insert_after(Soup(adddiv, features="html.parser"))
        soup = str(soup).replace(
            'embedOpt = {"mode": "vega-lite"};',
            'embedOpt = {"mode": "vega-lite", "loader": vega.loader({target: \'_blank\'})};')
    with open(workdir + '/output/' + 'gene_phenotypes/' + str(i) + '.html', 'w') as fout:
        fout.write(str(soup))
