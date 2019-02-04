import subprocess
from bs4 import BeautifulSoup as Soup
import os
from sys import argv

workdir = str(argv[1])

# dataframe describing studies
f_reference = workdir + '/input/' + "gwas_reference"

# corresponding correlations
f_correlations = workdir + '/input/' + "correlation_matrix"

# output base name for 2D maps
out_maps = ""

# create output directory if does not exist
outdir = workdir + '/output/' + 'choosemap'
if not os.path.exists(outdir):
    os.makedirs(outdir)

# generate output maps in 2D space
cmd = [
    'python',
    workdir +
    '/scripts/' +
    'dimred.py',
    f_correlations,
    outdir +
    '/' +
    out_maps]
process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
print("dimensionality reduction...")
for line in process.stdout:
    print(line)
print("done")

# outputs of dimred.py (2D coordinates)
output_umap = ["umap_5", "umap_10", "umap_20",
               "umap_30", "umap_40", "umap_50"]
output_tsne = ["tsne_5", "tsne_10", "tsne_20",
               "tsne_30", "tsne_40", "tsne_50"]
output_gtm = ["gtm_0.0001", "gtm_0.001", "gtm_0.01",
              "gtm_0.1", "gtm_1", "gtm_10"]

outall = output_umap + output_tsne + output_gtm

# paste reference file and coordinates together
for i in outall:
    ref = open(f_reference, "r")
    with open(outdir + '/' + i, 'r') as f:
        with open(outdir + '/' + i + '_map', 'w') as fout:
            for line in f:
                fout.write(ref.readline().strip() + "," + line.strip() + "\n")
    ref.close()
    os.rename(outdir + '/' + i + '_map', outdir + '/' + i)

# generate altair visualization for UMAP
for i in output_umap:
    cmd = [
        'python',
        workdir +
        '/scripts/' +
        'navigome_vis3_map.py',
        outdir +
        '/' +
        i,
        'UMAP',
        outdir +
        '/' +
        i]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    print('UMAP...')
    for line in process.stdout:
        print(line)
    print('done')
for i in output_umap:
    cmd = [
        'python',
        workdir +
        '/scripts/' +
        'navigome_vis3_map_mobile.py',
        outdir +
        '/' +
        i,
        'UMAP',
        outdir +
        '/' +
        i +
        "_mobi"]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    print('UMAP...')
    for line in process.stdout:
        print(line)
    print('done')

# generate altair visualization for GTM
for i in output_gtm:
    cmd = [
        'python',
        workdir +
        '/scripts/' +
        'navigome_vis3_map.py',
        outdir +
        '/' +
        i,
        'GTM',
        outdir +
        '/' +
        i]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    print('GTM...')
    for line in process.stdout:
        print(line)
    print('done')
for i in output_gtm:
    cmd = [
        'python',
        workdir +
        '/scripts/' +
        'navigome_vis3_map_mobile.py',
        outdir +
        '/' +
        i,
        'GTM',
        outdir +
        '/' +
        i +
        "_mobi"]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    print('GTM...')
    for line in process.stdout:
        print(line)
    print('done')


# generate altair visualization for t-SNE
for i in output_tsne:
    cmd = [
        'python',
        workdir +
        '/scripts/' +
        'navigome_vis3_map.py',
        outdir +
        '/' +
        i,
        't-SNE',
        outdir +
        '/' +
        i]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    print('t-SNE...')
    for line in process.stdout:
        print(line)
    print('done')
for i in output_tsne:
    cmd = [
        'python',
        workdir +
        '/scripts/' +
        'navigome_vis3_map_mobile.py',
        outdir +
        '/' +
        i,
        't-SNE',
        outdir +
        '/' +
        i +
        "_mobi"]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    print('t-SNE...')
    for line in process.stdout:
        print(line)
    print('done')

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
            '<title>PhenViz: GWAS-based phenotype vizualisation</title>'

mobilehandle1 = (
    '<script>' +
    '$(document).ready(function() {' +
    'window.mobilecheck = function() {' +
    'var check = false;' +
    '(function(a){if(/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce|xda|xiino/i.test(a)||/1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(a.substr(0,4))) check = true;})(navigator.userAgent||navigator.vendor||window.opera);' +
    'return check;' +
    '};' +
    'if( window.mobilecheck() == true ) {' +
    'window.location.replace("https://phenviz.navigome.com/choosemap/')

