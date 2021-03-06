import altair as alt
import pandas as pd
from sys import argv


df = pd.read_csv(argv[1], keep_default_na=False)

titleid = argv[2]


def shorten(x): return (x[:30] + '..') if len(x) > 32 else x


def funcsign(x): return 'positive' if x > 0.0 else (
    'negative' if x < 0.0 else 'null')


#df['abs_genetic_correlation'] = df['genetic_correlation'].apply(abs)
#df['correlation_direction'] = df['genetic_correlation'].apply(funcsign)


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

df['trait'] = df['phenotype'].apply(shorten)


def phenlink(x): return "https://www.ncbi.nlm.nih.gov/pubmed/" + \
    str(x) if (len(str(x).strip()) == 8 and x.isdigit()) else "nopmid.html"


df['phenotype_link'] = df['PMID or link'].apply(phenlink)


def fancycap(x): return x[0].upper() + x[1:]


df['phenotype_reference'] = df['phenotype_reference'].apply(fancycap)
df['phenotype'] = df['phenotype'].apply(fancycap)

df['urlcorrelations'] = "https://phenviz.navigome.com/correlations/" + \
    df['code'].astype(str) + '.correlations.html'

selection2 = alt.selection_interval(empty='none')
selection = alt.selection_multi(fields=['code', 'study size'])
selection3 = alt.selection_multi(fields=['category'])
selection4 = alt.selection_multi(fields=['category'])
size = alt.Size(
    'study size:Q',
    legend=None,
)


color2 = alt.condition(
    selection3,
    alt.Color(
        'category:N',
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
                'j: other']),
        legend=None),
    alt.value('whitesmoke'))


chartneutral = alt.Chart().mark_circle().encode(
    color=color2,
    tooltip=['phenotype', 'code',
             'category', 'study size', 'PMID or link',
             'LDSC Total Observed Scale h2:N', 'LDSC Lambda GC',
             'LDSC Intercept', 'LDSC Mean Chi-Square', 'LDSC Ratio:N'],
    x=alt.X('x'),
    y=alt.Y('y'),
).properties(width=300, height=300)


legend2 = alt.Chart().mark_square().encode(
    x=alt.X(
        'category:N',
        axis=alt.Axis(
            orient='bottom',
            labelAngle=-45,
            title="")),
    color=color2,
    size=alt.value(100),
).properties(
    title="",
    width=300).add_selection(selection3)

chart1 = chartneutral.encode(
    x=alt.X(
        'x',
        axis=alt.Axis(
            grid=False,
            title="Touch any phenotype for details.",
            ticks=False,
            labels=False,
            orient='top')),
    y=alt.Y(
        'y',
        axis=None),
    size=size,
    href=alt.Href('urlcorrelations:N'),
)

chartfinal = alt.vconcat(chart1, legend2, data=df, center=True)

chartfinal = chartfinal.configure(
).configure_axis(
    labelLimit=200
).properties(
    title="Map of genetic correlations: " + titleid
).configure_title(
    orient="top",
    anchor='middle',
    fontSize=16
)

chartfinal.save(argv[3] + '.html')
