import pandas as pd
from datetime import date

from server import app
from dash import dcc
import dash_bootstrap_components as dbc
from dash import html
from plotly import graph_objs as go
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dash import dash_table
import dash_daq as daq
from patients import Patients

dataframe_patients = Patients()


def build_banner():
    return html.Div(
        id="id_banner",
        className="banner",
        children=[
            html.Div(
                children=[
                    html.P("CardioAI Dashboard", className="banner-title"),
                    html.P("Cистема диагностики и прогнозирования инфаркта миокарда", className="banner-description")
                ],
            ),
        ],
    )


def build_layout_patients():
    return html.Div(
        id="id_layout_patients",
        className="layout_patients",
        children=[
            html.H6("Список пациентов"),
            html.Div([
                dash_table.DataTable(
                    id="id_table_patients",
                    style_header={"fontWeight": "bold", "color": "inherit"},
                    style_as_list_view=True,
                    fill_width=True,
                    style_cell_conditional=[
                        {"if": {"column_id": "Specs"}, "textAlign": "left"}
                    ],
                    style_cell={
                        "backgroundColor": "#F4F4F4",
                        "fontFamily": "Open Sans",
                        "padding": "0 2rem",
                        "color": "black",
                        "border": "none",
                    },
                    css=[
                        {"selector": "tr:hover td", "rule": "color: #4129f2 !important; font-weight: bold;"},
                        {"selector": "td", "rule": "border: none !important;"},
                        {
                            "selector": ".dash-cell.focused",
                            "rule": "background-color: #807e7e !important;",
                        },
                        {"selector": "table", "rule": "--accent: #807e7e;"},
                        {"selector": "tr", "rule": "background-color: transparent"},
                    ],
                    data=dataframe_patients.to_dict(columns=["surname", "name", "middle_name"], orient="rows"),
                    columns=[{"id": id, "name": name} for id, name in zip(["surname", "name", "middle_name"], ["Фамилия", "Имя", "Отчество"])],
                    style_data_conditional=[
                        {
                            "if": {"row_index": "even"},
                            "backgroundColor": "var(--report_background_page)",
                        }
                    ],
                    editable=True,
                )
            ]
                , className="table_patients_content"),
            html.Div([
                html.Button(
                    "Выгрузить данные",
                    id="id_data_upload_btn",
                    className="data_upload_btn",
                    n_clicks=0
                )
            ])
        ]
    )


def build_main_layout():
    return html.Div(
        id="id_main_layout",
        className="main_layout",
        children=[
            dcc.Tabs(
                id="app_tabs",
                value="tab_patients_info",
                className="custom_tabs",
                children=[
                    dcc.Tab(
                        id="id_patients_info_tab",
                        label="Данные о пациенте",
                        value="tab_patients_info",
                        className="custom_tab",
                        children=[build_patients_info_layout()]
                    ),
                    dcc.Tab(id="id_complications_tab",
                            label="Осложнения",
                            value="tab_complications",
                            className="custom_tab",
                            children=[build_patient_complication_layout()]
                            ),
                    dcc.Tab(id="id_fatalities_tab",
                            label="Смертельные исходы",
                            value="tab_fatalities",
                            className="custom_tab",
                            children=[build_fatal_outcome_treatment_layout()]
                            ),
                ]
            )
        ],
    )


def build_personal_data_patient_content():
    return html.Div([
        html.Div(children="Личные данные пациента", className="header_block"),
        html.Table(
            # Header
            [html.Tr([html.Th("Фамилия"),
                      html.Th("Имя"),
                      html.Th("Отчество"),
                      html.Th("Пол"),
                      html.Th("Дата рождения")])] +
            # Body
            [html.Tr([html.Td(html.Div(dcc.Input(
                id="id_input_surname",
                value="",
                placeholder="Введите фамилию пациента",
                className="input_surname",
                ), id="test")),
                html.Td(dcc.Input(
                    id="id_input_name",
                    value="",
                    placeholder="Введите имя пациента",
                    className="input_name",
                )),
                html.Td(dcc.Input(
                    id="id_middle_name",
                    value="",
                    placeholder="Введите отчество пациента",
                    className="input_middle_name",
                )),
                html.Td(dbc.FormGroup(
                    [
                        dcc.RadioItems(
                            id="id_select_patient_gender",
                            className="patient_gender",
                            options=[
                                {"label": "Мужской", "value": "мужской"},
                                {"label": "Женский", "value": "женский"},
                            ],
                            labelStyle={"display": "inline-block", "margin-right": "10px", 'font-weight': 300},
                            style={
                                'display': 'inline-block',
                                "margin-top": "10px"
                            })
                    ])),
                html.Td(dcc.DatePickerSingle(
                    placeholder='Выберите дату рождения пациента',
                    min_date_allowed=date(1930, 1, 1),
                    date=date.today(),
                    display_format='DD-MM-YYYY',
                    id="id_select_patient_date_birth",
                    className="patient_date_birth"
                ))
                ], style={"marginTop": "20px", "marginBottom": "20px"}),
            ], id="id_table_patient_personal_data")
        ], className="patient_personal_data", id="id_patient_personal_data")


