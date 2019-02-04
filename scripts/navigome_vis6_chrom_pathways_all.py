import altair as alt
import pandas as pd
from sys import argv
import numpy as np

df = pd.read_csv(argv[1])
df.replace([np.inf, -np.inf], np.nan, inplace=True)
df.fillna(0.0, inplace=True)

def sigfunc(x): return True if x >= 5.60206 else (False)

sequence = [str(x) for x in range(1, 23)]
sequence.append('X')
sequence.append('Y')


def label_filterchr(row):
    if(row in sequence):
        return True
    else:
        return False


df['MAGMA association'] = df['association']
df['magma_sig'] = df['association'].apply(sigfunc)
df['CHR'] = df['chromosome'].apply(
    lambda x: 23 if x == 'X' else (
        24 if x == 'Y' else int(x)))
df.columns = df.columns.str.replace('-', '_')
df.columns = df.columns.str.replace('target', 'gene')
df.columns = df.columns.str.replace('_basal_ganglia', '')
df.columns = df.columns.str.replace('c_1', 'C1')
df['urlgene'] = "https://phenviz.navigome.com/gene_phenotypes/" + \
    df['ENSEMBL'].astype(str) + '.html'

selectionsig = alt.selection_multi(fields=['predixcan_sig'], empty='all')
selectionsig2 = alt.selection_multi(fields=['magma_sig'], empty='all')

colorsig = alt.condition(selectionsig,
                         alt.value('black'),
                         alt.value('lightgray'))
colorsig2 = alt.condition(selectionsig2,
                          alt.value('black'),
                          alt.value('lightgray'))

adipose = ['Adipose_Subcutaneous',
           'Adipose_Visceral_Omentum',
           'Breast_Mammary_Tissue']

muscular = ['Muscle_Skeletal']

skin = ['Skin_Not_Sun_Exposed_Suprapubic',
        'Skin_Sun_Exposed_Lower_leg']

cell_lines = ['Cells_Transformed_fibroblasts',
              'Cells_EBV_transformed_lymphocytes']

circulatory = ['DGN_Whole_Blood',
               'Whole_Blood',
               'Artery_Aorta',
               'Artery_Coronary',
               'Artery_Tibial',
               'Heart_Atrial_Appendage',
               'Heart_Left_Ventricle',
               'Spleen']

nervous = ['Brain_Amygdala',
           'Brain_Anterior_cingulate_cortex_BA24',
           'Brain_Caudate',
           'Brain_Nucleus_accumbens',
           'Brain_Putamen',
           'Brain_Cerebellar_Hemisphere',
           'Brain_Cerebellum',
           'Brain_Cortex',
           'Brain_Frontal_Cortex_BA9',
           'Brain_Hippocampus',
           'Brain_Hypothalamus',
           'Brain_Spinal_cord_cervical_C1',
           'Brain_Substantia_nigra',
           'Nerve_Tibial']

digestive = [
    'Colon_Sigmoid',
    'Colon_Transverse',
    'Esophagus_Gastroesophageal_Junction',
    'Esophagus_Mucosa',
    'Esophagus_Muscularis',
    'Liver',
    'Minor_Salivary_Gland',
    'Small_Intestine_Terminal_Ileum',
    'Stomach'
]

endocrine = [
    'Adrenal_Gland',
    'Brain_Hypothalamus',
    'Pituitary',
    'Pancreas',
    'Thyroid',
    'Ovary',
    'Testis',
]

genitourinary = [
    'Prostate',
    'Testis',
    'Ovary',
    'Uterus',
    'Vagina'
]

lung = ['Lung']

mycolall = ['Adipose_Subcutaneous',
            'Adipose_Visceral_Omentum',
            'Breast_Mammary_Tissue',
            'Muscle_Skeletal',
            'DGN_Whole_Blood',
            'Whole_Blood',
            'Artery_Aorta',
            'Artery_Coronary',
            'Artery_Tibial',
            'Heart_Atrial_Appendage',
            'Heart_Left_Ventricle',
            'Spleen',
            'Brain_Amygdala',
            'Brain_Anterior_cingulate_cortex_BA24',
            'Brain_Caudate',
            'Brain_Nucleus_accumbens',
            'Brain_Putamen',
            'Brain_Cerebellar_Hemisphere',
            'Brain_Cerebellum',
            'Brain_Cortex',
            'Brain_Frontal_Cortex_BA9',
            'Brain_Hippocampus',
            'Brain_Hypothalamus',
            'Brain_Spinal_cord_cervical_C1',
            'Brain_Substantia_nigra',
            'Nerve_Tibial',
            'Cells_Transformed_fibroblasts',
            'Cells_EBV_transformed_lymphocytes',
            'Colon_Sigmoid',
            'Colon_Transverse',
            'Esophagus_Gastroesophageal_Junction',
            'Esophagus_Mucosa',
            'Esophagus_Muscularis',
            'Liver',
            'Minor_Salivary_Gland',
            'Small_Intestine_Terminal_Ileum',
            'Stomach',
            'Adrenal_Gland',
            'Pituitary',
            'Pancreas',
            'Thyroid',
            'Lung',
            'Ovary',
            'Prostate',
            'Testis',
            'Uterus',
            'Vagina',
            'Skin_Not_Sun_Exposed_Suprapubic',
            'Skin_Sun_Exposed_Lower_leg']

