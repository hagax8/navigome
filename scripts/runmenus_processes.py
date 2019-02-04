import subprocess
from bs4 import BeautifulSoup as Soup
import os
from sys import argv

workdir = str(argv[1])

# dataframe describing studies
f_reference = workdir + '/input/' + "gwas_reference"

# create output directory if does not exist
outdir = workdir + '/output/' + 'templates'
if not os.path.exists(outdir):
    os.makedirs(outdir)

# generate menus
out_maps = outdir + "/menu_phen"
cmd = [
    'python',
    workdir +
    '/scripts/' +
    'navigome_vis1_menu_phen.py',
    f_reference,
    out_maps]
process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
for line in process.stdout:
    print(line)
out_maps = outdir + "/menu_cat"
cmd = [
    'python',
    workdir +
    '/scripts/' +
    'navigome_vis1_menu_cat.py',
    f_reference,
    out_maps]
process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
for line in process.stdout:
    print(line)
out_maps = outdir + "/menu_pmid"
cmd = [
    'python',
    workdir +
    '/scripts/' +
    'navigome_vis1_menu_pmid.py',
    f_reference,
    out_maps]
process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
for line in process.stdout:
    print(line)

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
            '.vega-bind-name{' \
            'display: none' \
            '}' \
    'select{' \
    'font-family: Roboto;' \
    'font-size: 16px;' \
    'width: 350px;' \
            'margin-left: 5px;' \
    'height: 30px;' \
    'background-color: #98AFC7;' \
    'text-align-last: center;' \
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
            '<title>PhenViz: GWAS-based phenotype vizualisation</title>'
navbar1 = ('<nav class="navbar navbar-default align-middle" role="navigation" style="color:grey;font-family: \'Open Sans\', sans-serif;font-size: 18px;font-weight:300">' +
           '<ul class="nav nav-tabs bg-dark">' +
           '<li role="presentation" ><a href="https://phenviz.navigome.com/"><img src="https://phenviz.navigome.com/static/images/gnomic3.png" height="30"></a></li>' +
           '<li role="presentation" ><a  style="line-height: 30px;" href="https://phenviz.navigome.com/">Home</a></li>' +
           '<li role="presentation" ><a style="line-height: 30px;" href="https://phenviz.navigome.com/map">Phenotype map</a></li>' +
           '<li role="presentation"><a style="line-height: 30px;" href="https://phenviz.navigome.com/genes">Gene profiling</a></li>' +
           '<li role="presentation" class="active"><a style="line-height: 30px;" href="https://phenviz.navigome.com/menu">Phenotype browser</a></li>' +
           #          '<li role="presentation"><a style="line-height: 30px;" href="https://phenviz.navigome.com/downloads">Downloads</a></li>' +
           '</ul>' +
           '</nav>')
navbar2_phen = (
    '<nav class="navbar navbar-default" role="navigation" style="color:grey">' +
    '<ul class="nav nav-tabs bg-dark">' +
    '<li role="presentation" class="active"><a style="line-height: 30px;" href="https://phenviz.navigome.com/menu_phen">By phenotype</a></li>' +
    '<li role="presentation"><a style="line-height: 30px;" href="https://phenviz.navigome.com/menu_cat">By category</a></li>' +
    '<li role="presentation"><a style="line-height: 30px;" href="https://phenviz.navigome.com/menu_pmid">By PMID</a></li>' +
    '</ul>' +
    '</nav>')
navbar2_pmid = (
    '<nav class="navbar navbar-default" role="navigation" style="color:grey">' +
    '<ul class="nav nav-tabs bg-dark">' +
    '<li role="presentation"><a style="line-height: 30px;" href="https://phenviz.navigome.com/menu_phen">By phenotype</a></li>' +
    '<li role="presentation"><a style="line-height: 30px;" href="https://phenviz.navigome.com/menu_cat">By category</a></li>' +
    '<li role="presentation" class="active"><a style="line-height: 30px;" href="https://phenviz.navigome.com/menu_pmid">By PMID</a></li>' +
    '</ul>' +
    '</nav>')
navbar2_cat = (
    '<nav class="navbar navbar-default" role="navigation" style="color:grey">' +
    '<ul class="nav nav-tabs bg-dark">' +
    '<li role="presentation"><a style="line-height: 30px;" href="https://phenviz.navigome.com/menu_phen">By phenotype</a></li>' +
    '<li role="presentation" class="active"><a style="line-height: 30px;" href="https://phenviz.navigome.com/menu_cat">By category</a></li>' +
    '<li role="presentation"><a style="line-height: 30px;" href="https://phenviz.navigome.com/menu_pmid">By PMID</a></li>' +
    '</ul>' +
    '</nav>')
adddiv = (
    '<div class="col-lg-12 col-md-12 content-item content-item-1">' +
    '<p>' +
    '&#9632; = GWAS pathway analysis (MAGMA), <br>' +
    '&#9679; = genetic correlations (LD Score), <br>' +
    '&#10010; = position on t-SNE phenotype map, <br>' +
    '&#9650; = gene associations (MAGMA, S-PrediXcan): chromosome view, <br>' +
    '&#9660; = gene associations: parallel coordinates.' +
    '</p>' +
    '</div>')

for i in [outdir + '/menu_phen', outdir + '/menu_cat', outdir + '/menu_pmid']:
    with open(i + '.html', 'r') as f:
        html = f.read()
        soup = Soup(html, features="html.parser")
        if i == outdir + '/menu_phen':
            navbar = navbar1 + navbar2_phen
        elif i == outdir + '/menu_cat':
            navbar = navbar1 + navbar2_cat
        elif i == outdir + '/menu_pmid':
            navbar = navbar1 + navbar2_pmid
        navbar = navbar + adddiv
        soup.head.contents = Soup(newheader, features="html.parser")
        soup.body.insert_before(Soup(navbar, features="html.parser"))
        soup = str(soup).replace(
            'embedOpt = {"mode": "vega-lite"};',
            'embedOpt = {"mode": "vega-lite", "loader": vega.loader({target: \'_blank\'})};')
    with open(i + '.html', 'w') as fout:
        fout.write(str(soup))
