import altair as alt
import pandas as pd
from sys import argv
import numpy as np
df1 = pd.read_csv(argv[1])
df2 = pd.read_csv(argv[2])


def correctphen(x):
    x = x.replace('.', '')
    x = x.replace('Type-2', 'Type 2')
    x = x.replace('Type 2 diabetes', 'Type 2 Diabetes')
    x = x.replace('EUR', 'European')
    x = x.replace('MIX', 'Mixed ancestry')
    x = x.replace('IVGTT', 'IVGTT, intravenous glucose tolerance test')
    x = x.replace('DI', 'DI, disposition index')
    x = x.replace('AIR', 'AIR, acute insulin response')
    return x


df1.columns = df1.columns.str.replace('target', 'gene')
df2['phenotype'] = df2['phenotype'].apply(correctphen)
df1['magma_log10p'] = df1['association']
df2['phenotype_reference'] = df2['phenotype'].astype(
    str) + ' (' + df2['code'].astype(str) + ') '


def phenlink(x): return "https://www.ncbi.nlm.nih.gov/pubmed/" + \
    str(x) if (len(str(x).strip()) == 8 and x.isdigit()) else "nopmid.html"


df2['phenotype_link'] = df2['PMID or link'].apply(phenlink)


def fancycap(x): return x[0].upper() + x[1:]


df2['phenotype_reference'] = df2['phenotype_reference'].apply(fancycap)

df1.replace([np.inf, -np.inf], np.nan, inplace=True)
df1.fillna(0.0, inplace=True)
df1.columns = df1.columns.str.replace('-', '_')
df1.columns = df1.columns.str.replace('_basal_ganglia', '')
df1.columns = df1.columns.str.replace('c_1', 'C1')


df = pd.merge(df1,
              df2,
              on='code')

data2 = pd.DataFrame([{"ThresholdVal": 4.70813,
                       "Threshold": u"PrediXcan zscore \u2265 4.70813",
                       "Text": "Significance Threshold"}])
data3 = pd.DataFrame(
    [{"ThresholdVal": -4.70813, "Threshold": u"PrediXcan zscore \u2264 -4.70813"}])

data4 = pd.DataFrame(
    [{"ThresholdVal": 5.60206, "Threshold": u"MAGMA -log10(p) \u2265 5.60206"}])


highlight = alt.selection(type='single', empty='none', on='mouseover',
                          fields=['phenotype_reference'])

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

select6 = ['magma_log10p']

selectall = [select6, select1, select2, select3, select4, select5]

titles = ['MAGMA gene-wise association',
          'Nervous system', 'Digestive System',
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
query += ('>=4.70813' + ' or association >=5.60206')
df = df.query(query)
chartarray = []

selectioncat = alt.selection_multi(fields=['category'], empty='all')

colorcat = alt.condition(selectioncat,
                         alt.Color(
                             'category:N',
                             legend=None,
                             scale=alt.Scale(
                                 domain=[
                                     'a: metabolic',
                                     'b: anthropometric',
                                     'c: mental and behavioural',
                                     'd: nervous system',
                                     'e: autoimmune',
                                     'f: genitourinary',
                                     'g: blood',
                                     'h: musculoskeletal',
                                     'i: aging',
                                     'j: other'])),
                         alt.value('lightgray'))

legendcategory = alt.Chart().mark_square().encode(
    y=alt.Y(
        'category:N',
        axis=alt.Axis(
            orient='left',
            title="Click on a category")),
    color=colorcat,
    size=alt.value(100),
    opacity=alt.value(1),
).add_selection(selectioncat)


valuevars = mycolall + ['magma_log10p']
lstdf = list(df.reset_index().columns.values)
remaining = list(set(lstdf) - set(list(valuevars)))

for mycol in selectall:
    count += 1
    title = titles[count - 1]
    df_transformed = df.reset_index().melt(remaining, value_vars=valuevars)
    df_transformed = df_transformed[df_transformed['variable'].isin(mycol)]
    line = alt.Chart().mark_line().encode(
        color=alt.Color('category:N',
                        legend=None,
                        scale=alt.Scale(domain=['a: metabolic', 'b: anthropometric',
                                                'c: mental and behavioural',
                                                'd: nervous system',
                                                'e: autoimmune',
                                                'f: genitorurinary',
                                                'g: blood',
                                                'h: musculoskeletal',
                                                'i: aging',
                                                'j: other'])),
        detail='index',
        x=alt.X('variable:N', title='', axis=alt.Axis(labelAngle=-45)),
        y=alt.Y('value:Q', title='S-PrediXcan z-score',
                scale=alt.Scale(domain=(-maxall, maxall))),
        tooltip=list(['variable', 'value']) + list(df2)
    ).transform_filter(selectioncat)

    line1 = line.encode(
        size=alt.condition(~highlight, alt.value(1.5), alt.value(4)),
        opacity=alt.condition(~highlight, alt.value(0.7), alt.value(1))
    )

    line2 = line.mark_circle().encode(
        opacity=alt.value(0),
    ).add_selection(
        highlight
    )

    annotation = line.mark_text(
        align='center',
        baseline='middle',
        dy=-7,
        color='black',
    ).encode(
        text='code:N',
        href=alt.Href('phenotype_link:N'),
    ).transform_filter(
        ((abs(
            alt.datum.value) >= '4.70813'))).transform_filter(highlight)

    rules1 = alt.Chart(data2).mark_rule(color='black', size=1,
                                        ).encode(
        y='ThresholdVal:Q',
        tooltip=['Threshold'],
    )

    rules2 = alt.Chart(data3).mark_rule(color='black', size=1,
                                        ).encode(
        y='ThresholdVal:Q',
        tooltip=['Threshold']
    )
    rules3 = alt.Chart(data4).mark_rule(color='black', size=1,
                                        ).encode(
        x='ThresholdVal:Q',
        tooltip=['Threshold']
    )

    annotation2 = line.mark_circle(
        opacity=0
    ).encode(
        href=alt.Href('phenotype_link:N'),
    )

    if count > 1:
        chartcompound = alt.layer(line1, line2, annotation,
                                  annotation2, rules1, rules2,
                                  ).properties(width=500,
                                               height=250,
                                               title=title)
    else:
        chartcompound = alt.Chart().mark_bar().encode(
            x=alt.X('value:Q', axis=alt.Axis(title='MAGMA -log10(p)')),
            y=alt.Y('phenotype_reference:N', axis=alt.Axis(title='')),
            color=colorcat,
            href=alt.Href('phenotype_link:N'),
            tooltip=list(['variable', 'value']) + list(df2),
            opacity=alt.condition(~highlight, alt.value(0.7), alt.value(1)),
        ).add_selection(highlight).transform_filter(selectioncat)
        chartcompound = alt.layer(
            chartcompound,
            rules3).properties(
            title=title)

    chartcompound = alt.hconcat(legendcategory, chartcompound,
                                data=df_transformed, center=True)
    chartarray.append(chartcompound)


chartfinal = alt.vconcat(chartarray[1],
                         chartarray[2], chartarray[3], chartarray[4],
                         chartarray[5])


chartfinal = alt.vconcat(chartarray[0], chartfinal, spacing=40)
chartfinal.configure_axis(labelLimit=5000)

if df.isnull().values.all():
    chartfinal = alt.Chart(df).mark_point().encode(
        x=alt.X('phenotype:N', axis=alt.Axis(title='')),
        y=alt.Y('gene:N', axis=alt.Axis(title=''))
    ).properties(
        title="There is no phenotype significant for this gene (yet)."
    )

chartfinal.save(argv[3] + '.html')
