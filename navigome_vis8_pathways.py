import altair as alt
import pandas as pd
from sys import argv
import sys

df = pd.read_csv(argv[1])
code = argv[2]
data2 = pd.DataFrame([{"ThresholdValue": 0.0, "Threshold": "hazardous"}])
sort = alt.EncodingSortField(field='association', order='descending', op='min')

df['urlpredixcan'] = "https://phenviz.navigome.com/gene_content/"+code+'_'+df['pathway'].astype(str)+'.html'
df['urlmagma'] = "https://phenviz.navigome.com/gene_content_magma/"+code+'_'+df['pathway'].astype(str)+'.html'


if df.isnull().values.all():
    chartfinal = alt.Chart(df).mark_point().encode(
        x=alt.X('pathway',axis=alt.Axis(title='')),
        y=alt.Y('association',axis=alt.Axis(title=''))
        ).properties(title="There is no significant pathway for this phenotype (yet).")
    chartfinal.save(argv[3]+'.html')
    sys.exit()

if not df.isnull().values.all():
    minpred = df['association'].values.min()
    maxpred = df['association'].values.max()
else:
    minpred=1
    maxpred=2
if minpred == maxpred:
    maxpred += 1

chart1 = alt.Chart(df).mark_point(filled=True).encode(
    x=alt.X('t:Q',
            axis=alt.Axis(orient='top',
                          title="Significant pathways (click on the shapes for more info)",
                          grid=False,
                          labels=False,
                          ticks=False),
            scale=alt.Scale(domain=(-5,50))),
    y=alt.Y('pathway:N',axis=alt.Axis(title="",labels=False)),
    tooltip=['pathway', 'association','pathway_size']
).properties(
).transform_calculate(
    t='0'
)

chartbar = alt.Chart(df).mark_rect().encode(
    x=alt.X('association:Q',axis=alt.Axis(orient='top',title='-log10(p)')),
    y=alt.Y('pathway:N',axis=alt.Axis(labels=False,title="",ticks=False)),
    color=alt.Color('association:Q',scale=alt.Scale(scheme='viridis',domain=(minpred,maxpred))),
    tooltip=['pathway','association','pathway_size'],
).properties(
    width=40
    )

chart2 = chart1.encode(
    x = alt.value(10),
    y=alt.Y('pathway:N',axis=alt.Axis(title="",labels=False,ticks=False)),
    size = alt.value('120'),
    tooltip = alt.value("Click to show pathway source"),
    shape = alt.value('square'),
    href = alt.Href('source:N'),
)

chart3 = chart1.encode(
    x = alt.value(25),
    size = alt.value('120'),
    tooltip = alt.value("Click to show tissue-dependent S-PrediXcan gene associations (parallel coordinates)"),
    shape = alt.value('circle'),
    href = alt.Href('urlpredixcan:N'),
    )

chart4 = chart1.encode(
    x = alt.value(40),
    size = alt.value('120'),
    tooltip = alt.value('Click to show gene associations by chromosome'),
    shape = alt.value('triangle-up'),
    href = alt.Href('urlmagma:N')
    )

text = chart1.mark_text(
    align='left',
    baseline='middle',
    dx=15,
).encode(
    text='pathway',
    href = alt.Href('urlpredixcan:N')
)

chartfinal = chart2 + chart3 + chart4 + text


chartfinal = chartfinal.encode(
    y=alt.Y('pathway:N',axis=alt.Axis(title="",labels=False),sort=sort)
    )
chartfinal = alt.hconcat(chartbar,chartfinal,data=df).configure_axis(
     grid=False,
).configure_view(
     strokeWidth=0
)

chartfinal.spacing=-20


chartfinal.save(argv[3]+'.html')

