import dash
import dash_table
from dash import html
from dash import dcc
from dash import Dash, html, Input, Output, callback_context
import plotly.express as px
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc
import dash_auth
from dash.exceptions import PreventUpdate
from dash.dependencies import Output, Input, State
import plotly.graph_objects as go
from datetime import datetime
import dash_daq as daq
# Importar hojas de trabajo de google drive     https://bit.ly/3uQfOvs
from googleapiclient.discovery import build
from google.oauth2 import service_account
from datetime import datetime
from datetime import date



app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SANDSTONE])
server = app.server

auth = dash_auth.BasicAuth(
    app,
    {'NIKOGEO': 'BARRANCALOR',
     'CARLITOSGEO': 'PECHECHES',
     'ANDRESGEO': 'FORMALETAS',
     'EDGARGEO': 'AYAMIGA',
     }
)


badgeFecha = dbc.Button(
    [
        "Fecha:",
        dbc.Badge("", color="light", text_color="primary", className="ms-1"),
    ],
    color="primary", style={'font-family': "Franklin Gothic"}
)

badgeHoraInicial = dbc.Button(
    [
        "Hora Inicial:",
        dbc.Badge("", color="light", text_color="primary", className="ms-1"),
    ],
    color="primary", style={'font-family': "Franklin Gothic"}
)

badgeHoraFinal = dbc.Button(
    [
        "Hora Final:",
        dbc.Badge("", color="light", text_color="primary", className="ms-1"),
    ],
    color="primary", style={'font-family': "Franklin Gothic"}
)

badgeAlturaInicial = dbc.Button(
    [
        "Altura Inicial [m]:",
        dbc.Badge("", color="light", text_color="primary", className="ms-1"),
    ],
    color="primary", style={'font-family': "Franklin Gothic"}
)

badgeAlturaFinal = dbc.Button(
    [
        "Altura Final [m]:",
        dbc.Badge("", color="light", text_color="primary", className="ms-1"),
    ],
    color="primary", style={'font-family': "Franklin Gothic"}
)

badgeFase = dbc.Button(
    [
        "Fase:",
        dbc.Badge("", color="light", text_color="primary", className="ms-1"),
    ],
    color="primary", style={'font-family': "Franklin Gothic"}
)

badgeVi1 = dbc.Button(
    [
        "Vi_1 [m3]:",
        dbc.Badge("", color="light", text_color="primary", className="ms-1"),
    ],
    color="primary", style={'font-family': "Franklin Gothic"}
)

badgeVi2 = dbc.Button(
    [
        "Vi_2 [m3]:",
        dbc.Badge("", color="light", text_color="primary", className="ms-1"),
    ],
    color="primary", style={'font-family': "Franklin Gothic"}
)

badgeVi3 = dbc.Button(
    [
        "Vi_3 [m3]:",
        dbc.Badge("", color="light", text_color="primary", className="ms-1"),
    ],
    color="primary", style={'font-family': "Franklin Gothic"}
)

badgeVf1 = dbc.Button(
    [
        "Vf_1 [m3]:",
        dbc.Badge("", color="light", text_color="primary", className="ms-1"),
    ],
    color="primary", style={'font-family': "Franklin Gothic"}
)

badgeVf2 = dbc.Button(
    [
        "Vf_2 [m3]:",
        dbc.Badge("", color="light", text_color="primary", className="ms-1"),
    ],
    color="primary", style={'font-family': "Franklin Gothic"}
)

badgeVf3 = dbc.Button(
    [
        "Vf_3 [m3]:",
        dbc.Badge("", color="light", text_color="primary", className="ms-1"),
    ],
    color="primary", style={'font-family': "Franklin Gothic"}
)

badgepH = dbc.Button(
    [
        "pH:",
        dbc.Badge("", color="light", text_color="primary", className="ms-1"),
    ],
    color="primary", style={'font-family': "Franklin Gothic"}
)

badgeColor = dbc.Button(
    [
        "Color [Pt-Co]:",
        dbc.Badge("", color="light", text_color="primary", className="ms-1"),
    ],
    color="primary", style={'font-family': "Franklin Gothic"}
)

badgeTurbidez = dbc.Button(
    [
        "Turbidez [NTU]:",
        dbc.Badge("", color="light", text_color="primary", className="ms-1"),
    ],
    color="primary", style={'font-family': "Franklin Gothic"}
)

badgeGeotube = dbc.Button(
    [
        "Geotube:",
        dbc.Badge("", color="light", text_color="primary", className="ms-1"),
    ],
    color="primary", style={'font-family': "Franklin Gothic"}
)

badgeCapacidad = dbc.Button(
    [
        "Capacidad [m3]:",
        dbc.Badge("", color="light", text_color="primary", className="ms-1"),
    ],
    color="primary", style={'font-family': "Franklin Gothic"}
)

badgeP1 = dbc.Button(
    [
        "P1 [m]:",
        dbc.Badge("", color="light", text_color="primary", className="ms-1"),
    ],
    color="primary", style={'font-family': "Franklin Gothic"}
)

badgeP2 = dbc.Button(
    [
        "P2 [m]:",
        dbc.Badge("", color="light", text_color="primary", className="ms-1"),
    ],
    color="primary", style={'font-family': "Franklin Gothic"}
)

badgeP3 = dbc.Button(
    [
        "P3 [m]:",
        dbc.Badge("", color="light", text_color="primary", className="ms-1"),
    ],
    color="primary", style={'font-family': "Franklin Gothic"}
)

badgeP4 = dbc.Button(
    [
        "P4 [m]:",
        dbc.Badge("", color="light", text_color="primary", className="ms-1"),
    ],
    color="primary", style={'font-family': "Franklin Gothic"}
)

badgeP5 = dbc.Button(
    [
        "P5 [m]:",
        dbc.Badge("", color="light", text_color="primary", className="ms-1"),
    ],
    color="primary", style={'font-family': "Franklin Gothic"}
)

badgeP6 = dbc.Button(
    [
        "P6 [m]:",
        dbc.Badge("", color="light", text_color="primary", className="ms-1"),
    ],
    color="primary", style={'font-family': "Franklin Gothic"}
)

badgeP7 = dbc.Button(
    [
        "P7 [m]:",
        dbc.Badge("", color="light", text_color="primary", className="ms-1"),
    ],
    color="primary", style={'font-family': "Franklin Gothic"}
)

badgeP8 = dbc.Button(
    [
        "P8 [m]:",
        dbc.Badge("", color="light", text_color="primary", className="ms-1"),
    ],
    color="primary", style={'font-family': "Franklin Gothic"}
)

badgeP9 = dbc.Button(
    [
        "P9 [m]:",
        dbc.Badge("", color="light", text_color="primary", className="ms-1"),
    ],
    color="primary", style={'font-family': "Franklin Gothic"}
)

badgeP10 = dbc.Button(
    [
        "P10 [m]:",
        dbc.Badge("", color="light", text_color="primary", className="ms-1"),
    ],
    color="primary", style={'font-family': "Franklin Gothic"}
)

badgeP11 = dbc.Button(
    [
        "P11 [m]:",
        dbc.Badge("", color="light", text_color="primary", className="ms-1"),
    ],
    color="primary", style={'font-family': "Franklin Gothic"}
)

badgeP12 = dbc.Button(
    [
        "P12 [m]:",
        dbc.Badge("", color="light", text_color="primary", className="ms-1"),
    ],
    color="primary", style={'font-family': "Franklin Gothic"}
)

badgeNumero = dbc.Button(
    [
        "Número:",
        dbc.Badge("", color="light", text_color="primary", className="ms-1"),
    ],
    color="primary", style={'font-family': "Franklin Gothic"}
)

badgeCapacidad = dbc.Button(
    [
        "Capacidad [m3]:",
        dbc.Badge("", color="light", text_color="primary", className="ms-1"),
    ],
    color="primary", style={'font-family': "Franklin Gothic"}
)

badgeCapacidad = dbc.Button(
    [
        "Capacidad [m3]:",
        dbc.Badge("", color="light", text_color="primary", className="ms-1"),
    ],
    color="primary", style={'font-family': "Franklin Gothic"}
)

badgeLargo = dbc.Button(
    [
        "Largo [m]:",
        dbc.Badge("", color="light", text_color="primary", className="ms-1"),
    ],
    color="primary", style={'font-family': "Franklin Gothic"}
)

badgeAncho = dbc.Button(
    [
        "Ancho [m]:",
        dbc.Badge("", color="light", text_color="primary", className="ms-1"),
    ],
    color="primary", style={'font-family': "Franklin Gothic"}
)

badgeHora = dbc.Button(
    [
        "Hora:",
        dbc.Badge("", color="light", text_color="primary", className="ms-1"),
    ],
    color="primary", style={'font-family': "Franklin Gothic"}
)

badgeReferencia = dbc.Button(
    [
        "Referencia:",
        dbc.Badge("", color="light", text_color="primary", className="ms-1"),
    ],
    color="primary", style={'font-family': "Franklin Gothic"}
)




data = [['3/11/2020', '9:32:00 a. m.', '9:34:00 a. m.', '0.8', '1']]
data = [['3/11/2020', '9:32:00 a. m.', '9:34:00 a. m.', '0.8', '1', '2', '0.8', '211.3376', '303.2', '80096.9504', '344', '124', '1'], ['3/11/2020', '9:47:00 a. m.', '9:48:00 a. m.', '1.1', '1.8', '1', '2.8', '739.6816', '307.2', '81153.6384', '347', '126', '1'], ['3/11/2020', '9:55:00 a. m.', '9:57:00 a. m.', '1.8', '2.2', '2', '1.6', '422.6752', '308.8', '81576.3136', '349', '127', '1']]
data = [['Borrar!', 'Borrar!', 'Borrar!', 'Borrar!', 'Borrar!', 'Borrar!']]
data = []


