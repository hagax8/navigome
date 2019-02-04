import altair as alt
import pandas as pd
from sys import argv
import numpy as np
df = pd.read_csv(argv[1])

df.replace([np.inf, -np.inf], np.nan, inplace=True)
df.fillna(0.0, inplace=True)
df.columns = df.columns.str.replace('-', '_')
df.columns = df.columns.str.replace('_basal_ganglia', '')
df.columns = df.columns.str.replace('c_1', 'C1')
data2 = pd.DataFrame([{"ThresholdVal": 4.70813,
                       "Threshold": u"PrediXcan zscore \u2265 4.70813",
                       "Text": "Significance Threshold"}])
data3 = pd.DataFrame(
    [{"ThresholdVal": -4.70813, "Threshold": u"PrediXcan zscore \u2264 -4.70813"}])
highlight = alt.selection(type='single', on='mouseover',
                          fields=['name'], nearest=True)
df['urlgene'] = "https://phenviz.navigome.com/gene_phenotypes/" + \
    df['ENSEMBL'].astype(str) + '.html'

select4 = [
    'Adipose_Subcutaneous',
    'Adipose_Visceral_Omentum',
    'Breast_Mammary_Tissue',
    'Muscle_Skeletal',
    'Skin_Not_Sun_Exposed_Suprapubic',
    'Skin_Sun_Exposed_Lower_leg',
    'Cells_Transformed_fibroblasts',
    'Cells_EBV_transformed_lymphocytes']
select3 = ['DGN_Whole_Blood', 'Whole_Blood',
           'Artery_Aorta', 'Artery_Coronary', 'Artery_Tibial',
           'Heart_Atrial_Appendage', 'Heart_Left_Ventricle', 'Spleen']
select1 = ['Brain_Amygdala', 'Brain_Anterior_cingulate_cortex_BA24',
           'Brain_Caudate',
           'Brain_Nucleus_accumbens',
           'Brain_Putamen',
           'Brain_Cerebellar_Hemisphere',
           'Brain_Cerebellum', 'Brain_Cortex', 'Brain_Frontal_Cortex_BA9',
           'Brain_Hippocampus', 'Brain_Hypothalamus',
           'Brain_Spinal_cord_cervical_C1',
           'Brain_Substantia_nigra', 'Nerve_Tibial']
select2 = ['Colon_Sigmoid', 'Colon_Transverse',
           'Esophagus_Gastroesophageal_Junction',
           'Esophagus_Mucosa',
           'Esophagus_Muscularis', 'Liver', 'Minor_Salivary_Gland',
           'Small_Intestine_Terminal_Ileum', 'Stomach']
select5 = ['Adrenal_Gland', 'Pituitary', 'Pancreas', 'Thyroid',
           'Lung', 'Ovary', 'Prostate', 'Testis', 'Uterus', 'Vagina']

selectall = [select1, select2, select3, select4, select5]
titles = ['Nervous system', 'Digestive System',
          'Blood, Arteries and Heart',
          'Adipose Tissue, Muscle, Skin and Cells',
          'Endocrine System and Others']
mycolall = [
    'Adipose_Subcutaneous',
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
count = 0

if not df[mycolall].isnull().values.all():
    maxpred = df[mycolall].values.max()
    minpred = df[mycolall].values.min()

else:
    maxpred = 5
    minpred = -5

maxall = max(maxpred, abs(minpred))
query = ('>=4.70813 or ').join(['abs(' + str(x) + ')' for x in mycolall])
query += ('>=4.70813')
df = df.query(query)
chartarray = []
for mycol in selectall:
    count += 1
    title = titles[count - 1]
    df_transformed = df.reset_index().melt(
        ['index', 'name', 'urlgene', 'ENSEMBL', 'association'])
    df_transformed = df_transformed[df_transformed['variable'].isin(mycol)]
    sorterIndex = dict(zip(mycol, range(len(mycol))))
    df_transformed['Rank'] = df_transformed['variable'].map(sorterIndex)
    df_transformed.sort_values(by='Rank', inplace=True)
    df_transformed.columns = df_transformed.columns.str.replace(
        'value', 'predixcan_zscore')
    line = alt.Chart().mark_line().encode(
        detail='index',
        x=alt.X(
            'variable:N',
            title='',
            axis=alt.Axis(
                labelAngle=45)),
        y=alt.Y(
            'predixcan_zscore:Q',
            title='S-PrediXcan z-score',
            scale=alt.Scale(
                domain=(
                    -maxall,
                    maxall))),
        tooltip=[
            'name',
            'ENSEMBL',
            'association',
            'predixcan_zscore'],
        color=alt.condition(
            ~highlight,
            alt.value('grey'),
            alt.value('black')))

    line1 = line.encode(
        size=alt.condition(~highlight, alt.value(0.5), alt.value(4))
    )

    line2 = line.mark_circle().encode(
        opacity=alt.value(0),
        tooltip=['name', 'ENSEMBL', 'association', 'predixcan_zscore'],
    ).add_selection(
        highlight
    )

    annotation = line.mark_text(
        align='center',
        baseline='middle',
        dy=-7,
        color='black',
        tooltip=['name', 'ENSEMBL', 'association', 'predixcan_zscore'],
    ).encode(
        text='name',
        href=alt.Href('urlgene:N'),
    ).transform_filter(
        ((abs(alt.datum.predixcan_zscore) >= '4.70813'))
    ).transform_filter(
        highlight
    )

    rules1 = alt.Chart(data2).mark_rule(color='red', size=2,
                                        ).encode(
        y='ThresholdVal:Q',
        tooltip=['Threshold'],
    )

    rules2 = alt.Chart(data3).mark_rule(color='red', size=2,
                                        ).encode(
        y='ThresholdVal:Q',
        tooltip=['Threshold']
    )
    chartcompound = alt.layer(
        line1,
        line2,
        annotation,
        rules1,
        rules2,
        data=df_transformed).properties(
        width=500,
        height=250,
        title=title)
    chartarray.append(chartcompound)

charta = alt.hconcat(chartarray[0], chartarray[1])
chartb = alt.hconcat(chartarray[2], chartarray[3])
chartfinal = alt.vconcat(charta, chartb, chartarray[4])

chartfinal.configure_axis(labelLimit=1000)

if df.isnull().values.all():
    chartfinal = alt.Chart(df).mark_point().encode(
        x=alt.X('phenotype:N', axis=alt.Axis(title='')),
        y=alt.Y('name:N', axis=alt.Axis(title=''))
    ).properties(
        title="There is no gene significant tissue-wise for this phenotype (yet)."
    )


chartfinal.save(argv[2] + '.html')
