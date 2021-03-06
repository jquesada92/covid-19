import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


df = pd.read_csv('data/Lasted_cases_deaths_countries.csv')

CACHE_CONFIG = {
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': './cache-directory',
    'CACHE_DEFAULT_TIMEOUT' : 60*60 *24
                }


def register_Callback(app):

    from flask_caching import Cache
    cache = Cache()
    cache.init_app(app.server, config=CACHE_CONFIG)


    @app.callback(
        Output('map', 'figure'),
        [
        Input("_indicator", "value")
        ])
    def MapCloropleth(indicator):
        df_filter = df.copy().loc[lambda x: x.indicator==f"{indicator}"]
        fig_map = go.Figure(go.Choropleth(
                locations=df_filter.country_code,
                z=df_filter.log_scale,
                colorscale ='Viridis' ,
                hoverinfo = 'text' ,
                hovertext = df_filter.apply(lambda x: "{country} {indicator}: {value} \n rate_14 Days: {rate} ".format(
                                                                        country=x.country,
                                                                        indicator=indicator
                                                                        ,value= int(x.weekly_count)
                                                                        ,rate = round(x.rate_14_day,1)
                                                                        )
                                                                        ,axis=1
                                                                        )                 
                        ))
        fig_map.update_layout(
        geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type='equirectangular'
        ),
            plot_bgcolor=	"#f8f9fa",
            paper_bgcolor="#f8f9fa",
        )


        return fig_map
        
        
        
    @app.callback(
            Output('dist', 'figure'),
            [
            Input("dist-marginal", "value")
            ])
    def Displot(scale):
        fig_dist  = px.histogram(
            df,  x=scale,  color="indicator",
            marginal='box',
            opacity = 0.20,
            hover_data=df.columns)
        fig_dist.update_layout(
         autosize=True,
            plot_bgcolor=	"#f8f9fa",
            paper_bgcolor="#f8f9fa")
        return fig_dist