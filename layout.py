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
    color="primary",
    dark=True

)

map_covid = dbc.Card(
    [
        dbc.CardHeader([
        html.Label(['Indicator']),
        dcc.Dropdown(
            id='_indicator', clearable=False,
            placeholder="Select a city",
            value='cases', options=[
                {'label': 'Weekly Count of %s Reproted'%c.capitalize(), 'value': c}
                for c in ['cases','deaths']
            ])]
        ,
        className='d-inline w-100'),
        dbc.CardBody(
            [
                
             dcc.Loading(dcc.Graph(id='map',config=config,loading_state = {'is_loading':True}))], className= 'd-block'
             )
    ],className='card bg-light my-3')


dist = dbc.Card([
    html.P("Log10 Scale:"),
    dcc.RadioItems(
                        id='dist-marginal',
                        value='On',
                        options=[{'label': x, 'value': x} 
                                for x in ['On', 'Off']],
                    ),
                    dcc.Loading(dcc.Graph(id="dist",config=config,loading_state = {'is_loading':True}))
                    
                    
                ],className='card bg-light my-3')

layout =html.Div([
dcc.Interval(
        id='actualizar',
        interval=120000*5, # in milliseconds
        n_intervals=0
    ),
navbar,
map_covid,
dist

])