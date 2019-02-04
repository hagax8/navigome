import altair as alt
import pandas as pd
from sys import argv

correlationfile = pd.read_csv(argv[1])
coordinates = pd.read_csv(argv[2])
f_reference = pd.read_csv(argv[5], keep_default_na=False)
bonferroni_cutoff = argv[3]
coordinates = coordinates[['code', 'x', 'y']]
df = correlationfile.set_index('code').join(coordinates.set_index('code'),
                                            on='code', how='left').join(
    f_reference.set_index('code'),
    on='code', how='left')
df.reset_index(inplace=True)
df.set_index('code', drop=False, inplace=True)

code = argv[4]


def funcsel(x): return code if x == code else 'other phenotypes'


def funcsign(x): return 'positive' if x >= 0.0 else 'negative'


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
selectioncat = alt.selection_multi(fields=['category'], empty='all')
selectionsig = alt.selection_multi(fields=['cutoff1'], empty='all')
selectionsig2 = alt.selection_multi(fields=['cutoff2'], empty='all')
selectionsig3 = alt.selection_multi(fields=['cutoff3'], empty='all')
selectionneg = alt.selection_multi(fields=['direction'], empty='all')

colorcat = alt.condition(selectioncat,
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

df['selected_phenotype'] = df['code'].apply(funcsel)
df['abs_genetic_correlation'] = df['genetic_correlation'].apply(abs)
df['correlation_direction'] = df['genetic_correlation'].apply(funcsign)
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


def phenlink(x): return "https://www.ncbi.nlm.nih.gov/pubmed/" + \
    str(x) if (len(str(x).strip()) == 8 and x.isdigit()) else "nopmid.html"


df['phenotype_link'] = df['PMID or link'].apply(phenlink)


def fancycap(x): return x[0].upper() + x[1:]


df['phenotype_reference'] = df['phenotype_reference'].apply(fancycap)
df['urlcorrelations'] = "https://phenviz.navigome.com/correlations/" + \
    df['code'].astype(str) + '.correlations.html'

phenref = df.loc[df['code'] == code].iloc[0]['phenotype_reference']

selection = alt.selection_multi(fields=['code', 'study size'])
selection2 = alt.selection_interval(empty='none')

color = alt.condition(
    selection,
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


chartneutral = alt.Chart().mark_circle().encode(
    color=color,
    tooltip=['phenotype', 'code', 'genetic_correlation', 'standard_error',
             'pvalue', 'category', 'study size', 'PMID or link',
             'LDSC Total Observed Scale h2:N', 'LDSC Lambda GC',
             'LDSC Intercept', 'LDSC Mean Chi-Square', 'LDSC Ratio:N'],
    x=alt.X('x'),
    y=alt.Y('y')
)

chartneutral_bis = alt.Chart().mark_circle().encode(
    tooltip=['phenotype', 'code', 'genetic_correlation', 'standard_error',
             'pvalue', 'category', 'study size', 'PMID or link',
             'LDSC Total Observed Scale h2:N', 'LDSC Lambda GC',
             'LDSC Intercept', 'LDSC Mean Chi-Square', 'LDSC Ratio:N'],
    x=alt.X('x'),
    y=alt.Y('y')
)


chart1 = chartneutral.encode(
    x=alt.X(
        'x',
        axis=alt.Axis(
            title="Select interval to generate phenotype list. Cross = reference phenotype.",
            ticks=False,
            labels=False,
            orient='top')),
    y=alt.Y(
        'y',
        axis=alt.Axis(
            title="",
            ticks=False,
            labels=False)),
    size=alt.Size(
        'abs_genetic_correlation:Q',
        legend=None),
    href=alt.Href('urlcorrelations:N')).transform_filter(
    (alt.datum.code != code)).add_selection(
        selection2).transform_filter(
            selectioncat).transform_filter(
                selectionsig).transform_filter(
                    selectionsig2).transform_filter(
                        selectionsig3).transform_filter(
                            selectionneg)

chart1_bis = chartneutral_bis.encode(
    color=alt.condition(
        selection,
        alt.Color(
            'correlation_direction:N',
            legend=None,
            scale=alt.Scale(
                domain=[
                    'negative',
                    'positive'],
                range=[
                    'red',
                    'green'])),
        alt.value('lightgray')),
    x=alt.X(
        'x',
        axis=alt.Axis(
            title="Map coloured by direction of gen. correlation (red: negative, green: positive).",
            ticks=False,
            labels=False,
            orient='top')),
    y=alt.Y(
        'y',
        axis=alt.Axis(
            title="",
            ticks=False,
            labels=False)),
    size=alt.Size(
        'abs_genetic_correlation:Q',
        legend=None),
    shape=alt.Shape('selected_phenotype:N'),
    href=alt.Href('urlcorrelations:N')).transform_filter(
        (alt.datum.code != code)).add_selection(
            selection2).transform_filter(
                selectioncat).transform_filter(
                    selectionsig).transform_filter(
                        selectionsig2).transform_filter(
                            selectionsig3).transform_filter(
                                selectionneg)

chart2 = chartneutral.mark_point(
    filled=True).encode(
        shape=alt.value('cross'),
        color=alt.value('black'),
        size=alt.value(350)).transform_filter(
    ((alt.datum.code == code)))

chart2_bis = chartneutral_bis.mark_point(
    filled=True).encode(
        shape=alt.value('cross'),
        color=alt.value('black'),
        size=alt.value(350)).transform_filter(
    ((alt.datum.code == code)))

chartlegend = alt.Chart().mark_point(
    clip=True,
    filled=True).encode(
        x=alt.X(
            'genetic_correlation:Q',
            axis=alt.Axis(
                orient='top',
                title="genetic correlation (selected phenotypes)")),
    y=alt.Y(
            'phenotype_reference:N',
            axis=alt.Axis(
                title="",
                minExtent=150)),
    tooltip=[
            'phenotype',
            'code',
            'genetic_correlation',
            'standard_error',
            'pvalue',
            'category',
            'study size',
            'PMID or link',
            'LDSC Total Observed Scale h2:N',
            'LDSC Lambda GC',
            'LDSC Intercept',
            'LDSC Mean Chi-Square',
            'LDSC Ratio:N'],
    color=alt.condition(
            selection,
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
            alt.value('lightgray'))).properties(
    height=400,
    width=200).add_selection(selection).transform_filter(
        selection2).transform_filter(
            selectioncat).transform_filter(
                selectionsig).transform_filter(
                    selectionsig2).transform_filter(
                        selectionsig3).transform_filter(
                            selectionneg)

errorbars = alt.Chart().mark_rule().encode(
    y=alt.Y('phenotype_reference:N', axis=alt.Axis(title="", orient='right')),
    x=alt.X("xmin:Q"),
    x2=alt.X2("xmax:Q"),
).transform_calculate(
    xmin="datum.genetic_correlation-(1.96*datum.standard_error)",
    xmax="datum.genetic_correlation+(1.96*datum.standard_error)"
).transform_filter(
    selection2
).properties(
    height=400,
    width=200
).transform_filter(
    selection2).transform_filter(
        selectioncat).transform_filter(
            selectionsig).transform_filter(
                selectionsig2).transform_filter(
                    selectionsig3).transform_filter(
                        selectionneg)


rule = alt.Chart(data2).mark_rule().encode(
    x=alt.X('ThresholdValue:Q')
)

legendcategory = alt.Chart().mark_square().encode(
    y=alt.Y(
        'category:N',
        axis=alt.Axis(
            orient='left',
            title="Click on a category")),
    color=colorcat,
    size=alt.value(100)).add_selection(selectioncat)

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

legend = alt.vconcat(legendcategory, legendsig)
legend = alt.vconcat(legend, legendsig2)
legend = alt.vconcat(legend, legendsig3)
legend = alt.vconcat(legend, legendneg)

legendcat = errorbars + chartlegend + rule

chart3 = alt.layer(chart1, chart2)
chart3_bis = alt.layer(chart1_bis, chart2_bis)
chart4 = alt.vconcat(chart3, chart3_bis).resolve_scale(color='independent')
chartfinal = alt.hconcat(
    legend,
    chart4,
    legendcat,
    data=df).configure_axis(
        grid=False,
        labelLimit=150,
        labelFontSize=10).properties(
            title='Interactive t-SNE map of genetic correlations for ' +
            phenref).configure_title(
                offset=20,
    fontSize=12)


chartfinal.save(argv[6] + '.html')