app.layout = dbc.Container([
    dcc.Store(id='store-data-lodos', storage_type='session'),  # 'local' or 'session'
    dcc.Store(id='store-data-purgas', storage_type='session'),  # 'local' or 'session'
    dcc.Store(id='store-data-clarificado', storage_type='session'),  # 'local' or 'session'
    dbc.Row([
        dbc.Col([dbc.CardImg(
            src="/assets/Logo.jpg",

            style={"width": "6rem",
                   'text-align': 'center'},
        ),
        ]),
        dbc.Col(html.H5('"Cualquier tecnología lo suficientemente avanzada, es indistinguible de la magia." - Arthur C. Clarke '),style={'color':"green", 'font-family': "Franklin Gothic"})
    ]),
    dbc.Row([
        dbc.Col(html.H1(
            "Formulario de Inscripción de Datos - PTAP - Refinería de Barrancabermeja",
            style={'textAlign': 'center', 'color': '#082255', 'font-family': "Franklin Gothic"}), width=12, )
    ]),

    dcc.Tabs([
        dcc.Tab([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    dbc.Row(html.H2(['Purgas Captadas']),
                                            style={'color': '#082255', 'font-family': "Franklin Gothic"})
                                ])
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    badgeFecha
                                ], className="d-grid gap-2"),
                                dbc.Col([
                                    dcc.DatePickerSingle(
                                        id='fecha-purgas',
                                        first_day_of_week=1,  # Display of calendar when open (0 = Sunday)
                                        month_format='MMMM Y',
                                        placeholder='D/M/AAAA',
                                        date=date.today(),
                                        style={'font-family': "Franklin Gothic"},
                                        display_format='D/M/YYYY'

                                    )
                                ], className="d-grid gap-2"),
                                dbc.Col([
                                    badgeFase
                                ], className="d-grid gap-2"),
                                dbc.Col([
                                    html.Div([
                                        dcc.Input(
                                            id='fase-purgas',
                                            type='number',
                                            placeholder="1, 2, 3, etc",
                                            # A hint to the user of what can be entered in the control
                                            debounce=True,
                                            # Changes to input are sent to Dash server only on enter or losing focus
                                            min=1, max=10, step=1,  # Ranges of numeric value. Step refers to increments
                                            # minLength=0, maxLength=5,  # Ranges for character length inside input box
                                            autoComplete='off',
                                            disabled=False,  # Disable input box
                                            readOnly=False,  # Make input box read only
                                            required=True,  # Require user to insert something into input box
                                            size="6",  # Number of characters that will be visible inside box
                                            style={'font-family': "Franklin Gothic", 'textAlign': 'center', }

                                        )
                                    ], className="d-grid gap-2"),
                                ], className="d-grid gap-2"),
                            ]),
                            html.Br(),
                            dbc.Row([
                                dbc.Col([
                                    badgeHoraInicial
                                ], className="d-grid gap-2"),
                                dbc.Col([
                                    html.Div([
                                        dcc.Input(
                                            id='hora-inicial-purgas',
                                            type='text',
                                            placeholder="HH:mm",
                                            # A hint to the user of what can be entered in the control
                                            debounce=True,
                                            # Changes to input are sent to Dash server only on enter or losing focus
                                            # min=2015, max=2019, step=1,  # Ranges of numeric value. Step refers to increments
                                            # minLength=0, maxLength=5,  # Ranges for character length inside input box
                                            autoComplete='off',
                                            disabled=False,  # Disable input box
                                            readOnly=False,  # Make input box read only
                                            required=True,  # Require user to insert something into input box
                                            # size="6",  # Number of characters that will be visible inside box
                                            style={'font-family': "Franklin Gothic", 'textAlign': 'center', }

                                        )
                                    ], className="d-grid gap-2"),
                                ], className="d-grid gap-2"),
                                dbc.Col([
                                    badgeHoraFinal
                                ], className="d-grid gap-2"),

                                dbc.Col([
                                    html.Div([
                                        dcc.Input(
                                            id='hora-final-purgas',
                                            type='text',
                                            placeholder="HH:mm",
                                            # A hint to the user of what can be entered in the control
                                            debounce=True,
                                            # Changes to input are sent to Dash server only on enter or losing focus
                                            # min=2015, max=2019, step=1,  # Ranges of numeric value. Step refers to increments
                                            minLength=0, maxLength=5,  # Ranges for character length inside input box
                                            autoComplete='off',
                                            disabled=False,  # Disable input box
                                            readOnly=False,  # Make input box read only
                                            required=True,  # Require user to insert something into input box
                                            size="6",  # Number of characters that will be visible inside box
                                            style={'font-family': "Franklin Gothic", 'textAlign': 'center', }

                                        )
                                    ], className="d-grid gap-2"),
                                ], className="d-grid gap-2"),
                            ]),
                            html.Br(),
                            dbc.Row([
                                dbc.Col([
                                    badgeAlturaInicial
                                ], className="d-grid gap-2"),
                                dbc.Col([
                                    html.Div([
                                        dcc.Input(
                                            id='altura-inicial-purgas',
                                            type='number',
                                            placeholder="m.cm",
                                            # A hint to the user of what can be entered in the control
                                            debounce=True,
                                            # Changes to input are sent to Dash server only on enter or losing focus
                                            min=0, max=3, step=0.1,
                                            # Ranges of numeric value. Step refers to increments
                                            minLength=0, maxLength=5,  # Ranges for character length inside input box
                                            autoComplete='off',
                                            disabled=False,  # Disable input box
                                            readOnly=False,  # Make input box read only
                                            required=True,  # Require user to insert something into input box
                                            size="6",  # Number of characters that will be visible inside box
                                            style={'font-family': "Franklin Gothic", 'textAlign': 'center', }

                                        )
                                    ], className="d-grid gap-2"),
                                ], className="d-grid gap-2"),
                                dbc.Col([
                                    badgeAlturaFinal
                                ], className="d-grid gap-2"),
                                dbc.Col([
                                    html.Div([
                                        dcc.Input(
                                            id='altura-final-purgas',
                                            type='number',
                                            placeholder="m.cm",
                                            # A hint to the user of what can be entered in the control
                                            debounce=True,
                                            # Changes to input are sent to Dash server only on enter or losing focus
                                            min=0, max=3, step=0.1,
                                            # Ranges of numeric value. Step refers to increments
                                            minLength=0, maxLength=5,  # Ranges for character length inside input box
                                            autoComplete='off',
                                            disabled=False,  # Disable input box
                                            readOnly=False,  # Make input box read only
                                            required=True,  # Require user to insert something into input box
                                            size="6",  # Number of characters that will be visible inside box
                                            style={'font-family': "Franklin Gothic", 'textAlign': 'center', }

                                        )
                                    ], className="d-grid gap-2"),
                                ], className="d-grid gap-2"),

                            ]),
                            html.Br(),
                            dbc.Row([
                                dbc.Col([
                                    html.Button('Registrar', id='registro-purgas', n_clicks=0,
                                                style={'font-family': "Franklin Gothic"}),
                                ], className="d-grid gap-2"),
                                dbc.Col([
                                    html.Button('Guardar Cambios', id='guardar-cambios-purgas', n_clicks=0,
                                                style={'font-family': "Franklin Gothic"}),
                                ], className="d-grid gap-2"),
                            ]),
                            html.Br(),
                            dbc.Row(
                                dash_table.DataTable(
                                    id='datatable-interactivity-purgas',
                                    columns=[
                                        {"name": "Fecha", "id": 0, "deletable": False, "selectable": False,
                                         "hideable": False, },
                                        {"name": "Hora Inicial [m]", "id": 1, "deletable": False, "selectable": False,
                                         "hideable": False},
                                        {"name": "Hora Final [m]", "id": 2, "deletable": False, "selectable": False,
                                         "hideable": False},
                                        {"name": "Altura Inicial [m]", "id": 3, "deletable": False, "selectable": False,
                                         "hideable": False},
                                        {"name": "Altura Final [m]", "id": 4, "deletable": False, "selectable": False,
                                         "hideable": False},
                                        {"name": "Fase", "id": 5, "deletable": False, "selectable": False,
                                         "hideable": False},

                                    ],
                                    data=[],  # the contents of the table NO INICIALIZAR CON [] SINO CON EL ID!!!

                                    editable=True,  # allow editing of data inside all cells
                                    filter_action="none",  # allow filtering of data by user ('native') or not ('none')
                                    sort_action="none",  # enables data to be sorted per-column by user or not ('none')
                                    sort_mode="none",  # sort across 'multi' or 'single' columns
                                    column_selectable="none",  # allow users to select 'multi' or 'single' columns
                                    row_selectable="multi",  # allow users to select 'multi' or 'single' rows
                                    row_deletable=True,  # choose if user can delete a row (True) or not (False)
                                    selected_columns=[],  # ids of columns that user selects
                                    selected_rows=[],  # indices of rows that user selects
                                    page_action="native",  # all data is passed to the table up-front or not ('none')
                                    page_current=0,  # page number that user is on
                                    page_size=6,  # number of rows visible per page
                                    style_cell={  # ensure adequate header width when text is shorter than cell's text
                                        'minWidth': 95, 'maxWidth': 95, 'width': 95
                                    },
                                    style_data={  # overflow cells' content into multiple lines
                                        'whiteSpace': 'normal',
                                        'height': 'auto',
                                        'font-family': "Franklin Gothic",
                                        'textAlign': 'center'
                                    },
                                    style_header={
                                        'font-family': "Franklin Gothic",
                                        'textAlign': 'center',
                                        'fontWeight': 'bold'
                                    },

                                )
                            ),
                            html.Br(),
                            dbc.Row([
                                dbc.Col([
                                    # html.Button('Enviar', id='enviar-lodos', n_clicks=0),
                                    dcc.ConfirmDialogProvider(
                                        children=html.Button('Enviar', ),
                                        id='enviar-purgas',
                                        message='¿Está seguro que desea enviar los datos de purgas captadas?'
                                                'No olvide borrar los datos después del envío.',
                                        # style={'font-family': "Franklin Gothic"},
                                    ),
                                ], style={'font-family': "Franklin Gothic"}),
                                dbc.Col([
                                    dbc.Accordion([
                                        dbc.AccordionItem(
                                            html.Button('Borrar', id='borrar-purgas', n_clicks=0), title="Borrar"
                                        ),
                                    ], start_collapsed=True, style={'font-family': "Franklin Gothic"}),

                                ]),

                            ]),

                        ])
                    ])
                ])
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    dbc.Row(html.H2(['Bombeo de Lodos']),
                                            style={'color': '#082255', 'font-family': "Franklin Gothic"})
                                ])
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    badgeFecha
                                ], className="d-grid gap-2"),
                                dbc.Col([
                                    dcc.DatePickerSingle(
                                        id='fecha-lodos',
                                        first_day_of_week=1,  # Display of calendar when open (0 = Sunday)
                                        month_format='MMMM Y',
                                        placeholder='D/M/AAAA',
                                        date=date.today(),
                                        style={'font-family': "Franklin Gothic"},
                                        display_format='D/M/YYYY'

                                    )
                                ], className="d-grid gap-2"),
                                dbc.Col([
                                    badgeFase
                                ], className="d-grid gap-2"),
                                dbc.Col([
                                    html.Div([
                                        dcc.Input(
                                            id='fase-lodos',
                                            type='number',
                                            placeholder="1, 2, 3, etc",
                                            # A hint to the user of what can be entered in the control
                                            debounce=True,
                                            # Changes to input are sent to Dash server only on enter or losing focus
                                            min=1, max=10, step=1,  # Ranges of numeric value. Step refers to increments
                                            minLength=0, maxLength=5,  # Ranges for character length inside input box
                                            autoComplete='off',
                                            disabled=False,  # Disable input box
                                            readOnly=False,  # Make input box read only
                                            required=True,  # Require user to insert something into input box
                                            size="6",  # Number of characters that will be visible inside box
                                            style={'font-family': "Franklin Gothic", 'textAlign': 'center', }

                                        )
                                    ], className="d-grid gap-2"),
                                ], className="d-grid gap-2"),
                            ]),
                            html.Br(),
                            dbc.Row([
                                dbc.Col([
                                    badgeHoraInicial
                                ], className="d-grid gap-2"),
                                dbc.Col([
                                    html.Div([
                                        dcc.Input(
                                            id='hora-inicial-lodos',
                                            type='text',
                                            placeholder="HH:mm",
                                            # A hint to the user of what can be entered in the control
                                            debounce=True,
                                            # Changes to input are sent to Dash server only on enter or losing focus
                                            # min=2015, max=2019, step=1,  # Ranges of numeric value. Step refers to increments
                                            minLength=0, maxLength=5,  # Ranges for character length inside input box
                                            autoComplete='off',
                                            disabled=False,  # Disable input box
                                            readOnly=False,  # Make input box read only
                                            required=True,  # Require user to insert something into input box
                                            size="6",  # Number of characters that will be visible inside box
                                            style={'font-family': "Franklin Gothic", 'textAlign': 'center', }

                                        )
                                    ], className="d-grid gap-2"),
                                ], className="d-grid gap-2"),
                                dbc.Col([
                                    badgeHoraFinal
                                ], className="d-grid gap-2"),
                                dbc.Col([
                                    html.Div([
                                        dcc.Input(
                                            id='hora-final-lodos',
                                            type='text',
                                            placeholder="HH:mm",
                                            # A hint to the user of what can be entered in the control
                                            debounce=True,
                                            # Changes to input are sent to Dash server only on enter or losing focus
                                            # min=2015, max=2019, step=1,  # Ranges of numeric value. Step refers to increments
                                            minLength=0, maxLength=5,  # Ranges for character length inside input box
                                            autoComplete='off',
                                            disabled=False,  # Disable input box
                                            readOnly=False,  # Make input box read only
                                            required=True,  # Require user to insert something into input box
                                            size="6",  # Number of characters that will be visible inside box
                                            style={'font-family': "Franklin Gothic", 'textAlign': 'center', }

                                        )
                                    ], className="d-grid gap-2"),
                                ], className="d-grid gap-2"),
                            ]),
                            html.Br(),
                            dbc.Row([
                                dbc.Col([
                                    badgeAlturaInicial
                                ], className="d-grid gap-2"),
                                dbc.Col([
                                    html.Div([
                                        dcc.Input(
                                            id='altura-inicial-lodos',
                                            type='number',
                                            placeholder="m.cm",
                                            # A hint to the user of what can be entered in the control
                                            debounce=True,
                                            # Changes to input are sent to Dash server only on enter or losing focus
                                            min=0, max=3, step=0.1,
                                            # Ranges of numeric value. Step refers to increments
                                            minLength=0, maxLength=5,  # Ranges for character length inside input box
                                            autoComplete='off',
                                            disabled=False,  # Disable input box
                                            readOnly=False,  # Make input box read only
                                            required=True,  # Require user to insert something into input box
                                            size="6",  # Number of characters that will be visible inside box
                                            style={'font-family': "Franklin Gothic", 'textAlign': 'center', }

                                        )
                                    ], className="d-grid gap-2"),
                                ], className="d-grid gap-2"),
                                dbc.Col([
                                    badgeAlturaFinal
                                ], className="d-grid gap-2"),
                                dbc.Col([
                                    html.Div([
                                        dcc.Input(
                                            id='altura-final-lodos',
                                            type='number',
                                            placeholder="m.cm",
                                            # A hint to the user of what can be entered in the control
                                            debounce=True,
                                            # Changes to input are sent to Dash server only on enter or losing focus
                                            min=0, max=3, step=0.1,
                                            # Ranges of numeric value. Step refers to increments
                                            minLength=0, maxLength=5,  # Ranges for character length inside input box
                                            autoComplete='off',
                                            disabled=False,  # Disable input box
                                            readOnly=False,  # Make input box read only
                                            required=True,  # Require user to insert something into input box
                                            size="6",  # Number of characters that will be visible inside box
                                            style={'font-family': "Franklin Gothic", 'textAlign': 'center', }

                                        )
                                    ], className="d-grid gap-2"),
                                ], className="d-grid gap-2"),

                            ]),
                            html.Br(),
                            dbc.Row([
                                dbc.Col([
                                    html.Button('Registrar', id='registro-lodos', n_clicks=0),
                                ], className="d-grid gap-2", style={'font-family': "Franklin Gothic"}),
                                dbc.Col([
                                    html.Button('Guardar Cambios', id='guardar-cambios-lodos', n_clicks=0),
                                ], className="d-grid gap-2", style={'font-family': "Franklin Gothic"}),
                            ]),
                            html.Br(),
                            dbc.Row(
                                dash_table.DataTable(
                                    id='datatable-interactivity-lodos',
                                    columns=[
                                        {"name": "Fecha", "id": 0, "deletable": False, "selectable": False,
                                         "hideable": False},
                                        {"name": "Hora Inicial [m]", "id": 1, "deletable": False, "selectable": False,
                                         "hideable": False},
                                        {"name": "Hora Final [m]", "id": 2, "deletable": False, "selectable": False,
                                         "hideable": False},
                                        {"name": "Altura Inicial [m]", "id": 3, "deletable": False, "selectable": False,
                                         "hideable": False},
                                        {"name": "Altura Final [m]", "id": 4, "deletable": False, "selectable": False,
                                         "hideable": False},
                                        {"name": "Fase", "id": 5, "deletable": False, "selectable": False,
                                         "hideable": False},

                                    ],
                                    data=[],  # the contents of the table NO INICIALIZAR CON [] SINO CON EL ID!!!

                                    editable=True,  # allow editing of data inside all cells
                                    filter_action="none",  # allow filtering of data by user ('native') or not ('none')
                                    sort_action="none",  # enables data to be sorted per-column by user or not ('none')
                                    sort_mode="none",  # sort across 'multi' or 'single' columns
                                    column_selectable="none",  # allow users to select 'multi' or 'single' columns
                                    row_selectable="multi",  # allow users to select 'multi' or 'single' rows
                                    row_deletable=True,  # choose if user can delete a row (True) or not (False)
                                    selected_columns=[],  # ids of columns that user selects
                                    selected_rows=[],  # indices of rows that user selects
                                    page_action="native",  # all data is passed to the table up-front or not ('none')
                                    page_current=0,  # page number that user is on
                                    page_size=6,  # number of rows visible per page
                                    style_cell={  # ensure adequate header width when text is shorter than cell's text
                                        'minWidth': 95, 'maxWidth': 95, 'width': 95
                                    },
                                    style_data={  # overflow cells' content into multiple lines
                                        'whiteSpace': 'normal',
                                        'height': 'auto',
                                        'font-family': "Franklin Gothic",
                                        'textAlign': 'center',
                                    },
                                    style_header={
                                        'font-family': "Franklin Gothic",
                                        'textAlign': 'center',
                                        'fontWeight': 'bold'
                                    },

                                )
                            ),
                            html.Br(),
                            dbc.Row([
                                dbc.Col([
                                    dcc.ConfirmDialogProvider(
                                        children=html.Button('Enviar', ),
                                        id='enviar-lodos',
                                        message='¿Está seguro que desea enviar los datos de agua lodosa bombeada?'
                                                'No olvide borrar los datos después del envío.',

                                    ),
                                ], style={'font-family': "Franklin Gothic"}),
                                dbc.Col([
                                    dbc.Accordion([
                                        dbc.AccordionItem(
                                            html.Button('Borrar', id='borrar-lodos', n_clicks=0), title="Borrar"
                                        ),
                                    ], start_collapsed=True),

                                ], style={'font-family': "Franklin Gothic"}),

                            ]),
                            dbc.Row([
                                html.Div(id='Hola3', style={'font-family': "Franklin Gothic"})
                            ]),
                            dbc.Row([
                                html.Div(id='Hola4', style={'font-family': "Franklin Gothic"})
                            ]),
                            dbc.Row([
                                html.Div(id='Hola5', style={'font-family': "Franklin Gothic"})
                            ]),
                            dbc.Row([
                                html.Div(id='Hola6', style={'font-family': "Franklin Gothic"})
                            ]),

                        ])
                    ])
                ])
            ]),
        ], label='Purgas Captadas & Bombeo de Lodos',
                ),
        dcc.Tab([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    dbc.Row(html.H2(['Bombeo de Clarificado']),
                                            style={'color': '#082255', 'font-family': "Franklin Gothic"})
                                ]),
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    badgeFecha
                                ], className="d-grid gap-2"),
                                dbc.Col([
                                    dcc.DatePickerSingle(
                                        id='fecha-clarificado',
                                        first_day_of_week=1,  # Display of calendar when open (0 = Sunday)
                                        month_format='MMMM Y',
                                        placeholder='D/M/AAAA',
                                        date=date.today(),
                                        style={'font-family': "Franklin Gothic", 'textAlign': 'center', },
                                        display_format='D/M/YYYY'

                                    )
                                ], className="d-grid gap-2"),
                                dbc.Col([
                                    badgeFase
                                ], className="d-grid gap-2"),
                                dbc.Col([
                                    html.Div([
                                        dcc.Input(
                                            id='fase-clarificado',
                                            type='number',
                                            placeholder="1, 2, 3, etc",
                                            # A hint to the user of what can be entered in the control
                                            debounce=True,
                                            # Changes to input are sent to Dash server only on enter or losing focus
                                            min=1, max=10, step=1,  # Ranges of numeric value. Step refers to increments
                                            minLength=0, maxLength=5,  # Ranges for character length inside input box
                                            autoComplete='off',
                                            disabled=False,  # Disable input box
                                            readOnly=False,  # Make input box read only
                                            required=True,  # Require user to insert something into input box
                                            size="6",  # Number of characters that will be visible inside box
                                            style={'font-family': "Franklin Gothic", 'textAlign': 'center', }

                                        )
                                    ], className="d-grid gap-2"),
                                ], className="d-grid gap-2"),
                            ]),
                            html.Br(),
                            dbc.Row([
                                dbc.Col([
                                    badgeHoraInicial
                                ], className="d-grid gap-2"),
                                dbc.Col([
                                    html.Div([
                                        dcc.Input(
                                            id='hora-inicial-clarificado',
                                            type='text',
                                            placeholder="HH:mm",
                                            # A hint to the user of what can be entered in the control
                                            debounce=True,
                                            # Changes to input are sent to Dash server only on enter or losing focus
                                            # min=2015, max=2019, step=1,  # Ranges of numeric value. Step refers to increments
                                            minLength=0, maxLength=5,  # Ranges for character length inside input box
                                            autoComplete='off',
                                            disabled=False,  # Disable input box
                                            readOnly=False,  # Make input box read only
                                            required=True,  # Require user to insert something into input box
                                            size="6",  # Number of characters that will be visible inside box
                                            style={'font-family': "Franklin Gothic", 'textAlign': 'center', }

                                        )
                                    ], className="d-grid gap-2"),
                                ], className="d-grid gap-2"),
                                dbc.Col([
                                    badgeHoraFinal
                                ], className="d-grid gap-2"),
                                dbc.Col([
                                    html.Div([
                                        dcc.Input(
                                            id='hora-final-clarificado',
                                            type='text',
                                            placeholder="HH:mm",
                                            # A hint to the user of what can be entered in the control
                                            debounce=True,
                                            # Changes to input are sent to Dash server only on enter or losing focus
                                            # min=2015, max=2019, step=1,  # Ranges of numeric value. Step refers to increments
                                            minLength=0, maxLength=5,  # Ranges for character length inside input box
                                            autoComplete='off',
                                            disabled=False,  # Disable input box
                                            readOnly=False,  # Make input box read only
                                            required=True,  # Require user to insert something into input box
                                            size="6",  # Number of characters that will be visible inside box
                                            style={'font-family': "Franklin Gothic", 'textAlign': 'center', }

                                        )
                                    ], className="d-grid gap-2"),
                                ], className="d-grid gap-2"),
                            ]),
                            html.Br(),
                            dbc.Row([
                                dbc.Col([
                                    dbc.Row(html.H5(['Lectura Inicial de Volumen [m3]']),
                                            style={'color': '#082255', 'font-family': "Franklin Gothic"})
                                ], style={'textAlign': 'center'}, align='center'),
                            ], className="d-grid gap-2"),
                            dbc.Row([
                                dbc.Col([
                                    badgeVi1
                                ], className="d-grid gap-2"),
                                dbc.Col([
                                    html.Div([
                                        dcc.Input(
                                            id='Vi1',
                                            type='number',
                                            placeholder="X10",
                                            # A hint to the user of what can be entered in the control
                                            debounce=True,
                                            # Changes to input are sent to Dash server only on enter or losing focus
                                            min=0, max=999999, step=1,
                                            # Ranges of numeric value. Step refers to increments
                                            minLength=0, maxLength=6,  # Ranges for character length inside input box
                                            autoComplete='off',
                                            disabled=False,  # Disable input box
                                            readOnly=False,  # Make input box read only
                                            required=True,  # Require user to insert something into input box
                                            size="9",  # Number of characters that will be visible inside box
                                            style={'font-family': "Franklin Gothic", 'textAlign': 'center', }
                                        )
                                    ], className="d-grid gap-2"),
                                ], className="d-grid gap-2"),
                                dbc.Col([
                                    badgeVi2
                                ], className="d-grid gap-2"),
                                dbc.Col([
                                    html.Div([
                                        dcc.Input(
                                            id='Vi2',
                                            type='number',
                                            placeholder="X1",
                                            # A hint to the user of what can be entered in the control
                                            debounce=True,
                                            # Changes to input are sent to Dash server only on enter or losing focus
                                            min=0, max=9.99, step=0.1,
                                            # Ranges of numeric value. Step refers to increments
                                            minLength=0, maxLength=4,  # Ranges for character length inside input box
                                            autoComplete='off',
                                            disabled=False,  # Disable input box
                                            readOnly=False,  # Make input box read only
                                            required=True,  # Require user to insert something into input box
                                            size="4",  # Number of characters that will be visible inside box
                                            style={'font-family': "Franklin Gothic", 'textAlign': 'center', }

                                        )
                                    ], className="d-grid gap-2"),
                                ], className="d-grid gap-2"),
                                dbc.Col([
                                    badgeVi3
                                ], className="d-grid gap-2"),
                                dbc.Col([
                                    html.Div([
                                        dcc.Input(
                                            id='Vi3',
                                            type='number',
                                            placeholder="X0.1",
                                            # A hint to the user of what can be entered in the control
                                            debounce=True,
                                            # Changes to input are sent to Dash server only on enter or losing focus
                                            min=0, max=9.99, step=0.1,
                                            # Ranges of numeric value. Step refers to increments
                                            minLength=0, maxLength=4,  # Ranges for character length inside input box
                                            autoComplete='off',
                                            disabled=False,  # Disable input box
                                            readOnly=False,  # Make input box read only
                                            required=True,  # Require user to insert something into input box
                                            size="4",  # Number of characters that will be visible inside box
                                            style={'font-family': "Franklin Gothic", 'textAlign': 'center', }

                                        )
                                    ], className="d-grid gap-2"),
                                ], className="d-grid gap-2"),
                            ]),
                            html.Br(),
                            dbc.Row([
                                dbc.Col([
                                    dbc.Row(html.H5(['Lectura Final de Volumen [m3]']),
                                            style={'color': '#082255', 'font-family': "Franklin Gothic"})
                                ], style={'textAlign': 'center'}, align='center'),
                            ], className="d-grid gap-2"),
                            dbc.Row([
                                dbc.Col([
                                    badgeVf1
                                ], className="d-grid gap-2"),
                                dbc.Col([
                                    html.Div([
                                        dcc.Input(
                                            id='Vf1',
                                            type='number',
                                            placeholder="X10",
                                            # A hint to the user of what can be entered in the control
                                            debounce=True,
                                            # Changes to input are sent to Dash server only on enter or losing focus
                                            min=0, max=999999, step=1,
                                            # Ranges of numeric value. Step refers to increments
                                            minLength=0, maxLength=6,  # Ranges for character length inside input box
                                            autoComplete='off',
                                            disabled=False,  # Disable input box
                                            readOnly=False,  # Make input box read only
                                            required=True,  # Require user to insert something into input box
                                            size="9",  # Number of characters that will be visible inside box
                                            style={'font-family': "Franklin Gothic", 'textAlign': 'center', }

                                        )
                                    ], className="d-grid gap-2"),
                                ], className="d-grid gap-2"),
                                dbc.Col([
                                    badgeVf2
                                ], className="d-grid gap-2"),
                                dbc.Col([
                                    html.Div([
                                        dcc.Input(
                                            id='Vf2',
                                            type='number',
                                            placeholder="X1",
                                            # A hint to the user of what can be entered in the control
                                            debounce=True,
                                            # Changes to input are sent to Dash server only on enter or losing focus
                                            min=0, max=9.99, step=0.1,
                                            # Ranges of numeric value. Step refers to increments
                                            minLength=0, maxLength=4,  # Ranges for character length inside input box
                                            autoComplete='off',
                                            disabled=False,  # Disable input box
                                            readOnly=False,  # Make input box read only
                                            required=True,  # Require user to insert something into input box
                                            size="4",  # Number of characters that will be visible inside box
                                            style={'font-family': "Franklin Gothic", 'textAlign': 'center', }

                                        )
                                    ], className="d-grid gap-2"),
                                ], className="d-grid gap-2"),
                                dbc.Col([
                                    badgeVf3
                                ], className="d-grid gap-2"),
                                dbc.Col([
                                    html.Div([
                                        dcc.Input(
                                            id='Vf3',
                                            type='number',
                                            placeholder="X0.1",
                                            # A hint to the user of what can be entered in the control
                                            debounce=True,
                                            # Changes to input are sent to Dash server only on enter or losing focus
                                            min=0, max=9.99, step=0.1,
                                            # Ranges of numeric value. Step refers to increments
                                            minLength=0, maxLength=4,  # Ranges for character length inside input box
                                            autoComplete='off',
                                            disabled=False,  # Disable input box
                                            readOnly=False,  # Make input box read only
                                            required=True,  # Require user to insert something into input box
                                            size="4",  # Number of characters that will be visible inside box
                                            style={'font-family': "Franklin Gothic", 'textAlign': 'center', }

                                        )
                                    ], className="d-grid gap-2"),
                                ], className="d-grid gap-2"),
                            ]),
                            html.Br(),
                            dbc.Row([
                                dbc.Col([
                                    dbc.Row(html.H5(['Propiedades de Agua Clarificada']),
                                            style={'color': '#082255', 'font-family': "Franklin Gothic"})
                                ], style={'textAlign': 'center'}, align='center'),
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    badgepH
                                ], className="d-grid gap-2"),
                                dbc.Col([
                                    html.Div([
                                        dcc.Input(
                                            id='pH',
                                            type='number',
                                            placeholder="pH",
                                            # A hint to the user of what can be entered in the control
                                            debounce=True,
                                            # Changes to input are sent to Dash server only on enter or losing focus
                                            min=0, max=14, step=0.01,
                                            # Ranges of numeric value. Step refers to increments
                                            minLength=0, maxLength=4,  # Ranges for character length inside input box
                                            autoComplete='off',
                                            disabled=False,  # Disable input box
                                            readOnly=False,  # Make input box read only
                                            required=True,  # Require user to insert something into input box
                                            size="4",  # Number of characters that will be visible inside box
                                            style={'font-family': "Franklin Gothic", 'textAlign': 'center', }

                                        )
                                    ], className="d-grid gap-2"),
                                ], className="d-grid gap-2"),
                                dbc.Col([
                                    badgeColor
                                ], className="d-grid gap-2"),
                                dbc.Col([
                                    html.Div([
                                        dcc.Input(
                                            id='color',
                                            type='number',
                                            placeholder="Pt-Co",
                                            # A hint to the user of what can be entered in the control
                                            debounce=True,
                                            # Changes to input are sent to Dash server only on enter or losing focus
                                            min=0, max=250, step=1,
                                            # Ranges of numeric value. Step refers to increments
                                            minLength=0, maxLength=4,  # Ranges for character length inside input box
                                            autoComplete='off',
                                            disabled=False,  # Disable input box
                                            readOnly=False,  # Make input box read only
                                            required=True,  # Require user to insert something into input box
                                            size="4",  # Number of characters that will be visible inside box
                                            style={'font-family': "Franklin Gothic", 'textAlign': 'center', }

                                        )
                                    ], className="d-grid gap-2"),
                                ], className="d-grid gap-2"),
                                dbc.Col([
                                    badgeTurbidez
                                ], className="d-grid gap-2"),
                                dbc.Col([
                                    html.Div([
                                        dcc.Input(
                                            id='turbidez',
                                            type='number',
                                            placeholder="NTU",
                                            # A hint to the user of what can be entered in the control
                                            debounce=True,
                                            # Changes to input are sent to Dash server only on enter or losing focus
                                            min=0, max=50, step=1,  # Ranges of numeric value. Step refers to increments
                                            minLength=0, maxLength=4,  # Ranges for character length inside input box
                                            autoComplete='off',
                                            disabled=False,  # Disable input box
                                            readOnly=False,  # Make input box read only
                                            required=True,  # Require user to insert something into input box
                                            size="4",  # Number of characters that will be visible inside box
                                            style={'font-family': "Franklin Gothic", 'textAlign': 'center', }

                                        )
                                    ], className="d-grid gap-2"),
                                ], className="d-grid gap-2"),
                            ]),
                            html.Br(),
                            dbc.Row([
                                dbc.Col([
                                    html.Button('Registrar', id='registro-clarificado', n_clicks=0),
                                ], className="d-grid gap-2",
                                    style={'font-family': "Franklin Gothic", 'textAlign': 'center', }),
                                dbc.Col([
                                    html.Button('Guardar Cambios', id='guardar-cambios-clarificado', n_clicks=0),
                                ], className="d-grid gap-2",
                                    style={'font-family': "Franklin Gothic", 'textAlign': 'center', }),
                            ]),
                            html.Br(),
                            dbc.Row(
                                dash_table.DataTable(
                                    id='datatable-interactivity-clarificado',
                                    columns=[
                                        {"name": "Fecha", "id": 0, "deletable": False, "selectable": False,
                                         "hideable": False},
                                        {"name": "Hora Inicial [m]", "id": 1, "deletable": False, "selectable": False,
                                         "hideable": False},
                                        {"name": "Hora Final [m]", "id": 2, "deletable": False, "selectable": False,
                                         "hideable": False},
                                        {"name": "Lectura Inicial [m3]", "id": 3, "deletable": False,
                                         "selectable": False,
                                         "hideable": False},
                                        {"name": "Lectura Final [m3]", "id": 4, "deletable": False, "selectable": False,
                                         "hideable": False},
                                        {"name": "pH", "id": 5, "deletable": False, "selectable": False,
                                         "hideable": False},
                                        {"name": "Color", "id": 6, "deletable": False, "selectable": False,
                                         "hideable": False},
                                        {"name": "Turbidez", "id": 7, "deletable": False, "selectable": False,
                                         "hideable": False},
                                        {"name": "Fase", "id": 8, "deletable": False, "selectable": False,
                                         "hideable": False},

                                    ],
                                    data=[],  # the contents of the table NO INICIALIZAR CON [] SINO CON EL ID!!!

                                    editable=True,  # allow editing of data inside all cells
                                    filter_action="none",  # allow filtering of data by user ('native') or not ('none')
                                    sort_action="none",  # enables data to be sorted per-column by user or not ('none')
                                    sort_mode="none",  # sort across 'multi' or 'single' columns
                                    column_selectable="none",  # allow users to select 'multi' or 'single' columns
                                    row_selectable="multi",  # allow users to select 'multi' or 'single' rows
                                    row_deletable=True,  # choose if user can delete a row (True) or not (False)
                                    selected_columns=[],  # ids of columns that user selects
                                    selected_rows=[],  # indices of rows that user selects
                                    page_action="native",  # all data is passed to the table up-front or not ('none')
                                    page_current=0,  # page number that user is on
                                    page_size=6,  # number of rows visible per page
                                    style_cell={  # ensure adequate header width when text is shorter than cell's text
                                        'minWidth': 95, 'maxWidth': 95, 'width': 95
                                    },
                                    style_data={  # overflow cells' content into multiple lines
                                        'whiteSpace': 'normal',
                                        'height': 'auto',
                                        'font-family': "Franklin Gothic",
                                        'textAlign': 'center',
                                    },
                                    style_header={
                                        'font-family': "Franklin Gothic",
                                        'textAlign': 'center',
                                        'fontWeight': 'bold'
                                    },

                                )
                            ),
                            html.Br(),
                            dbc.Row([
                                dbc.Col([
                                    dcc.ConfirmDialogProvider(
                                        children=html.Button('Enviar', ),
                                        id='enviar-clarificado',
                                        message='¿Está seguro que desea enviar los datos de agua clarificada retornada? '
                                                'No olvide borrar los datos después del envío.'
                                    ),
                                ], style={'font-family': "Franklin Gothic"}),
                                dbc.Col([
                                    dbc.Accordion([
                                        dbc.AccordionItem(
                                            html.Button('Borrar', id='borrar-clarificado', n_clicks=0), title="Borrar"
                                        ),
                                    ], start_collapsed=True),

                                ], style={'font-family': "Franklin Gothic", 'textAlign': 'center', }),

                            ]),
                        ]),
                    ]),
                ]),
            ]),
        ], label='Bombeo de Clarificado', ),
        dcc.Tab([
            dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dbc.Row(html.H2(['Control de Alturas de Geotube']), style={'color': '#082255', 'font-family': "Franklin Gothic"})
                        ]),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            badgeFecha
                        ], className="d-grid gap-2"),
                        dbc.Col([
                            dcc.DatePickerSingle(
                                id='fecha-geotube',
                                first_day_of_week=1,  # Display of calendar when open (0 = Sunday)
                                month_format='MMMM Y',
                                placeholder='D/M/AAAA',
                                date=date.today(),
                                style={'font-family': "Franklin Gothic"},
                                display_format='D/M/YYYY'

                            )
                        ], className="d-grid gap-2" ),
                        dbc.Col([
                            badgeHora
                        ], className="d-grid gap-2"),
                        dbc.Col(dbc.RadioItems(
                            options=[
                                {"label": "8:00", "value": True},
                                {"label": "16:00", "value": False},
                            ],
                            value=True,
                            id="hora-GT",
                            style={'font-family': "Franklin Gothic"}
                        ), className="d-grid gap-2" ),

                    ]),
                    html.Br(),
                    dbc.Row([
                        dbc.Col([
                            badgeFase
                        ], className="d-grid gap-2"),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='fase-geotube',
                                    type='number',
                                    placeholder="1, 2, 3, etc",
                                    # A hint to the user of what can be entered in the control
                                    debounce=True,
                                    # Changes to input are sent to Dash server only on enter or losing focus
                                    min=1, max=10, step=1,  # Ranges of numeric value. Step refers to increments
                                    minLength=0, maxLength=5,  # Ranges for character length inside input box
                                    autoComplete='off',
                                    disabled=False,  # Disable input box
                                    readOnly=False,  # Make input box read only
                                    required=True,  # Require user to insert something into input box
                                    size="6",  # Number of characters that will be visible inside box
                                    style={'font-family': "Franklin Gothic", 'textAlign': 'center',}

                                )
                            ], className="d-grid gap-2"),
                        ], className="d-grid gap-2"),
                        dbc.Col([
                            badgeReferencia
                        ], className="d-grid gap-2"),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='referencia-GT',
                                    type='text',
                                    placeholder="Ref",
                                    # A hint to the user of what can be entered in the control
                                    debounce=True,
                                    # Changes to input are sent to Dash server only on enter or losing focus
                                    # min=2015, max=2019, step=1,  # Ranges of numeric value. Step refers to increments
                                    minLength=0, maxLength=15,  # Ranges for character length inside input box
                                    autoComplete='off',
                                    disabled=False,  # Disable input box
                                    readOnly=False,  # Make input box read only
                                    required=True,  # Require user to insert something into input box
                                    size="6",  # Number of characters that will be visible inside box
                                    style={'font-family': "Franklin Gothic", 'textAlign': 'center', }

                                )
                            ], className="d-grid gap-2"),
                        ], className="d-grid gap-2"),
                    ]),
                    html.Br(),
                    dbc.Row([
                        dbc.Col([
                            badgeNumero
                        ], className="d-grid gap-2"),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='numero-geotube',
                                    type='number',
                                    placeholder="1, 2, 3, etc",
                                    # A hint to the user of what can be entered in the control
                                    debounce=True,
                                    # Changes to input are sent to Dash server only on enter or losing focus
                                    min=1, max=50, step=1,  # Ranges of numeric value. Step refers to increments
                                    minLength=0, maxLength=5,  # Ranges for character length inside input box
                                    autoComplete='off',
                                    disabled=False,  # Disable input box
                                    readOnly=False,  # Make input box read only
                                    required=True,  # Require user to insert something into input box
                                    size="6",  # Number of characters that will be visible inside box
                                    style={'font-family': "Franklin Gothic", 'textAlign': 'center', }

                                )
                            ], className="d-grid gap-2"),
                        ], className="d-grid gap-2"),
                        dbc.Col([
                            badgeCapacidad
                        ], className="d-grid gap-2"),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='capacidad-geotube',
                                    type='number',
                                    placeholder="m3",
                                    # A hint to the user of what can be entered in the control
                                    debounce=True,
                                    # Changes to input are sent to Dash server only on enter or losing focus
                                    min=1, max=1000, step=1,  # Ranges of numeric value. Step refers to increments
                                    minLength=0, maxLength=5,  # Ranges for character length inside input box
                                    autoComplete='off',
                                    disabled=False,  # Disable input box
                                    readOnly=False,  # Make input box read only
                                    required=True,  # Require user to insert something into input box
                                    size="6",  # Number of characters that will be visible inside box
                                    style={'font-family': "Franklin Gothic", 'textAlign': 'center', }

                                )
                            ], className="d-grid gap-2"),
                        ], className="d-grid gap-2"),
                    ]),
                    html.Br(),
                    dbc.Row([
                        dbc.Col([
                            badgeLargo
                        ], className="d-grid gap-2"),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='largo-geotube',
                                    type='number',
                                    placeholder="m. cm",
                                    # A hint to the user of what can be entered in the control
                                    debounce=True,
                                    # Changes to input are sent to Dash server only on enter or losing focus
                                    min=1, max=100, step=1,  # Ranges of numeric value. Step refers to increments
                                    minLength=0, maxLength=5,  # Ranges for character length inside input box
                                    autoComplete='off',
                                    disabled=False,  # Disable input box
                                    readOnly=False,  # Make input box read only
                                    required=True,  # Require user to insert something into input box
                                    size="6",  # Number of characters that will be visible inside box
                                    style={'font-family': "Franklin Gothic", 'textAlign': 'center', }

                                )
                            ], className="d-grid gap-2"),
                        ], className="d-grid gap-2"),
                        dbc.Col([
                            badgeAncho
                        ], className="d-grid gap-2"),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='ancho-geotube',
                                    type='number',
                                    placeholder="m. cm",
                                    # A hint to the user of what can be entered in the control
                                    debounce=True,
                                    # Changes to input are sent to Dash server only on enter or losing focus
                                    min=1, max=10, step=1,  # Ranges of numeric value. Step refers to increments
                                    minLength=0, maxLength=5,  # Ranges for character length inside input box
                                    autoComplete='off',
                                    disabled=False,  # Disable input box
                                    readOnly=False,  # Make input box read only
                                    required=True,  # Require user to insert something into input box
                                    size="6",  # Number of characters that will be visible inside box
                                    style={'font-family': "Franklin Gothic", 'textAlign': 'center', }

                                )
                            ], className="d-grid gap-2"),
                        ], className="d-grid gap-2"),
                    ]),
                    html.Br(),
                    dbc.Row([
                        dbc.Col([
                            dbc.Row(html.H5(['Puntos de Medición']),
                                    style={'color': '#082255', 'font-family': "Franklin Gothic"})
                        ], style={'textAlign': 'center'}, align='center'),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            badgeP1
                        ], className="d-grid gap-2"),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='P1',
                                    type='number',
                                    placeholder="m.cm",
                                    # A hint to the user of what can be entered in the control
                                    debounce=True,
                                    # Changes to input are sent to Dash server only on enter or losing focus
                                    min=0, max=3, step=0.01,  # Ranges of numeric value. Step refers to increments
                                    minLength=0, maxLength=5,  # Ranges for character length inside input box
                                    autoComplete='off',
                                    disabled=False,  # Disable input box
                                    readOnly=False,  # Make input box read only
                                    required=True,  # Require user to insert something into input box
                                    size="6",  # Number of characters that will be visible inside box
                                    style={'font-family': "Franklin Gothic", 'textAlign': 'center', }

                                )
                            ], className="d-grid gap-2"),
                        ], className="d-grid gap-2"),
                        dbc.Col([
                            badgeP7
                        ], className="d-grid gap-2"),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='P7',
                                    type='number',
                                    placeholder="m.cm",
                                    # A hint to the user of what can be entered in the control
                                    debounce=True,
                                    # Changes to input are sent to Dash server only on enter or losing focus
                                    min=0, max=3, step=0.01,  # Ranges of numeric value. Step refers to increments
                                    minLength=0, maxLength=5,  # Ranges for character length inside input box
                                    autoComplete='off',
                                    disabled=False,  # Disable input box
                                    readOnly=False,  # Make input box read only
                                    required=True,  # Require user to insert something into input box
                                    size="6",  # Number of characters that will be visible inside box
                                    style={'font-family': "Franklin Gothic", 'textAlign': 'center', }

                                )
                            ], className="d-grid gap-2"),
                        ], className="d-grid gap-2"),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            badgeP2
                        ], className="d-grid gap-2"),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='P2',
                                    type='number',
                                    placeholder="m.cm",
                                    # A hint to the user of what can be entered in the control
                                    debounce=True,
                                    # Changes to input are sent to Dash server only on enter or losing focus
                                    min=0, max=3, step=0.01,  # Ranges of numeric value. Step refers to increments
                                    minLength=0, maxLength=5,  # Ranges for character length inside input box
                                    autoComplete='off',
                                    disabled=False,  # Disable input box
                                    readOnly=False,  # Make input box read only
                                    required=True,  # Require user to insert something into input box
                                    size="6",  # Number of characters that will be visible inside box
                                    style={'font-family': "Franklin Gothic", 'textAlign': 'center', }

                                )
                            ], className="d-grid gap-2"),
                        ], className="d-grid gap-2"),
                        dbc.Col([
                            badgeP8
                        ], className="d-grid gap-2"),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='P8',
                                    type='number',
                                    placeholder="m.cm",
                                    # A hint to the user of what can be entered in the control
                                    debounce=True,
                                    # Changes to input are sent to Dash server only on enter or losing focus
                                    min=0, max=3, step=0.01,  # Ranges of numeric value. Step refers to increments
                                    minLength=0, maxLength=5,  # Ranges for character length inside input box
                                    autoComplete='off',
                                    disabled=False,  # Disable input box
                                    readOnly=False,  # Make input box read only
                                    required=True,  # Require user to insert something into input box
                                    size="6",  # Number of characters that will be visible inside box
                                    style={'font-family': "Franklin Gothic", 'textAlign': 'center', }

                                )
                            ], className="d-grid gap-2"),
                        ], className="d-grid gap-2"),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            badgeP3
                        ], className="d-grid gap-2"),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='P3',
                                    type='number',
                                    placeholder="m.cm",
                                    # A hint to the user of what can be entered in the control
                                    debounce=True,
                                    # Changes to input are sent to Dash server only on enter or losing focus
                                    min=0, max=3, step=0.01,  # Ranges of numeric value. Step refers to increments
                                    minLength=0, maxLength=5,  # Ranges for character length inside input box
                                    autoComplete='off',
                                    disabled=False,  # Disable input box
                                    readOnly=False,  # Make input box read only
                                    required=True,  # Require user to insert something into input box
                                    size="6",  # Number of characters that will be visible inside box
                                    style={'font-family': "Franklin Gothic", 'textAlign': 'center', }

                                )
                            ], className="d-grid gap-2"),
                        ], className="d-grid gap-2"),
                        dbc.Col([
                            badgeP9
                        ], className="d-grid gap-2"),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='P9',
                                    type='number',
                                    placeholder="m.cm",
                                    # A hint to the user of what can be entered in the control
                                    debounce=True,
                                    # Changes to input are sent to Dash server only on enter or losing focus
                                    min=0, max=3, step=0.01,  # Ranges of numeric value. Step refers to increments
                                    minLength=0, maxLength=5,  # Ranges for character length inside input box
                                    autoComplete='off',
                                    disabled=False,  # Disable input box
                                    readOnly=False,  # Make input box read only
                                    required=True,  # Require user to insert something into input box
                                    size="6",  # Number of characters that will be visible inside box
                                    style={'font-family': "Franklin Gothic", 'textAlign': 'center', }

                                )
                            ], className="d-grid gap-2"),
                        ], className="d-grid gap-2"),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            badgeP4
                        ], className="d-grid gap-2"),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='P4',
                                    type='number',
                                    placeholder="m.cm",
                                    # A hint to the user of what can be entered in the control
                                    debounce=True,
                                    # Changes to input are sent to Dash server only on enter or losing focus
                                    min=0, max=3, step=0.01,  # Ranges of numeric value. Step refers to increments
                                    minLength=0, maxLength=5,  # Ranges for character length inside input box
                                    autoComplete='off',
                                    disabled=False,  # Disable input box
                                    readOnly=False,  # Make input box read only
                                    required=True,  # Require user to insert something into input box
                                    size="6",  # Number of characters that will be visible inside box
                                    style={'font-family': "Franklin Gothic", 'textAlign': 'center', }

                                )
                            ], className="d-grid gap-2"),
                        ], className="d-grid gap-2"),
                        dbc.Col([
                            badgeP10
                        ], className="d-grid gap-2"),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='P10',
                                    type='number',
                                    placeholder="m.cm",
                                    # A hint to the user of what can be entered in the control
                                    debounce=True,
                                    # Changes to input are sent to Dash server only on enter or losing focus
                                    min=0, max=3, step=0.01,  # Ranges of numeric value. Step refers to increments
                                    minLength=0, maxLength=5,  # Ranges for character length inside input box
                                    autoComplete='off',
                                    disabled=False,  # Disable input box
                                    readOnly=False,  # Make input box read only
                                    required=True,  # Require user to insert something into input box
                                    size="6",  # Number of characters that will be visible inside box
                                    style={'font-family': "Franklin Gothic", 'textAlign': 'center', }

                                )
                            ], className="d-grid gap-2"),
                        ], className="d-grid gap-2"),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            badgeP5
                        ], className="d-grid gap-2"),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='P5',
                                    type='number',
                                    placeholder="m.cm",
                                    # A hint to the user of what can be entered in the control
                                    debounce=True,
                                    # Changes to input are sent to Dash server only on enter or losing focus
                                    min=0, max=3, step=0.01,  # Ranges of numeric value. Step refers to increments
                                    minLength=0, maxLength=5,  # Ranges for character length inside input box
                                    autoComplete='off',
                                    disabled=False,  # Disable input box
                                    readOnly=False,  # Make input box read only
                                    required=True,  # Require user to insert something into input box
                                    size="6",  # Number of characters that will be visible inside box
                                    style={'font-family': "Franklin Gothic", 'textAlign': 'center', }

                                )
                            ], className="d-grid gap-2"),
                        ], className="d-grid gap-2"),
                        dbc.Col([
                            badgeP11
                        ], className="d-grid gap-2"),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='P11',
                                    type='number',
                                    placeholder="m.cm",
                                    # A hint to the user of what can be entered in the control
                                    debounce=True,
                                    # Changes to input are sent to Dash server only on enter or losing focus
                                    min=0, max=3, step=0.01,  # Ranges of numeric value. Step refers to increments
                                    minLength=0, maxLength=5,  # Ranges for character length inside input box
                                    autoComplete='off',
                                    disabled=False,  # Disable input box
                                    readOnly=False,  # Make input box read only
                                    required=True,  # Require user to insert something into input box
                                    size="6",  # Number of characters that will be visible inside box
                                    style={'font-family': "Franklin Gothic", 'textAlign': 'center', }

                                )
                            ], className="d-grid gap-2"),
                        ], className="d-grid gap-2"),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            badgeP6
                        ], className="d-grid gap-2"),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='P6',
                                    type='number',
                                    placeholder="m.cm",
                                    # A hint to the user of what can be entered in the control
                                    debounce=True,
                                    # Changes to input are sent to Dash server only on enter or losing focus
                                    min=0, max=3, step=0.01,  # Ranges of numeric value. Step refers to increments
                                    minLength=0, maxLength=5,  # Ranges for character length inside input box
                                    autoComplete='off',
                                    disabled=False,  # Disable input box
                                    readOnly=False,  # Make input box read only
                                    required=True,  # Require user to insert something into input box
                                    size="6",  # Number of characters that will be visible inside box
                                    style={'font-family': "Franklin Gothic", 'textAlign': 'center', }

                                )
                            ], className="d-grid gap-2"),
                        ], className="d-grid gap-2"),
                        dbc.Col([
                            badgeP12
                        ], className="d-grid gap-2"),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='P12',
                                    type='number',
                                    placeholder="m.cm",
                                    # A hint to the user of what can be entered in the control
                                    debounce=True,
                                    # Changes to input are sent to Dash server only on enter or losing focus
                                    min=0, max=3, step=0.01,  # Ranges of numeric value. Step refers to increments
                                    minLength=0, maxLength=5,  # Ranges for character length inside input box
                                    autoComplete='off',
                                    disabled=False,  # Disable input box
                                    readOnly=False,  # Make input box read only
                                    required=True,  # Require user to insert something into input box
                                    size="6",  # Number of characters that will be visible inside box
                                    style={'font-family': "Franklin Gothic", 'textAlign': 'center', }

                                )
                            ], className="d-grid gap-2"),
                        ], className="d-grid gap-2"),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dcc.ConfirmDialogProvider(
                                children=html.Button('Enviar', ),
                                id='enviar-geotube',
                                message='¿Está seguro que desea enviar los datos de control de alturas de Geotube? '

                            ),
                        ], style={'font-family': "Franklin Gothic"}),
                    ]),

                ])
            ])
        ])
    ]),
        ], label='Control de Alturas de Geotube',),
    ]),


])
################################ Purgas ########################################################
@app.callback(
    Output(component_id='store-data-purgas', component_property='data'),

    Input('registro-purgas', 'n_clicks'),
    State('fecha-purgas', 'date'),
    State('hora-inicial-purgas', 'value'),
    State('hora-final-purgas', 'value'),
    State('altura-inicial-purgas', 'value'),
    State('altura-final-purgas', 'value'),
    State('fase-purgas', 'value'),
    State('store-data-purgas', component_property="data"),
    #State(component_id='datatable-interactivity-purgas', component_property='data'),
    Input('borrar-purgas', 'n_clicks'),
    Input('guardar-cambios-purgas', 'n_clicks'),
    State(component_id='datatable-interactivity-purgas', component_property='data'),

)

