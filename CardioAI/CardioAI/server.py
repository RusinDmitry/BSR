import dash
import dash_bootstrap_components as dbc

external_stylesheets = []
external_scripts = ['https://cdn.plot.ly/plotly-locale-ru-latest.js']
app = dash.Dash(__name__, title='CardioAI', update_title='Идёт загрузка',
                external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{"name": "viewport", "content": "width=device-width"}])
app.config.suppress_callback_exceptions = True
app.css.config.serve_locally = True
