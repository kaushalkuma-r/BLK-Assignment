import plotly.express as px
from config import shared_color_scale

def top_obligors_by_par(portfolio_data, top_n=10):
    obligor_par = (
        portfolio_data.groupby('Obligor Name')['Par']
        .sum()
        .reset_index()
        .sort_values(by='Par', ascending=False)
        .head(top_n)
    )

    fig = px.bar(
        obligor_par.sort_values('Par'), 
        x='Par',
        y='Obligor Name',
        orientation='h',
        text='Par',
        color='Obligor Name',
        color_discrete_sequence=shared_color_scale,
        title=f'Top {top_n} Obligors by Total Par Value Exposure'
    )

    fig.update_traces(textposition='outside', texttemplate='%{text:,.0f}')
    fig.update_layout(
        width=950,
        height=500,
        xaxis_title='Total Par Value',
        yaxis_title='Obligor Name',
        showlegend=False,
        font=dict(size=12),
        title_font_size=18,
        plot_bgcolor='white'
    )

    return fig