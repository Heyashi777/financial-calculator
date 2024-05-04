import dash
import dash_core_components as dcc
import dash_html_components as html
from dash import Dash, dcc, html, Input, Output, callback, dash_table
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
import numpy as np
import pandas as pd
def make_better_plot(fig: go.Figure, title: str, xaxis_title = 'Период', yaxis_title = 'Кол-во человек' ):
    fig.update_layout(title = title,
                                    xaxis_title = xaxis_title,
                                    yaxis_title = yaxis_title,
                                    font_family="Sitka Small",
                                    legend=dict(
                                                title=None,
                                                orientation="h",
                                                y=1,
                                                yanchor="bottom",
                                                x=0.5,
                                                xanchor="center"
                                               )
                                    )
    fig.update_xaxes(showline=True, linewidth=2, linecolor='black', mirror=True, gridwidth=1,
                               gridcolor='#E6FFFF')
    fig.update_yaxes(showline=True, linewidth=2, linecolor='black', mirror=True, gridwidth=1,
                               gridcolor='#E6FFFF')

app = dash. Dash(__name__)
app.layout = html.Div([
                        html.H1(children = 'Пример финансового калькулятора',
                                style = {
                                         'textAlign': 'center'
                                        }
                                ),
                        html.Hr(),
                        html.H5(children = 'Срок накопления (лет)',
                                style = {
                                         'textAlign': 'center'
                                        }
                                ),
                        dcc.Input(id="invest_age",
                                  type="number",
                                  min=1, max=100,
                                  step=1,
                                  placeholder="лет",
                                  style={'marginRight':'10px',
                                         'width': 300,
                                         'margin': '0 auto',
                                         'display': 'flex',
                                         'justify-content': 'center'
                                         }
                                  ),
                        html.Br(),
                        html.H5(children = 'среднегодовая доходность (%)',
                                style = {
                                         'textAlign': 'center'
                                        }
                                ),
                        dcc.Input(id="year_income_exp",
                                  type="number",
                                  min=1, max=1500,
                                  step=1,
                                  placeholder="%",
                                  style={'marginRight':'10px',
                                         'width': 300,
                                         'margin': '0 auto',
                                         'display': 'flex',
                                         'justify-content': 'center'
                                         }
                                  ),
                        html.Br(),
                        html.H5(children = 'разовая инвестиционная сумма ($)',
                                style = {
                                         'textAlign': 'center'
                                        }
                                ),
                        dcc.Input(id="first_pay",
                                  type="number",
                                  min=1000, max=100000000000,
                                  step=100,
                                  placeholder="$",
                                  style={'marginRight':'10px',
                                         'width': 300,
                                         'margin': '0 auto',
                                         'display': 'flex',
                                         'justify-content': 'center'
                                         }
                                  ),
                        html.Br(),
                        html.H5(children = 'ежемесяячно инвестируемая сумма ($)',
                                style = {
                                         'textAlign': 'center'
                                        }
                                ),
                        dcc.Input(id="month_pays",
                                  type="number",
                                  min=100, max=1000000000000,
                                  step=50,
                                  placeholder="$",
                                  style={'marginRight':'10px',
                                         'width': 300,
                                         'margin': '0 auto',
                                         'display': 'flex',
                                         'justify-content': 'center'
                                         }
                                  ),
                        html.Div(id="your_capital_after_years"),
    ])

@callback(Output('your_capital_after_years', 'children'),
          Input('invest_age', 'value'),
          Input('year_income_exp', 'value'),
          Input('first_pay', 'value'),
          Input('month_pays', 'value'))
def render_content(invest_age, year_income_exp, first_pay, month_pays):
    df = pd.DataFrame()
    df['Год'], df['НС'], df['Начальный баланс'] = range(invest_age + 1), range(invest_age + 1), range(invest_age + 1)
    df['Пополнено за год'], df['Суммарные покопления'] = range(invest_age + 1), range(invest_age + 1)
    df['Начисленные проценты'], df['Суммарный процент'] = range(invest_age + 1), range(invest_age + 1)
    df['Итоговый баланс'] = range(invest_age + 1)
    df.at[0, 'Итоговый баланс'] = first_pay
    for i in range(1, invest_age + 2):
        df.at[i, 'Год'] = i
        df.at[i, 'НС'] = first_pay
        df.at[i, 'Начальный баланс'] = df.iloc[i-1,7].astype(float)
        df.at[i, 'Пополнено за год'] = month_pays
        df.at[i, 'Суммарные покопления'] = month_pays * i
        df.at[i, 'Начисленные проценты'] = (df.iloc[i, 2].astype(float) + df.iloc[i, 3].astype(float))*(year_income_exp/100)
        df.at[i, 'Суммарный процент'] = df.iloc[i, 5].astype(float) + df.iloc[i-1, 6].astype(float)
        df.at[i, 'Итоговый баланс'] = df.iloc[i, 2].astype(float) + df.iloc[i, 3].astype(float) + df.iloc[i, 5].astype(float)
    df = df[1:]
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df['Год'], y=df['Итоговый баланс'], name="Итоговый баланс", marker_color='#233d4d'))
    fig.add_trace(go.Scatter(x=df['Год'], y=df['Суммарный процент'], name="Суммарный процент",
                             line_shape='linear', line_color='#fe7f2d'))
    fig.add_trace(go.Scatter(x=df['Год'], y=df['Суммарные покопления'], name="Суммарные покопления",
                             line_shape='linear', line_color='#fcca46'))
    make_better_plot(fig, 'итоговый баланс', 'Год', '$')
    return html.Div([
                        dcc.Graph(figure=fig)
                    ])





if __name__ == '__main__':
    app.run_server(port=3939, host="0.0.0.0")