def build_patient_anamnesis_content():
    row1 = html.Tr([html.Td(html.P("Количество инфарктов миокарда", className="input_heading")),
                    html.Td(daq.NumericInput(
                        id='id_number_myocardial_infarctions',
                        labelPosition='top',
                        value=0,
                        min=0,
                        max=50,
                        size=90
                    )
                )
            ])
    row2 = html.Tr([html.Td(html.P("Стенокардия напряжения", className="input_heading")),
                    html.Td(dcc.Dropdown(
                        id="id_duration_stenocardia",
                        options=[
                            {'label': 'нет', 'value': 0},
                            {'label': 'менее 1 года', 'value': 1},
                            {'label': '1 год', 'value': 2},
                            {'label': '2 года', 'value': 3},
                            {'label': '3 года', 'value': 4},
                            {'label': '4-5 лет', 'value': 5},
                            {'label': 'более 5 лет', 'value': 6}
                        ],
                        value=0,
                        className="duration_stenocardia",
                    )
                )
            ])
    row3 = html.Tr([html.Td(html.P("Функциональный класс стенокардии в последний год", className="input_heading")),
                    html.Td(daq.NumericInput(
                        id='id_functional_class_stenocardia',
                        labelPosition='top',
                        value=0,
                        min=0,
                        max=4,
                        size=90
                    )
                )
            ])
    row4 = html.Tr([html.Td(html.P("Характер ИБС в последние недели, дни перед пост. в больницу"
                                   , className="input_heading")),
                    html.Td(dcc.Dropdown(
                         id="id_characteristics_ashd",
                         options=[
                             {'label': 'нет ИБС', 'value': 0},
                             {'label': 'cтенокардия напряжения', 'value': 1},
                             {'label': 'нестабильная стенокардия', 'value': 2}
                         ],
                         value=0,
                         className="characteristics_ashd",
                    )
                )
            ])
    row5 = html.Tr([html.Td(html.P("Наличие гипертонической болезни", className="input_heading")),
                    html.Td(dcc.Dropdown(
                        id="id_hypertension",
                        options=[
                            {'label': 'нет', 'value': 0},
                            {'label': '1 стадия гипертонической болезни', 'value': 1},
                            {'label': '2 стадия гипертонической болезни', 'value': 2},
                            {'label': '3 стадия гипертонической болезни', 'value': 3}
                        ],
                        value=0,
                        className="hypertension",
                    )
                ),
                html.Td(html.P("Симптоматическая гипертония", className="input_heading")),
                html.Td(daq.BooleanSwitch(id='id_symptomatic_hypertension', on=False)),
            ])

    row6 = html.Tr([html.Td(html.P("Длительность течения артериальной гипертензии", className="input_heading")),
                    html.Td(dcc.Dropdown(
                        id="id_arterial_hypertension_duration",
                        options=[
                            {'label': 'нет артериальной гипертензии', 'value': 0},
                            {'label': '1 год', 'value': 1},
                            {'label': '2 года', 'value': 2},
                            {'label': '3 года', 'value': 3},
                            {'label': '4 года', 'value': 4},
                            {'label': '5 лет', 'value': 5},
                            {'label': '5-10 лет', 'value': 6},
                            {'label': 'более 10 лет', 'value': 7}
                        ],
                        value=0,
                        className="arterial_hypertension_duration",
                    )
                )])

    row7 = html.Tr([html.Td(html.P("Наличие хронической сердечной недостаточности", className="input_heading")),
                html.Td(dcc.Dropdown(
                    id="id_chronic_heart_failure",
                    options=[
                        {'label': 'нет', 'value': 0},
                        {'label': 'I стадия', 'value': 1},
                        {'label': 'IIА стадия (застой по большому кругу)', 'value': 2},
                        {'label': 'IIА стадия (застой по малому кругу)', 'value': 3},
                        {'label': 'IIБ стадия', 'value': 4},
                        {'label': 'III стадия ', 'value': 5}
                    ],
                    value=0,
                    className="chronic_heart_failure",
                    )
                )
            ])

    row8 = html.Tr([html.Td(html.P("Нарушения сердечно-сосудистой системы", className="input_heading")),
                    html.Td(dcc.Dropdown(
                        id="id_cardiovascular_disorders_anamnesis",
                        options=[
                            {'label': 'нарушения ритма', 'value': 'rhythm_disturbances_anamnesis'},
                            {'label': 'предсердная экстрасистолия', 'value': 'atrial_extrasystole_anamnesis'},
                            {'label': 'желудочковая экстрасистолия', 'value': 'ventricular_extrasystole_anamnesis'},
                            {'label': 'пароксизмы фибрилляции предсердий', 'value': 'paroxysms_atrial_fibrillation_anamnesis'},
                            {'label': 'постоянная форма фибрилляции предсердий', 'value': 'permanent_form_atrial_fibrillation_anamnesis'},
                            {'label': 'фибрилляция желудочков', 'value': 'ventricular_fibrillation_anamnesis'},
                            {'label': 'желудочковая пароксизмальная тахикардия', 'value': 'ventricular_paroxysmal_tachycardia_anamnesis'}
                        ],
                        value=[],
                        multi=True,
                        className="cardiovascular_disorders_anamnesis",
                    )
                )
            ])

    row9 = html.Tr([html.Td(html.P("Блокада сердца", className="input_heading")),
                    html.Td(dcc.Dropdown(
                        id="id_heart_block_anamnesis",
                        options=[
                            {'label': 'АВ блокада I степени', 'value': 'AV_block_one_degree_anamnesis'},
                            {'label': 'АВ блокада III степени', 'value': 'AV_block_three_degree_anamnesis'},
                            {'label': 'Блокада передней ветви левой ножки пучка Гиса', 'value': 'left_bundle_anterior_branch_block_anamnesis'},
                            {'label': 'Неполная блокада левой ножки пучка Гиса', 'value': 'left_bundle_branch_incomplete_block_anamnesis'},
                            {'label': 'Полная блокада левой ножки пучка Гиса', 'value': 'left bundle_branch_full_block_anamnesis'},
                            {'label': 'Неполная блокада правой ножки пучка Гиса', 'value': 'right_bundle_branch_incomplete_block_anamnesis'},
                            {'label': 'Полная блокада правой ножки пучка Гиса', 'value': 'right_bundle_branch_full_block_anamnesis'}
                        ],
                        value=[],
                        multi=True,
                        className="heart_block_anamnesis",
                    )
                )
            ])

    row10 = html.Tr([html.Td(html.P("Сопутствующие заболевания", className="input_heading")),
                    html.Td(dcc.Dropdown(
                        id="id_accompanying_illnesses",
                        options=[
                            {'label': 'cахарный диабет', 'value': 'diabetes_anamnesis'},
                            {'label': 'ожирение', 'value': 'obesity_anamnesis'},
                            {'label': 'тиреотоксикоз', 'value': 'thyrotoxicosis_anamnesis'},
                            {'label': 'хронический бронхит', 'value': 'chronical_bronchitis_anamnesis'},
                            {'label': 'обструктивный хронический бронхит', 'value': 'obstructive_chronic_bronchitis_anamnesis'},
                            {'label': 'бронхиальная астма', 'value': 'bronchial_asthma_anamnesis'},
                            {'label': 'хроническая пневмония', 'value': 'chronic_pneumonia_anamnesis'},
                            {'label': 'туберкулез легкого (легких) в анамнезе ', 'value': 'pulmonary_tuberculosis_anamnesis'}
                        ],
                        value=[],
                        multi=True,
                        className="accompanying_illnesses",
                    )
                )
            ])

    table_body_patient_anamnesis = [html.Tbody([row1, row2, row3, row4, row5, row6, row7, row8, row9, row10])]

    return html.Div([
        html.Div(children="Анамнез пациента", className="header_block"),
        dbc.Table(table_body_patient_anamnesis, bordered=False, borderless=True
                      , style={'vertical-align': 'middle'})
        ], className="patient_anamnesis")