def formulario_purgas(value_clicks, value_fecha_purgas, value_hora_inicial_purgas, value_hora_final_purgas,
                      value_altura_inicial_purgas, value_altura_final_purgas, value_fase_purgas, rows,
                      value_clicks_borrar, value_clicks_guardar, tabla
                      ):
    rows = rows or []

    if value_clicks is None:
        # prevent the None callbacks is important with the store component.
        # you don't want to update the store for nothing.
        raise PreventUpdate

    if value_clicks_borrar is None:
        # prevent the None callbacks is important with the store component.
        # you don't want to update the store for nothing.
        raise PreventUpdate

    if value_clicks_guardar is None:
        # prevent the None callbacks is important with the store component.
        # you don't want to update the store for nothing.
        raise PreventUpdate

    changed_id = [p['prop_id'] for p in callback_context.triggered][0]

    # Cambiar variables a tipo string
    value_fecha_purgas = str(value_fecha_purgas)
    value_hora_inicial_purgas = str(value_hora_inicial_purgas)
    value_hora_final_purgas = str(value_hora_final_purgas)
    value_altura_inicial_purgas = str(value_altura_inicial_purgas)
    value_altura_final_purgas = str(value_altura_final_purgas)
    value_fase_purgas = str(value_fase_purgas)

    introTabla = [value_fecha_purgas, value_hora_inicial_purgas, value_hora_final_purgas, value_altura_inicial_purgas,
                  value_altura_final_purgas, value_fase_purgas]

    # Reorganiza los datos de la fecha y cambia - por /
    vecFecha = value_fecha_purgas.rsplit("-")
    dia = vecFecha[2]
    mes = vecFecha[1]
    año = vecFecha[0]

    value_fecha_purgas = dia + '/' + mes + '/' + año


    # Quita el primer cero de la fecha si este aparece & quita el cero de la izquierda de los meses
    if value_fecha_purgas.find('0', 0, 1) >= 0:
        value_fecha_purgas = value_fecha_purgas.replace('0', '', 1)

    value_fecha_purgas = value_fecha_purgas.replace('/0', '/', 1)


    introTabla = [{'name': value_fecha_purgas, 'id': 0}, {'name': value_hora_inicial_purgas, 'id': 1},
                  {'name': value_hora_final_purgas, 'id': 2},
                  {'name': str(value_altura_inicial_purgas), 'id': 3},
                  {'name': str(value_altura_final_purgas), 'id': 4},
                  {'name': str(value_fase_purgas), 'id': 5}]


    if 'registro-purgas' in changed_id:
        rows.append({c['id']: c['name'] for c in introTabla})
    elif 'borrar-purgas' in changed_id:
        data = pd.DataFrame().to_dict('records')  #empty dataframe
        rows = data
    elif 'guardar-cambios-purgas' in changed_id:
        rows = tabla
    else:
        rows = rows

    return rows


