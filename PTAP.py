import dash
from dash import html
from dash import dcc
import plotly.express as px
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State
import plotly.graph_objects as go
from datetime import datetime
import dash_daq as daq
# Importar hojas de trabajo de google drive     https://bit.ly/3uQfOvs
from googleapiclient.discovery import build
from google.oauth2 import service_account
from datetime import datetime
import time
import mysql.connector

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SANDSTONE])
app.css.append_css({'external_url': '/static/reset.css'})
app.server.static_folder = 'static'
server = app.server

app.layout = dbc.Container([
    dcc.Store(id='store-data-purgas', storage_type='memory'),  # 'local' or 'session'
    dcc.Store(id='store-data-lodos', storage_type='memory'),  # 'local' or 'session'
    dcc.Store(id='store-data-clarificado', storage_type='memory'),  # 'local' or 'session'
    dcc.Store(id='store-data-geotube', storage_type='memory'),  # 'local' or 'session'
    dcc.Interval(
        id='my_interval',
        disabled=False,
        interval=1 * 1000,
        n_intervals=0,
        max_intervals=1
    ),
    dbc.Row([
        dbc.Col([dbc.CardImg(
            src="/assets/Logo.jpg",

            style={"width": "6rem",
                   'text-align': 'right'},
        ),

        ], align='right', width=2),
        dbc.Col(html.H5(
            '"Cualquier tecnología lo suficientemente avanzada, es indistinguible de la magia." - Arthur C. Clarke '),
                style={'color': "green", 'font-family': "Franklin Gothic"}, width=7),
        #dbc.Col([dbc.CardImg(
        #    src="/assets/Logo-Ecopetrol.png",

        #    style={
        #        "width": "16rem",
        #        'text-align': 'left'},
        #),

        #], align='left', width=3),
    ]),
    dbc.Row([
        dbc.Col(html.H1(
            "Resumen del Sistema de Deshidratación de Lodos - Clarificador CL-800C - Refinería de Barrancabermeja",
            style={'textAlign': 'center', 'color': '#082255', 'font-family': "Franklin Gothic"}), width=12, )
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Accordion([
                dbc.AccordionItem([
                    html.H5([
                                'El siguiente tablero interactivo presenta los resultados obtenidos por Geosoluciones SAS al operar el sistema de deshidratación de lodos mediante la tecnología de Geotube para tratar el agua lodosa proveniente de las purgas del clarificador CL-800C del departamento de Servicios Industriales Refinería, esto con el fin de reducir la cantidad de solidos suspendidos totales (SST) y sólidos sedimentables que actualmente se envían como vertimiento al Río Magdalena desde las purgas de los clarificadores de las unidades U800/U850, garantizando con lo anterior, el cumplimiento de la Resolución 631 de 2015 en el vertimiento al Río en cuanto a los parámetros descritos ya sea con el valor máximo permisible o mediante el respectivo balance de materia.'])

                ], title="Introducción"),
            ], start_collapsed=True, style={'textAlign': 'left', 'color': '#082255', 'font-family': "Franklin Gothic"}),

        ], style={'color': '#082255', 'font-family': "Franklin Gothic"}),
    ]),
    dbc.Row([
        dbc.Col([
            # html.H5('Última actualización: ' + str(ultAct), style={'textAlign': 'right'})
        ])
    ]),
    dbc.Row([
        dbc.Tabs([
            dbc.Tab([
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Row(html.H2(['Resumen Diario']),
                                                style={'color': '#082255', 'font-family': "Franklin Gothic"})
                                    ])
                                ]),
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Button(
                                            "Seleccionar Unidades:",
                                            id="selec-uni-dia-target",
                                            color="info",
                                            style={'font-family': "Franklin Gothic"},
                                            # className="me-1",
                                            n_clicks=0,
                                        ),
                                        dbc.Popover(
                                            "Son las unidades de volumen que son seleccionadas por el usuario. Se tiene como opciones galones y metros cúbicos.",
                                            target="selec-uni-dia-target",
                                            body=True,
                                            trigger="hover",
                                            style={'font-family': "Franklin Gothic"}
                                        ),

                                    ], width=2, align='center', className="d-grid gap-2"),
                                    dbc.Col([
                                        dbc.RadioItems(
                                            options=[
                                                {"label": "Galones", "value": True},
                                                {"label": "Metros cúbicos", "value": False},
                                            ],
                                            value=True,
                                            id="unidades-input",
                                            style={'font-family': "Franklin Gothic"}
                                        ),
                                    ], xs=3, sm=3, md=3, lg=2, xl=2, align='center'),
                                    dbc.Col([
                                        dbc.Button(
                                            "Seleccionar Día:",
                                            id="selec-dia-dia-target",
                                            color="info",
                                            style={'font-family': "Franklin Gothic"},
                                            className="me-1",
                                            n_clicks=0,
                                        ),
                                        dbc.Popover(
                                            "Es el día introducido por el usuario para conocer el resumen de la operación de agua captada, retornada y lodos confinados para el día seleccionado. Formato DD/MM/AAAA.",
                                            target="selec-dia-dia-target",
                                            body=True,
                                            trigger="hover",
                                            style={'font-family': "Franklin Gothic"}
                                        ),
                                    ], width=2, align='center', className="d-grid gap-2"),

                                    dbc.Col(
                                        dbc.Spinner(children=[dcc.Dropdown(id='Dia', style={'font-family': "Franklin Gothic"})], size="lg",
                                                    color="primary", type="border", fullscreen=True, ),
                                                                                xs=3, sm=3, md=3, lg=2, xl=2, align='center'),

                                ]),

                                dbc.Row([
                                    dbc.Col([
                                        dbc.Button(
                                            "Purgas Captadas:",
                                            id="purg-capt-dia-target",
                                            color="secondary",
                                            style={'font-family': "Franklin Gothic"},
                                            # className="me-1",
                                            n_clicks=0,
                                        ),
                                        dbc.Popover(
                                            "Es la cantidad de purgas enviadas del clarificador CL-800C a la caja de lodos (captación) en un día.",
                                            target="purg-capt-dia-target",
                                            body=True,
                                            trigger="hover",
                                            style={'font-family': "Franklin Gothic"}
                                        ),

                                    ], width=2, align='center', className="d-grid gap-2"),

                                    dbc.Col([
                                        dbc.Spinner(children=[daq.LEDDisplay(id='LED-purgcapt-dia', color='brown', size=14, value=0, )], size="lg",
                                                    color="primary", type="border", fullscreen=True, )],
                                        # spinner_style={"width": "10rem", "height": "10rem"}),
                                        # spinnerClassName="spinner"),
                                        # dcc.Loading(children=[dcc.Graph(id="loading-output")], color="#119DFF", type="dot", fullscreen=True,),

                                        xs=3, sm=3, md=3, lg=2, xl=2, align="center"),


                                    dbc.Col([
                                        dbc.Button(
                                            "pH:",
                                            id="pH-dia-target",
                                            color="success",
                                            className="me-1",
                                            style={'font-family': "Franklin Gothic"},
                                            # size="lg",
                                            n_clicks=0,
                                        ),
                                        dbc.Popover(
                                            "Es el promedio de pH de agua retornada clarificada al clarificador CL-800C después de haber sido tratada sistema de deshidratación de lodos en un día.",
                                            target="pH-dia-target",
                                            body=True,
                                            trigger="hover",
                                            style={'font-family': "Franklin Gothic"}
                                        ),

                                    ], width=2, align='center', className="d-grid gap-2"),
                                    dbc.Col([
                                        daq.LEDDisplay(id='LED-pH-dia', color='green', size=14, value=0, )
                                    ], width=1, align="center"),
                                    dbc.Col([
                                        html.Div("")
                                    ], xs=2, sm=2, md=2, lg=1, xl=1, style={'textAlign': 'left'}, align='end'),
                                    dbc.Col([
                                        dbc.Row([daq.GraduatedBar(
                                            id='barra-pH-dia',
                                            color={
                                                "ranges": {"green": [0, 8.8], "yellow": [8.8, 9.4], "red": [9.4, 10]}},
                                            showCurrentValue=False,
                                            step=0.2,
                                            value=0
                                        )]),
                                    ], width=2)
                                ]),
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Button(
                                            "Bombeos Retornados:",
                                            id="bomb-ret-dia-target",
                                            color="primary",
                                            style={'font-family': "Franklin Gothic"},
                                            className="me-1",
                                            n_clicks=0,
                                        ),
                                        dbc.Popover(
                                            "Es el número de bombeos de agua clarificada retornada al clarificador CL-800C después de haber sido tratada por el sistema de deshidratación de lodos en un día.",
                                            target="bomb-ret-dia-target",
                                            body=True,
                                            trigger="hover",
                                            style={'font-family': "Franklin Gothic"}
                                        ),

                                    ], width=2, align='center', className="d-grid gap-2"),
                                    dbc.Col([
                                        daq.LEDDisplay(id='LED-bomb-dia', color='blue', size=14, value=0, )
                                    ], xs=3, sm=3, md=3, lg=2, xl=2, ),
                                    dbc.Col([
                                        dbc.Button(
                                            "Turbidez:",
                                            id="turb-dia-target",
                                            color="success",
                                            style={'font-family': "Franklin Gothic"},
                                            className="me-1",
                                            n_clicks=0,
                                        ),
                                        dbc.Popover(
                                            "Es el promedio de turbidez de agua retornada clarificada al clarificador CL-800C después de haber sido tratada con la tecnología Geotube en un día.",
                                            target="turb-dia-target",
                                            body=True,
                                            trigger="hover",
                                            style={'font-family': "Franklin Gothic"}
                                        ),

                                    ], width=2, align='center', className="d-grid gap-2"),
                                    dbc.Col([
                                        daq.LEDDisplay(id='LED-turb-dia', color='green', size=14, value=0, )
                                    ], width=1),
                                    dbc.Col([
                                        html.Div("NTU")
                                    ], xs=2, sm=2, md=2, lg=1, xl=1,
                                        style={'textAlign': 'center', 'font-family': "Franklin Gothic"},
                                        align='center'),
                                    dbc.Col([
                                        dbc.Row([daq.GraduatedBar(
                                            id='barra-turb-dia',
                                            color={"ranges": {"green": [0, 4], "yellow": [4, 8], "red": [8, 10]}},
                                            showCurrentValue=False,
                                            step=0.2,
                                            value=0
                                        )]),
                                    ], width=2)
                                ]),
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Button(
                                            "Volumen Captado:",
                                            id="vol-capt-dia-target",
                                            color="secondary",
                                            className="me-1",
                                            n_clicks=0,
                                            style={'font-family': "Franklin Gothic"},
                                        ),
                                        dbc.Popover(
                                            "Es la sumatoria de la cantidad de agua lodosa bombeada de la caja de lodos al sistema de deshidratación de lodos en un día.",
                                            target="vol-capt-dia-target",
                                            body=True,
                                            trigger="hover",
                                            style={'font-family': "Franklin Gothic"}
                                        ),

                                    ], width=2, align='center', className="d-grid gap-2"),
                                    dbc.Col([
                                        daq.LEDDisplay(id='LED-volcapt-dia', color='brown', size=14, value=0, )
                                    ], width=1),
                                    dbc.Col([
                                        html.Div(id='unidades-volcapt-dia')
                                    ], xs=2, sm=2, md=2, lg=1, xl=1,
                                        style={'textAlign': 'center', 'font-family': "Franklin Gothic"},
                                        align='center'),
                                    dbc.Col([
                                        dbc.Button(
                                            "Color:",
                                            id="color-dia-target",
                                            color="success",
                                            className="me-1",
                                            n_clicks=0,
                                            style={'font-family': "Franklin Gothic"},
                                        ),
                                        dbc.Popover(
                                            "Es el promedio de color de agua retornada clarificada al clarificador CL-800C después de haber sido tratada con la tecnología Geotube en un día.",
                                            target="color-dia-target",
                                            body=True,
                                            trigger="hover",
                                            style={'font-family': "Franklin Gothic"}
                                        ),

                                    ], width=2, align='center', className="d-grid gap-2"),
                                    dbc.Col([
                                        daq.LEDDisplay(id='LED-color-dia', color='green', size=14, value=0, )
                                    ], width=1),
                                    dbc.Col([
                                        html.Div("Pt-Co")
                                    ], xs=2, sm=2, md=2, lg=1, xl=1,
                                        style={'textAlign': 'center', 'font-family': "Franklin Gothic"},
                                        align='center'),
                                    dbc.Col([
                                        dbc.Row([daq.GraduatedBar(
                                            id='barra-color-dia',
                                            color={
                                                "ranges": {"green": [0, 3.3], "yellow": [3.3, 6.6], "red": [6.6, 10]}},
                                            showCurrentValue=False,
                                            step=0.2,
                                            value=0
                                        )]),
                                    ], width=2)
                                ]),
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Button(
                                            "Volumen Retornado:",
                                            id="vol-ret-dia-target",
                                            color="primary",
                                            className="me-1",
                                            n_clicks=0,
                                            style={'font-family': "Franklin Gothic"},
                                        ),
                                        dbc.Popover(
                                            "Es la sumatoria de la cantidad de agua clarificada retornada al clarificador CL-800C después de haber sido tratada por el sistema de deshidratación de lodos en un día.",
                                            target="vol-ret-dia-target",
                                            body=True,
                                            trigger="hover",
                                            style={'font-family': "Franklin Gothic"}
                                        ),

                                    ], width=2, align='center', className="d-grid gap-2"),
                                    dbc.Col([
                                        daq.LEDDisplay(id='LED-volret-dia', color='blue', size=14, value=0, )
                                    ], width=1),
                                    dbc.Col([
                                        html.Div(id='unidades-volret-dia')
                                    ], xs=2, sm=2, md=2, lg=1, xl=1,
                                        style={'textAlign': 'center', 'font-family': "Franklin Gothic"},
                                        align='center'),
                                    dbc.Col([
                                        dbc.Button(
                                            "Agua Tratada:",
                                            id="agua-trat-dia-target",
                                            color="primary",
                                            className="me-1",
                                            n_clicks=0,
                                            style={'font-family': "Franklin Gothic"},
                                        ),
                                        dbc.Popover(
                                            "Es el cociente entre el agua clarificada retornada al clarificador CL-800C y el volumen captado de agua lodosa en un día. En algunos casos el porcentaje de agua tratada es mayor a 100 debido a captaciones de agua fuera del sistema (tales como aguas lluvia), en dichos casos se acota el porcentaje de agua tratada a 100.",
                                            target="agua-trat-dia-target",
                                            body=True,
                                            trigger="hover",
                                            style={'font-family': "Franklin Gothic"}
                                        ),

                                    ], width=2, align='center', className="d-grid gap-2"),
                                    dbc.Col([
                                        daq.LEDDisplay(id='LED-aguatrat-dia', color='blue', size=14, value=0, )
                                    ], width=1),
                                    dbc.Col([
                                        html.Div("%")
                                    ], xs=2, sm=2, md=2, lg=1, xl=1,
                                        style={'textAlign': 'left', 'font-family': "Franklin Gothic"}, align='center'),
                                    dbc.Col([
                                        dbc.Row([daq.GraduatedBar(
                                            id='barra-aguatrat-dia',
                                            color={
                                                "ranges": {"red": [0, 3.3], "yellow": [3.3, 6.6], "green": [6.6, 10]}},
                                            showCurrentValue=False,
                                            step=0.2,
                                            value=0,

                                        )]),
                                    ], width=2)
                                ]),
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Button(
                                            "Lodos Confinados:",
                                            id="lodos-conf-dia-target",
                                            color="secondary",
                                            className="me-1",
                                            n_clicks=0,
                                            style={'font-family': "Franklin Gothic"},
                                        ),
                                        dbc.Popover(
                                            "Es el peso de lodos confinados en un día a una humedad de aproximadamente 60%.",
                                            target="lodos-conf-dia-target",
                                            body=True,
                                            trigger="hover",
                                            style={'font-family': "Franklin Gothic"},
                                        ),

                                    ], width=2, align='center', className="d-grid gap-2"),
                                    dbc.Col([
                                        daq.LEDDisplay(id='LED-lodos-confinados-dia', color='brown', size=14, value=0)
                                    ], width=1),
                                    dbc.Col([html.Div("Ton")], xs=2, sm=2, md=2, lg=1, xl=1,
                                            style={'textAlign': 'left', 'font-family': "Franklin Gothic"},
                                            align='center'),
                                ]),
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Accordion([
                                            dbc.AccordionItem([

                                                html.H5([
                                                            'Barra de pH: es el indicador de pH acordado en las Especificaciones Técnicas para la Deshidratación de Lodos de Clarificación con la Tecnología de Geotubes (Geotube). Color verde es pH excelente (6-7.5), color amarillo es pH aceptable (7.5-8.0), color rojo es alerta de pH (8.0-8.5).']),

                                                html.H5([
                                                            'Barra de Turbidez: es el indicador de turbidez acordado en las Especificaciones Técnicas para la Deshidratación de Lodos de Clarificación con la Tecnología de Geotubes (Geotube). Color verde es turbidez excelente (0-10 NTU), color amarillo es turbidez aceptable (10-20 NTU), color rojo es alerta de turbidez (20-25 NTU).']),

                                                html.H5([
                                                            'Barra de color: es el indicador de color. Color de barra verde es color bajo (0-46 Pt-Co), color de barra amarillo es color medio (46-92 Pt-Co), color de barra rojo es color alto (92-140 Pt-Co).']),

                                                html.H5([
                                                            'Barra de agua tratada: es el indicador de agua tratada. Color de barra rojo es porcentaje de agua tratada bajo (0-33%), color de barra amarillo es porcentaje de agua tratada medio (33-66% ), color de barra verde es porcentaje de agua tratada alto (66-100%).']),

                                            ], title="Descripción de Íconos"),
                                        ], start_collapsed=True,
                                            style={'color': '#082255', 'font-family': "Franklin Gothic"}),

                                    ], style={'color': '#082255', 'font-family': "Franklin Gothic"}),
                                ]),
                            ])
                        ]),

                    ]),

                ]),
            ], label="Resumen Diario", label_style={'color': '#082255', 'font-family': "Franklin Gothic"}),
            dbc.Tab([
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Row(html.H2(['Resumen Mensual']),
                                                style={'color': '#082255', 'font-family': "Franklin Gothic"})
                                    ])
                                ]),
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Button(
                                            "Seleccionar Unidades:",
                                            id="selec-uni-mes-target",
                                            color="info",
                                            className="me-1",
                                            n_clicks=0,
                                            style={'font-family': "Franklin Gothic"},
                                        ),
                                        dbc.Popover(
                                            "Son las unidades de volumen que son seleccionadas por el usuario. Se tiene como opciones galones y metros cúbicos.",
                                            target="selec-uni-mes-target",
                                            body=True,
                                            trigger="hover",
                                            style={'font-family': "Franklin Gothic"}
                                        ),

                                    ], width=2, align='center', className="d-grid gap-2"),
                                    dbc.Col([
                                        dbc.RadioItems(
                                            options=[
                                                {"label": "Galones", "value": True},
                                                {"label": "Metros cúbicos", "value": False},
                                            ],
                                            value=True,
                                            id="unidades-mes-input", style={'font-family': "Franklin Gothic"}
                                        ),
                                    ], xs=3, sm=3, md=3, lg=2, xl=2, ),
                                    dbc.Col([
                                        dbc.Button(
                                            "Seleccionar Año:",
                                            id="selec-ano-mes-target",
                                            color="info",
                                            className="me-1",
                                            n_clicks=0,
                                            style={'font-family': "Franklin Gothic"},
                                        ),
                                        dbc.Popover(
                                            "Es el año introducido por el usuario para conocer el resumen de la operación para el año y mes seleccionado.",
                                            target="selec-ano-mes-target",
                                            body=True,
                                            trigger="hover",
                                            style={'font-family': "Franklin Gothic"}
                                        ),

                                    ], width=2, align='center', className="d-grid gap-2"),
                                    dbc.Col([
                                        dcc.Dropdown(id='Ano',
                                                     options=[],
                                                     #value=2021,
                                                     style={'font-family': "Franklin Gothic"}
                                                     )
                                    ], width=2, align='center'),
                                    dbc.Col([
                                        dbc.Button(
                                            "Seleccionar Mes:",
                                            id="selec-mes-mes-target",
                                            color="info",
                                            className="me-1",
                                            n_clicks=0,
                                            style={'font-family': "Franklin Gothic"},
                                        ),
                                        dbc.Popover(
                                            "Es el mes introducido por el usuario para conocer el resumen de la operación para el año y mes seleccionado.",
                                            target="selec-mes-mes-target",
                                            body=True,
                                            trigger="hover",
                                            style={'font-family': "Franklin Gothic"}
                                        ),

                                    ], width=2, align='center', className="d-grid gap-2"),
                                    dbc.Col([
                                        dcc.Dropdown(id='meses',  # PONER DROPDOWN DINÁMICO DEPENDIENDO DE LAS FECHAS
                                                     options=[],
                                                     #value=5
                                                     )
                                    ], width=1, style={'font-family': "Franklin Gothic"}, align='center'),
                                ]),
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Button(
                                            "Purgas Captadas:",
                                            id="purg-capt-mes-target",
                                            color="secondary",
                                            className="me-1",
                                            n_clicks=0,
                                            style={'font-family': "Franklin Gothic"},
                                        ),
                                        dbc.Popover(
                                            "Es la cantidad de purgas enviadas del clarificador CL-800C a la caja de lodos (captación) en un mes.",
                                            target="purg-capt-mes-target",
                                            body=True,
                                            trigger="hover",
                                            style={'font-family': "Franklin Gothic"}
                                        ),

                                    ], width=2, align='center', className="d-grid gap-2"),
                                    dbc.Col([
                                        daq.LEDDisplay(id='LED-purgcapt-mes', color='brown', size=14, value=0)
                                    ], xs=3, sm=3, md=3, lg=2, xl=2, align="center"),
                                    dbc.Col([
                                        dbc.Button(
                                            "pH:",
                                            id="pH-mes-target",
                                            color="success",
                                            className="me-1",
                                            n_clicks=0,
                                            style={'font-family': "Franklin Gothic"},
                                        ),
                                        dbc.Popover(
                                            "Es el promedio de pH de agua retornada clarificada al clarificador CL-800C después de haber sido tratada por el sistema de deshidratación de lodos en un mes.",
                                            target="pH-mes-target",
                                            body=True,
                                            trigger="hover",
                                            style={'font-family': "Franklin Gothic"}
                                        ),

                                    ], width=2, align='center', className="d-grid gap-2"),
                                    dbc.Col([
                                        daq.LEDDisplay(id='LED-pH-mes', color='green', size=14, value=0)
                                    ], width=1, align="center"),
                                    dbc.Col([
                                        html.Div("")
                                    ], xs=2, sm=2, md=2, lg=1, xl=1, style={'textAlign': 'left'}, align='end'),
                                    dbc.Col([
                                        dbc.Row([daq.GraduatedBar(
                                            id='barra-pH-mes',
                                            color={
                                                "ranges": {"green": [0, 8.8], "yellow": [8.8, 9.4], "red": [9.4, 10]}},
                                            showCurrentValue=False,
                                            step=0.2,
                                            value=0
                                        )]),
                                    ], width=2)
                                ]),
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Button(
                                            "Bombeos Retornados:",
                                            id="bomb-ret-mes-target",
                                            color="primary",
                                            className="me-1",
                                            n_clicks=0,
                                            style={'font-family': "Franklin Gothic"},
                                        ),
                                        dbc.Popover(
                                            "Es el número de bombeos de agua clarificada retornada al clarificador CL-800C después de haber sido tratada por el sistema de deshidratación de lodos en un mes.",
                                            target="bomb-ret-mes-target",
                                            body=True,
                                            trigger="hover",
                                            style={'font-family': "Franklin Gothic"}
                                        ),

                                    ], width=2, align='center', className="d-grid gap-2"),
                                    dbc.Col([
                                        daq.LEDDisplay(id='LED-bomb-mes', color='blue', size=14, value=0)
                                    ], xs=3, sm=3, md=3, lg=2, xl=2, ),
                                    dbc.Col([
                                        dbc.Button(
                                            "Turbidez:",
                                            id="turb-mes-target",
                                            color="success",
                                            className="me-1",
                                            n_clicks=0,
                                            style={'font-family': "Franklin Gothic"},
                                        ),
                                        dbc.Popover(
                                            "Es el promedio de turbidez de agua retornada clarificada al clarificador CL-800C después de haber sido tratada por el sistema de deshidratación de lodos en un mes.",
                                            target="turb-mes-target",
                                            body=True,
                                            trigger="hover",
                                            style={'font-family': "Franklin Gothic"}
                                        ),

                                    ], width=2, align='center', className="d-grid gap-2"),
                                    dbc.Col([
                                        daq.LEDDisplay(id='LED-turb-mes', color='green', size=14, value=0)
                                    ], width=1),
                                    dbc.Col([
                                        html.Div("NTU")
                                    ], xs=2, sm=2, md=2, lg=1, xl=1,
                                        style={'textAlign': 'center', 'font-family': "Franklin Gothic"},
                                        align='center'),
                                    dbc.Col([
                                        dbc.Row([daq.GraduatedBar(
                                            id='barra-turb-mes',
                                            color={"ranges": {"green": [0, 4], "yellow": [4, 8], "red": [8, 10]}},
                                            showCurrentValue=False,
                                            step=0.2,
                                            value=0
                                        )]),
                                    ], width=2)

                                ]),
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Button(
                                            "Volumen Captado:",
                                            id="vol-capt-mes-target",
                                            color="secondary",
                                            className="me-1",
                                            n_clicks=0,
                                            style={'font-family': "Franklin Gothic"},
                                        ),
                                        dbc.Popover(
                                            "Es la sumatoria de la cantidad de agua lodosa bombeada de la caja de lodos al sistema de deshidratación de lodos en un mes.",
                                            target="vol-capt-mes-target",
                                            body=True,
                                            trigger="hover",
                                            style={'font-family': "Franklin Gothic"}
                                        ),

                                    ], width=2, align='center', className="d-grid gap-2"),
                                    dbc.Col([
                                        daq.LEDDisplay(id='LED-volcapt-mes', color='brown', size=14, value=0)
                                    ], width=1),
                                    dbc.Col([
                                        html.Div(id='unidades-volcapt-mes')
                                    ], xs=2, sm=2, md=2, lg=1, xl=1,
                                        style={'textAlign': 'center', 'font-family': "Franklin Gothic"},
                                        align='center'),
                                    dbc.Col([
                                        dbc.Button(
                                            "Color:",
                                            id="color-mes-target",
                                            color="success",
                                            className="me-1",
                                            n_clicks=0,
                                            style={'font-family': "Franklin Gothic"},
                                        ),
                                        dbc.Popover(
                                            "Es el promedio de color de agua retornada clarificada al clarificador CL-800C después de haber sido tratada por el sistema de deshidratación de lodos en un mes.",
                                            target="color-mes-target",
                                            body=True,
                                            trigger="hover",
                                            style={'font-family': "Franklin Gothic"}
                                        ),

                                    ], width=2, align='center', className="d-grid gap-2"),
                                    dbc.Col([
                                        daq.LEDDisplay(id='LED-color-mes', color='green', size=14, value=0)
                                    ], width=1),
                                    dbc.Col([
                                        html.Div("Pt-Co")
                                    ], xs=2, sm=2, md=2, lg=1, xl=1,
                                        style={'textAlign': 'center', 'font-family': "Franklin Gothic"},
                                        align='center'),
                                    dbc.Col([
                                        dbc.Row([daq.GraduatedBar(
                                            id='barra-color-mes',
                                            color={
                                                "ranges": {"green": [0, 3.3], "yellow": [3.3, 6.6], "red": [6.6, 10]}},
                                            showCurrentValue=False,
                                            step=0.2,
                                            value=0
                                        )]),
                                    ], width=2)
                                ]),
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Button(
                                            "Volumen Retornado:",
                                            id="vol-ret-mes-target",
                                            color="primary",
                                            className="me-1",
                                            n_clicks=0,
                                            style={'font-family': "Franklin Gothic"},
                                        ),
                                        dbc.Popover(
                                            "Es la sumatoria de la cantidad de agua clarificada retornada al clarificador CL-800C después de haber sido tratada por el sistema de deshidratación de lodos en un mes.",
                                            target="vol-ret-mes-target",
                                            body=True,
                                            trigger="hover",
                                            style={'font-family': "Franklin Gothic"}
                                        ),

                                    ], width=2, align='center', className="d-grid gap-2"),
                                    dbc.Col([
                                        daq.LEDDisplay(id='LED-volret-mes', color='blue', size=14, value=0)
                                    ], width=1),
                                    dbc.Col([
                                        html.Div(id='unidades-volret-mes')
                                    ], xs=2, sm=2, md=2, lg=1, xl=1,
                                        style={'textAlign': 'center', 'font-family': "Franklin Gothic"},
                                        align='center'),
                                    dbc.Col([
                                        dbc.Button(
                                            "Agua Tratada:",
                                            id="agua-trat-mes-target",
                                            color="primary",
                                            className="me-1",
                                            n_clicks=0,
                                            style={'font-family': "Franklin Gothic"},
                                        ),
                                        dbc.Popover(
                                            "Es el cociente entre el agua clarificada retornada al clarificador CL-800C y el volumen captado de agua lodosa en un mes. En algunos casos el porcentaje de agua tratada es mayor a 100 debido a captaciones de agua fuera del sistema (tales como aguas lluvia), en dichos casos se acota el porcentaje de agua tratada a 100.",
                                            target="agua-trat-mes-target",
                                            body=True,
                                            trigger="hover",
                                            style={'font-family': "Franklin Gothic"}
                                        ),

                                    ], width=2, align='center', className="d-grid gap-2"),
                                    dbc.Col([
                                        daq.LEDDisplay(id='LED-aguatrat-mes', color='blue', size=14, value=0, )
                                    ], width=1),
                                    dbc.Col([
                                        html.Div("%")
                                    ], xs=2, sm=2, md=2, lg=1, xl=1,
                                        style={'textAlign': 'left', 'font-family': "Franklin Gothic"}, align='center'),
                                    dbc.Col([
                                        dbc.Row([daq.GraduatedBar(
                                            id='barra-aguatrat-mes',
                                            color={
                                                "ranges": {"red": [0, 3.3], "yellow": [3.3, 6.6], "green": [6.6, 10]}},
                                            showCurrentValue=False,
                                            step=0.2,
                                            value=0
                                        )]),
                                    ], width=2)
                                ]),
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Button(
                                            "Días Operados:",
                                            id="dia-oper-mes-target",
                                            color="primary",
                                            className="me-1",
                                            n_clicks=0,
                                            style={'font-family': "Franklin Gothic"},
                                        ),
                                        dbc.Popover(
                                            "Es la cantidad de días operados en un mes.",
                                            target="dia-oper-mes-target",
                                            body=True,
                                            trigger="hover",
                                            style={'font-family': "Franklin Gothic"}
                                        ),

                                    ], width=2, align='center', className="d-grid gap-2"),
                                    dbc.Col([
                                        daq.LEDDisplay(id='LED-dias-mes', color='blue', size=14, value=0)
                                    ], xs=3, sm=3, md=3, lg=2, xl=2, align="center"),
                                    dbc.Col([
                                        dbc.Button(
                                            "Lodos Confinados:",
                                            id="lodos-confi-mes-target",
                                            color="secondary",
                                            className="me-1",
                                            n_clicks=0,
                                            style={'font-family': "Franklin Gothic"},
                                        ),
                                        dbc.Popover(
                                            "Es el peso de lodos confinados en un día a una humedad de aproximadamente 60%.",
                                            target="lodos-confi-mes-target",
                                            body=True,
                                            trigger="hover",
                                            style={'font-family': "Franklin Gothic"}
                                        ),

                                    ], width=2, align='center', className="d-grid gap-2"),
                                    dbc.Col([
                                        daq.LEDDisplay(id='LED-lodos-confinados-mes', color='brown', size=14, value=0)
                                    ], width=1),
                                    dbc.Col([html.Div("Ton")], xs=2, sm=2, md=2, lg=1, xl=1,
                                            style={'textAlign': 'left', 'font-family': "Franklin Gothic"},
                                            align='center'),
                                ]),
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Button(
                                            "Geotubos Utilizados:",
                                            id="GT-util-mes-target",
                                            color="secondary",
                                            className="me-1",
                                            n_clicks=0,
                                            style={'font-family': "Franklin Gothic"},
                                        ),
                                        dbc.Popover(
                                            "Es la cantidad de Geotubos utilizados en un mes.",
                                            target="GT-util-mes-target",
                                            body=True,
                                            trigger="hover",
                                            style={'font-family': "Franklin Gothic"}
                                        ),

                                    ], width=2, align='center', className="d-grid gap-2"),
                                    dbc.Col([
                                        daq.LEDDisplay(id='LED-geotube-utilizados-mes', color='brown', size=14, value=0)
                                    ], width=2),
                                ]),
                                #dbc.Row(dcc.Graph(id='mi-mes-vol')),
                                dbc.Row(dbc.Col(
                                    dbc.Spinner(children=[dcc.Graph(id="mi-mes-vol")], size="lg", color="primary",
                                                type="border", fullscreen=True, ),
                                    # spinner_style={"width": "10rem", "height": "10rem"}),
                                    # spinnerClassName="spinner"),
                                    # dcc.Loading(children=[dcc.Graph(id="loading-output")], color="#119DFF", type="dot", fullscreen=True,),

                                    width={'size': 12, 'offset': 0}),
                                ),
                                dbc.Row(dcc.Graph(id='mi-mes-prop')),
                                dbc.Row(dcc.Graph(id='mi-mes-lodos')),
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Accordion([
                                            dbc.AccordionItem([

                                                html.H5([
                                                            'Barra de pH: es el indicador de pH acordado en las Especificaciones Técnicas para la Deshidratación de Lodos de Clarificación con la Tecnología de Geotubes (Geotube). Color verde es pH excelente (6-7.5), color amarillo es pH aceptable (7.5-8.0), color rojo es alerta de pH (8.0-8.5).']),

                                                html.H5([
                                                            'Barra de Turbidez: es el indicador de turbidez acordado en las Especificaciones Técnicas para la Deshidratación de Lodos de Clarificación con la Tecnología de Geotubes (Geotube). Color verde es turbidez excelente (0-10 NTU), color amarillo es turbidez aceptable (10-20 NTU), color rojo es alerta de turbidez (20-25 NTU).']),

                                                html.H5([
                                                            'Barra de color: es el indicador de color. Color de barra verde es color bajo (0-46 Pt-Co), color de barra amarillo es color medio (46-92 Pt-Co), color de barra rojo es color alto (92-140 Pt-Co).']),

                                                html.H5([
                                                            'Barra de agua tratada: es el indicador de agua tratada. Color de barra rojo es porcentaje de agua tratada bajo (0-33%), color de barra amarillo es porcentaje de agua tratada medio (33-66%), color de barra verde es porcentaje de agua tratada alto (66-100%).']),

                                            ], title="Descripción de Íconos"),
                                        ], start_collapsed=True,
                                            style={'color': '#082255', 'font-family': "Franklin Gothic"}),

                                    ], style={'color': '#082255', 'font-family': "Franklin Gothic"}),
                                ]),
                            ])
                        ]),
                    ])
                ]),
            ], label="Resumen Mensual", label_style={'color': '#082255', 'font-family': "Franklin Gothic"}),
            dbc.Tab([
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Row(html.H2(['Resumen Fase']),
                                                style={'color': '#082255', 'font-family': "Franklin Gothic"})
                                    ])
                                ]),
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Button(
                                            "Seleccionar Unidades:",
                                            id="selec-uni-fase-target",
                                            color="info",
                                            className="me-1",
                                            n_clicks=0,
                                            style={'font-family': "Franklin Gothic"},
                                        ),
                                        dbc.Popover(
                                            "Son las unidades de volumen que son seleccionadas por el usuario. Se tiene como opciones galones y metros cúbicos.",
                                            target="selec-uni-fase-target",
                                            body=True,
                                            trigger="hover",
                                            style={'font-family': "Franklin Gothic"}
                                        ),

                                    ], width=2, align='center', className="d-grid gap-2"),
                                    dbc.Col([
                                        dbc.RadioItems(
                                            options=[
                                                {"label": "Galones", "value": True},
                                                {"label": "Metros cúbicos", "value": False},
                                            ],
                                            value=True,
                                            id="unidades-fase-input",
                                            style={'font-family': "Franklin Gothic"}
                                        ),
                                    ], xs=3, sm=3, md=3, lg=2, xl=2, ),
                                    dbc.Col([
                                        dbc.Button(
                                            "Seleccionar Fase:",
                                            id="selec-fase-target",
                                            color="info",
                                            className="me-1",
                                            n_clicks=0,
                                            style={'font-family': "Franklin Gothic"},
                                        ),
                                        dbc.Popover(
                                            "Es la fase introducida por el usuario para conocer el resumen de la operación para una fase seleccionada.",
                                            target="selec-fase-target",
                                            body=True,
                                            trigger="hover",
                                            style={'font-family': "Franklin Gothic"}
                                        ),

                                    ], width=2, align='center', className="d-grid gap-2"),
                                    dbc.Col([
                                        dcc.Dropdown(id='fase',
                                                     options=[],
                                                     #value='2',
                                                     style={'font-family': "Franklin Gothic"}
                                                     )
                                    ], width=2, align='center'),
                                ]),
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Button(
                                            "Día Inicial:",
                                            id="dia-inicial-fase-target",
                                            color="primary",
                                            className="me-1",
                                            n_clicks=0,
                                            style={'font-family': "Franklin Gothic"},
                                        ),
                                        dbc.Popover(
                                            "Es el día de inicio de operación de una fase.",
                                            target="dia-inicial-fase-target",
                                            body=True,
                                            trigger="hover",
                                            style={'font-family': "Franklin Gothic"}
                                        ),

                                    ], width=2, align='center', className="d-grid gap-2"),
                                    dbc.Col([
                                        html.Div(id='dia-inicial-fase', style={'font-family': "Franklin Gothic"})
                                    ], xs=3, sm=3, md=3, lg=2, xl=2, align="center"),
                                    dbc.Col([
                                        dbc.Button(
                                            "Día Final:",
                                            id="dia-final-fase-target",
                                            color="primary",
                                            className="me-1",
                                            n_clicks=0,
                                            style={'font-family': "Franklin Gothic"},
                                        ),
                                        dbc.Popover(
                                            "Es el último día de operación de una fase.",
                                            target="dia-final-fase-target",
                                            body=True,
                                            trigger="hover",
                                            style={'font-family': "Franklin Gothic"}
                                        ),

                                    ], width=2, align='center', className="d-grid gap-2"),
                                    dbc.Col([
                                        html.Div(id='dia-final-fase', style={'font-family': "Franklin Gothic"})
                                    ], xs=2, sm=2, md=2, lg=2, xl=2, style={'textAlign': 'center'}, align='center'),
                                ]),
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Button(
                                            "Purgas Captadas:",
                                            id="purg-capt-fase-target",
                                            color="secondary",
                                            className="me-1",
                                            n_clicks=0,
                                            style={'font-family': "Franklin Gothic"},
                                        ),
                                        dbc.Popover(
                                            "Es la cantidad de purgas enviadas del clarificador CL-800C a la caja de lodos (captación) en una fase.",
                                            target="purg-capt-fase-target",
                                            body=True,
                                            trigger="hover",
                                            style={'font-family': "Franklin Gothic"}
                                        ),

                                    ], width=2, align='center', className="d-grid gap-2"),
                                    dbc.Col([
                                        daq.LEDDisplay(id='LED-purgcapt-fase', color='brown', size=14, value=0)
                                    ], xs=3, sm=3, md=3, lg=2, xl=2, align="center"),
                                    dbc.Col([
                                        dbc.Button(
                                            "pH:",
                                            id="pH-fase-target",
                                            color="success",
                                            className="me-1",
                                            n_clicks=0,
                                            style={'font-family': "Franklin Gothic"},
                                        ),
                                        dbc.Popover(
                                            "Es el promedio de pH de agua retornada clarificada al clarificador CL-800C después de haber sido tratada con la tecnología Geotube en una fase.",
                                            target="pH-fase-target",
                                            body=True,
                                            trigger="hover",
                                            style={'font-family': "Franklin Gothic"}
                                        ),

                                    ], width=2, align='center', className="d-grid gap-2"),
                                    dbc.Col([
                                        daq.LEDDisplay(id='LED-pH-fase', color='green', size=14, value=0)
                                    ], width=1, align="center"),
                                    dbc.Col([
                                        html.Div("")
                                    ], xs=2, sm=2, md=2, lg=1, xl=1, style={'textAlign': 'left'}, align='end'),
                                    dbc.Col([
                                        dbc.Row([daq.GraduatedBar(
                                            id='barra-pH-fase',
                                            color={
                                                "ranges": {"green": [0, 8.8], "yellow": [8.8, 9.4], "red": [9.4, 10]}},
                                            showCurrentValue=False,
                                            step=0.2,
                                            value=0
                                        )]),
                                    ], width=2)
                                ]),
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Button(
                                            "Bombeos Retornados:",
                                            id="bomb-ret-fase-target",
                                            color="primary",
                                            className="me-1",
                                            n_clicks=0,
                                            style={'font-family': "Franklin Gothic"},
                                        ),
                                        dbc.Popover(
                                            "Es el número de bombeos de agua clarificada retornada al clarificador CL-800C después de haber sido tratada por el sistema de deshidratación de lodos en una fase.",
                                            target="bomb-ret-fase-target",
                                            body=True,
                                            trigger="hover",
                                            style={'font-family': "Franklin Gothic"}
                                        ),

                                    ], width=2, align='center', className="d-grid gap-2"),
                                    dbc.Col([
                                        daq.LEDDisplay(id='LED-bomb-fase', color='blue', size=14, value=0)
                                    ], xs=3, sm=3, md=3, lg=2, xl=2, ),
                                    dbc.Col([
                                        dbc.Button(
                                            "Turbidez:",
                                            id="turb-fase-target",
                                            color="success",
                                            className="me-1",
                                            n_clicks=0,
                                            style={'font-family': "Franklin Gothic"},
                                        ),
                                        dbc.Popover(
                                            "Es el promedio de turbidez de agua retornada clarificada al clarificador CL-800C después de haber sido tratada por el sistema de deshidratación de lodos en una fase.",
                                            target="turb-fase-target",
                                            body=True,
                                            trigger="hover",
                                            style={'font-family': "Franklin Gothic"}
                                        ),

                                    ], width=2, align='center', className="d-grid gap-2"),
                                    dbc.Col([
                                        daq.LEDDisplay(id='LED-turb-fase', color='green', size=14, value=0)
                                    ], width=1),
                                    dbc.Col([
                                        html.Div("NTU")
                                    ], xs=2, sm=2, md=2, lg=1, xl=1,
                                        style={'textAlign': 'center', 'font-family': "Franklin Gothic"},
                                        align='center'),
                                    dbc.Col([
                                        dbc.Row([daq.GraduatedBar(
                                            id='barra-turb-fase',
                                            color={"ranges": {"green": [0, 4], "yellow": [4, 8], "red": [8, 10]}},
                                            showCurrentValue=False,
                                            step=0.2,
                                            value=0
                                        )]),
                                    ], width=2)
                                ]),
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Button(
                                            "Volumen Captado:",
                                            id="vol-capt-fase-target",
                                            color="secondary",
                                            className="me-1",
                                            n_clicks=0,
                                            style={'font-family': "Franklin Gothic"},
                                        ),
                                        dbc.Popover(
                                            "Es la sumatoria de la cantidad de agua lodosa bombeada de la caja de lodos al sistema de deshidratación de lodos en una fase.",
                                            target="vol-capt-fase-target",
                                            body=True,
                                            trigger="hover",
                                            style={'font-family': "Franklin Gothic"}
                                        ),

                                    ], width=2, align='center', className="d-grid gap-2"),
                                    dbc.Col([
                                        daq.LEDDisplay(id='LED-volcapt-fase', color='brown', size=14, value=0)
                                    ], width=1),
                                    dbc.Col([
                                        html.Div(id='unidades-volcapt-fase')
                                    ], xs=2, sm=2, md=2, lg=1, xl=1,
                                        style={'textAlign': 'right', 'font-family': "Franklin Gothic"}, align='center'),
                                    dbc.Col([
                                        dbc.Button(
                                            "Color:",
                                            id="color-fase-target",
                                            color="success",
                                            className="me-1",
                                            n_clicks=0,
                                            style={'font-family': "Franklin Gothic"},
                                        ),
                                        dbc.Popover(
                                            "Es el promedio de color de agua retornada clarificada al clarificador CL-800C después de haber sido tratada por el sistema de deshidratación de lodos en una fase.",
                                            target="color-fase-target",
                                            body=True,
                                            trigger="hover",
                                            style={'font-family': "Franklin Gothic"}
                                        ),

                                    ], width=2, align='center', className="d-grid gap-2"),
                                    dbc.Col([
                                        daq.LEDDisplay(id='LED-color-fase', color='green', size=14, value=0)
                                    ], width=1),
                                    dbc.Col([
                                        html.Div("Pt-Co")
                                    ], xs=2, sm=2, md=2, lg=1, xl=1,
                                        style={'textAlign': 'center', 'font-family': "Franklin Gothic"},
                                        align='center'),
                                    dbc.Col([
                                        dbc.Row([daq.GraduatedBar(
                                            id='barra-color-fase',
                                            color={
                                                "ranges": {"green": [0, 3.3], "yellow": [3.3, 6.6], "red": [6.6, 10]}},
                                            showCurrentValue=False,
                                            step=0.2,
                                            value=0
                                        )]),
                                    ], width=2)
                                ]),
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Button(
                                            "Volumen Retornado:",
                                            id="vol-ret-fase-target",
                                            color="primary",
                                            className="me-1",
                                            n_clicks=0,
                                            style={'font-family': "Franklin Gothic"},
                                        ),
                                        dbc.Popover(
                                            "Es la sumatoria de la cantidad de agua clarificada retornada al clarificador CL-800C después de haber sido tratada por el sistema de deshidratación de lodos en una fase.",
                                            target="vol-ret-fase-target",
                                            body=True,
                                            trigger="hover",
                                            style={'font-family': "Franklin Gothic"}
                                        ),

                                    ], width=2, align='center', className="d-grid gap-2"),
                                    dbc.Col([
                                        daq.LEDDisplay(id='LED-volret-fase', color='blue', size=14, value=0)
                                    ], width=1),
                                    dbc.Col([
                                        html.Div(id='unidades-volret-fase')
                                    ], xs=2, sm=2, md=2, lg=1, xl=1,
                                        style={'textAlign': 'right', 'font-family': "Franklin Gothic"}, align='center'),
                                    dbc.Col([
                                        dbc.Button(
                                            "Agua Tratada:",
                                            id="agua-trat-fase-target",
                                            color="primary",
                                            className="me-1",
                                            n_clicks=0,
                                            style={'font-family': "Franklin Gothic"},
                                        ),
                                        dbc.Popover(
                                            "Es el cociente entre el agua clarificada retornada al clarificador CL-800C y el volumen captado de agua lodosa en una fase. En algunos casos el porcentaje de agua tratada es mayor a 100 debido a captaciones de agua fuera del sistema (tales como aguas lluvia), en dichos casos se acota el porcentaje de agua tratada a 100.",
                                            target="agua-trat-fase-target",
                                            body=True,
                                            trigger="hover",
                                            style={'font-family': "Franklin Gothic"}
                                        ),

                                    ], width=2, align='center', className="d-grid gap-2"),
                                    dbc.Col([
                                        daq.LEDDisplay(id='LED-aguatrat-fase', color='blue', size=14, value=0)
                                    ], width=1),
                                    dbc.Col([
                                        html.Div("%")
                                    ], xs=2, sm=2, md=2, lg=1, xl=1,
                                        style={'textAlign': 'left', 'font-family': "Franklin Gothic"}, align='center'),
                                    dbc.Col([
                                        dbc.Row([daq.GraduatedBar(
                                            id='barra-aguatrat-fase',
                                            color={
                                                "ranges": {"red": [0, 3.3], "yellow": [3.3, 6.6], "green": [6.6, 10]}},
                                            showCurrentValue=False,
                                            step=0.2,
                                            value=0
                                        )]),
                                    ], width=2)
                                ]),
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Button(
                                            "Días Operados:",
                                            id="dia-oper-fase-target",
                                            color="primary",
                                            className="me-1",
                                            n_clicks=0,
                                            style={'font-family': "Franklin Gothic"},
                                        ),
                                        dbc.Popover(
                                            "Es la cantidad de días operados en una fase.",
                                            target="dia-oper-fase-target",
                                            body=True,
                                            trigger="hover",
                                            style={'font-family': "Franklin Gothic"}
                                        ),

                                    ], width=2, align='center', className="d-grid gap-2"),
                                    dbc.Col([
                                        daq.LEDDisplay(id='LED-dias-fase', color='blue', size=14, value=0)
                                    ], xs=3, sm=3, md=3, lg=2, xl=2, align="center"),
                                    dbc.Col([
                                        dbc.Button(
                                            "Lodos Confinados:",
                                            id="lodos-confi-fase-target",
                                            color="secondary",
                                            className="me-1",
                                            n_clicks=0,
                                            style={'font-family': "Franklin Gothic"},
                                        ),
                                        dbc.Popover(
                                            "Es el peso de lodos confinados en una fase a una humedad de aproximadamente 60%.",
                                            target="lodos-confi-fase-target",
                                            body=True,
                                            trigger="hover",
                                            style={'font-family': "Franklin Gothic"}
                                        ),

                                    ], width=2, align='center', className="d-grid gap-2"),
                                    dbc.Col([
                                        daq.LEDDisplay(id='LED-lodos-confinados-fase', color='brown', size=14, value=0)
                                    ], width=1),
                                    dbc.Col([html.Div("Ton")], xs=2, sm=2, md=2, lg=1, xl=1,
                                            style={'textAlign': 'center', 'font-family': "Franklin Gothic"},
                                            align='center'),
                                ]),
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Button(
                                            "Geotubos Utilizados:",
                                            id="GT-util-fase-target",
                                            color="secondary",
                                            className="me-1",
                                            n_clicks=0,
                                            style={'font-family': "Franklin Gothic"},
                                        ),
                                        dbc.Popover(
                                            "Es la cantidad de Geotubos utilizados en una fase.",
                                            target="GT-util-fase-target",
                                            body=True,
                                            trigger="hover",
                                            style={'font-family': "Franklin Gothic"}
                                        ),

                                    ], width=2, align='center', className="d-grid gap-2"),
                                    dbc.Col([
                                        daq.LEDDisplay(id='LED-geotube-utilizados-fase', color='brown', size=14,
                                                       value=0)
                                    ], width=2),
                                ]),
                                #dbc.Row(dcc.Graph(id='mi-fase-vol')),
                                dbc.Row(dbc.Col(
                                    dbc.Spinner(children=[dcc.Graph(id="mi-fase-vol")], size="lg", color="primary",
                                                type="border", fullscreen=True, ),
                                    # spinner_style={"width": "10rem", "height": "10rem"}),
                                    # spinnerClassName="spinner"),
                                    # dcc.Loading(children=[dcc.Graph(id="loading-output")], color="#119DFF", type="dot", fullscreen=True,),

                                    width={'size': 12, 'offset': 0}),
                                ),
                                dbc.Row(dcc.Graph(id='mi-fase-prop')),
                                dbc.Row(dcc.Graph(id='mi-fase-lodos')),
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Accordion([
                                            dbc.AccordionItem([

                                                html.H5([
                                                            'Barra de pH: es el indicador de pH acordado en las Especificaciones Técnicas para la Deshidratación de Lodos de Clarificación con la Tecnología de Geotubes (Geotube). Color verde es pH excelente (6-7.5), color amarillo es pH aceptable (7.5-8.0), color rojo es alerta de pH (8.0-8.5).']),

                                                html.H5([
                                                            'Barra de Turbidez: es el indicador de turbidez acordado en las Especificaciones Técnicas para la Deshidratación de Lodos de Clarificación con la Tecnología de Geotubes (Geotube). Color verde es turbidez excelente (0-10 NTU), color amarillo es turbidez aceptable (10-20 NTU), color rojo es alerta de turbidez (20-25 NTU).']),

                                                html.H5([
                                                            'Barra de color: es el indicador de color. Color de barra verde es color bajo (0-46 Pt-Co), color de barra amarillo es color medio (46-92 Pt-Co), color de barra rojo es color alto (92-140 Pt-Co).']),
                                                html.H5([
                                                            'Barra de agua tratada: es el indicador de agua tratada. Color de barra rojo es porcentaje de agua tratada bajo (0-33%), color de barra amarillo es porcentaje de agua tratada medio (33-66%), color de barra verde es porcentaje de agua tratada alto (66-100%).']),

                                            ], title="Descripción de Íconos"),
                                        ], start_collapsed=True,
                                            style={'color': '#082255', 'font-family': "Franklin Gothic"}),

                                    ], style={'color': '#082255', 'font-family': "Franklin Gothic"}),
                                ]),

                            ])
                        ]),
                    ])
                ]),
            ], label="Resumen Fase", label_style={'color': '#082255', 'font-family': "Franklin Gothic"}),
            dbc.Tab([
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Row(html.H2(['Resumen Total']),
                                                style={'color': '#082255', 'font-family': "Franklin Gothic"})
                                    ]),

                                ]),
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Button(
                                            "Seleccionar Unidades:",
                                            id="selec-uni-acum-target",
                                            color="info",
                                            className="me-1",
                                            n_clicks=0,
                                            style={'font-family': "Franklin Gothic"},
                                        ),
                                        dbc.Popover(
                                            "Son las unidades de volumen que son seleccionadas por el usuario. Se tiene como opciones galones y metros cúbicos.",
                                            target="selec-uni-acum-target",
                                            body=True,
                                            trigger="hover",
                                            style={'font-family': "Franklin Gothic"}
                                        ),

                                    ], width=2, align='center', className="d-grid gap-2"),
                                    dbc.Col(dbc.RadioItems(
                                        options=[
                                            {"label": "Galones", "value": True},
                                            {"label": "Metros cúbicos", "value": False},
                                        ],
                                        value=True,
                                        id="unidades-acum-input",
                                        style={'font-family': "Franklin Gothic"}
                                    ), xs=3, sm=3, md=3, lg=2, xl=2, ),
                                ]),
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Button(
                                            "Día Inicial:",
                                            id="dia-inicial-acum-target",
                                            color="primary",
                                            className="me-1",
                                            n_clicks=0,
                                            style={'font-family': "Franklin Gothic"},
                                        ),
                                        dbc.Popover(
                                            "Es el día de inicio de operación de la primera fase.",
                                            target="dia-inicial-acum-target",
                                            body=True,
                                            trigger="hover",
                                            style={'font-family': "Franklin Gothic"}
                                        ),

                                    ], width=2, align='center', className="d-grid gap-2"),
                                    dbc.Col([
                                        html.Div(id='dia-inicial-acum', style={'font-family': "Franklin Gothic"})
                                    ], xs=3, sm=3, md=3, lg=2, xl=2, align="center"),
                                    dbc.Col([
                                        dbc.Button(
                                            "Día Final:",
                                            id="dia-final-acum-target",
                                            color="primary",
                                            className="me-1",
                                            n_clicks=0,
                                            style={'font-family': "Franklin Gothic"},
                                        ),
                                        dbc.Popover(
                                            "Es el último día operado de la última fase.",
                                            target="dia-final-acum-target",
                                            body=True,
                                            trigger="hover",
                                            style={'font-family': "Franklin Gothic"}
                                        ),

                                    ], width=2, align='center', className="d-grid gap-2"),
                                    dbc.Col([
                                        html.Div(id='dia-final-acum', style={'font-family': "Franklin Gothic"})
                                    ], xs=2, sm=2, md=2, lg=2, xl=2, style={'textAlign': 'center'}, align='center'),
                                ]),
                                dbc.Row([
                                    dbc.Row([
                                        dbc.Col([
                                            dbc.Button(
                                                "Purgas Captadas:",
                                                id="purg-capt-acum-target",
                                                color="secondary",
                                                className="me-1",
                                                n_clicks=0,
                                                style={'font-family': "Franklin Gothic"},
                                            ),
                                            dbc.Popover(
                                                "Es la cantidad de purgas enviadas del clarificador CL-800C a la caja de lodos (captación) en el total de la operación.",
                                                target="purg-capt-acum-target",
                                                body=True,
                                                trigger="hover",
                                                style={'font-family': "Franklin Gothic"}
                                            ),

                                        ], width=2, align='center', className="d-grid gap-2"),
                                        dbc.Col([
                                            daq.LEDDisplay(id='LED-purgcapt-acum', color='brown', size=14, value=0)
                                        ], xs=3, sm=3, md=3, lg=2, xl=2, align="center"),
                                        dbc.Col([
                                            dbc.Button(
                                                "pH:",
                                                id="pH-acum-target",
                                                color="success",
                                                className="me-1",
                                                n_clicks=0,
                                                style={'font-family': "Franklin Gothic"},
                                            ),
                                            dbc.Popover(
                                                "Es el promedio de pH de agua retornada clarificada al clarificador CL-800C después de haber sido tratada con la tecnología Geotube en el total de la operación.",
                                                target="pH-acum-target",
                                                body=True,
                                                trigger="hover",
                                                style={'font-family': "Franklin Gothic"}
                                            ),

                                        ], width=2, align='center', className="d-grid gap-2"),
                                        dbc.Col([
                                            daq.LEDDisplay(id='LED-pH-acum', color='green', size=14, value=0)
                                        ], width=1, align="center"),
                                        dbc.Col([
                                            html.Div("")
                                        ], xs=2, sm=2, md=2, lg=1, xl=1, style={'textAlign': 'left'}, align='end'),
                                        dbc.Col([
                                            dbc.Row([daq.GraduatedBar(
                                                id='barra-pH-acum',
                                                color={"ranges": {"green": [0, 8.8], "yellow": [8.8, 9.4],
                                                                  "red": [9.4, 10]}},
                                                showCurrentValue=False,
                                                step=0.2,
                                                value=0
                                            )]),
                                        ], width=2)
                                    ]),
                                    dbc.Row([
                                        dbc.Col([
                                            dbc.Button(
                                                "Bombeos Retornados:",
                                                id="bomb-ret-acum-target",
                                                color="primary",
                                                className="me-1",
                                                n_clicks=0,
                                                style={'font-family': "Franklin Gothic"},
                                            ),
                                            dbc.Popover(
                                                "Es el número de bombeos de agua clarificada retornada al clarificador CL-800C después de haber sido tratada por el sistema de deshidratación de lodos en el total de la operación.",
                                                target="bomb-ret-acum-target",
                                                body=True,
                                                trigger="hover",
                                                style={'font-family': "Franklin Gothic"}
                                            ),

                                        ], width=2, align='center', className="d-grid gap-2"),
                                        dbc.Col([
                                            daq.LEDDisplay(id='LED-bomb-acum', color='blue', size=14, value=0)
                                        ], xs=3, sm=3, md=3, lg=2, xl=2, ),
                                        dbc.Col([
                                            dbc.Button(
                                                "Turbidez:",
                                                id="turb-acum-target",
                                                color="success",
                                                className="me-1",
                                                n_clicks=0,
                                                style={'font-family': "Franklin Gothic"},
                                            ),
                                            dbc.Popover(
                                                "Es el promedio de turbidez de agua retornada clarificada al clarificador CL-800C después de haber sido tratada por el sistema de deshidratación de lodos en el total de la operación.",
                                                target="turb-acum-target",
                                                body=True,
                                                trigger="hover",
                                                style={'font-family': "Franklin Gothic"}
                                            ),

                                        ], width=2, align='center', className="d-grid gap-2"),
                                        dbc.Col([
                                            daq.LEDDisplay(id='LED-turb-acum', color='green', size=14, value=0)
                                        ], width=1),
                                        dbc.Col([
                                            html.Div("NTU")
                                        ], xs=2, sm=2, md=2, lg=1, xl=1,
                                            style={'textAlign': 'center', 'font-family': "Franklin Gothic"},
                                            align='center'),
                                        dbc.Col([
                                            dbc.Row([daq.GraduatedBar(
                                                id='barra-turb-acum',
                                                color={"ranges": {"green": [0, 4], "yellow": [4, 8], "red": [8, 10]}},
                                                showCurrentValue=False,
                                                step=0.2,
                                                value=0
                                                # value=10
                                            )]),
                                        ], width=2)
                                    ]),
                                    dbc.Row([
                                        dbc.Col([
                                            dbc.Button(
                                                "Volumen Captado:",
                                                id="vol-capt-acum-target",
                                                color="secondary",
                                                className="me-1",
                                                n_clicks=0,
                                                style={'font-family': "Franklin Gothic"},
                                            ),
                                            dbc.Popover(
                                                "Es la sumatoria de la cantidad de agua lodosa bombeada de la caja de lodos al sistema de deshidratación de lodos en el total de la operación.",
                                                target="vol-capt-acum-target",
                                                body=True,
                                                trigger="hover",
                                                style={'font-family': "Franklin Gothic"}
                                            ),

                                        ], width=2, align='center', className="d-grid gap-2"),
                                        dbc.Col([
                                            daq.LEDDisplay(id='LED-volcapt-acum', color='brown', size=14, value=0)
                                        ], width=1),
                                        dbc.Col([
                                            html.Div(id='unidades-volcapt-acum')
                                        ], xs=2, sm=2, md=2, lg=1, xl=1,
                                            style={'textAlign': 'right', 'font-family': "Franklin Gothic"},
                                            align='center'),
                                        dbc.Col([
                                            dbc.Button(
                                                "Color:",
                                                id="color-acum-target",
                                                color="success",
                                                className="me-1",
                                                n_clicks=0,
                                                style={'font-family': "Franklin Gothic"},
                                            ),
                                            dbc.Popover(
                                                "Es el promedio de color de agua retornada clarificada al clarificador CL-800C después de haber sido tratada por el sistema de deshidratación de lodos en el total de la operación.",
                                                target="color-acum-target",
                                                body=True,
                                                trigger="hover",
                                                style={'font-family': "Franklin Gothic"}
                                            ),

                                        ], width=2, align='center', className="d-grid gap-2"),
                                        dbc.Col([
                                            daq.LEDDisplay(id='LED-color-acum', color='green', size=14, value=0)
                                        ], width=1),
                                        dbc.Col([
                                            html.Div("Pt-Co")
                                        ], xs=2, sm=2, md=2, lg=1, xl=1,
                                            style={'textAlign': 'center', 'font-family': "Franklin Gothic"},
                                            align='center'),
                                        dbc.Col([
                                            dbc.Row([daq.GraduatedBar(
                                                id='barra-color-acum',
                                                color={"ranges": {"green": [0, 3.3], "yellow": [3.3, 6.6],
                                                                  "red": [6.6, 10]}},
                                                showCurrentValue=False,
                                                step=0.2,
                                                value=0
                                            )]),
                                        ], width=2)
                                    ]),
                                    dbc.Row([
                                        dbc.Col([
                                            dbc.Button(
                                                "Volumen Retornado:",
                                                id="vol-ret-acum-target",
                                                color="primary",
                                                className="me-1",
                                                n_clicks=0,
                                                style={'font-family': "Franklin Gothic"},
                                            ),
                                            dbc.Popover(
                                                "Es la sumatoria de la cantidad de agua clarificada retornada al clarificador CL-800C después de haber sido tratada por el sistema de deshidratación de lodos en el total de la operación.",
                                                target="vol-ret-acum-target",
                                                body=True,
                                                trigger="hover",
                                                style={'font-family': "Franklin Gothic"}
                                            ),

                                        ], width=2, align='center', className="d-grid gap-2"),
                                        dbc.Col([
                                            daq.LEDDisplay(id='LED-volret-acum', color='blue', size=14, value=0)
                                        ], width=1),
                                        dbc.Col([
                                            html.Div(id='unidades-volret-acum')
                                        ], xs=2, sm=2, md=2, lg=1, xl=1,
                                            style={'textAlign': 'right', 'font-family': "Franklin Gothic"},
                                            align='center'),
                                        dbc.Col([
                                            dbc.Button(
                                                "Agua Tratada:",
                                                id="agua-trat-acum-target",
                                                color="primary",
                                                className="me-1",
                                                n_clicks=0,
                                                style={'font-family': "Franklin Gothic"},
                                            ),
                                            dbc.Popover(
                                                "Es el cociente entre el agua clarificada retornada al clarificador CL-800C y el volumen captado de agua lodosa en el total de la operación. En algunos casos el porcentaje de agua tratada es mayor a 100 debido a captaciones de agua fuera del sistema (tales como aguas lluvia), en dichos casos se acota el porcentaje de agua tratada a 100.",
                                                target="agua-trat-acum-target",
                                                body=True,
                                                trigger="hover",
                                                style={'font-family': "Franklin Gothic"}
                                            ),

                                        ], width=2, align='center', className="d-grid gap-2"),
                                        dbc.Col([
                                            daq.LEDDisplay(id='LED-aguatrat-acum', color='blue', size=14, value=0, )
                                        ], width=1),
                                        dbc.Col([
                                            html.Div("%")
                                        ], xs=2, sm=2, md=2, lg=1, xl=1,
                                            style={'textAlign': 'left', 'font-family': "Franklin Gothic"},
                                            align='center'),
                                        dbc.Col([
                                            dbc.Row([daq.GraduatedBar(
                                                id='barra-aguatrat-acum',
                                                color={"ranges": {"red": [0, 3.3], "yellow": [3.3, 6.6],
                                                                  "green": [6.6, 10]}},
                                                showCurrentValue=False,
                                                step=0.2,
                                                value=0
                                                # value=10
                                            )]),
                                        ], width=2)
                                    ]),

                                    dbc.Row([
                                        dbc.Col([
                                            dbc.Button(
                                                "Días Operados:",
                                                id="dia-oper-acum-target",
                                                color="primary",
                                                className="me-1",
                                                n_clicks=0,
                                                style={'font-family': "Franklin Gothic"},
                                            ),
                                            dbc.Popover(
                                                "Es la cantidad de días operados en el total de la operación.",
                                                target="dia-oper-acum-target",
                                                body=True,
                                                trigger="hover",
                                                style={'font-family': "Franklin Gothic"}
                                            ),

                                        ], width=2, align='center', className="d-grid gap-2"),
                                        dbc.Col([
                                            daq.LEDDisplay(id='LED-dias-acum', color='blue', size=14, value=0)
                                        ], xs=3, sm=3, md=3, lg=2, xl=2, align="center"),
                                        dbc.Col([
                                            dbc.Button(
                                                "Lodos Confinados:",
                                                id="lodos-confi-acum-target",
                                                color="secondary",
                                                className="me-1",
                                                n_clicks=0,
                                                style={'font-family': "Franklin Gothic"},
                                            ),
                                            dbc.Popover(
                                                "Es el peso de lodos confinados en el total de la operación a una humedad de aproximadamente 60%.",
                                                target="lodos-confi-acum-target",
                                                body=True,
                                                trigger="hover",
                                                style={'font-family': "Franklin Gothic"}
                                            ),

                                        ], width=2, align='center', className="d-grid gap-2"),
                                        dbc.Col([
                                            daq.LEDDisplay(id='LED-lodos-confinados-acum', color='brown', size=14,
                                                           value=0)
                                        ], width=1),
                                        dbc.Col([html.Div("Ton")], xs=2, sm=2, md=2, lg=1, xl=1,
                                                style={'textAlign': 'center', 'font-family': "Franklin Gothic"},
                                                align='center'),
                                    ]),
                                    dbc.Row([
                                        dbc.Col([
                                            dbc.Button(
                                                "Geotubos Utilizados:",
                                                id="GT-util-acum-target",
                                                color="secondary",
                                                className="me-1",
                                                n_clicks=0,
                                                style={'font-family': "Franklin Gothic"},
                                            ),
                                            dbc.Popover(
                                                "Es la cantidad de Geotubos utilizados en el total de la operación.",
                                                target="GT-util-acum-target",
                                                body=True,
                                                trigger="hover",
                                                style={'font-family': "Franklin Gothic"}
                                            ),

                                        ], width=2, align='center', className="d-grid gap-2"),
                                        dbc.Col([
                                            daq.LEDDisplay(id='LED-geotube-utilizados-acum', color='brown', size=14,
                                                           value=0)
                                        ], width=1),

                                    ]),
                                    #dbc.Row(dcc.Graph(id='mi-acum-vol')),
                                    dbc.Row(dbc.Col(
                                        dbc.Spinner(children=[dcc.Graph(id="mi-acum-vol")], size="lg",
                                                    color="primary", type="border", fullscreen=True, ),
                                        # spinner_style={"width": "10rem", "height": "10rem"}),
                                        # spinnerClassName="spinner"),
                                        # dcc.Loading(children=[dcc.Graph(id="loading-output")], color="#119DFF", type="dot", fullscreen=True,),

                                        width={'size': 12, 'offset': 0}),
                                    ),
                                    dbc.Row(dcc.Graph(id='mi-acum-prop')),
                                    dbc.Row(dcc.Graph(id='mi-acum-lodos')),
                                    dbc.Row([
                                        dbc.Col([
                                            dbc.Accordion([
                                                dbc.AccordionItem([

                                                    html.H5([
                                                                'Barra de pH: es el indicador de pH acordado en las Especificaciones Técnicas para la Deshidratación de Lodos de Clarificación con la Tecnología de Geotubes (Geotube). Color verde es pH excelente (6-7.5), color amarillo es pH aceptable (7.5-8.0), color rojo es alerta de pH (8.0-8.5).']),

                                                    html.H5([
                                                                'Barra de Turbidez: es el indicador de turbidez acordado en las Especificaciones Técnicas para la Deshidratación de Lodos de Clarificación con la Tecnología de Geotubes (Geotube). Color verde es turbidez excelente (0-10 NTU), color amarillo es turbidez aceptable (10-20 NTU), color rojo es alerta de turbidez (20-25 NTU).']),

                                                    html.H5([
                                                                'Barra de color: es el indicador de color. Color de barra verde es color bajo (0-46 Pt-Co), color de barra amarillo es color medio (46-92 Pt-Co), color de barra rojo es color alto (92-140 Pt-Co).']),

                                                    html.H5([
                                                                'Barra de agua tratada: es el indicador de agua tratada. Color de barra rojo es porcentaje de agua tratada bajo (0-33%), color de barra amarillo es porcentaje de agua tratada medio (33-66%), color de barra verde es porcentaje de agua tratada alto (66-100%).']),

                                                ], title="Descripción de Íconos"),
                                            ], start_collapsed=True,
                                                style={'color': '#082255', 'font-family': "Franklin Gothic"}),

                                        ], style={'color': '#082255', 'font-family': "Franklin Gothic"}),
                                    ]),

                                ])

                            ]),
                        ])

                    ])
                ]),
            ], label="Resumen Total", label_style={'color': '#082255', 'font-family': "Franklin Gothic"}),
            dbc.Tab([
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                dbc.Row([
                                    dbc.Row([
                                        dbc.Col([
                                            dbc.Row(html.H2(['Resumen Geotube']),
                                                    style={'color': '#082255', 'font-family': "Franklin Gothic"})
                                        ]),

                                    ]),
                                    dbc.Row([
                                        dbc.Col([
                                            dbc.Button(
                                                "Seleccionar Unidades:",
                                                id="selec-uni-GT-target",
                                                color="info",
                                                className="me-1",
                                                n_clicks=0,
                                                style={'font-family': "Franklin Gothic"},
                                            ),
                                            dbc.Popover(
                                                "Son las unidades de volumen que son seleccionadas por el usuario. Se tiene como opciones galones y metros cúbicos.",
                                                target="selec-uni-GT-target",
                                                body=True,
                                                trigger="hover",
                                                style={'font-family': "Franklin Gothic"}
                                            ),

                                        ], width=2, align='center', className="d-grid gap-2"),
                                        dbc.Col(dbc.RadioItems(
                                            options=[
                                                {"label": "Galones", "value": True},
                                                {"label": "Metros cúbicos", "value": False},
                                            ],
                                            value=False,
                                            id="unidades-GT-input",
                                            style={'font-family': "Franklin Gothic"}
                                        ), xs=2, sm=2, md=2, lg=2, xl=2, ),
                                        dbc.Col([
                                            dbc.Button(
                                                "Seleccionar Número:",
                                                id="selec-num-GT-target",
                                                color="info",
                                                className="me-1",
                                                n_clicks=0,
                                                style={'font-family': "Franklin Gothic"},
                                            ),
                                            dbc.Popover(
                                                "Es el número del Geotube ingresado por el usuario.",
                                                target="selec-num-GT-target",
                                                body=True,
                                                trigger="hover",
                                                style={'font-family': "Franklin Gothic"}
                                            ),

                                        ], width=2, align='center', className="d-grid gap-2"),
                                        dbc.Col([
                                            dcc.Dropdown(id='numGTDD',
                                                         options=[],
                                                         #value='6',
                                                         style={'font-family': "Franklin Gothic"}
                                                         )
                                        ], width=2, align='center'),
                                        dbc.Col([
                                            dbc.Button(
                                                "Seleccionar Día:",
                                                id="selec-dia-GT-target",
                                                color="info",
                                                className="me-1",
                                                n_clicks=0,
                                                style={'font-family': "Franklin Gothic"},
                                            ),
                                            dbc.Popover(
                                                "Es el día introducido por el usuario para conocer el resumen de la operación del Geotube para el día seleccionado. Formato DD/MM/AAAA.",
                                                target="selec-dia-GT-target",
                                                body=True,
                                                trigger="hover",
                                                style={'font-family': "Franklin Gothic"}
                                            ),

                                        ], width=2, align='center', className="d-grid gap-2"),
                                        dbc.Col([
                                            dcc.Dropdown(id='fechaGTDD',
                                                         options=[],
                                                         style={'font-family': "Franklin Gothic"}
                                                         )
                                        ], width=2, align='center'),

                                    ]),
                                    dbc.Row([
                                        dbc.Col([
                                            dbc.Button(
                                                "Capacidad:",
                                                id="dia-cap-GT-target",
                                                color="primary",
                                                className="me-1",
                                                n_clicks=0,
                                                style={'font-family': "Franklin Gothic"},
                                            ),
                                            dbc.Popover(
                                                "Es la capacidad máxima del Geotube seleccionado.",
                                                target="dia-cap-GT-target",
                                                body=True,
                                                trigger="hover",
                                                style={'font-family': "Franklin Gothic"}
                                            ),

                                        ], width=2, align='center', className="d-grid gap-2"),
                                        dbc.Col(daq.LEDDisplay(id='LED-cap-GT', color='blue', size=14, value=0),
                                                width=1),
                                        dbc.Col([html.Div(id='unidades-cap-GT')], xs=2, sm=2, md=2, lg=1, xl=1,
                                                style={'textAlign': 'center', 'font-family': "Franklin Gothic"},
                                                align='center'),
                                        dbc.Col([html.Div("")], width=3, style={'textAlign': 'center'}, align='center'),
                                        dbc.Col(daq.Tank(id="tanque-GT",
                                                         height=75,
                                                         width=370,
                                                         value=0,
                                                         min=0,
                                                         max=100,
                                                         color="brown",
                                                         showCurrentValue=True,
                                                         units="%",
                                                         style={'margin-left': '50px', 'font-family': "Franklin Gothic"}
                                                         ), xs=4, sm=4, md=4, lg=4, xl=4, )
                                    ]),
                                    dbc.Row([
                                        dbc.Col([
                                            dbc.Button(
                                                "Volumen:",
                                                id="dia-vol-GT-target",
                                                color="primary",
                                                className="me-1",
                                                n_clicks=0,
                                                style={'font-family': "Franklin Gothic"},
                                            ),
                                            dbc.Popover(
                                                "Es el volumen del Geotube para el día seleccionado.",
                                                target="dia-vol-GT-target",
                                                body=True,
                                                trigger="hover",
                                                style={'font-family': "Franklin Gothic"}
                                            ),

                                        ], width=2, align='center', className="d-grid gap-2"),
                                        dbc.Col(daq.LEDDisplay(id='LED-vol-GT', color='blue', size=14, value=0),
                                                width=1),
                                        dbc.Col([html.Div(id='unidades-vol-GT')], xs=2, sm=2, md=2, lg=1, xl=1,
                                                style={'textAlign': 'center', 'font-family': "Franklin Gothic"},
                                                align='center'),
                                        dbc.Col([
                                            dbc.Row([daq.GraduatedBar(
                                                id='barra-vol-GT',
                                                color={"ranges": {"red": [0, 4], "yellow": [4, 8], "green": [8, 10]}},
                                                showCurrentValue=False,
                                                step=0.2,
                                                value=0

                                            )]),
                                        ]),
                                    ]),
                                    dbc.Row([
                                        dbc.Col([
                                            dbc.Button(
                                                "Peso:",
                                                id="dia-peso-GT-target",
                                                color="primary",
                                                className="me-1",
                                                n_clicks=0,
                                                style={'font-family': "Franklin Gothic"},
                                            ),
                                            dbc.Popover(
                                                "Es el peso del Geotube para el día seleccionado.",
                                                target="dia-peso-GT-target",
                                                body=True,
                                                trigger="hover",
                                                style={'font-family': "Franklin Gothic"}
                                            ),

                                        ], width=2, align='center', className="d-grid gap-2"),
                                        dbc.Col(daq.LEDDisplay(id='LED-peso-GT', color='blue', size=14, value=0),
                                                width=1),
                                        dbc.Col([html.Div("Ton")], xs=2, sm=2, md=2, lg=1, xl=1,
                                                style={'textAlign': 'left', 'font-family': "Franklin Gothic"},
                                                align='center'),
                                        dbc.Col([
                                            dbc.Row([daq.GraduatedBar(
                                                id='barra-peso-GT',
                                                color={"ranges": {"red": [0, 4], "yellow": [4, 8], "green": [8, 10]}},
                                                showCurrentValue=False,
                                                step=0.2,
                                                value=0

                                            )]),
                                        ]),
                                    ]),
                                    dbc.Row([
                                        dbc.Col([
                                            dbc.Button(
                                                "Días Operados:",
                                                id="dia-oper-GT-target",
                                                color="primary",
                                                className="me-1",
                                                n_clicks=0,
                                                style={'font-family': "Franklin Gothic"},
                                            ),
                                            dbc.Popover(
                                                "Es la cantidad de días operados para el Geotube seleccionado.",
                                                target="dia-oper-GT-target",
                                                body=True,
                                                trigger="hover",
                                                style={'font-family': "Franklin Gothic"}
                                            ),

                                        ], width=2, align='center', className="d-grid gap-2"),
                                        dbc.Col(daq.LEDDisplay(id='LED-dias-oper-GT', color='blue', size=14, value=0),
                                                width=1),
                                    ]),
                                    #dbc.Row(dcc.Graph(id='fig-GT')),
                                    dbc.Row(dbc.Col(
                                        dbc.Spinner(children=[dcc.Graph(id="fig-GT")], size="lg",
                                                    color="primary", type="border", fullscreen=True, ),
                                        # spinner_style={"width": "10rem", "height": "10rem"}),
                                        # spinnerClassName="spinner"),
                                        # dcc.Loading(children=[dcc.Graph(id="loading-output")], color="#119DFF", type="dot", fullscreen=True,),

                                        width={'size': 12, 'offset': 0}),
                                    ),
                                    dbc.Row(dcc.Graph(id='fig-uso-GT')),
                                    dbc.Row([
                                        dbc.Col([
                                            dbc.Accordion([
                                                dbc.AccordionItem([

                                                    html.H5([
                                                                'Barra volumen: es el indicador de volumen del Geotube. Color de barra rojo es volumen bajo (0-33%), color de barra amarillo es volumen medio (33-66%), color de barra verde es volumen alto (66-100%).']),

                                                    html.H5([
                                                                'Barra peso: es el indicador de peso del Geotube. Color de barra rojo es peso bajo (0-33%), color de barra amarillo es peso medio (33-66%), color de barra verde es peso alto (66-100%).']),
                                                    html.H5([
                                                                'Porcentaje de llenado: es el porcentaje de llenado del Geotube para el día seleccionado.']),
                                                ], title="Descripción de Íconos"),
                                            ], start_collapsed=True,
                                                style={'color': '#082255', 'font-family': "Franklin Gothic"}),

                                        ], style={'color': '#082255', 'font-family': "Franklin Gothic"}),
                                    ]),
                                ])
                            ])
                        ])

                    ])
                ]),
            ], label="Resumen Geotube", label_style={'color': '#082255', 'font-family': "Franklin Gothic"}),
        ]),
    ]),

])