def build_medical_examination_content():
    row1 = html.Tr([html.Td(html.P("Систолическое артериальное давление", className="input_heading")),
                      html.Td(daq.NumericInput(
                          id='id_systolic_pressure',
                          labelPosition='top',
                          value=0,
                          min=0,
                          max=300,
                          size=90
                      )),
                      html.Td(html.P("Диастолическое артериальное давление", className="input_heading")),
                      html.Td(daq.NumericInput(
                          id='id_diastolic_pressure',
                          labelPosition='top',
                          value=0,
                          min=0,
                          max=300,
                          size=90
                      ))
    ])

    row2 = html.Tr([html.Td(html.P("Нарушения сердечно-сосудистой системы (на момент поступления)", className="input_heading")),
                    html.Td(dcc.Dropdown(
                        id="id_cardiovascular_disorders",
                        options=[
                            {'label': 'отек легких', 'value': 'pulmonary_edema_intensive_care_unit'},
                            {'label': 'кардиогенный шок', 'value': 'cardiogenic_shock_intensive_care_unit'},
                            {'label': 'пароксизм фибрилляции предсердий', 'value': 'paroxysms_atrial_fibrillation_intensive_care_unit'},
                            {'label': 'пароксизм суправентрикулярной тахикардии', 'value': 'paroxysm_supraventricular_tachycardia_intensive_care_unit'},
                            {'label': 'пароксизм желудочковой тахикардии', 'value': 'paroxysm_ventricular_tachycardia_intensive_care_unit'},
                            {'label': 'фибрилляция желудочков', 'value': 'ventricular_fibrillation_intensive_care_unit'}
                        ],
                        value=[],
                        multi=True,
                        className="cardiovascular_disorders",
                    ))
    ])

    row3 = html.Tr([html.Td(html.P("Наличие инфаркта передней стенки левого желудочка (изменения на ЭКГ в отведениях V1 - V4)"
                                   , className="input_heading")),
                      html.Td(dcc.Dropdown(
                          id="id_infarction_anterior_wall_left_ventricle",
                          options=[
                              {'label': 'нет', 'value': 0},
                              {'label': 'форма комплекса QRS не изменена', 'value': 1},
                              {'label': 'форма QRS комплекса QR', 'value': 2},
                              {'label': 'форма QRS комплекса Qr', 'value': 3},
                              {'label': 'форма QRS комплекса QS', 'value': 4}
                          ],
                          value=0,
                          className="infarction_anterior_wall_left_ventricle",
                      )),
                      html.Td(html.P("Наличие инфаркта боковой стенки левого желудочка (изменения на ЭКГ в отведениях V5 - V6, I, AVL)"
                                     , className="input_heading")),
                      html.Td(dcc.Dropdown(
                          id="id_infarction_lateral_wall_left_ventricle",
                          options=[
                              {'label': 'нет', 'value': 0},
                              {'label': 'форма комплекса QRS не изменена', 'value': 1},
                              {'label': 'форма QRS комплекса QR', 'value': 2},
                              {'label': 'форма QRS комплекса Qr', 'value': 3},
                              {'label': 'форма QRS комплекса QS', 'value': 4}
                          ],
                          value=0,
                          className="infarction_lateral_wall_left_ventricle",
                      ))
    ])

    row4 = html.Tr([html.Td(html.P("Наличие инфаркта нижней стенки левого желудочка (изменения на ЭКГ в отведениях III, AVF, II)",
                                   className="input_heading")),
                    html.Td(dcc.Dropdown(
                        id="id_infarction_inferior_wall_left_ventricle",
                        options=[
                            {'label': 'нет', 'value': 0},
                            {'label': 'форма комплекса QRS не изменена', 'value': 1},
                            {'label': 'форма QRS комплекса QR', 'value': 2},
                            {'label': 'форма QRS комплекса Qr', 'value': 3},
                            {'label': 'форма QRS комплекса QS', 'value': 4}
                        ],
                        value=0,
                        className="infarction_inferior_wall_left_ventricle",
                    )),
                    html.Td(html.P("Наличие инфаркта задней стенки левого желудочка (изменения на ЭКГ в отведениях V7 - V9, "
                                   "реципрокные изменения в отведениях V1 - V3)",
                                   className="input_heading")),
                    html.Td(dcc.Dropdown(
                        id="id_infarction_posterior_wall_left_ventricle",
                        options=[
                            {'label': 'нет', 'value': 0},
                            {'label': 'форма комплекса QRS не изменена', 'value': 1},
                            {'label': 'форма QRS комплекса QR', 'value': 2},
                            {'label': 'форма QRS комплекса Qr', 'value': 3},
                            {'label': 'форма QRS комплекса QS', 'value': 4}
                        ],
                        value=0,
                        className="infarction_posterior_wall_left_ventricle",
                    ))
    ])

    row5 = html.Tr(
        [html.Td(html.P("Наличие инфаркта миокарда правого желудочка"
                        , className="input_heading")),
         html.Td(daq.BooleanSwitch(id='id_right_ventricular_myocardial_infarction', on=False))])

    row6 = html.Tr([html.Td(html.P("Ритм по ЭКГ", className="input_heading")),
                    html.Td(dcc.Dropdown(
                        id="id_rhythm_ecg",
                        options=[
                            {'label': 'синусовый (с чсс 60-90 в мин.)', 'value': 'sinus rhythm'},
                            {'label': 'фибрилляция предсердий', 'value': 'atrial_fibrillation'},
                            {'label': 'предсердный', 'value': 'atrial_rhythm'},
                            {'label': 'идиовентрикулярный', 'value': 'idioventricular_rhythm'},
                            {'label': 'синусовый с ЧСС более 90 в мин. (синусовая тахикардия)', 'value': 'sinus_tachycardia'},
                            {'label': 'синусовый с ЧСС менее 60 в мин. (синусовая брадикардия)', 'value': 'sinus_bradycardia'}
                        ],
                        value=[],
                        className="rhythm_ecg",
                    ))
    ])

    row7 = html.Tr([html.Td(html.P("Нарушения сердечно-сосудистой системы (по данным на ЭКГ)", className="input_heading")),
                    html.Td(dcc.Dropdown(
                        id="id_cardiovascular_disorders_ecg",
                        options=[
                            {'label': 'предсердная экстрасистолия', 'value': 'atrial_extrasystole_ecg'},
                            {'label': 'частая предсердная экстрасистолия', 'value': 'frequent_atrial_extrasystoles_ecg'},
                            {'label': 'желудочковая экстрасистолия', 'value': 'ventricular_extrasystole_ecg'},
                            {'label': 'частая желудочковая экстрасистолия', 'value': 'frequent_ventricular_extrasystole_ecg'},
                            {'label': 'пароксизмы фибрилляции предсердий', 'value': 'paroxysms_atrial_fibrillation_ecg'},
                            {'label': 'постоянная форма фибрилляции предсердий', 'value': 'permanent_form_atrial_fibrillation_ecg'},
                            {'label': 'суправентрикулярная пароксизмальная тахикардия', 'value': 'supraventricular_paroxysmal_tachycardia_ecg'},
                            {'label': 'желудочковая пароксизмальная тахикардия', 'value': 'ventricular_paroxysmal_tachycardia_ecg'},
                            {'label': 'фибрилляция желудочков', 'value': 'ventricular_fibrillation_ecg'}
                        ],
                        multi=True,
                        value=[],
                        className="arrhythmia",
                    ))
    ])

    row8 = html.Tr([html.Td(html.P("Блокада сердца", className="input_heading")),
                    html.Td(dcc.Dropdown(
                        id="id_heart_block_ecg",
                        options=[
                            {'label': 'синоатриальная блокада', 'value': 'sinoatrial blockade_ecg'},
                            {'label': 'АВ блокада I степени', 'value': 'AV_block_one_degree_ecg'},
                            {'label': 'АВ блокада II степени I типа', 'value': 'AV_block_two_degree_one_type_ecg'},
                            {'label': 'АВ блокада II степени II типа', 'value': 'AV_block_two_degree_two_type_ecg'},
                            {'label': 'АВ блокада III степени', 'value': 'AV_block_three_degree_ecg'},
                            {'label': 'Блокада передней ветви левой ножки пучка Гиса', 'value': 'left_bundle_anterior_branch_his_ecg'},
                            {'label': 'Блокада задней ветви левой ножки пучка', 'value': 'left_bundle_posterior_branch_block_ecg'},
                            {'label': 'Неполная блокада левой ножки пучка Гиса', 'value': 'left_bundle_branch_incomplete_block_ecg'},
                            {'label': 'Полная блокада левой ножки пучка Гиса', 'value': 'left bundle_branch_full_block_ecg'},
                            {'label': 'Неполная блокада правой ножки пучка Гиса', 'value': 'right_bundle_branch_incomplete_block_ecg'},
                            {'label': 'Полная блокада правой ножки пучка Гиса', 'value': 'right_bundle_branch_full_block_ecg'}
                        ],
                        multi=True,
                        value=[],
                        className="heart_block_ecg",
                    ))
    ])

    row9 = html.Tr([html.Td(html.P("Фибринолитическая терапия", className="input_heading")),
                    html.Td(dcc.Dropdown(
                        id="id_fibrinolytic_therapy",
                        options=[
                            {'label': 'целиаза 250 тыс. ЕД', 'value': 'celiasum_250'},
                            {'label': 'целиаза 500 тыс. ЕД', 'value': 'celiasum_500'},
                            {'label': 'целиаза 750 тыс. ЕД', 'value': 'celiasum_750'},
                            {'label': 'целиаза 1 млн. ЕД', 'value': 'celiasum_1_mln'},
                            {'label': 'стрептодеказа 1,5 млн. ЕД', 'value': 'streptodecasum_1_5'},
                            {'label': 'стрептодеказа 3 млн. ЕД', 'value': 'streptodecasum_3'},
                            {'label': 'стрептаза', 'value': 'streptasum'}
                        ],
                        multi=True,
                        value=[],
                        className="fibrinolytic_therapy",
                    ))
    ])

    row10 = html.Tr([html.Td(html.P("Гипокалиемия", className="input_heading")),
                    html.Td(daq.BooleanSwitch(id='id_hypokalemia', on=False)),
                    html.Td(html.P("Содержание калия в сыворотке крови", className="input_heading")),
                    html.Td(dcc.Input(
                        id='id_potassium_content',
                        type='number',
                        value=0,
                        min=0,
                        step=0.1,
                        size=90
                    ))
    ])

    row11 = html.Tr([html.Td(html.P("Увеличение натрия в сыворотке крови (более 150 ммоль/л)", className="input_heading")),
                     html.Td(daq.BooleanSwitch(id='id_increasing_sodium', on=False)),
                     html.Td(html.P("Содержание натрия в сыворотке крови", className="input_heading")),
                     html.Td(dcc.Input(
                        id='id_sodium',
                        type='number',
                        value=0,
                        min=0,
                        step=0.1,
                        size=90
                     ))
    ])

    row12 = html.Tr([html.Td(html.P("Содержание АлАТ в крови", className="input_heading")),
                     html.Td(dcc.Input(
                         id='id_alt',
                         type='number',
                         value=0,
                         min=0,
                         step=0.01,
                         size=90
                     )),
                     html.Td(html.P("Содержание АсАТ в крови", className="input_heading")),
                     html.Td(dcc.Input(
                        id='id_ast',
                         type='number',
                         value=0,
                         min=0,
                         step=0.01,
                         size=90
                     ))
    ])

    row13 = html.Tr([html.Td(html.P("Содержание лейкоцитов в крови", className="input_heading")),
                     html.Td(dcc.Input(
                         id='id_leukocytes',
                         type='number',
                         value=0,
                         min=0,
                         step=0.1,
                         size=90
                     )),
                     html.Td(html.P("Скорость оседания эритроцитов", className="input_heading")),
                     html.Td(dcc.Input(
                         id='id_erythrocytes',
                         type='number',
                         value=0,
                         min=0,
                         step=1,
                         size=90
                     ))
    ])

    row14 = html.Tr([html.Td(html.P("Время, прошедшее от начала ангинозного приступа до поступления в стационар"
                                    , className="input_heading")),
                     html.Td(dcc.Dropdown(
                         id="id_time_anginal_attack",
                         options=[
                             {'label': 'менее 2 часов', 'value': 1},
                             {'label': '2-4 часа', 'value': 2},
                             {'label': '4-6 часов', 'value': 3},
                             {'label': '6-8 часов', 'value': 4},
                             {'label': '8-12 часов', 'value': 5},
                             {'label': '12-24 часов', 'value': 6},
                             {'label': 'более 1 суток', 'value': 7},
                             {'label': 'более 2 суток', 'value': 8},
                             {'label': 'более 3 суток', 'value': 9}
                        ],
                        value=[],
                        className="time_anginal_attack",
                    ))
    ])

    row15 = html.Tr([html.Td(html.P("Лекарственные препараты (кардиобригада)", className="input_heading")),
                     html.Td(dcc.Dropdown(
                         id="id_medications_cardio_team",
                         options=[
                             {'label': 'наркотические анальгетики', 'value': 'narcotic_analgesics_cardio_team'},
                             {'label': 'ненаркотические анальгетики', 'value': 'nonnarcotic_analgesics_cardio_team'},
                             {'label': 'лидокаин', 'value': 'lidocaine_cardio_team'}
                         ],
                         multi=True,
                         value=[],
                         className="medications_cardio_team",
                     )),
                     html.Td(html.P("Лекарственные препараты (ОРиИТ)", className="input_heading")),
                     html.Td(dcc.Dropdown(
                         id="id_medications",
                         options=[
                             {'label': 'лидокаин', 'value': 'lidocaine_intensive_care_unit'},
                             {'label': 'бета-блокаторы', 'value': 'beta_blockers_intensive_care_unit'},
                             {'label': 'антагонисты кальция', 'value': 'calcium_antagonists_intensive_care_unit'},
                             {'label': 'антикоагулянты (гепарин)', 'value': 'anticoagulants_intensive_care_unit'},
                             {'label': 'аспирин', 'value': 'aspirin_intensive_care_unit'},
                             {'label': 'тиклид', 'value': 'ticklid_intensive_care_unit'},
                             {'label': 'трентал', 'value': 'trental_intensive_care_unit'},
                             {'label': 'жидкие нитраты', 'value': 'liquid_nitrates_intensive_care_unit'}
                         ],
                         multi=True,
                         value=[],
                         className="medications",
                     ))
    ])

    table_body_patient_examination = [html.Tbody([row1, row2, row3, row4, row5, row6, row7, row8
                                                  , row9, row10, row11, row12, row13, row14, row15])]

    return html.Div([
        html.Div(children="Данные обследования пациента при поступлении в ОРиИТ"
                 , className="header_block"),
        dbc.Table(table_body_patient_examination, bordered=False, borderless=True
                  , style={'vertical-align': 'middle'}),
    ], className='results_patient_medical_examination')