@app.callback(
    Output(component_id='datatable-interactivity-purgas', component_property='data'),

    Input('store-data-purgas', 'modified_timestamp'),
    State('store-data-purgas', 'data'),



)

def pegar_tabla_purgas(ts, data):

    return data


@app.callback(

    Output('Hola3', 'children'),

    Input('enviar-purgas', 'submit_n_clicks'),
    State('datatable-interactivity-purgas', 'data'),

)


def enviar_purgas(value_clicks_regis, df_purgas):

    retorno = ''

    fecha_0 = []
    horaInicial_0 = []
    horaFinal_0 = []
    altInicial = []
    altFinal = []
    fase = []

    for i in range(0, len(df_purgas)):
        lista = df_purgas[i]

        x0 = lista['0']
        x1 = lista['1']
        x2 = lista['2']
        x3 = lista['3']
        x4 = lista['4']
        x5 = lista['5']

        fecha_0.append(str(x0))
        horaInicial_0.append(str(x1))
        horaFinal_0.append(str(x2))
        altInicial.append(str(x3))
        altFinal.append(str(x4))
        fase.append(str(x5))

    altInicial = np.array(altInicial)
    altFinal = np.array(altFinal)

    # Calcula la diferencia entre tiempo final el inicial
    fase = np.array(fase)

    # Transformar datos de fecha
    fecha = []
    # Quita el primer cero de la fecha si este aparece & quita el cero de la izquierda de los meses
    for i in range(0,len(fecha_0)):
        if fecha_0[i].find('0', 0, 1) >= 0:
            fecha_0[i] = fecha_0[i].replace('0', '', 1)

        fecha_0[i] = fecha_0[i].replace('/0', '/', 1)
        fecha.append(fecha_0[i])
    fecha = np.array(fecha)

    # Transformar datos de hora inicial
    horaInicial = []
    for i in range(0, len(horaInicial_0)):
        horas = horaInicial_0[i]
        horasVec = horas.split(":")
        horas = int(horasVec[0])
        minutos = int(horasVec[1])
        if horas < 13:
            t = str(horas) + ':' + str(minutos) + ':' + '00 a. m.'
        else:
            horas = horas - 12
            t = str(horas) + ':' + str(minutos) + ':' + '00 p. m.'

        horaInicial.append(t)
    horaInicial = np.array(horaInicial)

    # Transformar datos de hora final
    horaFinal = []
    for i in range(0, len(horaFinal_0)):
        horas = horaFinal_0[i]
        horasVec = horas.split(":")
        horas = int(horasVec[0])
        minutos = int(horasVec[1])
        if horas < 13:
            t = str(horas) + ':' + str(minutos) + ':' + '00 a. m.'
        else:
            horas = horas - 12
            t = str(horas) + ':' + str(minutos) + ':' + '00 p. m.'

        horaFinal.append(t)
    horaFinal = np.array(horaFinal)

    # Convertir cada variable a dataframe
    fecha = pd.DataFrame(fecha, columns=['Fecha'])
    horaInicial = pd.DataFrame(horaInicial, columns=['Hora Inicial'])
    horaFinal = pd.DataFrame(horaFinal, columns=['Hora Final'])
    altInicial = pd.DataFrame(altInicial, columns=['Altura Inicial [m]'])
    altFinal = pd.DataFrame(altFinal, columns=['Altura Final [m]'])
    fase = pd.DataFrame(fase, columns=['Fase'])


    df_purgas_final = pd.concat([fecha, horaInicial, horaFinal, altInicial, altFinal, fase], axis=1)


    ####### Escritura de datos al Excel API

    SERVICE_ACCOUNT_FILE = 'keys-PTAP.json'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    creds = None
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    # The ID spreadsheet.
    SAMPLE_SPREADSHEET_ID = '1hT5gjZ8QES6GtPmnoxhmR3NG8xyzf0kFUfd7sunzV70'
    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    #value_clicks_regis = 0


    if value_clicks_regis > 0:
        # rango = "Combinado!A:M"
        rango = "Fase 5 MySQL!A:F"
        valores = df_purgas_final.values.tolist()
        valoresF = valores
        res = sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=rango,
                                   valueInputOption="USER_ENTERED", insertDataOption="OVERWRITE",
                                   body={"values": valoresF}).execute()


    #rows = []

    return retorno, #rows