@app.callback(
    Output(component_id='Dia', component_property='options'),
    Output(component_id='Ano', component_property='options'),
    Output(component_id='fase', component_property='options'),
    Output(component_id='numGTDD', component_property='options'),
    Output(component_id='store-data-purgas', component_property='data'),
    Output(component_id='store-data-lodos', component_property='data'),
    Output(component_id='store-data-clarificado', component_property='data'),
    Output(component_id='store-data-geotube', component_property='data'),
    Output(component_id='Dia', component_property='value'),
    Output(component_id='Ano', component_property='value'),
    Output(component_id='fase', component_property='value'),
    Output(component_id='numGTDD', component_property='value'),

    Input('my_interval', 'n_intervals'),
)
def dropdownTiempoReal(value_intervals):
    start = time.time()
    names = ["Fecha", "Hora Inicio", "Hora Fin", "Altura Inicial [m]", "Altura Final [m]", "Tiempo [min]",
             "Volumen [m3]",
             "Volumen [gal]", "Volumen acumulado [m3]", "Volumen acumulado [gal]", "Tiempo acumulado [min]",
             "Total Purgas Captadas", "Fase", "", "", "", "Fecha", "Hora Inicio", "Hora Fin", "Altura Inicial [m]",
             "Altura Final [m]", "Tiempo [min]",
             "Volumen [m3]",
             "Volumen [gal]", "Volumen acumulado [m3]", "Volumen acumulado [gal]", "Tiempo acumulado [min]",
             "Total Purgas Bombeadas", "Fase", "", "", "", "Fecha", "Hora Inicio", "Hora Fin", "Lectura Inicial",
             "Lectura Final", "Turbidez [NTU]", "Color [Pt-Co]",
             "pH", "Tiempo [min]", "Volumen [m3]", "Volumen [gal]", "Tiempo Acumulado [min]", "Volumen Acumulado [m3]",
             "Volumen Acumulado [gal]", "Fase", "", "", "", "Fase", "Numero", "Largo", "Ancho", "Fecha", "Hora",
             "Altura Promedio", "Volumen Teórico [m3]", "% Uso", "Peso [Ton]", "Capacidad [m3]", "Referencia"]

    # Extraer Fases 1, 2, 3 y 4 del archivo csv
    start = time.time()
    dfCOMBINADO2 = pd.read_excel('Datos_PTAP_Fase1_Fase2_Fase3_Fase4.xlsx')
    dfCOMBINADO2.columns = [names]
    dfCOMBINADO2 = pd.DataFrame(dfCOMBINADO2)


    dfPURG49 = dfCOMBINADO2.iloc[:, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]]
    dfLDS49 = dfCOMBINADO2.iloc[:, [16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28]]
    dfCLR49 = dfCOMBINADO2.iloc[:, [32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46]]
    dfGT49 = dfCOMBINADO2.iloc[:, [50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61]]

    dfPURG49 = dfPURG49.replace(to_replace='None', value=np.nan).dropna(axis=0, how="all")
    dfLDS49 = dfLDS49.replace(to_replace='None', value=np.nan).dropna(axis=0, how="all")
    dfCLR49 = dfCLR49.replace(to_replace='None', value=np.nan).dropna(axis=0, how="all")
    dfGT49 = dfGT49.replace(to_replace='None', value=np.nan).dropna(axis=0, how="all")

    # Extraer Fase 5 de google sheets
    #SERVICE_ACCOUNT_FILE = 'keys.json'
    SERVICE_ACCOUNT_FILE = 'keys-PTAP.json'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    creds = None
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    # The ID spreadsheet.
    #SAMPLE_SPREADSHEET_ID = '1uHo9KZbHzh1QXidL1-2c6uNjK4plKZHAM9GaPc8pcok'
    SAMPLE_SPREADSHEET_ID = '1hT5gjZ8QES6GtPmnoxhmR3NG8xyzf0kFUfd7sunzV70'

    #SAMPLE_RANGE_COMBINADO = "Combinado"
    SAMPLE_RANGE_COMBINADO = "Fase 5"

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result_COMBINADO = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                           range=SAMPLE_RANGE_COMBINADO).execute()

    dfCOMBINADO3 = result_COMBINADO.get('values', [])

    dfCOMBINADO3 = pd.DataFrame(dfCOMBINADO3, columns=names)
    dfCOMBINADO3 = dfCOMBINADO3.apply(lambda x: x.str.replace(",", ".")).apply(pd.to_numeric, errors='ignore')

    dfCOMBINADO3.drop([0], inplace=True)
    dfCOMBINADO3 = dfCOMBINADO3.rename(index=lambda x: x - 1)

    dfPURG50 = dfCOMBINADO3.iloc[:, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]]
    dfLDS50 = dfCOMBINADO3.iloc[:, [16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28]]
    dfCLR50 = dfCOMBINADO3.iloc[:, [32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46]]
    dfGT50 = dfCOMBINADO3.iloc[:, [50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61]]

    dfPURG50 = dfPURG50.replace(to_replace='None', value=np.nan).dropna(axis=0, how="all")
    dfLDS50 = dfLDS50.replace(to_replace='None', value=np.nan).dropna(axis=0, how="all")
    dfCLR50 = dfCLR50.replace(to_replace='None', value=np.nan).dropna(axis=0, how="all")
    dfGT50 = dfGT50.replace(to_replace='None', value=np.nan).dropna(axis=0, how="all")

    dfPURG49 = dfPURG49.to_numpy()
    dfPURG50 = dfPURG50.to_numpy()

    dfPURGopti = np.concatenate((dfPURG49, dfPURG50))
    dfPURGopti = pd.DataFrame(dfPURGopti,  columns =["Fecha", "Hora Inicio", "Hora Fin", "Altura Inicial [m]", "Altura Final [m]", "Tiempo [min]",
              "Volumen [m3]",
              "Volumen [gal]", "Volumen acumulado [m3]", "Volumen acumulado [gal]", "Tiempo acumulado [min]",
              "Total Purgas Captadas", "Fase"])

    dfPURGopti = dfPURGopti.astype({"Fecha": str, "Hora Inicio": str, "Hora Fin": str,
         "Altura Inicial [m]": float, "Altura Final [m]": float,
                                 "Tiempo [min]": 'int64', "Volumen [m3]": float, "Volumen [gal]": float,
                                 "Volumen acumulado [m3]": float, "Volumen acumulado [gal]": float,
                                 "Tiempo acumulado [min]": 'int64', "Total Purgas Captadas": 'int64',
                                 "Fase": 'int64'
                                 })

    dfLDS49 = dfLDS49.to_numpy()
    dfLDS50 = dfLDS50.to_numpy()

    dfLDSopti = np.concatenate((dfLDS49, dfLDS50))
    dfLDSopti = pd.DataFrame(dfLDSopti,  columns =["Fecha", "Hora Inicio", "Hora Fin", "Altura Inicial [m]",
              "Altura Final [m]", "Tiempo [min]",
              "Volumen [m3]",
              "Volumen [gal]", "Volumen acumulado [m3]", "Volumen acumulado [gal]", "Tiempo acumulado [min]",
              "Total Purgas Bombeadas", "Fase"])


    dfCLR49 = dfCLR49.to_numpy()
    dfCLR50 = dfCLR50.to_numpy()

    dfCLRopti = np.concatenate((dfCLR49, dfCLR50))
    dfCLRopti = pd.DataFrame(dfCLRopti,  columns =["Fecha", "Hora Inicio", "Hora Fin", "Lectura Inicial",
              "Lectura Final", "Turbidez [NTU]", "Color [Pt-Co]",
              "pH", "Tiempo [min]", "Volumen [m3]", "Volumen [gal]", "Tiempo Acumulado [min]", "Volumen Acumulado [m3]",
              "Volumen Acumulado [gal]", "Fase"])


    dfGT49 = dfGT49.to_numpy()
    dfGT50 = dfGT50.to_numpy()

    dfGTopti = np.concatenate((dfGT49, dfGT50))
    dfGTopti = pd.DataFrame(dfGTopti,  columns =["Fase", "Numero", "Largo", "Ancho", "Fecha", "Hora",
              "Altura Promedio", "Volumen Teórico [m3]", "% Uso", "Peso [Ton]", "Capacidad [m3]", "Referencia"])

    dfPURG = dfPURGopti
    dfLDS = dfLDSopti
    dfCLR = dfCLRopti
    dfGT = dfGTopti

    end = time.time()
    t = end - start
    print('Tiempo optimizado es:')
    print(t)

    # convertir datos de string a tipo fecha
    fechaPURG = dfPURG.loc[:, "Fecha"]
    fechaCLR = dfCLR.loc[:, "Fecha"]
    fechaLDS = dfLDS.loc[:, "Fecha"]
    fechaGT = dfGT.loc[:, "Fecha"]

    ultAct = dfCLR["Fecha"].iloc[-1]
    ultAct = str(ultAct)


    fechaCLRdd = list(dict.fromkeys(fechaCLR))

    fechaGTdd = list(dict.fromkeys(fechaGT))

    fechaPURG = list(map(lambda fecha: datetime.strptime(fecha, "%d/%m/%Y"), fechaPURG))
    fechaCLR = list(map(lambda fecha: datetime.strptime(fecha, "%d/%m/%Y"), fechaCLR))
    fechaLDS = list(map(lambda fecha: datetime.strptime(fecha, "%d/%m/%Y"), fechaLDS))
    fechaGT = list(map(lambda fecha: datetime.strptime(fecha, "%d/%m/%Y"), fechaGT))

    fechaPURGdd = list(dict.fromkeys(fechaPURG))
    fechaPURGdd.sort(reverse=True)
    fechaPURGdd = list(map(lambda fecha: str(fecha.day) + "/" + str(fecha.month) + "/" + str(fecha.year), fechaPURGdd))


    # Obtiene la lista de los años que se han trabajado
    anosfechaLDS = list(map(lambda fecha: fecha.year, fechaLDS))

    anosfechaLDS = list(dict.fromkeys(anosfechaLDS))
    anosfechaLDS.sort(reverse=True)
    fasedd = list(dict.fromkeys(dfLDS["Fase"]))

    m3GTvec = dfGT.loc[:, "Volumen Teórico [m3]"]  # vector de volumen teórico de Geotube
    usoGTvec = dfGT.loc[:, "% Uso"]  # vector de volumen teórico de Geotube
    pesoGTvec = dfGT.loc[:, "Peso [Ton]"]  # vector de volumen teórico de Geotube
    numGTvec = dfGT.loc[:, "Numero"]
    capGTvec = dfGT.loc[:, "Capacidad [m3]"]

    m3GTvec = list(map(lambda x: float(x), m3GTvec))
    usoGTvec = list(map(lambda x: float(x), usoGTvec))
    pesoGTvec = list(map(lambda x: float(x), pesoGTvec))
    numGTvec = list(map(lambda x: float(x), numGTvec))
    capGTvec = list(map(lambda x: float(x), capGTvec))

    numGTdd = list(dict.fromkeys(numGTvec))
    numGTdd.sort(reverse=True)
    fasedd = list(dict.fromkeys(dfPURG["Fase"]))
    fasedd.sort(reverse=True)

    # Calcula último día operado
    diaHoy = fechaPURG[-1]
    diaHoy = str(diaHoy.day) + "/" + str(diaHoy.month) + "/" + str(diaHoy.year)

    # Calcula último año operado
    anoHoy = fechaPURG[-1]
    anoHoy = anoHoy.year

    # Calcula última fase operada
    faseHoy = fasedd[0]

    # Devuelve último geotube utilizado
    GTHoy = numGTdd[0]


    return fechaPURGdd, anosfechaLDS, fasedd, numGTdd, dfPURG.to_dict('records'), dfLDS.to_dict('records'), \
           dfCLR.to_dict('records'), dfGT.to_dict('records'), diaHoy, anoHoy, faseHoy, GTHoy