def build_patients_info_layout():
    return html.Div([
        build_personal_data_patient_content(),
        build_patient_anamnesis_content(),
        build_medical_examination_content(),
        html.Div([
                html.Button(
                    "Сохранить данные по пациенту",
                    id="id_add_patient_btn",
                    className="button",
                    n_clicks=0
                )
        ])
    ], className="patients_info_layout")


def build_patient_complication_layout():
    return html.Div([
        html.Div(children="Вероятность возникновения осложнения состояния пациента", className="header_block"),
        html.Div(
            [dcc.Graph(id="id_complication_graph"
                       , style={"height": "89%", "width": "98%"}
                       , figure=create_forecasting_complication_graph()
                       , config=dict(displayModeBar=True))],
            id="id_complication_graph_container",
            className="complication_graph_container"
        ),
        html.Div([
            html.Button(
                "Получить прогноз",
                id="id_forecasting_complication_btn",
                className="button",
                n_clicks=0
            )
        ]),
    ], className='patient_complication_layout')


def create_forecasting_complication_graph():
    x_axis = {
        "title": "Вероятность",
        "titlefont": {"family": "Helvetica, sans-serif", "size": 16}, "range": [0, 100],
    }
    y_axis = {"title": "Виды осложнений", "titlefont": {"family": "Helvetica, sans-serif", "size": 16}}

    layout = go.Layout(
        autosize=True,
        showlegend=False,
        paper_bgcolor='#FAFAFA',
        hovermode="closest",
        barmode="stack",
        height=500,
        font={"family": "Helvetica Neue, sans-serif", "size": 12},
        margin=dict(l=40, r=40, t=40, b=40, pad=10),
        titlefont={
            "family": "Helvetica, sans-serif",
            "size": 26,
        },
        xaxis=x_axis,
        yaxis=y_axis,
        plot_bgcolor="white",
        selectdirection="v"
    )

    data = [
        go.Bar(
            y=["Фибрилляция предсердий", "Суправентрикулярная тахикардия", "Желудочковая тахикардия"
               , "Фибрилляция желудочков", "Полная АВ блокада", "Отек легких", "Разрыв сердца"
               , "Синдром Дресслера", "Хроническая сердечная недостаточность", "Рецидив инфаркта миокарда"
               , "Постинфарктная стенокардия"],
            x=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            orientation="h",
            marker=dict(color="#0073e4"),
        )
    ]
    figure = dict(data=data, layout=layout)

    return figure