################################ Lodos ########################################################

@app.callback(

    Output(component_id='store-data-lodos', component_property='data'),

    Input('registro-lodos', 'n_clicks'),
    State('fecha-lodos', 'date'),
    State('hora-inicial-lodos', 'value'),
    State('hora-final-lodos', 'value'),
    State('altura-inicial-lodos', 'value'),
    State('altura-final-lodos', 'value'),
    State('fase-lodos', 'value'),
    State('store-data-lodos', component_property="data"),
    #State(component_id='datatable-interactivity-lodos', component_property='data'),
    Input('borrar-lodos', 'n_clicks'),
    Input('guardar-cambios-lodos', 'n_clicks'),
    State(component_id='datatable-interactivity-lodos', component_property='data'),


)


def formulario_lodos(value_clicks, value_fecha_purgas, value_hora_inicial_purgas, value_hora_final_purgas,
                     value_altura_inicial_purgas, value_altura_final_purgas, value_fase_purgas,
                     rows, value_clicks_borrar, value_clicks_guardar, tabla):
    rows = rows or []

    if value_clicks is None:
        # prevent the None callbacks is important with the store component.
        # you don't want to update the store for nothing.
        raise PreventUpdate

    if value_clicks_borrar is None:
        # prevent the None callbacks is important with the store component.
        # you don't want to update the store for nothing.
        raise PreventUpdate

    if value_clicks_guardar is None:
        # prevent the None callbacks is important with the store component.
        # you don't want to update the store for nothing.
        raise PreventUpdate

    changed_id = [p['prop_id'] for p in callback_context.triggered][0]

    # Cambiar variables a tipo string
    value_fecha_purgas = str(value_fecha_purgas)
    value_hora_inicial_purgas = str(value_hora_inicial_purgas)
    value_hora_final_purgas = str(value_hora_final_purgas)
    value_altura_inicial_purgas = str(value_altura_inicial_purgas)
    value_altura_final_purgas = str(value_altura_final_purgas)
    value_fase_purgas = str(value_fase_purgas)

    # Reorganiza los datos de la fecha y cambia - por /
    vecFecha = value_fecha_purgas.rsplit("-")
    dia = vecFecha[2]
    mes = vecFecha[1]
    año = vecFecha[0]

    value_fecha_purgas = dia + '/' + mes + '/' + año

    introTabla = [value_fecha_purgas, value_hora_inicial_purgas, value_hora_final_purgas, value_altura_inicial_purgas,
                  value_altura_final_purgas, value_fase_purgas]

    # Quita el primer cero de la fecha si este aparece & quita el cero de la izquierda de los meses
    if value_fecha_purgas.find('0', 0, 1) >= 0:
        value_fecha_purgas = value_fecha_purgas.replace('0', '', 1)

    value_fecha_purgas = value_fecha_purgas.replace('/0', '/', 1)


    introTabla = [{'name': value_fecha_purgas, 'id': 0}, {'name': value_hora_inicial_purgas, 'id': 1},
                  {'name': value_hora_final_purgas, 'id': 2},
                  {'name': str(value_altura_inicial_purgas), 'id': 3},
                  {'name': str(value_altura_final_purgas), 'id': 4},
                  {'name': str(value_fase_purgas), 'id': 5}]


    if 'registro-lodos' in changed_id:
        rows.append({c['id']: c['name'] for c in introTabla})
    elif 'borrar-lodos' in changed_id:
        data = pd.DataFrame().to_dict('records')  #empty dataframe
        rows = data
    elif 'guardar-cambios-lodos' in changed_id:
        rows = tabla
    else:
        rows = rows

    return rows