@app.callback(
    Output('meses', 'options'),
    Input(component_id='Ano', component_property='value'),
    Input(component_id='store-data-purgas', component_property='data'),
    Input(component_id='store-data-lodos', component_property='data'),
    Input(component_id='store-data-clarificado', component_property='data'),
    Input(component_id='store-data-geotube', component_property='data'),
)
def Selec_mes_interactivo(value_ano, data1, data2, data3, data4):
    data1 = pd.DataFrame(data1)
    data2 = pd.DataFrame(data2)
    data3 = pd.DataFrame(data3)
    data4 = pd.DataFrame(data4)

    dfPURG = data1
    dfLDS = data2
    dfCLR = data3
    dfGT = data4

    # convertir datos de string a tipo fecha
    fechaLDS = dfLDS.loc[:, "Fecha"]
    fechaLDS = list(map(lambda fecha: datetime.strptime(fecha, "%d/%m/%Y"), fechaLDS))

    meses_selec = []
    for x in fechaLDS:
        if x.year == value_ano:
            y = x.month
            meses_selec.append(y)

    meses_selec = list(dict.fromkeys(meses_selec))
    meses_selec.sort(reverse=True)

    # Calcula último mes operado
    mesHoy = str(meses_selec[-1])


    return [{'label': c, 'value': c} for c in meses_selec]