mobilehandle2 = ('");' +
                 'return false;' +
                 '}' +
                 'else {' +
                 '}' +
                 '});' +
                 '</script>')

navbar1 = ('<nav class="navbar navbar-default align-middle" role="navigation" style="color:grey;font-family: \'Open Sans\', sans-serif;font-size: 18px;font-weight:300">' +
           '<ul class="nav nav-tabs bg-dark">' +
           '<li role="presentation" ><a href="https://phenviz.navigome.com/"><img src="https://phenviz.navigome.com/static/images/gnomic3.png" height="30"></a></li>' +
           '<li role="presentation" ><a  style="line-height: 30px;" href="https://phenviz.navigome.com/">Home</a></li>' +
           '<li role="presentation" class="active" ><a style="line-height: 30px;" href="https://phenviz.navigome.com/map">Phenotype map</a></li>' +
           '<li role="presentation"><a style="line-height: 30px;" href="https://phenviz.navigome.com/genes">Gene profiling</a></li>' +
           '<li role="presentation"><a style="line-height: 30px;" href="https://phenviz.navigome.com/menu">Phenotype browser</a></li>' +
           # '<li role="presentation"><a style="line-height: 30px;" href="https://phenviz.navigome.com/downloads">Downloads</a></li>' +
           '</ul>' +
           '</nav>')
navbar2 = (
    '<nav class="navbar navbar-default" role="navigation" style="color:grey">' +
    '<ul class="nav nav-tabs bg-dark">' +
    '<li role="presentation" class="dropdown">' +
    '<a class="dropdown-toggle" data-toggle="dropdown" href="#" aria-haspopup="true" aria-expanded="true">' +
    't-SNE<span class="caret"></span>' +
    '</a>' +
    '<ul class="dropdown-menu">' +
    '<li role="presentation"><a href="https://phenviz.navigome.com/choosemap/tsne_5.html">t-SNE perplexity = 5</a></li>' +
    '<li role="presentation"><a href="https://phenviz.navigome.com/choosemap/tsne_10.html">t-SNE perplexity = 10</a></li>' +
    '<li role="presentation"><a href="https://phenviz.navigome.com/choosemap/tsne_20.html">t-SNE perplexity = 20</a></li>' +
    '<li role="presentation"><a href="https://phenviz.navigome.com/choosemap/tsne_30.html">t-SNE perplexity = 30</a></li>' +
    '<li role="presentation"><a href="https://phenviz.navigome.com/choosemap/tsne_40.html">t-SNE perplexity = 40</a></li>' +
    '<li role="presentation"><a href="https://phenviz.navigome.com/choosemap/tsne_50.html">t-SNE perplexity = 50</a></li>' +
    '</ul>' +
    '</li>' +
    '<li role="presentation" class="dropdown">' +
    '<a class="dropdown-toggle" data-toggle="dropdown" href="#" aria-haspopup="true" aria-expanded="true">' +
    'GTM<span class="caret"></span>' +
    '</a>' +
    '<ul class="dropdown-menu">' +
    '<li role="presentation"><a href="https://phenviz.navigome.com/choosemap/gtm_0.0001.html">GTM regularization = 0.0001</a></li>' +
    '<li role="presentation"><a href="https://phenviz.navigome.com/choosemap/gtm_0.001.html">GTM regularization = 0.001</a></li>' +
    '<li role="presentation"><a href="https://phenviz.navigome.com/choosemap/gtm_0.01.html">GTM regularization = 0.01</a></li>' +
    '<li role="presentation"><a href="https://phenviz.navigome.com/choosemap/gtm_0.1.html">GTM regularization = 0.1</a></li>' +
    '<li role="presentation"><a href="https://phenviz.navigome.com/choosemap/gtm_1.html">GTM regularization = 1</a></li>' +
    '<li role="presentation"><a href="https://phenviz.navigome.com/choosemap/gtm_10.html">GTM regularization = 10</a></li>' +
    '</ul>' +
    '</li>' +
    '<li role="presentation" class="dropdown">' +
    '<a class="dropdown-toggle" data-toggle="dropdown" href="#" aria-haspopup="true" aria-expanded="true">' +
    'UMAP<span class="caret"></span>' +
    '</a>' +
    '<ul class="dropdown-menu">' +
    '<li role="presentation"><a href="https://phenviz.navigome.com/choosemap/umap_5.html">UMAP n_neighbors = 5</a></li>' +
    '<li role="presentation"><a href="https://phenviz.navigome.com/choosemap/umap_10.html">UMAP n_neighbors = 10</a></li>' +
    '<li role="presentation"><a href="https://phenviz.navigome.com/choosemap/umap_20.html">UMAP n_neighbors = 20</a></li>' +
    '<li role="presentation"><a href="https://phenviz.navigome.com/choosemap/umap_30.html">UMAP n_neighbors = 30</a></li>' +
    '<li role="presentation"><a href="https://phenviz.navigome.com/choosemap/umap_40.html">UMAP n_neighbors = 40</a></li>' +
    '<li role="presentation"><a href="https://phenviz.navigome.com/choosemap/umap_50.html">UMAP n_neighbors = 50</a></li>' +
    '</ul>' +
    '</li>' +
    '</ul>' +
    '</nav>')