@app.callback(
    Output(component_id='datatable-interactivity-lodos', component_property='data'),

    Input('store-data-lodos', 'modified_timestamp'),
    State('store-data-lodos', 'data')


)

def pegar_tabla_lodos(ts, data):
    if ts is None:
        raise PreventUpdate

    return data


@app.callback(

    Output('Hola4', 'children'),

    Input('enviar-lodos', 'submit_n_clicks'),
    State('datatable-interactivity-lodos', 'data'),

)


def enviar_lodos(value_clicks_regis, df_purgas):

    retorno = ''

    fecha_0 = []
    horaInicial_0 = []
    horaFinal_0 = []
    altInicial = []
    altFinal = []
    fase = []

    for i in range(0, len(df_purgas)):
        lista = df_purgas[i]

        x0 = lista['0']
        x1 = lista['1']
        x2 = lista['2']
        x3 = lista['3']
        x4 = lista['4']
        x5 = lista['5']

        fecha_0.append(str(x0))
        horaInicial_0.append(str(x1))
        horaFinal_0.append(str(x2))
        altInicial.append(str(x3))
        altFinal.append(str(x4))
        fase.append(str(x5))

    altInicial = np.array(altInicial)
    altFinal = np.array(altFinal)

    # Calcula la diferencia entre tiempo final el inicial
    horaInicial_t = list(map(lambda fecha: datetime.strptime(fecha, "%H:%M"), horaInicial_0))
    horaFinal_t = list(map(lambda fecha: datetime.strptime(fecha, "%H:%M"), horaFinal_0))
    tiempo = np.array(horaFinal_t) - np.array(horaInicial_t)
    tiempo = list(map(lambda t: int(t.total_seconds()/60), tiempo))
    fase = np.array(fase)


    # Transformar datos de fecha
    fecha = []
    # Quita el primer cero de la fecha si este aparece & quita el cero de la izquierda de los meses
    for i in range(0,len(fecha_0)):
        if fecha_0[i].find('0', 0, 1) >= 0:
            fecha_0[i] = fecha_0[i].replace('0', '', 1)

        fecha_0[i] = fecha_0[i].replace('/0', '/', 1)
        fecha.append(fecha_0[i])
    fecha = np.array(fecha)

    # Transformar datos de hora inicial
    horaInicial = []
    for i in range(0, len(horaInicial_0)):
        horas = horaInicial_0[i]
        horasVec = horas.split(":")
        horas = int(horasVec[0])
        minutos = int(horasVec[1])
        if horas < 13:
            t = str(horas) + ':' + str(minutos) + ':' + '00 a. m.'
        else:
            horas = horas - 12
            t = str(horas) + ':' + str(minutos) + ':' + '00 p. m.'

        horaInicial.append(t)
    horaInicial = np.array(horaInicial)

    # Transformar datos de hora final
    horaFinal = []
    for i in range(0, len(horaFinal_0)):
        horas = horaFinal_0[i]
        horasVec = horas.split(":")
        horas = int(horasVec[0])
        minutos = int(horasVec[1])
        if horas < 13:
            t = str(horas) + ':' + str(minutos) + ':' + '00 a. m.'
        else:
            horas = horas - 12
            t = str(horas) + ':' + str(minutos) + ':' + '00 p. m.'

        horaFinal.append(t)
    horaFinal = np.array(horaFinal)


    # Convertir cada variable a dataframe
    fecha = pd.DataFrame(fecha, columns=['Fecha'])
    horaInicial = pd.DataFrame(horaInicial, columns=['Hora Inicial'])
    horaFinal = pd.DataFrame(horaFinal, columns=['Hora Final'])
    altInicial = pd.DataFrame(altInicial, columns=['Altura Inicial [m]'])
    altFinal = pd.DataFrame(altFinal, columns=['Altura Final [m]'])
    fase = pd.DataFrame(fase, columns=['Fase'])

    df_purgas_final = pd.concat([fecha, horaInicial, horaFinal, altInicial, altFinal, fase], axis=1)


    ####### Escritura de datos al Excel API

    SERVICE_ACCOUNT_FILE = 'keys-PTAP.json'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    creds = None
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    # The ID spreadsheet.
    SAMPLE_SPREADSHEET_ID = '1hT5gjZ8QES6GtPmnoxhmR3NG8xyzf0kFUfd7sunzV70'
    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    #value_clicks_regis = 0


    if value_clicks_regis > 0:
        rango = "Fase 5 MySQL!J:O"
        # rango = "Combinado!A:M"
        valores = df_purgas_final.values.tolist()
        valoresF = valores
        res = sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=rango,
                                   valueInputOption="USER_ENTERED", insertDataOption="OVERWRITE",
                                   body={"values": valoresF}).execute()

    return retorno,