@app.callback(
    Output('meses', 'value'),
    Input('meses', 'options'),
)
def set_Mes_fecha_value(mes_selec):
    x = mes_selec[0]
    x = x["value"]
    return x


@app.callback(
    Output('fechaGTDD', 'options'),
    Input(component_id='numGTDD', component_property='value'),
    Input(component_id='store-data-purgas', component_property='data'),
    Input(component_id='store-data-lodos', component_property='data'),
    Input(component_id='store-data-clarificado', component_property='data'),
    Input(component_id='store-data-geotube', component_property='data'),
)
def Num_Geotube_interactivo(value_numGT, data1, data2, data3, data4):
    data1 = pd.DataFrame(data1)
    data2 = pd.DataFrame(data2)
    data3 = pd.DataFrame(data3)
    data4 = pd.DataFrame(data4)

    dfPURG = data1
    dfLDS = data2
    dfCLR = data3
    dfGT = data4


    dff = dfGT[dfGT.Numero == str(value_numGT)]
    dff = dff["Fecha"]

    dff = list(dict.fromkeys(dff))
    dff = list(map(lambda fecha: datetime.strptime(fecha, "%d/%m/%Y"), dff))
    dff.sort(reverse=True)
    dff = list(map(lambda fecha: str(fecha.day) + "/" + str(fecha.month) + "/" + str(fecha.year), dff))

    return [{'label': c, 'value': c} for c in dff]


