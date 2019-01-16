import altair as alt
import pandas as pd
from sys import argv
import numpy as np
df = pd.read_csv(argv[1])
data2 = pd.DataFrame([{"ThresholdValue": 0.0, "Threshold": "hazardous"}])


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

df['PMID'] = df['PMID or link']
def phenlink(x): return "https://www.ncbi.nlm.nih.gov/pubmed/" + \
    str(x) if (len(str(x).strip()) == 8 and str(x).isdigit()) else "nopmid.html"


df['phenotype_link'] = df['PMID or link'].apply(phenlink)


def fancycap(x): return x[0].upper() + x[1:]


df['phenotype_reference'] = df['phenotype_reference'].apply(fancycap)
df['urlcorrelations'] = "https://phenviz.navigome.com/correlations/" + \
    df['code'].astype(str) + '.correlations.html'
df['urlgeneschromosomes'] = "https://phenviz.navigome.com/genes_chromosomes/" + \
    df['code'].astype(str) + '.geneschromosomes.html'
df['urlgenestissues'] = "https://phenviz.navigome.com/genes_tissues/" + \
    df['code'].astype(str) + '.genestissues.html'
df['urlpathways'] = "https://phenviz.navigome.com/pathways/" + df['code'].astype(str) + '.pathways.html'
df['urlphenmap'] = "https://phenviz.navigome.com/phenotype_map/" + \
    df['code'].astype(str) + '.phenotypemap.html'


def fancycap(x): return x[0].upper() + x[1:]


df['phenotype_reference'] = df['phenotype_reference'].apply(fancycap)
df['phenotype'] = df['phenotype'].apply(fancycap)
df['a_phenotype'] = df['phenotype'].apply(
    lambda x: x[:50] + '...' if len(x) > 50 else x)
df['a_phenotype_code'] = df['a_phenotype'].astype(
    str) + ' (' + df['code'].astype(str) + ') '

select_box_category = alt.binding_select(
    options=list(np.sort(np.asarray(df["PMID"].unique()))))
selection_category = alt.selection_single(name='select',
                                          fields=["PMID"],
                                          bind=select_box_category,
                                          empty='none')

selection = alt.selection_multi(fields=['category'])
chart1 = alt.Chart().mark_point(filled=True, stroke='black').encode(
    x=alt.X('t:Q', axis=alt.Axis(orient='top',
                                 title="Select PMID, then " +
                                 "choose a visualization",
                                 grid=False, labels=False,
                                 ticks=False),
            scale=alt.Scale(domain=(-100, 115))),
    y=alt.Y('phenotype_reference:N', axis=None),
    color=alt.Color('category:N', legend=None,
                    scale=alt.Scale(domain=list(np.sort(np.asarray(df['category'].unique()))))),
    tooltip=['phenotype', 'code',
             'category', 'study size', 'PMID or link',
             'LDSC Total Observed Scale h2:N', 'LDSC Lambda GC',
             'LDSC Intercept', 'LDSC Mean Chi-Square', 'LDSC Ratio:N'],
).properties(
).transform_calculate(
    t='0'
)

chart2 = chart1.encode(
    x=alt.value(15),
    size=alt.value('250'),
    tooltip=alt.value("Click to show pathways"),
    href=alt.Href('urlpathways:N'),
    shape=alt.value('square'),
).add_selection(
    selection_category
).transform_filter(
    selection_category
)

chart3 = chart1.encode(
    x=alt.value(35),
    size=alt.value('250'),
    tooltip=alt.value("Click to show genetic correlations"),
    shape=alt.value('circle'),
    href=alt.Href('urlcorrelations:N')
).transform_filter(
    selection_category
)

chart4 = chart1.encode(
    x=alt.value(55),
    size=alt.value('250'),
    tooltip=alt.value("Click to show position relative to other phenotypes on t-SNE map"),
    shape=alt.value('cross'),
    href=alt.Href('urlphenmap:N')
).transform_filter(
    selection_category
)


chart5 = chart1.encode(
    x=alt.value(75),
    size=alt.value('250'),
    tooltip=alt.value("Click to show gene associations (chromosome view, MAGMA + S-PrediXcan)"),
    shape=alt.value('triangle-up'),
    href=alt.Href('urlgeneschromosomes:N')
).transform_filter(
    selection_category
)

chart6 = chart1.encode(
    x=alt.value(95),
    size=alt.value('250'),
    tooltip=alt.value("Click to show S-PrediXcan per-tissue gene associations (parallel coordinates)"),
    shape=alt.value('triangle-down'),
    href=alt.Href('urlgenestissues:N')
).transform_filter(
    selection_category
)

text = chart1.mark_text(
    align='left',
    baseline='middle',
    dx=-50,
    fontSize=13,
    limit=230
).encode(
    text='a_phenotype_code:N',
    href=alt.Href('phenotype_link:N')
).transform_filter(
    selection_category
).properties(
    width=350
)

chartfinal = chart2 + chart3 + chart4 + chart5 + chart6

chartfinal = alt.layer(chartfinal, text, data=df).configure_axis(
    grid=False,
    titleFontSize=16,
    titlePadding=30,
    labelLimit=200,
    domainColor='transparent',
).configure_view(
)

chartfinal.save(argv[2] + '.html')
