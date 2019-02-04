import os
import pandas as pd
from sys import argv


workdir = argv[1]
f_reference = workdir + '/input/' + "gwas_reference_toadd"
directory_files = workdir + '/input/' + "genes_chromosomes_data"
f_refgenelist = workdir + '/input/' + "list_genes.csv"
refgenelist = pd.read_csv(f_refgenelist, keep_default_na=False)
csvfile = pd.read_csv(f_reference, keep_default_na=False)
codes = csvfile['code']
genelist = set([])


def label_filter_any(row):
    result = False
    for i in mycolall:
        if abs(row[i]) >= 4.70813:
            result = True
            break
    if row['association'] >= 5.60206:
        result = True
    return result


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

for i in codes:
    file_data = directory_files + "/" + str(i) + '_fusion_targetor'
    print(i)
    df = pd.read_csv(file_data)
    df.columns = df.columns.str.replace('-', '_')
    df.columns = df.columns.str.replace('target', 'gene')
    df.columns = df.columns.str.replace('_basal_ganglia', '')
    df.columns = df.columns.str.replace('c_1', 'C1')
    df['any_filter'] = df.apply(lambda row: label_filter_any(row), axis=1)
    df = df.loc[df['any_filter']]
    genelist = genelist.union(set(df['ENSEMBL']))

with open(workdir + '/input/' + 'genes_to_update.csv', 'w') as f:
    f.write('ensembl,name\n')
    for i in list(genelist):
        name = refgenelist[refgenelist['ensembl'] == i]['name'].iloc[0]
        print(str(name))
        f.write(i + ',' + str(name) + '\n')