def build_fatal_outcome_treatment_layout():
    return dbc.Card([
        html.Div(children="Вероятность летального исхода при лечении", className="header_block"),
            dbc.Row([
                dbc.Col(
                    html.Div(
                        [dcc.Graph(id="id_fatal_outcome_pie"
                                   , style={"height": "89%", "width": "98%"}
                                   , figure=create_forecasting_fatal_outcome_graph()
                                   , config=dict(displayModeBar=False))],
                    )
                ),
                dbc.Col(
                    html.Div(
                        [dcc.Graph(id="id_fatal_outcome_bar"
                            , style={"height": "89%", "width": "98%"}
                            , figure=create_forecasting_cause_fatal_outcome_graph()
                            , config=dict(displayModeBar=True))],
                    )
                )
            ], form=True),
            html.Div([
                html.Button(
                    "Получить прогноз",
                    id="id_forecasting_fatal_outcome_btn",
                    className="button",
                    n_clicks=0
                )
            ]),
        ], body=True, className='fatal_outcome_treatment_layout')


def create_forecasting_fatal_outcome_graph():
    layout = go.Layout(
        autosize=True,
        showlegend=False,
        paper_bgcolor='#FAFAFA',
        hovermode="closest",
        barmode="stack",
        height=500,
        font={"family": "Helvetica Neue, sans-serif", "size": 12},
        margin=dict(l=40, r=40, t=40, b=40, pad=10),
        titlefont={
            "family": "Helvetica, sans-serif",
            "size": 26,
        },
        plot_bgcolor="white"
    )

    data = [
        go.Pie(
            labels=["Выжил", "Умер"],
            values=[50, 50],
            textinfo='label+percent',
            insidetextorientation='radial',

        )
    ]
    figure = dict(data=data, layout=layout)

    return figure


