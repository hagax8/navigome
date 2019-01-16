import subprocess
from bs4 import BeautifulSoup as Soup
import os
import pandas as pd
from navigome_independent_tests import bonferroni_cutoff

f_reference = "gwas_reference_toadd"
cutoff = bonferroni_cutoff('mat_correls_filt2_noANKY')
csvfile = pd.read_csv(f_reference)
codes = csvfile['code']

outdir = 'phenotype_map'
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

navbar1 = ('<nav class="navbar navbar-default align-middle" role="navigation" style="color:grey;font-family: \'Open Sans\', sans-serif;font-size: 18px;font-weight:300">' +
          '<ul class="nav nav-tabs bg-dark">' +
          '<li role="presentation" ><a href="https://phenviz.navigome.com/"><img src="https://phenviz.navigome.com/static/images/gnomic3.png" height="30"></a></li>' +
          '<li role="presentation" ><a  style="line-height: 30px;" href="https://phenviz.navigome.com/">Home</a></li>' +
          '<li role="presentation" class="active" ><a style="line-height: 30px;" href="https://phenviz.navigome.com/map">Phenotype map</a></li>' +
          '<li role="presentation"><a style="line-height: 30px;" href="https://phenviz.navigome.com/genes">Gene profiling</a></li>' +
          '<li role="presentation"><a style="line-height: 30px;" href="https://phenviz.navigome.com/menu">Phenotype browser</a></li>' +
          #'<li role="presentation"><a style="line-height: 30px;" href="https://phenviz.navigome.com/downloads">Downloads</a></li>' +
          '</ul>' +
          '</nav>')
navbar = navbar1

adddiv = ('<div class="col-lg-12 col-md-12 content-item content-item-1">' +
          '<p>We use this type of map to cluster phenotypes by genetic relatedness. ' +
          'Each point is a genome-wide association study (GWAS) ' +
          'for a specific phenotype, with a radius proportional to ' +
          'the absolute correlation with the phenotype of interest. ' +
          'The map is based on genetic correlations ' +
          '(computed using <a href="https://github.com/bulik/ldsc">' +
          'LD Score regression</a>). ' +
          'The genetic correlation matrix was mapped into a 2D space ' +
          'using t-SNE (scikit-learn 0.20.0 implementation) ' +
          'with the following hyperparameters: ' +
          '{perplexity = 30, early exaggeration = 12, learning rate = 200}. ' +
          'You may filter phenotypes ' +
          'by selecting different options (significance of correlation, '+
          'direction, category). ' +
          'The number of independent traits was estimated by ' +
          'computing the number of principal components accounting for 99.5% ' +
          'of variance explained in the trait/trait genetic correlation matrix, ' +
          'and used to estimate the Bonferroni significance threshold.' +
          '</p>' +
          '</div>')

for i in codes:
    # merge reference data and correlations
    cmd = ['python', 'navigome_vis5_map+corr.py',
           'correlation_data/'+str(i)+'.correlations', 'tsne_30', " %.2e" % (cutoff),
           str(i),
           'phenotype_map/'+str(i)+'.phenotypemap']
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    (output, err) = process.communicate()
    p_status = process.wait()
    print(str(i))

    with open('phenotype_map/'+str(i)+'.phenotypemap'+'.html','r') as f:
        head = newheader + '<title>' + "Map: " + str(i) + '</title>'
        html = f.read()
        soup = Soup(html,features="html.parser")
        soup.head.contents = Soup(head,
                                  features="html.parser")
        #soup.body.insert_before(Soup(navbar,features="html.parser"))
        soup.div.insert_after(Soup(adddiv,features="html.parser"))
        soup = str(soup).replace('embedOpt = {"mode": "vega-lite"};',
                                 'embedOpt = {"mode": "vega-lite", "loader": vega.loader({target: \'_blank\'})};')
    with open('phenotype_map/'+str(i)+'.phenotypemap'+'.html','w') as fout:
        fout.write(str(soup))