navbar = navbar1 + navbar2

adddiv = (
    '<div class="col-lg-12 col-md-12 content-item content-item-1">' +
    '<h2 class="main-title">Some info...</h2>' +
    '<p>We use this type of map to cluster phenotypes by genetic relatedness. ' +
    'Each point is a genome-wide association study (GWAS) ' +
    'for a specific phenotype, with a radius proportional to ' +
    'the GWAS sample size. ' +
    'The map is based on genetic correlations ' +
    '(computed using <a href="https://github.com/bulik/ldsc">' +
    'LD Score regression</a>). ' +
    'The genetic correlation matrix was mapped into a 2D space ' +
    'using different algorithms: UMAP, GTM, and t-SNE, ' +
    'using the python packages umap-learn 0.3.7, ugtm 2.0.0, ' +
    'and scikit-learn 0.20.0 with the following hyperparameters: ' +
    '{n_neibhbors = 30, min_dist = 0.1} for UMAP, ' +
    '{perplexity = 30, early exaggeration = 12, learning rate = 200} ' +
    'for t-SNE, ' +
    '{map resolution = 12*12, radial basis function grid size = 3*3, ' +
    'regularization = 0.1, rbf width factor = 0.3} for GTM. ' +
    'Maps with different hyperparameter settings can be ' +
    'selected in the navigation bar. ' +
    'The interactive visualization was generated using the python ' +
    'package altair, which is built on top of ' +
    'the Vega-Lite visualization grammar. ' +
    'Tablets and smartphones will not provide a full user experience (' +
    'no click or interval selection available).' +
    '</p>' +
    '</div>')

# replace header and insert nav bars
# the mobile handler will redict to the mobile page if appropriate
for i in outall:
    with open(outdir + '/' + i + '.html', 'r') as f:
        html = f.read()
        soup = Soup(html, features="html.parser")
        soup.head.contents = Soup(newheader + mobilehandle1 +
                                  i + '_mobi.html' + mobilehandle2,
                                  features="html.parser")
        soup.body.insert_before(Soup(navbar, features="html.parser"))
        soup.div.insert_after(Soup(adddiv, features="html.parser"))
        soup = str(soup).replace(
            'embedOpt = {"mode": "vega-lite"};',
            'embedOpt = {"mode": "vega-lite", "loader": vega.loader({target: \'_blank\'})};')
    with open(outdir + '/' + i + '.html', 'w') as fout:
        fout.write(str(soup))
    # os.remove(outdir+'/'+i)

for i in outall:
    with open(outdir + '/' + i + '_mobi.html', 'r') as f:
        html = f.read()
        soup = Soup(html, features="html.parser")
        soup.head.contents = Soup(newheader, features="html.parser")
        soup.body.insert_before(Soup(navbar, features="html.parser"))
        soup.div.insert_after(Soup(adddiv, features="html.parser"))
        soup = str(soup).replace(
            'embedOpt = {"mode": "vega-lite"};',
            'embedOpt = {"mode": "vega-lite", "loader": vega.loader({target: \'_blank\'})};')
    with open(outdir + '/' + i + '_mobi.html', 'w') as fout:
        fout.write(str(soup))