def create_forecasting_cause_fatal_outcome_graph():
    x_axis = {
        "title": "Вероятность",
        "titlefont": {"family": "Helvetica, sans-serif", "size": 16}, "range": [0, 100],
    }
    y_axis = {"title": "Причины летального исхода", "titlefont": {"family": "Helvetica, sans-serif", "size": 16}}

    layout = go.Layout(
        autosize=True,
        showlegend=False,
        paper_bgcolor='#FAFAFA',
        hovermode="closest",
        barmode="stack",
        height=500,
        font={"family": "Helvetica Neue, sans-serif", "size": 12},
        margin=dict(l=40, r=40, t=40, b=40, pad=10),
        titlefont={
            "family": "Helvetica, sans-serif",
            "size": 26,
        },
        xaxis=x_axis,
        yaxis=y_axis,
        plot_bgcolor="white",
        selectdirection="v"
    )

    data = [
        go.Bar(
            y=["Кардиогенный шок", "Отек легких", "Разрыв сердца"
               , "Прогрессирование застойной сердечной недостаточности", "Тромбоэмболия", "Асистолия"
               , "Фибрилляция желудочков "],
            x=[0, 0, 0, 0, 0, 0, 0],
            orientation="h",
            marker=dict(color="#0073e4"),
        )
    ]
    figure = dict(data=data, layout=layout)

    return figure