sigArray = ['1: gene and tissue analyses',
            '2: tissue analyses only',
            '3: gene analysis only',
            '4: not significant']

if not df['association'].isnull().values.all():
    maxpred = df['association'].values.max()
else:
    maxpred = 5

# S-PrediXcan cut-off
def label_filter(row):
    result = False
    for i in mycolall:
        if abs(row[i]) >= 4.70813:
            result = True
    return result


def label_filter_category(row):
    result = False
    for i in mycolall:
        if abs(row[i]) >= 4.70813:
            result = True
    return result


df['predixcan_sig'] = df.apply(lambda row: label_filter(row), axis=1)


def label_sig(row):
    if row['predixcan_sig'] and row['magma_sig']:
        return sigArray[0]
    elif row['predixcan_sig']:
        return sigArray[1]
    elif row['magma_sig']:
        return sigArray[2]
    else:
        return sigArray[3]


sigArray2 = ['significant', 'not significant']


def label_sig2(row):
    if row['predixcan_sig'] or row['magma_sig']:
        return sigArray2[0]
    else:
        return sigArray2[1]


df['significant'] = df.apply(lambda row: label_sig2(row), axis=1)

df['significant in tissue'] = df.apply(lambda row: label_sig(row), axis=1)

selection = alt.selection_multi(fields=['chromosome'], empty='all')
color = alt.condition(selection,
                      alt.Color('chromosome:N', legend=None),
                      alt.value('lightgray'))


legendsig = alt.Chart().mark_square().encode(
    y=alt.Y(
        'predixcan_sig:N',
        axis=alt.Axis(
            orient='left',
            title="S-PrediXcan sig.")),
    size=alt.value(100),
    color=colorsig).add_selection(selectionsig)

legendsig2 = alt.Chart().mark_square().encode(
    y=alt.Y('magma_sig:N', axis=alt.Axis(orient='left', title="MAGMA sig.")),
    size=alt.value(100),
    color=colorsig2
).add_selection(
    selectionsig2
)

legendfilter = alt.vconcat(legendsig, legendsig2)

chart = alt.Chart().mark_point(
    opacity=0.8,
    stroke='black',
    strokeWidth=0.5,
    size=3,
    filled=True
).encode(
    shape=alt.Shape(
        'significant in tissue:N',
        legend=None,
        scale=alt.Scale(
            domain=sigArray)),
    x=alt.X('median:Q', title="Gene location (base pairs)"),
    size=alt.Size(
        'significant:N',
        scale=alt.Scale(
            domain=sigArray2,
            range=[
                100,
                40]),
        legend=None),
    color=alt.Color('association:Q',
                    scale=alt.Scale(scheme='viridis', domain=[0, maxpred]),
                    legend=alt.Legend(title='MAGMA -log10(p)',
                                      orient='right')
                    ),
    tooltip=['ENSEMBL', 'name', 'size', 'MAGMA association'],
    href=alt.Href('urlgene')
).properties(
    width=650,
    height=20
).transform_filter(selection).transform_filter(
    selectionsig
).transform_filter(
    selectionsig2
)


therule = alt.Chart().mark_rule(strokeWidth=15, opacity=0.4).encode(
    x=alt.X("begin:Q"),
    x2=alt.X2("end:Q"),
    tooltip=['ENSEMBL', 'name', 'size', 'MAGMA association'],
    color=alt.Color('association'),
    href=alt.Href('urlgene')
).transform_filter(selection)

legend = alt.Chart().mark_rect().encode(
    x=alt.X('chromosome:N',
            axis=alt.Axis(title="Choose a chromosome " +
                          "(click one of the coloured squares), " +
                          "then zoom in using trackpad or mouse wheel",
                          orient='top'), scale=alt.Scale(domain=sequence)),
    color=color
).properties(width=650).add_selection(
    selection
)

annotation = alt.Chart().mark_text(
    align='center',
    baseline='middle',
    fontSize=7,
    color='black',
    dy=-6
).encode(
    x=alt.X('median:Q', title="Gene location (base pairs)"),
    text='name',
    href=alt.Href('urlgene')
).transform_filter(selection).transform_filter(
    ((alt.datum.significant == 'significant'))
).transform_filter(
    selectionsig
).transform_filter(
    selectionsig2
)

chartfinal = chart + therule + annotation

infine = chartfinal.facet(row='CHR').interactive()
infine.spacing = -32
infine = infine.transform_filter(
    selection
)

infine2 = alt.vconcat(legend, infine)

infine2 = alt.hconcat(legendfilter, infine2, data=df).properties(
    title='Gene associations - ' + str(argv[2])
).configure_title(
    offset=30
)


infine2.save(argv[3] + '.html')
