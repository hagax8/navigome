import altair as alt
import pandas as pd
import numpy as np
from sys import argv
import os

f_reference = argv[4]
csvfile = pd.read_csv(f_reference, keep_default_na=False)

correlations = pd.read_csv(argv[1], keep_default_na=False)
phencode = argv[2]
bonferroni_cutoff = argv[3]


df = correlations.join(csvfile.set_index('code'), on='code')


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


df['phenotype'] = df['phenotype'].apply(correctphen)
df['phenotype_reference'] = df['phenotype'].astype(
    str) + ' (' + df['code'].astype(str) + ') '


def phenlink(x): return "https://www.ncbi.nlm.nih.gov/pubmed/" + \
    str(x) if (len(str(x).strip()) == 8 and x.isdigit()) else "nopmid.html"


df['phenotype_link'] = df['PMID or link'].apply(phenlink)


def fancycap(x): return x[0].upper() + x[1:]


df['phenotype_reference'] = df['phenotype_reference'].apply(fancycap)
df['logp'] = df['pvalue'].apply(lambda x: np.log10(x))
phenref = df.loc[df['code'] == phencode].iloc[0]['phenotype_reference']


def label_sig(row, limit):
    if row['pvalue'] <= limit:
        result = True
    else:
        result = False
    return result


def label_neg(row):
    if row['genetic_correlation'] < 0:
        return 'negative'
    else:
        return 'positive'


df['cutoff1'] = df.apply(lambda row: label_sig(row, 0.05), axis=1)
df['cutoff2'] = df.apply(lambda row: label_sig(row, 0.005), axis=1)
df['cutoff3'] = df.apply(
    lambda row: label_sig(
        row,
        float(bonferroni_cutoff)),
    axis=1)
df['direction'] = df.apply(lambda row: label_neg(row), axis=1)

data2 = pd.DataFrame([{"ThresholdValue": 0.0, "Threshold": "hazardous"}])
selection = alt.selection_multi(fields=['category'], empty='all')
selectionsig = alt.selection_multi(fields=['cutoff1'], empty='all')
selectionsig2 = alt.selection_multi(fields=['cutoff2'], empty='all')
selectionsig3 = alt.selection_multi(fields=['cutoff3'], empty='all')
selectionneg = alt.selection_multi(fields=['direction'], empty='all')

slider = alt.binding_checkbox()

color = alt.condition(selection,
                      alt.Color('category:N', legend=None),
                      alt.value('lightgray'))
colorsig = alt.condition(selectionsig,
                         alt.value('black'),
                         alt.value('lightgray'))
colorsig2 = alt.condition(selectionsig2,
                          alt.value('black'),
                          alt.value('lightgray'))
colorsig3 = alt.condition(selectionsig3,
                          alt.value('black'),
                          alt.value('lightgray'))
colorneg = alt.condition(selectionneg,
                         alt.value('black'),
                         alt.value('lightgray'))

chart1 = alt.Chart().mark_circle(clip=True).encode(
    x=alt.X('genetic_correlation:Q', axis=alt.Axis(orient='top', title="Genetic correlations for " + phenref)),
    y=alt.Y('phenotype_reference:N',
            axis=alt.Axis(title="", minExtent=200)),
    size=alt.value('30'),
    href=alt.Href('phenotype_link:N'),
    color=alt.Color('category:N', legend=None),
    tooltip=['phenotype', 'code', 'genetic_correlation', 'standard_error',
             'pvalue', 'category', 'study size', 'PMID or link',
             'LDSC Total Observed Scale h2:N', 'LDSC Lambda GC',
             'LDSC Intercept', 'LDSC Mean Chi-Square', 'LDSC Ratio:N']
).properties(
    height=500,
    width=500
).transform_filter(
    selection,
).transform_filter(
    selectionsig
).transform_filter(
    selectionsig2
).transform_filter(
    selectionsig3
).transform_filter(
    selectionneg
)


errorbars = alt.Chart().mark_rule().encode(
    y=alt.Y('phenotype_reference:N', axis=alt.Axis(title="", orient='right'),
            ),
    x=alt.X("xmin:Q"),
    x2=alt.X2("xmax:Q"),
    href=alt.Href('phenotype_link:N'),
    color=alt.Color('category:N', legend=None),
    tooltip=['phenotype', 'code', 'genetic_correlation', 'standard_error',
             'pvalue', 'category', 'study size', 'PMID or link',
             'LDSC Total Observed Scale h2:N', 'LDSC Lambda GC',
             'LDSC Intercept', 'LDSC Mean Chi-Square', 'LDSC Ratio:N']
).transform_calculate(
    xmin="datum.genetic_correlation-(1.96*datum.standard_error)",
    xmax="datum.genetic_correlation+(1.96*datum.standard_error)"
).transform_filter(
    selection
).transform_filter(
    selectionsig
).transform_filter(
    selectionsig2
).transform_filter(
    selectionsig3
).transform_filter(
    selectionneg
)


legend = alt.Chart().mark_square().encode(
    y=alt.Y(
        'category:N',
        axis=alt.Axis(
            orient='left',
            title="Click on a category")),
    color=color,
    size=alt.value(100)).add_selection(selection)

legendsig = alt.Chart().mark_square().encode(
    y=alt.Y('cutoff1:N', axis=alt.Axis(orient='left', title=u"p \u2264 0.05")),
    size=alt.value(100),
    color=colorsig
).add_selection(
    selectionsig
)

legendsig2 = alt.Chart().mark_square().encode(
    y=alt.Y('cutoff2:N', axis=alt.Axis(orient='left', title=u"p \u2264 0.005")),
    size=alt.value(100),
    color=colorsig2
).add_selection(
    selectionsig2
)

legendsig3 = alt.Chart().mark_square().encode(
    y=alt.Y('cutoff3:N', axis=alt.Axis(orient='left',
                                       title=u"Bonferroni (p \u2264 " +
                                             str(bonferroni_cutoff) +
                                             ")")),
    size=alt.value(100),
    color=colorsig3
).add_selection(
    selectionsig3
)

legendneg = alt.Chart().mark_square().encode(
    y=alt.Y('direction:N', axis=alt.Axis(orient='left', title="Direction")),
    size=alt.value(100),
    color=colorneg
).add_selection(
    selectionneg
)


legend = alt.vconcat(legend, legendsig)

legend = alt.vconcat(legend, legendsig2)

legend = alt.vconcat(legend, legendsig3)

legend = alt.vconcat(legend, legendneg)

rule = alt.Chart(data2).mark_rule().encode(
    x=alt.X('ThresholdValue:Q')
)

chartfinal = chart1 + errorbars + rule

chartfinal = alt.hconcat(legend, chartfinal, data=df).configure_axis(
    labelLimit=200,
    labelOverlap=True
)

chartfinal.save(argv[5] + '.html')