app.layout = html.Div(
    id="app_container",
    children=[
        build_banner(),
        dbc.Row(
            [
                dbc.Col(build_layout_patients(), width='auto'),
                dbc.Col(build_main_layout())
            ]
        )
    ]
)


@app.callback(
    Output("id_complication_graph", "figure"),
    Input("id_forecasting_complication_btn", "n_clicks"),
    State("id_complication_graph", "figure"),
)
def forecasting_complication(n_clicks, figure):
    if n_clicks > 0:
        figure["data"] = [go.Bar(
                y=["Фибрилляция предсердий", "Суправентрикулярная тахикардия", "Желудочковая тахикардия"
                    , "Фибрилляция желудочков", "Полная АВ блокада", "Отек легких", "Разрыв сердца"
                    , "Синдром Дресслера", "Хроническая сердечная недостаточность", "Рецидив инфаркта миокарда"
                    , "Постинфарктная стенокардия"],
                x=dataframe_patients.get_forecast_complication(),
                orientation="h",
                marker=dict(color="#0073e4")
            )]
        return figure
    else:
        return figure


@app.callback(
    [Output("id_fatal_outcome_pie", "figure"),
     Output("id_fatal_outcome_bar", "figure")],
    Input("id_forecasting_fatal_outcome_btn", "n_clicks"),
    [State("id_fatal_outcome_pie", "figure"),
    State("id_fatal_outcome_bar", "figure")]
)
def forecasting_fatal_outcome(n_clicks, pie, bar):
    if n_clicks > 0:
        pie["data"] = [go.Pie(
            labels=["Выжил", "Умер"],
            values=dataframe_patients.get_forecasting_fatal_outcome(),
            textinfo='label+percent',
            insidetextorientation='radial',
            )
        ]
        bar["data"] = [go.Bar(
            y=["Кардиогенный шок", "Отек легких", "Разрыв сердца"
               , "Прогрессирование застойной сердечной недостаточности", "Тромбоэмболия", "Асистолия"
               , "Фибрилляция желудочков "],
            x=dataframe_patients.get_forecasting_cause_fatal_outcome(),
            orientation="h",
            marker=dict(color="#0073e4"),
        )]
        return pie, bar
    else:
        return pie, bar


