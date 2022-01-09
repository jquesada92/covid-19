import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc

config = {'displaylogo': False,
          'scrollZoom': False,
           'displayModeBar': False
          }

navbar = dbc.Navbar(
    [
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(html.Img(src="https://img.search.brave.com/gURW74z3KKD-HoNnLX8he3oq1pspX147ptWwNMVeUDk/fit/512/512/ce/1/aHR0cHM6Ly9pbWFn/ZXMudmV4ZWxzLmNv/bS9tZWRpYS91c2Vy/cy8zLzE5OTg0MS9p/c29sYXRlZC9wcmV2/aWV3Lzk2YTdjYWMw/OGFkNDUzOWUxODg4/ZDhmNWM4MmI1ZjQ4/LWNvcm9uYXZpcnVz/LWNvdmlkMTktaWNv/bi1ieS12ZXhlbHMu/cG5n", height="40px")),
                    dbc.Col(dbc.NavbarBrand("DASHBOARD COVID-19", className="text-lg-left font-weight-bold ml-1")),
                ],
                align="center"
            ),
            href="https://plot.ly",
        ),

    ],
    sticky = 'top',
    color="primary",
    dark=True

)

option_menu = html.Div([
        html.Label(['Indicator']),
        dcc.Dropdown(
            id='_indicator', clearable=False,
            placeholder="Select Indicator",
            value='cases', options=[
                {'label': 'Weekly Count of %s Reproted'%c.capitalize(), 'value': c}
                for c in ['cases','deaths']
            ]),
           ]
                    )

map_covid = dbc.Col(
            [
                option_menu,
                
             dcc.Loading(dcc.Graph(id='map',config=config,loading_state = {'is_loading':True}))
    ],className='w-65 px-1'
    ,style={'background-color':"#f8f9fa"}
    )


dist =  dbc.Col([
                     dcc.RadioItems(
                        id='dist-marginal',
                        value='log_scale',
                        options=[{'label': 'Log Scale', 'value': 'log_scale'},
                                {'label': 'None Scale', 'value': 'weekly_count'},
                                ]
                                ,labelStyle={'display': 'inline-block',
                                              "margin-left": "15px"}
                    ),
                     dcc.Loading(dcc.Graph(id="dist",config=config,loading_state = {'is_loading':True}))     
                    ]
                  ,style={'background-color':"#f8f9fa"}
                  ,className="w-35" )


layout =html.Div([
dcc.Interval(
        id='actualizar',
        interval=120000*5, # in milliseconds
        n_intervals=0
    ),
navbar,
dbc.Row([
map_covid,
dist], class_name="mx-1 g-2 my-3")
])