################################ Clarificado ########################################################
@app.callback(

    Output(component_id='store-data-clarificado', component_property='data'),

    Input('registro-clarificado', 'n_clicks'),
    State('fecha-clarificado', 'date'),
    State('hora-inicial-clarificado', 'value'),
    State('hora-final-clarificado', 'value'),
    State('Vi1', 'value'),
    State('Vi2', 'value'),
    State('Vi3', 'value'),
    State('Vf1', 'value'),
    State('Vf2', 'value'),
    State('Vf3', 'value'),
    State('pH', 'value'),
    State('color', 'value'),
    State('turbidez', 'value'),
    State('fase-clarificado', 'value'),
    State('store-data-clarificado', component_property="data"),
    #State(component_id='datatable-interactivity-clarificado', component_property='data'),
    Input('borrar-clarificado', 'n_clicks'),
    Input('guardar-cambios-clarificado', 'n_clicks'),
    State(component_id='datatable-interactivity-clarificado', component_property='data'),


)


def formulario_clarificado(value_clicks, value_fecha, value_hora_inicial, value_hora_final,
                     value_vi1, value_vi2, value_vi3, value_vf1, value_vf2, value_vf3,
                     value_pH, value_color, value_turbidez, value_fase,
                     rows, value_clicks_borrar, value_clicks_guardar, tabla):
    rows = rows or []

    if value_clicks is None:
        # prevent the None callbacks is important with the store component.
        # you don't want to update the store for nothing.
        raise PreventUpdate

    if value_clicks_borrar is None:
        # prevent the None callbacks is important with the store component.
        # you don't want to update the store for nothing.
        raise PreventUpdate

    if value_clicks_guardar is None:
        # prevent the None callbacks is important with the store component.
        # you don't want to update the store for nothing.
        raise PreventUpdate

    changed_id = [p['prop_id'] for p in callback_context.triggered][0]

    # Cambiar variables a tipo string
    value_fecha = str(value_fecha)
    value_hora_inicial = str(value_hora_inicial)
    value_hora_final = str(value_hora_final)
    value_fase = str(value_fase)
    value_vi1 = str(value_vi1)
    value_vi2 = str(value_vi2)
    value_vi3 = str(value_vi3)
    value_vf1 = str(value_vf1)
    value_vf2 = str(value_vf2)
    value_vf3 = str(value_vf3)
    value_pH = str(value_pH)
    value_color = str(value_color)
    value_turbidez = str(value_turbidez)

    # Reorganiza los datos de la fecha y cambia - por /
    vecFecha = value_fecha.rsplit("-")
    dia = vecFecha[2]
    mes = vecFecha[1]
    año = vecFecha[0]

    value_fecha = dia + '/' + mes + '/' + año

    vi = float(value_vi1)*10 + float(value_vi2) + float(value_vi3)*0.1
    vf = float(value_vf1)*10 + float(value_vf2) + float(value_vf3)*0.1

    vi = str(round(vi, 2))
    vf = str(round(vf, 2))


    # Quita el primer cero de la fecha si este aparece & quita el cero de la izquierda de los meses
    if value_fecha.find('0', 0, 1) >= 0:
        value_fecha = value_fecha.replace('0', '', 1)

    value_fecha = value_fecha.replace('/0', '/', 1)


    introTabla = [{'name': value_fecha, 'id': 0},
                  {'name': value_hora_inicial, 'id': 1},
                  {'name': value_hora_final, 'id': 2},
                  {'name': vi, 'id': 3},
                  {'name': vf, 'id': 4},
                  {'name': value_pH, 'id': 5},
                  {'name': value_color, 'id': 6},
                  {'name': value_turbidez, 'id': 7},
                  {'name': value_fase, 'id': 8}]


    if 'registro-clarificado' in changed_id:
        rows.append({c['id']: c['name'] for c in introTabla})
    elif 'borrar-clarificado' in changed_id:
        data = pd.DataFrame().to_dict('records')  #empty dataframe
        rows = data
    elif 'guardar-cambios-clarificado' in changed_id:
        rows = tabla
    else:
        rows = rows

    return rows