@app.callback(
    Output("id_data_upload_btn", "n_clicks"),
    Input("id_data_upload_btn", "n_clicks"),
)
def data_upload(n_clicks):
    if n_clicks:
        dataframe_patients.upload_data()
        return None
    raise PreventUpdate


@app.callback(
    [Output("id_table_patients", "data"),
    Output("id_add_patient_btn", "n_clicks"),
    Output("id_patients_info_tab", "children")],
    inputs={
        "all_inputs": {
            "button": Input("id_add_patient_btn", "n_clicks"),
            "surname": Input("id_input_surname", "value"),
            "name": Input("id_input_name", "value"),
            "middle_name": Input("id_middle_name", "value"),
            "gender": Input("id_select_patient_gender", "value"),
            "date_birth": Input("id_select_patient_date_birth", "date"),
            "number_myocardial_infarctions": Input("id_number_myocardial_infarctions", "value"),
            "duration_stenocardia": Input("id_duration_stenocardia", "value"),
            "functional_class_stenocardia": Input("id_functional_class_stenocardia", "value"),
            "characteristics_ashd": Input("id_characteristics_ashd", "value"),
            "hypertension": Input("id_hypertension", "value"),
            "symptomatic_hypertension": Input("id_symptomatic_hypertension", "on"),
            "arterial_hypertension_duration": Input("id_arterial_hypertension_duration", "value"),
            "chronic_heart_failure": Input("id_chronic_heart_failure", "value"),
            "cardiovascular_disorders_anamnesis": Input("id_cardiovascular_disorders_anamnesis", "value"),
            "heart_block_anamnesis": Input("id_heart_block_anamnesis", "value"),
            "accompanying_illnesses": Input("id_accompanying_illnesses", "value"),
            "systolic_pressure": Input("id_systolic_pressure", "value"),
            "diastolic_pressure": Input("id_diastolic_pressure", "value"),
            "cardiovascular_disorders": Input("id_cardiovascular_disorders", "value"),
            "infarction_anterior_wall_left_ventricle": Input("id_infarction_anterior_wall_left_ventricle", "value"),
            "infarction_lateral_wall_left_ventricle": Input("id_infarction_lateral_wall_left_ventricle", "value"),
            "infarction_inferior_wall_left_ventricle": Input("id_infarction_inferior_wall_left_ventricle", "value"),
            "infarction_posterior_wall_left_ventricle": Input("id_infarction_posterior_wall_left_ventricle", "value"),
            "right_ventricular_myocardial_infarction": Input("id_right_ventricular_myocardial_infarction", "on"),
            "rhythm_ecg": Input("id_rhythm_ecg", "value"),
            "cardiovascular_disorders_ecg": Input("id_cardiovascular_disorders_ecg", "value"),
            "heart_block_ecg": Input("id_heart_block_ecg", "value"),
            "fibrinolytic_therapy": Input("id_fibrinolytic_therapy", "value"),
            "hypokalemia": Input("id_hypokalemia", "on"),
            "potassium_content": Input("id_potassium_content", "value"),
            "increasing_sodium": Input("id_increasing_sodium", "on"),
            "sodium": Input("id_sodium", "value"),
            "alt": Input("id_alt", "value"),
            "ast": Input("id_ast", "value"),
            "leukocytes": Input("id_leukocytes", "value"),
            "erythrocytes": Input("id_erythrocytes", "value"),
            "time_anginal_attack": Input("id_time_anginal_attack", "value"),
            "medications_cardio_team": Input("id_medications_cardio_team", "value"),
            "medications": Input("id_medications", "value")
        }
    },
)
def entry_patient_into_df(all_inputs):
    if all_inputs['button']:
        del all_inputs['button']

        dataframe_patients.add_entry(all_inputs)
        table = dataframe_patients.to_dict(columns=["surname", "name", "middle_name"], orient="rows")
        return table, None, build_patients_info_layout()
    raise PreventUpdate


if __name__ == "__main__":
    app.run_server(debug=True)