@app.callback(
    Output('fechaGTDD', 'value'),
    Input('fechaGTDD', 'options'),
)
def set_Geotube_fecha_value(fecha_selec):
    x = fecha_selec[0]
    x = x["value"]
    return x


@app.callback(

    Output(component_id='mi-acum-vol', component_property="figure"),
    Output(component_id='mi-acum-prop', component_property="figure"),
    Output(component_id='fig-GT', component_property="figure"),
    Output(component_id='fig-uso-GT', component_property="figure"),
    Output(component_id='LED-pH-dia', component_property="value"),
    Output(component_id='barra-pH-dia', component_property="value"),
    Output(component_id='LED-turb-dia', component_property="value"),
    Output(component_id='barra-turb-dia', component_property="value"),
    Output(component_id='LED-color-dia', component_property="value"),
    Output(component_id='barra-color-dia', component_property="value"),
    Output(component_id='LED-aguatrat-dia', component_property="value"),
    Output(component_id='barra-aguatrat-dia', component_property="value"),
    Output(component_id='LED-purgcapt-dia', component_property="value"),
    Output(component_id='LED-volcapt-dia', component_property="value"),
    Output(component_id='LED-bomb-dia', component_property="value"),
    Output(component_id='LED-volret-dia', component_property="value"),
    Output(component_id='LED-purgcapt-mes', component_property="value"),
    Output(component_id='LED-volcapt-mes', component_property="value"),
    Output(component_id='LED-bomb-mes', component_property="value"),
    Output(component_id='LED-volret-mes', component_property="value"),
    Output(component_id='LED-pH-mes', component_property="value"),
    Output(component_id='LED-turb-mes', component_property="value"),
    Output(component_id='LED-color-mes', component_property="value"),
    Output(component_id='LED-aguatrat-mes', component_property="value"),
    Output(component_id='LED-dias-mes', component_property="value"),
    Output(component_id='barra-pH-mes', component_property="value"),
    Output(component_id='barra-turb-mes', component_property="value"),
    Output(component_id='barra-color-mes', component_property="value"),
    Output(component_id='barra-aguatrat-mes', component_property="value"),
    Output(component_id='LED-purgcapt-fase', component_property="value"),
    Output(component_id='LED-volcapt-fase', component_property="value"),
    Output(component_id='LED-bomb-fase', component_property="value"),
    Output(component_id='LED-volret-fase', component_property="value"),
    Output(component_id='LED-pH-fase', component_property="value"),
    Output(component_id='LED-turb-fase', component_property="value"),
    Output(component_id='LED-color-fase', component_property="value"),
    Output(component_id='LED-aguatrat-fase', component_property="value"),
    Output(component_id='LED-dias-fase', component_property="value"),
    Output(component_id='barra-pH-fase', component_property="value"),
    Output(component_id='barra-turb-fase', component_property="value"),
    Output(component_id='barra-color-fase', component_property="value"),
    Output(component_id='barra-aguatrat-fase', component_property="value"),
    Output(component_id='LED-purgcapt-acum', component_property="value"),
    Output(component_id='LED-volcapt-acum', component_property="value"),
    Output(component_id='LED-bomb-acum', component_property="value"),
    Output(component_id='LED-volret-acum', component_property="value"),
    Output(component_id='LED-pH-acum', component_property="value"),
    Output(component_id='LED-turb-acum', component_property="value"),
    Output(component_id='LED-color-acum', component_property="value"),
    Output(component_id='LED-aguatrat-acum', component_property="value"),
    Output(component_id='LED-dias-acum', component_property="value"),
    Output(component_id='barra-pH-acum', component_property="value"),
    Output(component_id='barra-turb-acum', component_property="value"),
    Output(component_id='barra-color-acum', component_property="value"),
    Output(component_id='barra-aguatrat-acum', component_property="value"),
    Output(component_id='LED-cap-GT', component_property="value"),
    Output(component_id='LED-vol-GT', component_property="value"),
    Output(component_id='LED-peso-GT', component_property="value"),

    Output(component_id='unidades-volcapt-dia', component_property='children'),
    Output(component_id='unidades-volret-dia', component_property='children'),
    Output(component_id='unidades-volcapt-mes', component_property='children'),
    Output(component_id='unidades-volret-mes', component_property='children'),
    Output(component_id='unidades-volcapt-fase', component_property='children'),
    Output(component_id='unidades-volret-fase', component_property='children'),
    Output(component_id='unidades-volcapt-acum', component_property='children'),
    Output(component_id='unidades-volret-acum', component_property='children'),
    Output(component_id='unidades-cap-GT', component_property='children'),
    Output(component_id='barra-vol-GT', component_property='value'),
    Output(component_id='barra-peso-GT', component_property='value'),
    Output(component_id='unidades-vol-GT', component_property='children'),
    Output(component_id='tanque-GT', component_property='value'),

    Output(component_id='LED-lodos-confinados-dia', component_property="value"),
    Output(component_id='LED-geotube-utilizados-mes', component_property="value"),
    Output(component_id='LED-lodos-confinados-mes', component_property="value"),
    Output(component_id='LED-geotube-utilizados-fase', component_property="value"),
    Output(component_id='LED-lodos-confinados-fase', component_property="value"),
    Output(component_id='LED-geotube-utilizados-acum', component_property="value"),
    Output(component_id='LED-lodos-confinados-acum', component_property="value"),

    Output(component_id='dia-inicial-fase', component_property="children"),
    Output(component_id='dia-final-fase', component_property="children"),
    Output(component_id='dia-inicial-acum', component_property="children"),
    Output(component_id='dia-final-acum', component_property="children"),

    Output(component_id='mi-mes-vol', component_property="figure"),
    Output(component_id='mi-mes-prop', component_property="figure"),
    Output(component_id='mi-fase-vol', component_property="figure"),
    Output(component_id='mi-fase-prop', component_property="figure"),

    Output(component_id='mi-mes-lodos', component_property="figure"),
    Output(component_id='mi-fase-lodos', component_property="figure"),
    Output(component_id='mi-acum-lodos', component_property="figure"),
    Output(component_id='LED-dias-oper-GT', component_property="value"),

    Input(component_id='Dia', component_property='value'),
    Input(component_id='unidades-input', component_property='value'),
    Input(component_id='meses', component_property='value'),
    Input(component_id='unidades-mes-input', component_property='value'),
    Input(component_id='Ano', component_property='value'),
    Input(component_id='unidades-acum-input', component_property='value'),
    Input(component_id='unidades-fase-input', component_property='value'),
    Input(component_id='fase', component_property='value'),
    Input('fechaGTDD', 'value'),
    Input('numGTDD', 'value'),
    Input('unidades-GT-input', 'value'),
    Input('my_interval', 'n_intervals'),
    Input(component_id='store-data-purgas', component_property='data'),
    Input(component_id='store-data-lodos', component_property='data'),
    Input(component_id='store-data-clarificado', component_property='data'),
    Input(component_id='store-data-geotube', component_property='data'),

)
def dashboard_interactivo(value_dia, value_unidades, value_mes, value_unidades_mes, value_año, value_unidades_acum,
                          value_unidades_fase, value_fase, value_fechaGT, value_numGT, value_unidades_GT,
                          value_intervals, data1, data2, data3, data4):
    start = time.time()
    data1 = pd.DataFrame(data1)
    data2 = pd.DataFrame(data2)
    data3 = pd.DataFrame(data3)
    data4 = pd.DataFrame(data4)

    dfPURG = data1
    dfLDS = data2
    dfCLR = data3
    dfGT = data4

    # Cambiar comas a puntos
    # dfPURG = dfPURG.apply(lambda x: x.replace(",", ".")).apply(pd.to_numeric, errors='ignore')
    # dfLDS = dfLDS.apply(lambda x: x.replace(",", ".")).apply(pd.to_numeric, errors='ignore')
    # dfCLR = dfCLR.apply(lambda x: x.replace(",", ".")).apply(pd.to_numeric, errors='ignore')
    # dfGT = dfGT.apply(lambda x: x.replace(",", ".")).apply(pd.to_numeric, errors='ignore')


    # convertir datos de string a tipo fecha
    y = dfCLR["Fecha"]
    print('y')
    print(y)
    print(type(y))
    ultAct = dfCLR["Fecha"].iloc[-1]
    ultAct = str(ultAct)

    # convertir datos de string a tipo numérico decimal
    galCLRvec = dfCLR.loc[:, "Volumen [gal]"]  # vector de los galones bombeados al clrificador
    pHCLRvec = dfCLR.loc[:, "pH"]  # vector del pH de agua clarificada
    turbCLRvec = dfCLR.loc[:, "Turbidez [NTU]"]  # vector de la turbidez de agua clarificada
    colorCLRvec = dfCLR.loc[:, "Color [Pt-Co]"]  # vector del color de agua clarificada

    galCLRvec = list(map(lambda x: float(x), galCLRvec))
    pHCLRvec = list(map(lambda x: float(x), pHCLRvec))
    turbCLRvec = list(map(lambda x: float(x), turbCLRvec))
    colorCLRvec = list(map(lambda x: float(x), colorCLRvec))

    galPURGvec = dfPURG.loc[:, "Volumen [gal]"]  # vector de los galones captados del clarificador
    galPURGvec = list(map(lambda x: float(x), galPURGvec))

    # --------------------------------- Módulo 1 ------------------------------------------

    # Calcula las purgas captadas para un día determinado & volumen [gal] total para un día determinado
    fechaDIA = value_dia

    print('fechaDIA')
    print(fechaDIA)

    #print('dfLDS')
    #print(dfLDS)
    #print('dfPURG')
    #print(dfPURG)

    dfLDSfecha = dfLDS[dfLDS["Fecha"] == fechaDIA]
    dfPURGfecha = dfPURG[dfPURG["Fecha"] == fechaDIA]

    print('dfLDSfecha')
    print(dfLDSfecha)
    print('dfPURGfecha')
    print(dfPURGfecha)

    purgsdiaLDS = len(dfPURGfecha["Fecha"])

    galdiaLDSacum = dfLDSfecha["Volumen [gal]"]
    galdiaLDSacum = list(map(lambda x: float(x), galdiaLDSacum))
    galdiaLDSacum25 = round(sum(galdiaLDSacum), 0)
    galdiaLDSacum = round(sum(galdiaLDSacum), 0)

    # Calcula los bombeos de clarificado para un día determinado & volumen [gal] total de bombeo de clarificado para un día determinado & turbidez, color y pH de agua clarificada para un día determinado
    dfCLRfecha = dfCLR[dfCLR["Fecha"] == fechaDIA]

    purgsdiaCLR = len(dfCLRfecha["Fecha"])
    galdiaCLRacum = dfCLRfecha["Volumen [gal]"]
    galdiaCLRacum = list(map(lambda x: float(x), galdiaCLRacum))
    galdiaCLRacum = round(sum(galdiaCLRacum, 0))

    pHdiaCLRprom = dfCLRfecha["pH"]
    pHdiaCLRprom = list(map(lambda x: float(x), pHdiaCLRprom))
    pHdiaCLRprom = round(sum(pHdiaCLRprom) / len(pHdiaCLRprom), 2)

    turbdiaCLRprom = dfCLRfecha["Turbidez [NTU]"]
    turbdiaCLRprom = list(map(lambda x: float(x), turbdiaCLRprom))
    turbdiaCLRprom = round(sum(turbdiaCLRprom) / len(turbdiaCLRprom), 2)

    colordiaCLRprom = dfCLRfecha["Color [Pt-Co]"]
    colordiaCLRprom = list(map(lambda x: float(x), colordiaCLRprom))
    colordiaCLRprom = round(sum(colordiaCLRprom) / len(colordiaCLRprom), 2)

    prctOutDiavec = [0.052, 0.061, 0.078, 0.1, 0.074, 0.064, 0.058, 0.05, 0.053, 0.084, 0.082, 0.061]

    # Calcula porcentaje de agua tratada
    prctaguatratdia = galdiaCLRacum / galdiaLDSacum * 100
    prctaguatratdia = round(prctaguatratdia, 1)

    if prctaguatratdia > 100:
        prctaguatratdia = 100

    # Cambia unidades a m3 por radioitem
    suffix_galdiaacum_dia = "gal"
    if value_unidades == False:
        galdiaLDSacum = round(galdiaLDSacum / 264.72, 0)
        galdiaCLRacum = round(galdiaCLRacum / 264.72, 0)
        suffix_galdiaacum_dia = "m3"

    # --------------------------------- Módulo 2 ------------------------------------------

    # Calcula las purgas captadas para un mes determinado & volumen [gal] total para un mes determinado
    mes = value_mes
    año = value_año

    dfPURGfechames = dfPURG["Fecha"]
    fechasmes = [x for x in dfPURGfechames if
                 (datetime.strptime(x, "%d/%m/%Y").month == mes) and (datetime.strptime(x, "%d/%m/%Y").year == año)]

    dfPURGmes = dfPURG[dfPURG.Fecha.isin(fechasmes)]
    dfLDSmes = dfLDS[dfLDS.Fecha.isin(fechasmes)]
    purgsmesLDS = len(dfPURGmes["Fecha"])

    galmesLDSacum = dfLDSmes["Volumen [gal]"]
    galmesLDSacum = list(map(lambda x: float(x), galmesLDSacum))
    galmesLDSacum25 = round(sum(galmesLDSacum), 0)
    galmesLDSacum = round(sum(galmesLDSacum), 0)

    # Calcula los bombeos de clarificado para un mes determinado & volumen [gal] total de bombeo de clarificado para un mes determinado & turbidez, color y pH de agua clarificada para un día determinado
    dfCLRmes = dfCLR[dfCLR.Fecha.isin(fechasmes)]

    purgsmesCLR = len(dfCLRmes["Fecha"])
    galmesCLRacum = dfCLRmes["Volumen [gal]"]
    galmesCLRacum = list(map(lambda x: float(x), galmesCLRacum))
    galmesCLRacum = round(sum(galmesCLRacum, 0))

    pHmesCLRprom = dfCLRmes["pH"]
    pHmesCLRprom = list(map(lambda x: float(x), pHmesCLRprom))
    pHmesCLRprom = round(sum(pHmesCLRprom) / len(pHmesCLRprom), 2)

    turbmesCLRprom = dfCLRmes["Turbidez [NTU]"]
    turbmesCLRprom = list(map(lambda x: float(x), turbmesCLRprom))
    turbmesCLRprom = round(sum(turbmesCLRprom) / len(turbmesCLRprom), 2)

    colormesCLRprom = dfCLRmes["Color [Pt-Co]"]
    colormesCLRprom = list(map(lambda x: float(x), colormesCLRprom))
    colormesCLRprom = round(sum(colormesCLRprom) / len(colormesCLRprom), 2)

    # Cuenta los días trabajados en un mes
    diasMes = len(dict.fromkeys(dfCLRmes["Fecha"]))

    # Calcula el porcentaje de agua tratada proveniente de las purgas en el mes
    prctaguatratmes = galmesCLRacum / galmesLDSacum * 100
    prctaguatratmes = round(prctaguatratmes, 1)

    if prctaguatratmes > 100:
        prctaguatratmes = 100

    # Cambia unidades a m3 por radioitem
    suffix_galdiaacum_mes = "gal"
    yaxis_label = "Volumen [gal]"
    if value_unidades_mes == False:
        galmesLDSacum = round(galmesLDSacum / 264.72, 0)
        galmesCLRacum = round(galmesCLRacum / 264.72, 0)
        suffix_galdiaacum_mes = "m3"
        yaxis_label = "Volumen [m3]"

    # Crea vector de fechas para la gráfica
    fechaMesLDS45 = dfLDSmes["Fecha"]
    fechaMesCLR45 = dfCLRmes["Fecha"]

    fechaMesLDS45 = list(dict.fromkeys(fechaMesLDS45))
    fechaMesCLR45 = list(dict.fromkeys(fechaMesCLR45))

    # Calcula los galones totales acumulados enviados por día
    # Calcula la turbidez, color y pH promedios de agua clarificada enviados por día acumulado

    galMesCLRylbl45 = [None]
    pHMesCLRylbl45 = [None]
    turbMesCLRylbl45 = [None]
    colorMesCLRylbl45 = [None]

    for i in fechaMesCLR45:
        dffechaMesCLR = dfCLRmes[dfCLRmes["Fecha"] == i]

        galMesCLRvec45 = dffechaMesCLR["Volumen [gal]"]
        galMesCLRvec45 = list(map(lambda x: float(x), galMesCLRvec45))
        galMesCLRacum45 = sum(galMesCLRvec45)

        colorMesCLRprom = dffechaMesCLR["Color [Pt-Co]"]
        colorMesCLRprom = list(map(lambda x: float(x), colorMesCLRprom))
        colorMesCLRprom = sum(colorMesCLRprom) / len(colorMesCLRprom)

        pHMesCLRprom = dffechaMesCLR["pH"]
        pHMesCLRprom = list(map(lambda x: float(x), pHMesCLRprom))
        pHMesCLRprom = sum(pHMesCLRprom) / len(pHMesCLRprom)

        turbMesCLRprom = dffechaMesCLR["Turbidez [NTU]"]
        turbMesCLRprom = list(map(lambda x: float(x), turbMesCLRprom))
        turbMesCLRprom = sum(turbMesCLRprom) / len(turbMesCLRprom)

        galMesCLRylbl45.append(galMesCLRacum45)
        colorMesCLRylbl45.append(colorMesCLRprom)
        pHMesCLRylbl45.append(pHMesCLRprom)
        turbMesCLRylbl45.append(turbMesCLRprom)

    galMesCLRylbl45.remove(None)
    colorMesCLRylbl45.remove(None)
    pHMesCLRylbl45.remove(None)
    turbMesCLRylbl45.remove(None)

    # Calcula los galones totales captados enviados por día
    galMesLDSylbl45 = [None]

    for i in fechaMesLDS45:
        dffechaMesLDS = dfLDSmes[dfLDSmes["Fecha"] == i]
        galMesLDSacum45 = dffechaMesLDS["Volumen [gal]"]
        galMesLDSacum45 = list(map(lambda x: float(x), galMesLDSacum45))
        galMesLDSacum45 = sum(galMesLDSacum45)
        galMesLDSylbl45.append(galMesLDSacum45)

    galMesLDSylbl45.remove(None)

    fechaMesLDS45 = list(map(lambda fecha: datetime.strptime(fecha, "%d/%m/%Y"), fechaMesLDS45))
    fechaMesCLR45 = list(map(lambda fecha: datetime.strptime(fecha, "%d/%m/%Y"), fechaMesCLR45))

    # Cambia unidades a m3 por radioitem
    nameFigCLRMes = "Volumen retornado de agua clarificada [gal]"
    nameFigLDSMes = "Volumen captado de agua lodosa [gal]"
    yaxis_labelMes = "Volumen [gal]"
    if value_unidades_mes == False:
        galMesCLRylbl45 = [number / 264.72 for number in galMesCLRylbl45]
        galMesLDSylbl45 = [number / 264.72 for number in galMesLDSylbl45]
        yaxis_labelMes = "Volumen [m3]"
        nameFigCLRMes = "Volumen retornado de agua clarificada [m3]"
        nameFigLDSMes = "Volumen captado de agua lodosa [m3]"

    # Crea la figura de el volumen captado y retornado
    figMesvol = go.Figure()

    figMesvol.add_trace(go.Scatter(x=fechaMesCLR45, y=galMesCLRylbl45, name=nameFigCLRMes))
    figMesvol.add_trace(go.Scatter(x=fechaMesLDS45, y=galMesLDSylbl45, name=nameFigLDSMes))
    figMesvol.update_layout(title="Agua Captada/Retornada Mensual", xaxis_title="Fecha",
                            yaxis_title=yaxis_labelMes)
    figMesvol.update_layout(legend=dict(
        yanchor="bottom",
        y=-0.5,
        xanchor="center",
        x=0.5
    ))

    figMesvol.update_layout(
        font_family="Franklin Gothic",
        title_font_family="Franklin Gothic",
    )
    figMesvol.update_xaxes(title_font_family="Franklin Gothic")

    # Crea la figura de las propiedades de agua retornada
    figMesprop = go.Figure()
    figMesprop.add_trace(go.Scatter(x=fechaMesCLR45, y=pHMesCLRylbl45, name="pH"))
    figMesprop.add_trace(go.Scatter(x=fechaMesCLR45, y=colorMesCLRylbl45, name="Color [Pt-Co]"))
    figMesprop.add_trace(go.Scatter(x=fechaMesCLR45, y=turbMesCLRylbl45, name="Turbidez [NTU]"))
    figMesprop.update_layout(title="Propiedades de Agua Clarificada", xaxis_title="Fecha")
    figMesprop.update_layout(legend=dict(orientation="h",
                                         yanchor="bottom",
                                         y=-0.5,
                                         xanchor="center",
                                         x=0.5
                                         ))

    figMesprop.update_layout(
        font_family="Franklin Gothic",
        title_font_family="Franklin Gothic",
    )
    figMesprop.update_xaxes(title_font_family="Franklin Gothic")

    # --------------------------------- Módulo 3 ------------------------------------------
    # Calcula las purgas totales captadas
    purgstotLDS = len(galPURGvec)

    # Calcula los galones totales de agua lodosa captados
    galLDSvec = dfLDS["Volumen [gal]"]
    galLDSvec = list(map(lambda x: float(x), galLDSvec))
    galtotLDSacum = round(sum(galLDSvec), 0)

    # Calcula los bombeos de clarificado totales
    purgstotCLR = len(galCLRvec)

    # Calcula los galones totales de clarificado retornados
    galtotCLRacum = round(sum(galCLRvec), 0)

    # Calcula el pH de clarificado total acumulado promedio
    pHtotCLRprom = round(sum(pHCLRvec) / len(pHCLRvec), 2)

    # Calcula la turbidez de clarificado total acumulado promedio
    turbtotCLRprom = round(sum(turbCLRvec) / len(turbCLRvec), 2)

    # Calcula el color de clarificado total acumulado promedio
    colortotCLRprom = round(sum(colorCLRvec) / len(colorCLRvec), 2)

    # Calcula los galones totales acumulados enviados por día
    # Calcula la turbidez, color y pH promedios de agua clarificada enviados por día acumulado

    fechaCLR45 = dfCLR["Fecha"]
    fechaCLR45 = list(dict.fromkeys(fechaCLR45))
    galCLRylbl45 = [None]
    pHCLRylbl45 = [None]
    turbCLRylbl45 = [None]
    colorCLRylbl45 = [None]

    for i in fechaCLR45:
        dffechaCLR = dfCLR[dfCLR["Fecha"] == i]

        galCLRvec45 = dffechaCLR["Volumen [gal]"]
        galCLRvec45 = list(map(lambda x: float(x), galCLRvec45))
        galCLRacum45 = sum(galCLRvec45)

        colorCLRprom = dffechaCLR["Color [Pt-Co]"]
        colorCLRprom = list(map(lambda x: float(x), colorCLRprom))
        colorCLRprom = sum(colorCLRprom) / len(colorCLRprom)

        pHCLRprom = dffechaCLR["pH"]
        pHCLRprom = list(map(lambda x: float(x), pHCLRprom))
        pHCLRprom = sum(pHCLRprom) / len(pHCLRprom)

        turbCLRprom = dffechaCLR["Turbidez [NTU]"]
        turbCLRprom = list(map(lambda x: float(x), turbCLRprom))
        turbCLRprom = sum(turbCLRprom) / len(turbCLRprom)

        galCLRylbl45.append(galCLRacum45)
        colorCLRylbl45.append(colorCLRprom)
        pHCLRylbl45.append(pHCLRprom)
        turbCLRylbl45.append(turbCLRprom)

    galCLRylbl45.remove(None)
    colorCLRylbl45.remove(None)
    pHCLRylbl45.remove(None)
    turbCLRylbl45.remove(None)

    # Calcula los galones totales captados enviados por día
    galLDSylbl45 = [None]
    fechaLDS45 = dfLDS["Fecha"]
    fechaLDS45 = list(dict.fromkeys(fechaLDS45))

    for i in fechaLDS45:
        dffechaLDS = dfLDS[dfLDS["Fecha"] == i]
        galLDSacum45 = dffechaLDS["Volumen [gal]"]
        galLDSacum45 = list(map(lambda x: float(x), galLDSacum45))
        galLDSacum45 = sum(galLDSacum45)
        galLDSylbl45.append(galLDSacum45)

    galLDSylbl45.remove(None)
    fechaLDS45 = list(map(lambda fecha: datetime.strptime(fecha, "%d/%m/%Y"), fechaLDS45))
    fechaCLR45 = list(map(lambda fecha: datetime.strptime(fecha, "%d/%m/%Y"), fechaCLR45))

    # Obtiene el flujo de entrada promedio del al clarificador
    galInCLRacum = 2527  # [GPM]

    # Calcula la diferencia entre el último y el primer día trabajado
    datediff = fechaCLR45[-1] - fechaCLR45[0]
    datediff = datediff.days

    # Calcula el porcentaje de agua tratada de las purgas acumulado
    prctaguatrattot = galtotCLRacum / galtotLDSacum * 100
    prctaguatrattot = round(prctaguatrattot, 1)

    if prctaguatrattot > 100:
        prctaguatrattot = 100

    # Cuenta los días trabajados acumulados
    diastot = len(fechaCLR45)

    # Calcula los lodos totales confinados
    pesoGTtot = 0
    vecGT = list(dict.fromkeys(dfGT["Numero"]))
    for i in vecGT:
        pesoGT = dfGT[dfGT['Numero'] == i]
        pesoGT = np.array(pesoGT['Peso [Ton]'])
        pesoGT = pesoGT[-1]
        pesoGTtot = pesoGTtot + float(pesoGT)

    # Calcula los Geotubos utilizados
    GTutiliTot = len(list(dict.fromkeys(dfGT["Numero"])))

    # Cambia unidades a m3 por radioitem
    suffix_galdiaacum_acum = "gal"
    nameFigCLR = "Volumen retornado de agua clarificada [gal]"
    nameFigLDS = "Volumen captado de agua lodosa [gal]"
    yaxis_label = "Volumen [gal]"
    if value_unidades_acum == False:
        galtotLDSacum = round(galtotLDSacum / 264.72, 0)
        galtotCLRacum = round(galtotCLRacum / 264.72, 0)
        galCLRylbl45 = [number / 264.72 for number in galCLRylbl45]
        galLDSylbl45 = [number / 264.72 for number in galLDSylbl45]
        suffix_galdiaacum_acum = "m3"
        yaxis_label = "Volumen [m3]"
        nameFigCLR = "Volumen retornado de agua clarificada [m3]"
        nameFigLDS = "Volumen captado de agua lodosa [m3]"

    # Crea la figura de el volumen captado y retornado
    figacumvol = go.Figure()

    figacumvol.add_trace(go.Scatter(x=fechaCLR45, y=galCLRylbl45, name=nameFigCLR))
    figacumvol.add_trace(go.Scatter(x=fechaLDS45, y=galLDSylbl45, name=nameFigLDS))
    figacumvol.update_layout(title="Agua Captada/Retornada Total", xaxis_title="Fecha",
                             yaxis_title=yaxis_label)
    figacumvol.update_layout(legend=dict(
        yanchor="bottom",
        y=-0.5,
        xanchor="center",
        x=0.5
    ))

    figacumvol.update_layout(
        font_family="Franklin Gothic",
        title_font_family="Franklin Gothic",
    )
    figacumvol.update_xaxes(title_font_family="Franklin Gothic")

    # Crea la figura de las propiedades de agua retornada
    figacumprop = go.Figure()
    figacumprop.add_trace(go.Scatter(x=fechaCLR45, y=pHCLRylbl45, name="pH"))
    figacumprop.add_trace(go.Scatter(x=fechaCLR45, y=colorCLRylbl45, name="Color [Pt-Co]"))
    figacumprop.add_trace(go.Scatter(x=fechaCLR45, y=turbCLRylbl45, name="Turbidez [NTU]"))
    figacumprop.update_layout(title="Propiedades de Agua Clarificada", xaxis_title="Fecha")
    figacumprop.update_layout(legend=dict(orientation="h",
                                          yanchor="bottom",
                                          y=-0.5,
                                          xanchor="center",
                                          x=0.5
                                          ))

    figacumprop.update_layout(
        font_family="Franklin Gothic",
        # font_color="blue",
        title_font_family="Franklin Gothic",
        # title_font_color="red",
        # legend_title_font_color="green"
    )
    figacumprop.update_xaxes(title_font_family="Franklin Gothic")

    ################################# Módulo Fase ###########################################

    fase = int(value_fase)
    #fase = value_fase

    dfCLR['Fase'] = dfCLR['Fase'].astype(int)
    dfLDS['Fase'] = dfLDS['Fase'].astype(int)
    dfPURG['Fase'] = dfPURG['Fase'].astype(int)

    # Calcula número de purgas totales y volumen de agua lodosa total por fase

    dfPURGfase = dfPURG[dfPURG["Fase"] == fase]
    dfLDSfase = dfLDS[dfLDS["Fase"] == fase]
    a = dfCLR['Fase']

    dfCLRfase = dfCLR[dfCLR["Fase"] == fase]
    purgsfaseLDS = len(dfPURGfase["Fecha"])

    galfaseLDSacum = dfLDSfase["Volumen [gal]"]
    galfaseLDSacum = list(map(lambda x: float(x), galfaseLDSacum))
    galfaseLDSacum25 = round(sum(galfaseLDSacum, 0))
    galfaseLDSacum = round(sum(galfaseLDSacum, 0))

    # Calcula los bombeos de clarificado para una fase determinada & volumen [gal] total de bombeo de clarificado para una fase determinada & turbidez, color y pH de agua clarificada para un día determinado

    purgsfaseCLR = len(dfCLRfase["Fecha"])
    galfaseCLRacum = dfCLRfase["Volumen [gal]"]
    galfaseCLRacum = list(map(lambda x: float(x), galfaseCLRacum))
    galfaseCLRacum = round(sum(galfaseCLRacum, 0))

    pHfaseCLRprom = dfCLRfase["pH"]
    pHfaseCLRprom = list(map(lambda x: float(x), pHfaseCLRprom))
    pHfaseCLRprom = round(sum(pHfaseCLRprom) / len(pHfaseCLRprom), 2)

    turbfaseCLRprom = dfCLRfase["Turbidez [NTU]"]
    turbfaseCLRprom = list(map(lambda x: float(x), turbfaseCLRprom))
    turbfaseCLRprom = round(sum(turbfaseCLRprom) / len(turbfaseCLRprom), 2)

    colorfaseCLRprom = dfCLRfase["Color [Pt-Co]"]
    colorfaseCLRprom = list(map(lambda x: float(x), colorfaseCLRprom))
    colorfaseCLRprom = round(sum(colorfaseCLRprom) / len(colorfaseCLRprom), 2)

    # Cuenta los días trabajados en una fase
    diasfase = len(dict.fromkeys(dfCLRfase["Fecha"]))

    # Obtiene el flujo de entrada promedio del al clarificador
    galInCLRacum = 2527  # [GPM]

    # Calcula la diferencia entre el último y el primer día trabajado
    x = dfCLRfase["Fecha"]
    m = x[:1]
    n = x[-1:]
    m = m.rename(index=lambda z: 0)
    n = n.rename(index=lambda z: 0)
    datediff = datetime.strptime(n[0], "%d/%m/%Y") - datetime.strptime(m[0], "%d/%m/%Y")
    datediff = datediff.days + 1

    # Calcula el porcentaje de agua tratada de las purgas en una fase
    prctaguatratfase = galfaseCLRacum / galfaseLDSacum * 100
    prctaguatratfase = round(prctaguatratfase, 1)

    if prctaguatratfase > 100:
        prctaguatratfase = 100

    # Cambia unidades a m3 por radioitem
    suffix_galdiaacum_fase = "gal"
    if value_unidades_fase == False:
        galfaseLDSacum = round(galfaseLDSacum / 264.72, 0)
        galfaseCLRacum = round(galfaseCLRacum / 264.72, 0)
        suffix_galdiaacum_fase = "m3"

    # Calcula los lodos totales confinados
    pesoGTfase = 0
    dfGTfase = dfGT[dfGT["Fase"] == fase]
    vecGT = list(dict.fromkeys(dfGTfase["Numero"]))
    for i in vecGT:
        pesoGT = dfGTfase[dfGTfase['Numero'] == i]
        pesoGT = np.array(pesoGT['Peso [Ton]'])
        pesoGT = pesoGT[-1]

        pesoGTfase = pesoGTfase + float(pesoGT)

    # Calcula los lodos confinados en un día
    pesoGTdia = round((pesoGTtot / galtotLDSacum) * galdiaLDSacum25, 0)

    # Calcula los lodos confinados en un mes
    pesoGTmes = round((pesoGTtot / galtotLDSacum) * galmesLDSacum25, 0)

    # Calcula los lodos confinados en una fase


    pesoGTfase = round((pesoGTtot / galtotLDSacum) * galfaseLDSacum25, 0)

    # Calcula los lodos totales confinados
    pesoGTtot = 0
    vecGT = list(dict.fromkeys(dfGT["Numero"]))
    for i in vecGT:
        pesoGT = dfGT[dfGT['Numero'] == i]
        pesoGT = np.array(pesoGT['Peso [Ton]'])
        pesoGT = pesoGT[-1]
        pesoGTtot = pesoGTtot + float(pesoGT)

    pesoGTtot = round(pesoGTtot, 0)
    dfGTfechames = dfGT["Fecha"]
    fechasmesGT = [x for x in dfGTfechames if
                   (datetime.strptime(x, "%d/%m/%Y").month == mes) and (datetime.strptime(x, "%d/%m/%Y").year == año)]

    dfGTmes = dfGT[dfGT.Fecha.isin(fechasmesGT)]

    # Calcula los Geotubos utilizados en un mes
    GTutiliMes = len(list(dict.fromkeys(dfGTmes["Numero"])))

    # Calcula los Geotubos utilizados en una fase
    GTutiliFase = len(list(dict.fromkeys(dfGTfase["Numero"])))

    # Calcula los Geotubos utilizados en total
    GTutiliTot = len(list(dict.fromkeys(dfGT["Numero"])))

    # Obtiene el día inicial y final de la fase
    fechaIniFase = np.array(dfPURGfase['Fecha'])
    fechaFinFase = np.array(dfPURGfase['Fecha'])
    fechaIniFase = fechaIniFase[0]
    fechaFinFase = fechaFinFase[-1]

    # Obtiene el día inicial y final Total
    fechaIniTot = np.array(dfPURG['Fecha'])
    fechaFinTot = np.array(dfPURG['Fecha'])
    fechaIniTot = fechaIniTot[0]
    fechaFinTot = fechaFinTot[-1]

    # Crea vector de fechas para la gráfica
    fechaFaseLDS45 = dfLDSfase["Fecha"]
    fechaFaseCLR45 = dfCLRfase["Fecha"]

    fechaFaseLDS45 = list(dict.fromkeys(fechaFaseLDS45))
    fechaFaseCLR45 = list(dict.fromkeys(fechaFaseCLR45))

    # Calcula los galones totales acumulados enviados por día
    # Calcula la turbidez, color y pH promedios de agua clarificada enviados por día acumulado
    galFaseCLRylbl45 = [None]
    pHFaseCLRylbl45 = [None]
    turbFaseCLRylbl45 = [None]
    colorFaseCLRylbl45 = [None]

    for i in fechaFaseCLR45:
        dffechaFaseCLR = dfCLRfase[dfCLRfase["Fecha"] == i]

        galFaseCLRvec45 = dffechaFaseCLR["Volumen [gal]"]
        galFaseCLRvec45 = list(map(lambda x: float(x), galFaseCLRvec45))
        galFaseCLRacum45 = sum(galFaseCLRvec45)

        colorFaseCLRprom = dffechaFaseCLR["Color [Pt-Co]"]
        colorFaseCLRprom = list(map(lambda x: float(x), colorFaseCLRprom))
        colorFaseCLRprom = sum(colorFaseCLRprom) / len(colorFaseCLRprom)

        pHFaseCLRprom = dffechaFaseCLR["pH"]
        pHFaseCLRprom = list(map(lambda x: float(x), pHFaseCLRprom))
        pHFaseCLRprom = sum(pHFaseCLRprom) / len(pHFaseCLRprom)

        turbFaseCLRprom = dffechaFaseCLR["Turbidez [NTU]"]
        turbFaseCLRprom = list(map(lambda x: float(x), turbFaseCLRprom))
        turbFaseCLRprom = sum(turbFaseCLRprom) / len(turbFaseCLRprom)

        galFaseCLRylbl45.append(galFaseCLRacum45)
        colorFaseCLRylbl45.append(colorFaseCLRprom)
        pHFaseCLRylbl45.append(pHFaseCLRprom)
        turbFaseCLRylbl45.append(turbFaseCLRprom)

    galFaseCLRylbl45.remove(None)
    colorFaseCLRylbl45.remove(None)
    pHFaseCLRylbl45.remove(None)
    turbFaseCLRylbl45.remove(None)

    # Calcula los galones totales captados enviados por día
    galFaseLDSylbl45 = [None]

    for i in fechaFaseLDS45:
        dffechaFaseLDS = dfLDSfase[dfLDSfase["Fecha"] == i]
        galFaseLDSacum45 = dffechaFaseLDS["Volumen [gal]"]
        galFaseLDSacum45 = list(map(lambda x: float(x), galFaseLDSacum45))
        galFaseLDSacum45 = sum(galFaseLDSacum45)
        galFaseLDSylbl45.append(galFaseLDSacum45)

    galFaseLDSylbl45.remove(None)

    fechaFaseLDS45 = list(map(lambda fecha: datetime.strptime(fecha, "%d/%m/%Y"), fechaFaseLDS45))
    fechaFaseCLR45 = list(map(lambda fecha: datetime.strptime(fecha, "%d/%m/%Y"), fechaFaseCLR45))

    # Cambia unidades a m3 por radioitem
    nameFigCLRFase = "Volumen retornado de agua clarificada [gal]"
    nameFigLDSFase = "Volumen captado de agua lodosa [gal]"
    yaxis_labelFase = "Volumen [gal]"
    if value_unidades_fase == False:
        galFaseCLRylbl45 = [number / 264.72 for number in galFaseCLRylbl45]
        galFaseLDSylbl45 = [number / 264.72 for number in galFaseLDSylbl45]
        yaxis_labelFase = "Volumen [m3]"
        nameFigCLRFase = "Volumen retornado de agua clarificada [m3]"
        nameFigLDSFase = "Volumen captado de agua lodosa [m3]"

    # Crea la figura de el volumen captado y retornado
    figFasevol = go.Figure()

    figFasevol.add_trace(go.Scatter(x=fechaFaseCLR45, y=galFaseCLRylbl45, name=nameFigCLRFase))
    figFasevol.add_trace(go.Scatter(x=fechaFaseLDS45, y=galFaseLDSylbl45, name=nameFigLDSFase))
    figFasevol.update_layout(title="Agua Captada/Retornada Fase", xaxis_title="Fecha",
                             yaxis_title=yaxis_labelFase)
    figFasevol.update_layout(legend=dict(
        yanchor="bottom",
        y=-0.5,
        xanchor="center",
        x=0.5
    ))

    figFasevol.update_layout(
        font_family="Franklin Gothic",
        title_font_family="Franklin Gothic",
    )
    figFasevol.update_xaxes(title_font_family="Franklin Gothic")

    # Crea la figura de las propiedades de agua retornada
    figFaseprop = go.Figure()
    figFaseprop.add_trace(go.Scatter(x=fechaFaseCLR45, y=pHFaseCLRylbl45, name="pH"))
    figFaseprop.add_trace(go.Scatter(x=fechaFaseCLR45, y=colorFaseCLRylbl45, name="Color [Pt-Co]"))
    figFaseprop.add_trace(go.Scatter(x=fechaFaseCLR45, y=turbFaseCLRylbl45, name="Turbidez [NTU]"))
    figFaseprop.update_layout(title="Propiedades de Agua Clarificada", xaxis_title="Fecha")
    figFaseprop.update_layout(legend=dict(orientation="h",
                                          yanchor="bottom",
                                          y=-0.5,
                                          xanchor="center",
                                          x=0.5
                                          ))

    figFaseprop.update_layout(
        font_family="Franklin Gothic",
        title_font_family="Franklin Gothic",
    )
    figFaseprop.update_xaxes(title_font_family="Franklin Gothic")

    # --------------------------------- Módulo 4 ------------------------------------------
    numGT = str(value_numGT)
    diaGT = value_fechaGT
    diaGTmañana = str(value_fechaGT) + " 8:00:00"
    diaGTtarde = str(value_fechaGT) + " 16:00:00"

    dfGTnum = dfGT[dfGT["Numero"] == numGT]
    dfGTnum["Fecha"] = list(map(lambda fecha: datetime.strptime(fecha, "%d/%m/%Y"), dfGTnum["Fecha"]))
    dfGTnum["Fecha"] = list(map(lambda fecha: str(fecha.day) + "/" + str(fecha.month) + "/" + str(fecha.year), dfGTnum["Fecha"]))
    print(dfGTnum["Fecha"])
    print(dfGTnum["Hora"])
    dfGTnum["Fecha Completa"] = dfGTnum["Fecha"] + " " + dfGTnum["Hora"]

    fechaGTvec = dfGTnum["Fecha Completa"]
    pesoGTvec = dfGTnum["Peso [Ton]"]
    volGTvec = dfGTnum["Volumen Teórico [m3]"]
    usoGTvec = dfGTnum["% Uso"]

    fechaGTvec = list(map(lambda fecha: datetime.strptime(fecha, "%d/%m/%Y %H:%M:%S"), fechaGTvec))
    pesoGTvec = list(map(lambda x: float(x), pesoGTvec))
    volGTvec = list(map(lambda x: float(x), volGTvec))
    usoGTvec = list(map(lambda x: float(x) * 100, usoGTvec))

    # Determina la capacidad del Geotube
    dfGTnumP = dfGTnum[dfGTnum['Fecha Completa'] == diaGTtarde]
    if len(dfGTnumP) == 1:
        dfGTnum = dfGTnum[dfGTnum['Fecha Completa'] == diaGTtarde]

    else:
        dfGTnum = dfGTnum[dfGTnum['Fecha Completa'] == diaGTmañana]

    capGT = dfGTnum["Capacidad [m3]"]
    capGT = list(map(lambda x: float(x), capGT))
    capGT = round(capGT[0], 0)

    # print(dfGTnum.iloc[:, [8, 9, 10, 11]])
    prctUso = dfGTnum["% Uso"]

    prctUso = list(map(lambda x: float(x), prctUso))

    prctUso = round(prctUso[0] * 100, 2)

    volGT = dfGTnum["Volumen Teórico [m3]"]
    volGT = list(map(lambda x: float(x), volGT))
    volGT = round(volGT[0], 0)

    pesoGT = dfGTnum["Peso [Ton]"]
    pesoGT = list(map(lambda x: float(x), pesoGT))
    pesoGT = round(pesoGT[0], 0)

    # Cuenta los días operados del GT
    diasOperGTvec = fechaGTvec
    diasOperGTvec = list(map(lambda x: str(x.day) + "/" + str(x.month) + "/" +str(x.year), diasOperGTvec))
    diasOperGTvec = list(dict.fromkeys(diasOperGTvec))
    diaGT = datetime.strptime(diaGT, "%d/%m/%Y")
    diaGT = str(diaGT.day) + "/" + str(diaGT.month) + "/" +str(diaGT.year)


    for i in range(0, len(diasOperGTvec)):
        if diaGT == diasOperGTvec[i]:
            diasOperGT = i + 1

    # Cambia unidades a m3 por radioitem
    suffix_galdiaacum_GT = "m3"
    yaxis_label = "Volumen del Geotube [gal]"
    if value_unidades_GT == True:
        capGT = round(capGT * 264.72, 0)
        volGT = round(volGT * 264.72, 0)
        suffix_galdiaacum_GT = "gal"
        yaxis_label = "Volumen del Geotube [m3]"

    # Crea la figura de peso y volumen del Geotube
    figGT = go.Figure()

    figGT.add_trace(go.Scatter(x=fechaGTvec, y=pesoGTvec, name="Volumen del Geotube [m3]"))
    figGT.add_trace(go.Scatter(x=fechaGTvec, y=volGTvec, name="Peso del Geotube [Ton]"))
    figGT.update_layout(title="Peso y Volumen del Geotube", xaxis_title="Fecha",
                        yaxis_title="")
    figGT.update_layout(legend=dict(
        yanchor="bottom",
        y=-0.5,
        xanchor="center",
        x=0.5
    ))

    figGT.update_layout(
        font_family="Franklin Gothic",
        # font_color="blue",
        title_font_family="Franklin Gothic",
        # title_font_color="red",
        # legend_title_font_color="green"
    )
    figGT.update_xaxes(title_font_family="Franklin Gothic")

    # Crea la figura de porcentaje de uso del Geotube

    figusoGT = go.Figure()

    figusoGT.add_trace(go.Scatter(x=fechaGTvec, y=usoGTvec))
    figusoGT.update_layout(title="Uso del Geotube", xaxis_title="Fecha",
                           yaxis_title="Uso [%]")
    figusoGT.update_layout(legend=dict(
        yanchor="bottom",
        y=-0.5,
        xanchor="center",
        x=0.5
    ))

    figusoGT.update_layout(
        font_family="Franklin Gothic",
        # font_color="blue",
        title_font_family="Franklin Gothic",
        # title_font_color="red",
        # legend_title_font_color="green"
    )
    figusoGT.update_xaxes(title_font_family="Franklin Gothic")

    # Crea la figura de lodos confinados mes
    figMesLodos = go.Figure()
    yLodosValue = galMesLDSylbl45
    yLodosValue = list(map(lambda x: float(x) * (pesoGTtot / galtotLDSacum), yLodosValue))
    figMesLodos.add_trace(go.Scatter(x=fechaMesCLR45, y=yLodosValue, marker_color='brown'))
    figMesLodos.update_layout(title="Lodos Confinados al Mes", xaxis_title="Fecha",
                              yaxis_title="Lodos Confinados [Ton]")

    figMesLodos.update_layout(
        font_family="Franklin Gothic",
        title_font_family="Franklin Gothic",
    )
    figMesLodos.update_xaxes(title_font_family="Franklin Gothic")

    # Crea la figura de lodos confinados fase
    figFaseLodos = go.Figure()
    yLodosValue = galFaseLDSylbl45
    yLodosValue = list(map(lambda x: float(x) * (pesoGTtot / galtotLDSacum), yLodosValue))
    figFaseLodos.add_trace(go.Scatter(x=fechaFaseCLR45, y=yLodosValue, marker_color='brown'))
    figFaseLodos.update_layout(title="Lodos Confinados por Fase", xaxis_title="Fecha",
                               yaxis_title="Lodos Confinados [Ton]")

    figFaseLodos.update_layout(
        font_family="Franklin Gothic",
        title_font_family="Franklin Gothic",
    )
    figFaseLodos.update_xaxes(title_font_family="Franklin Gothic")

    # Crea la figura de lodos confinados totales
    figTotLodos = go.Figure()
    yLodosValue = galLDSylbl45
    yLodosValue = list(map(lambda x: float(x) * (pesoGTtot / galtotLDSacum), yLodosValue))
    figTotLodos.add_trace(go.Scatter(x=fechaLDS45, y=yLodosValue, marker_color='brown'))
    figTotLodos.update_layout(title="Lodos Confinados en Total", xaxis_title="Fecha",
                              yaxis_title="Lodos Confinados [Ton]")

    figTotLodos.update_layout(
        font_family="Franklin Gothic",
        title_font_family="Franklin Gothic",
    )
    figTotLodos.update_xaxes(title_font_family="Franklin Gothic")

    pHdiaCLRprom4 = (pHdiaCLRprom / 8.5) * 10
    turbdiaCLRprom4 = (turbdiaCLRprom / 25) * 10
    colordiaCLRprom4 = (colordiaCLRprom / 140) * 10
    prctaguatratdia4 = (prctaguatratdia / 100) * 10

    pHmesCLRprom4 = (pHmesCLRprom / 8.5) * 10
    turbmesCLRprom4 = (turbmesCLRprom / 25) * 10
    colormesCLRprom4 = (colormesCLRprom / 140) * 10
    prctaguatratmes4 = (prctaguatratmes / 100) * 10

    pHfaseCLRprom4 = (pHfaseCLRprom / 8.5) * 10
    turbfaseCLRprom4 = (turbfaseCLRprom / 25) * 10
    colorfaseCLRprom4 = (colorfaseCLRprom / 140) * 10
    prctaguatratfase4 = (prctaguatratfase / 100) * 10

    pHtotCLRprom4 = (pHtotCLRprom / 8.5) * 10
    turbtotCLRprom4 = (turbtotCLRprom / 25) * 10
    colortotCLRprom4 = (colortotCLRprom / 140) * 10
    prctaguatrattot4 = (prctaguatrattot / 100) * 10

    prctUso4 = round((prctUso / 100) * 100, 2)
    pesoGT4 = (pesoGT / 100) * 10

    volGT4 = (volGT / capGT) * 10
    end = time.time()

    return figacumvol, figacumprop, \
           figGT, figusoGT, \
           pHdiaCLRprom, pHdiaCLRprom4, turbdiaCLRprom, turbdiaCLRprom4, colordiaCLRprom, colordiaCLRprom4, prctaguatratdia, prctaguatratdia4, \
           purgsdiaLDS, galdiaLDSacum, purgsdiaCLR, galdiaCLRacum, \
           purgsmesLDS, galmesLDSacum, purgsmesCLR, galmesCLRacum, \
           pHmesCLRprom, turbmesCLRprom, colormesCLRprom, prctaguatratmes, diasMes, \
           pHmesCLRprom4, turbmesCLRprom4, colormesCLRprom4, prctaguatratmes4, \
           purgsfaseLDS, galfaseLDSacum, purgsfaseCLR, galfaseCLRacum, \
           pHfaseCLRprom, turbfaseCLRprom, colorfaseCLRprom, prctaguatratfase, diasfase, \
           pHfaseCLRprom4, turbfaseCLRprom4, colorfaseCLRprom4, prctaguatratfase4, \
           purgstotLDS, galtotLDSacum, purgstotCLR, galtotCLRacum, \
           pHtotCLRprom, turbtotCLRprom, colortotCLRprom, prctaguatrattot, diastot, \
           pHtotCLRprom4, turbtotCLRprom4, colortotCLRprom4, prctaguatrattot4, \
           capGT, volGT, pesoGT, \
           suffix_galdiaacum_dia, suffix_galdiaacum_dia, suffix_galdiaacum_mes, suffix_galdiaacum_mes, \
           suffix_galdiaacum_fase, suffix_galdiaacum_fase, suffix_galdiaacum_acum, suffix_galdiaacum_acum, \
           suffix_galdiaacum_GT, volGT4, volGT4, suffix_galdiaacum_GT, prctUso4, \
           pesoGTdia, GTutiliMes, pesoGTmes, GTutiliFase, pesoGTfase, GTutiliTot, pesoGTtot, \
           fechaIniFase, fechaFinFase, fechaIniTot, fechaFinTot, figMesvol, figMesprop, figFasevol, figFaseprop, \
           figMesLodos, figFaseLodos, figTotLodos, diasOperGT


@app.callback(
    Output("download-component", "data"),
    Input("btn", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    return dcc.send_file("./assets/Instructivo.pdf")


if __name__ == '__main__':
    app.run_server()