@app.callback(
    Output(component_id='datatable-interactivity-clarificado', component_property='data'),

    Input('store-data-clarificado', 'modified_timestamp'),
    State('store-data-clarificado', 'data')


)

def pegar_tabla_clarificado(ts, data):
    if ts is None:
        raise PreventUpdate

    return data



@app.callback(

    Output('Hola5', 'children'),

    Input('enviar-clarificado', 'submit_n_clicks'),
    State('datatable-interactivity-clarificado', 'data'),

)


def enviar_clarificado(value_clicks_regis, df):

    retorno = ''

    fecha_0 = []
    horaInicial_0 = []
    horaFinal_0 = []
    vi_0 = []
    vf_0 = []
    pH = []
    color = []
    turbidez = []
    fase = []


    for i in range(0, len(df)):
        lista = df[i]

        x0 = lista['0']
        x1 = lista['1']
        x2 = lista['2']
        x3 = lista['3']
        x4 = lista['4']
        x5 = lista['5']
        x6 = lista['6']
        x7 = lista['7']
        x8 = lista['8']

        fecha_0.append(str(x0))
        horaInicial_0.append(str(x1))
        horaFinal_0.append(str(x2))
        vi_0.append(str(x3))
        vf_0.append(str(x4))
        pH.append(str(x5))
        color.append(str(x6))
        turbidez.append(str(x7))
        fase.append(str(x8))


    vi = np.array(vi_0)
    vf = np.array(vf_0)

    # Calcula la diferencia entre tiempo final el inicial
    fase = np.array(fase)

    # Transformar datos de fecha
    fecha = []
    # Quita el primer cero de la fecha si este aparece & quita el cero de la izquierda de los meses
    for i in range(0, len(fecha_0)):
        if fecha_0[i].find('0', 0, 1) >= 0:
            fecha_0[i] = fecha_0[i].replace('0', '', 1)

        fecha_0[i] = fecha_0[i].replace('/0', '/', 1)
        fecha.append(fecha_0[i])
    fecha = np.array(fecha)

    # Transformar datos de hora inicial
    horaInicial = []
    for i in range(0, len(horaInicial_0)):
        horas = horaInicial_0[i]
        horasVec = horas.split(":")
        horas = int(horasVec[0])
        minutos = int(horasVec[1])
        if horas < 13:
            t = str(horas) + ':' + str(minutos) + ':' + '00 a. m.'
        else:
            horas = horas - 12
            t = str(horas) + ':' + str(minutos) + ':' + '00 p. m.'

        horaInicial.append(t)
    horaInicial = np.array(horaInicial)

    # Transformar datos de hora final
    horaFinal = []
    for i in range(0, len(horaFinal_0)):
        horas = horaFinal_0[i]
        horasVec = horas.split(":")
        horas = int(horasVec[0])
        minutos = int(horasVec[1])
        if horas < 13:
            t = str(horas) + ':' + str(minutos) + ':' + '00 a. m.'
        else:
            horas = horas - 12
            t = str(horas) + ':' + str(minutos) + ':' + '00 p. m.'

        horaFinal.append(t)
    horaFinal = np.array(horaFinal)

    # Calcula los m3 y galones recibidos
    vi_float = list(map(lambda x: float(x), vi))
    vf_float = list(map(lambda x: float(x), vf))

    # Convertir cada variable a dataframe
    fecha = pd.DataFrame(fecha, columns=['Fecha'])
    horaInicial = pd.DataFrame(horaInicial, columns=['Hora Inicial'])
    horaFinal = pd.DataFrame(horaFinal, columns=['Hora Final'])
    vi = pd.DataFrame(vi_float, columns=['Lectura Inicial [m]'])
    vf = pd.DataFrame(vf_float, columns=['Lectura Final [m]'])
    fase = pd.DataFrame(fase, columns=['Fase'])
    pH = pd.DataFrame(pH, columns=['pH'])
    color = pd.DataFrame(color, columns=['Color [Pt-Co]'])
    turbidez = pd.DataFrame(turbidez, columns=['Turbidez [NTU]'])

    df_final = pd.concat([fecha, horaInicial, horaFinal, vi, vf, turbidez, color,
                                 pH, fase], axis=1)



    ####### Escritura de datos al Excel API

    SERVICE_ACCOUNT_FILE = 'keys-PTAP.json'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    creds = None
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    # The ID spreadsheet.
    SAMPLE_SPREADSHEET_ID = '1hT5gjZ8QES6GtPmnoxhmR3NG8xyzf0kFUfd7sunzV70'
    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    #value_clicks_regis = 0


    if value_clicks_regis > 0:
        rango = "Fase 5 MySQL!S:AA"
        valores = df_final.values.tolist()
        valoresF = valores
        res = sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=rango,
                                   valueInputOption="USER_ENTERED", insertDataOption="OVERWRITE",
                                   body={"values": valoresF}).execute()
    return retorno,


################################ Geotube ########################################################

@app.callback(

    Output('Hola6', 'children'),

    Input('enviar-geotube', 'submit_n_clicks'),
    Input('fecha-geotube', 'date'),
    Input('fase-geotube', 'value'),
    Input('P1', 'value'),
    Input('P2', 'value'),
    Input('P3', 'value'),
    Input('P4', 'value'),
    Input('P5', 'value'),
    Input('P6', 'value'),
    Input('P7', 'value'),
    Input('P8', 'value'),
    Input('P9', 'value'),
    Input('P10', 'value'),
    Input('P11', 'value'),
    Input('P12', 'value'),
    Input('capacidad-geotube', 'value'),
    Input('numero-geotube', 'value'),
    Input('largo-geotube', 'value'),
    Input('ancho-geotube', 'value'),
    Input('hora-GT', 'value'),
    Input('referencia-GT', 'value'),


)

def formulario_geotube_y_enviar(value_clicks, value_fecha, value_fase, value_P1,  value_P2,  value_P3,
                                value_P4,  value_P5,  value_P6,  value_P7,  value_P8,  value_P9,  value_P10,
                                value_P11,  value_P12, value_capacidad, value_numero, value_largo
                                , value_ancho, value_hora, value_referencia):
    retorno = ''



    # Cambiar variables a tipo string
    value_fecha = str(value_fecha)
    value_fase = str(value_fase)
    P1 = str(value_P1)
    P2 = str(value_P2)
    P3 = str(value_P3)
    P4 = str(value_P4)
    P5 = str(value_P5)
    P6 = str(value_P6)
    P7 = str(value_P7)
    P8 = str(value_P8)
    P9 = str(value_P9)
    P10 = str(value_P10)
    P11 = str(value_P11)
    P12 = str(value_P12)
    value_capacidad = str(value_capacidad)
    value_numero = str(value_numero)
    value_largo = str(value_largo)
    value_ancho = str(value_ancho)
    value_referencia = str(value_referencia)


    # Reorganiza los datos de la fecha y cambia - por /
    vecFecha = value_fecha.rsplit("-")
    dia = vecFecha[2]
    mes = vecFecha[1]
    año = vecFecha[0]

    value_fecha = dia + '/' + mes + '/' + año


    # Quita el primer cero de la fecha si este aparece & quita el cero de la izquierda de los meses
    if value_fecha.find('0', 0, 1) >= 0:
        value_fecha = value_fecha.replace('0', '', 1)

    value_fecha = value_fecha.replace('/0', '/', 1)

    # Calcula el promedio de alturas de geotube
    promedio_altura = (float(P1) + float(P2) + float(P3) + float(P4) + float(P5) + float(P6) +
                      float(P6) + float(P7) + float(P8) + float(P9) + float(P10) + float(P11) + float(P12)) / 12

    # Calcula volumen del Geotube
    volumen = promedio_altura * float(value_ancho) * float(value_largo)

    # Calcula peso del Geotube
    peso = volumen * 1.23

    # Calcula uso del Geotube
    uso = volumen / float(value_capacidad)

    # Calcula la hora
    if value_hora == True:
        hora = '8:00:00'
    else:
        hora = '16:00:00'


    # Convertir en array
    numero = value_numero
    fecha = value_fecha
    volumen = volumen
    uso = uso
    peso = peso
    capacidad = value_capacidad
    fase = value_fase
    referencia = value_referencia
    largo = value_largo
    ancho = value_ancho

    df = [numero, fecha, volumen, uso, peso, capacidad, fase]
    df = [fase, numero, largo, ancho, fecha, hora, promedio_altura, capacidad, referencia]

    print(df)
    print(type(df))
    print(value_clicks)


    ####### Escritura de datos al Excel API

    SERVICE_ACCOUNT_FILE = 'keys-PTAP.json'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    creds = None
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    # The ID spreadsheet.
    SAMPLE_SPREADSHEET_ID = '1hT5gjZ8QES6GtPmnoxhmR3NG8xyzf0kFUfd7sunzV70'
    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    #value_clicks_regis = 0


    if value_clicks > 0:
        print('Botón oprimido')
        rango = "Fase 5 MySQL!AE:AM"
        #valores = df_final.values.tolist()
        valoresF = [df]
        res = sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=rango,
                                   valueInputOption="USER_ENTERED", insertDataOption="OVERWRITE",
                                   body={"values": valoresF}).execute()


    return retorno


if __name__ == '__main__':
    app.run_server()


