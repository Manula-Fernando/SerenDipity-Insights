# Dinil Bandara- 003
# Manula Fernando - 004

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import calendar
import requests
from dash.dependencies import Input, Output, State
import time
import pycountry
import json
from urllib.request import urlopen
import os
import base64
from PIL import Image
import io
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM


app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[
        'https://cdnjs.cloudflare.com/ajax/libs/tailwindcss/2.2.19/tailwind.min.css',
        'https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap',
        'https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css',
        'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css'
    ]
)

app.title = "Sri Lanka Tourism Dashboard"
server = app.server


COLORS = {
    'primary': '#FF4B2B',  
    'secondary': '#009C72',  
    'accent1': '#FFB800',   
    'accent2': '#1A73E8',   
    'background': '#FFF9F0', 
    'text': '#2C3E50'
}



app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
            
            body {
                font-family: 'Poppins', sans-serif;
                background: linear-gradient(rgba(255,255,255,0.92), rgba(255,255,255,0.92)),
                            url('https://images.unsplash.com/photo-1546708723-b4a0f2c80481?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80');
                background-size: cover;
                background-attachment: fixed;
                background-position: center;
            }

            .sl-pattern {
                background-color: #ffffff;
                background-image: url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M11 18c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm48 25c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm-43-7c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm63 31c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM34 90c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm56-76c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM12 86c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm28-65c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm23-11c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-6 60c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm29 22c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zM32 63c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm57-13c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-9-21c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM60 91c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM35 41c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM12 60c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2z' fill='%23ff4b2b' fill-opacity='0.05' fill-rule='evenodd'/%3E%3C/svg%3E");
            }

            .overview-card {
                background: rgba(255, 255, 255, 0.95);
                border-radius: 15px;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
                transition: all 0.3s ease;
                border: 2px solid transparent;
                position: relative;
                overflow: hidden;
            }

            .overview-card::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 4px;
                background: linear-gradient(90deg, #FF4B2B, #009C72);
            }

            .overview-card:hover {
                transform: translateY(-5px);
                border-color: #FF4B2B;
            }

            .stat-value {
                font-size: 2.5rem;
                font-weight: bold;
                background: linear-gradient(120deg, #FF4B2B, #009C72);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
            }

            .sl-icon {
                font-size: 2.5rem;
                color: #FF4B2B;
                margin-bottom: 15px;
                transition: all 0.3s ease;
            }

            .overview-card:hover .sl-icon {
                transform: scale(1.1);
                color: #009C72;
            }

            .dash-tabs {
                margin-bottom: 20px;
            }

            .dash-tab {
                padding: 15px 25px !important;
                font-weight: 500 !important;
                color: #2C3E50 !important;
                border-radius: 10px 10px 0 0 !important;
                border: none !important;
                background-color: rgba(255, 255, 255, 0.9) !important;
                transition: all 0.3s ease !important;
            }

            .dash-tab--selected {
                background: linear-gradient(135deg, #FF4B2B, #009C72) !important;
                color: white !important;
            }

            .quick-facts {
                background: rgba(255, 255, 255, 0.95);
                border-radius: 15px;
                border: 1px solid rgba(255, 75, 43, 0.2);
            }

            .quick-fact-item {
                padding: 12px;
                border-radius: 8px;
                background: rgba(255, 75, 43, 0.05);
                margin-bottom: 8px;
                transition: all 0.3s ease;
            }

            .quick-fact-item:hover {
                background: rgba(0, 156, 114, 0.1);
                transform: translateX(5px);
            }

            .chart-container {
                background: white;
                border-radius: 15px;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
                padding: 20px;
                margin-top: 20px;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''


def safe_read_csv(file_path, **kwargs):
    try:
        return pd.read_csv(file_path, **kwargs)
    except FileNotFoundError:
        print(f"Warning: {file_path} not found")
        return pd.DataFrame()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return pd.DataFrame()


arrivals_data = {
    '2024': safe_read_csv(r'C:\Users\wwmsf\Documents\Computational Financial Analytics\Dashboard\Dashboard\2024_arrivals.csv', thousands=',', decimal='.'),
    '2023': safe_read_csv(r'C:\Users\wwmsf\Documents\Computational Financial Analytics\Dashboard\Dashboard\2023_arrivals.csv', thousands=',', decimal='.'),
    '2022': safe_read_csv(r'C:\Users\wwmsf\Documents\Computational Financial Analytics\Dashboard\Dashboard\2022_arrivals.csv', thousands=',', decimal='.'),
    '2021': safe_read_csv(r'C:\Users\wwmsf\Documents\Computational Financial Analytics\Dashboard\Dashboard\2021_arrivals.csv', thousands=',', decimal='.'),
    '2020': safe_read_csv(r'C:\Users\wwmsf\Documents\Computational Financial Analytics\Dashboard\Dashboard\2020_arrivals.csv', thousands=',', decimal='.'),
    '2019': safe_read_csv(r'C:\Users\wwmsf\Documents\Computational Financial Analytics\Dashboard\Dashboard\2019_arrivals.csv', thousands=',', decimal='.')
}
purpose_data = pd.read_csv(r'C:\Users\wwmsf\Documents\Computational Financial Analytics\Dashboard\Dashboard\tourism_data_purpose_of_visit.csv')

def create_overview_card(title, value, icon, description):
    return html.Div([
        html.Div([
            html.I(className=f"fas {icon} sl-icon animate__animated animate__fadeIn"),
            html.H3(title, className="text-xl font-semibold mb-2 text-gray-700"),
            html.Div(value, className="stat-value animate__animated animate__fadeInUp"),
            html.P(description, className="text-sm text-gray-600 mt-2")
        ], className="p-6")
    ], className="overview-card")

def get_exchange_rate():
        url = "https://api.exchangerate-api.com/v4/latest/USD"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return round(data['rates'].get('LKR', 'Unavailable'), 2)
        else:
            return 'Unavailable'

@app.callback(
Output('exchange-rate', 'children'),
[Input('interval-component', 'n_intervals')]
    )
def update_exchange_rate(n):
    return f"{get_exchange_rate()} LKR"


dcc.Interval(
    id='interval-component',
    interval=24*60*60*1000, 
    n_intervals=0
    )

def get_2024_total_arrivals():
    try:
       
        data_2024 = arrivals_data['2024']
        
        
        total_2024 = data_2024.iloc[-1]['TOTAL (Jan - Dec)']
        
     
        if isinstance(total_2024, str):
            total_2024 = int(total_2024.replace(',', ''))
        
        return int(total_2024)
        
    except Exception as e:
        print(f"Error calculating 2024 arrivals: {e}")
        return 0
        
def create_overview_layout():
    try:
        current_year = '2024'
        current_year_data = arrivals_data[current_year]
        
        total_arrivals = get_2024_total_arrivals()
        
        
        months = [col for col in current_year_data.columns if col not in ['Country', 'TOTAL (Jan - Dec)']]
        latest_month = months[-1] if len(months) >= 1 else "No data"
        latest_arrivals = current_year_data[latest_month].sum() if latest_month != "No data" else 0
        
       
        if 'Country' in current_year_data.columns and months:
            if 'TOTAL' in current_year_data['Country'].values:
                current_year_data = current_year_data[current_year_data['Country'] != 'TOTAL']
            country_totals = current_year_data[months].sum(axis=1)
            top_country = current_year_data.loc[country_totals.idxmax(), 'Country']
        else:
            top_country = "Data unavailable"

        return html.Div([
            html.Div([
                html.Div([
                    html.H1(" 🏖️ SerenDipity InsiGhts 🌴 ", 
                           className="text-4xl font-bold text-center mb-2 text-primary"),
                    html.P("Experience the Wonder of Asia 🇱🇰 ", 
                           className="text-xl text-center text-gray-600")
                ], className="mb-8 animate__animated animate__fadeIn")
            ], className="container mx-auto px-4"),

           
            html.Div([
                create_overview_card(
                    "Total Tourist Arrivals",
                    f"{int(total_arrivals):,}",
                    "fa-plane-arrival",
                    "Cumulative arrivals for the current year"
                ),
                create_overview_card(
                    f"Latest Month ({latest_month})",
                    f"{int(latest_arrivals):,}",
                    "fa-calendar-alt",
                    "Most recent monthly arrivals"
                ),
                create_overview_card(
                    "Top Source Market",
                    top_country,
                    "fa-globe-asia",
                    "Leading tourist origin country"
                ),
                create_overview_card(
                        "LKR to USD Rate",
                        f"{get_exchange_rate()} LKR",
                        "fa-money-bill-wave",
                        "Live exchange rate updated every day"
                )
            ], className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8"),

            
            html.Div([
                html.H3("🌟 Discover Sri Lanka", className="text-2xl font-bold mb-4"),
                html.Div([
                    html.Div([
                        html.Div("🏖️ 1,340km of Pristine Coastline", className="quick-fact-item"),
                        html.Div("🍃 8 UNESCO World Heritage Sites", className="quick-fact-item"),
                        html.Div("🐘 26 National Parks", className="quick-fact-item"),
                    ], className="space-y-4"),
                    html.Div([
                        html.Div("☀️ Year-round Tropical Climate", className="quick-fact-item"),
                        html.Div("🌿 500,000 Acres of Tea Plantations", className="quick-fact-item"),
                        html.Div("🏔️ Central Highlands up to 2,524m", className="quick-fact-item"),
                    ], className="space-y-4")
                ], className="grid grid-cols-1 md:grid-cols-2 gap-4")
            ], className="quick-facts p-6 mb-8"),

            
            html.Div([
                dcc.Graph(
                    id='tourism-highlights',
                    figure=create_highlights_chart(current_year_data)
                )
            ], className="chart-container")
        ], className="container mx-auto px-4 py-8 sl-pattern")
    except Exception as e:
        return html.Div([
            html.H2("Error Loading Dashboard", 
                    className="text-2xl font-bold text-center text-red-600 mb-4"),
            html.P(f"Error details: {str(e)}", 
                  className="text-center text-gray-600")
        ], className="p-6")

def create_highlights_chart(data):
    try:
        
        months = [col for col in data.columns if col not in ['Country', 'TOTAL (Jan - Dec)']]
        values = [data[month].sum() for month in months]
        
        fig = go.Figure()
        
       
        fig.add_trace(go.Bar(
            x=months,
            y=values,
            marker_color=COLORS['secondary'],
            hovertemplate='Month: %{x}<br>Arrivals: %{y:,.0f}<extra></extra>'
        ))
        
        
        fig.add_trace(go.Scatter(
            x=months,
            y=values,
            mode='lines',
            name='Trend',
            line=dict(color=COLORS['primary'], width=2, dash='dot'),
            hovertemplate='Month: %{x}<br>Trend: %{y:,.0f}<extra></extra>'
        ))
        
        fig.update_layout(
            title={
                'text': "Monthly Tourist Arrivals Trend for 2024",
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': dict(size=20, color=COLORS['text'])
            },
            template='plotly_white',
            height=500,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            paper_bgcolor='rgba(255,255,255,0)',
            plot_bgcolor='rgba(255,255,255,0.5)',
            margin=dict(t=80, r=30, b=40, l=30),
            xaxis_title="Month",
            yaxis_title="Number of Arrivals",
            xaxis=dict(
                tickangle=-45,
                gridcolor='rgba(0,0,0,0.1)',
                zeroline=False
            ),
            yaxis=dict(
                gridcolor='rgba(0,0,0,0.1)',
                zeroline=False
            ),
            hovermode='x unified'
        )
        
        return fig
    except Exception as e:
        print(f"Error creating highlights chart: {e}")
        return go.Figure()


def create_arrivals_layout():
    current_year = '2024'
    months = [col for col in arrivals_data[current_year].columns if col != 'Country']
    
    return html.Div([
        
        html.H2(
    "Tourist Arrivals Analysis",
    style={
        'background': f'linear-gradient(to right, {COLORS["primary"]}, {COLORS["secondary"]})',
        'WebkitBackgroundClip': 'text',
        'WebkitTextFillColor': 'transparent',
        'backgroundClip': 'text',
        'fontSize': '2.25rem',
        'fontWeight': 'bold',
        'textAlign': 'center',
        'marginBottom': '0.5rem'
    },
    className="animate__animated animate__fadeIn"
),
        html.P(
            "Explore and analyze tourist arrival patterns across different time periods",
            className="text-xl text-center text-gray-600 mb-8"
        ),
        
       
        html.Div([
            
            html.Div([
                html.Div(style={
                    'cssText': '''
                        .year-radio-group input[type="radio"]:checked + label {
                            background: linear-gradient(135deg, #FF4B2B, #009C72) !important;
                            color: white !important;
                            border-color: transparent !important;
                            box-shadow: 0 4px 12px rgba(255, 75, 43, 0.3);
                        }
                        .year-radio-group label:hover {
                            background: #FFF0ED;
                            transform: translateY(-2px);
                            box-shadow: 0 4px 8px rgba(255, 75, 43, 0.2);
                        }
                    '''
                })
            ]),

            
            html.Div([
                
                html.Div([
                    html.Label(
                        'Select Year:', 
                        className="font-bold text-primary mb-2 block"
                    ),
                    dcc.RadioItems(
                        id='year-selector',
                        options=[
                            {'label': str(year), 'value': str(year)}
                            for year in ['2019', '2020', '2021', '2022', '2024']
                        ],
                        value='2024',
                        className="year-radio-group",
                        inline=True,
                        inputStyle={"margin-right": "8px"},
                        labelStyle={
                            'display': 'inline-block',
                            'margin': '8px',
                            'padding': '8px 16px',
                            'border-radius': '20px',
                            'border': f'2px solid {COLORS["primary"]}',
                            'cursor': 'pointer',
                            'transition': 'all 0.3s ease',
                            'background': 'white',
                            'color': '#2C3E50',
                            'font-weight': '500'
                        }
                    )
                ], className="flex-grow"),

               
                html.Div([
                    html.Label(
                        'Select Metric:', 
                        className="font-bold text-primary mb-2 block"
                    ),
                    dcc.Dropdown(
                        id='metric-selector',
                        options=[
                            {'label': 'Total Arrivals', 'value': 'total'},
                            {'label': 'Percentage Change', 'value': 'percentage'},
                            {'label': 'Arrivals by Region', 'value': 'region'}
                        ],
                        value='total',
                        className="w-64"
                    )
                ])
            ], className="flex justify-between items-end mb-6"),

            
            html.Div([
                html.Label(
                    'Select Month Range:', 
                    className="font-bold text-primary mb-2 block"
                ),
                dcc.RangeSlider(
                    id='month-slider',
                    min=0,
                    max=len(months)-1,
                    value=[0, len(months)-1],
                    marks={i: month for i, month in enumerate(months)},
                    step=1,
                    className="mt-4"
                )
            ], className="mb-6")
        ], className="overview-card p-6 mb-6 animate__animated animate__fadeIn"),

        
        html.Div([
            
            html.Div([
                dcc.Graph(id='arrivals-graph')
            ], className="overview-card p-6 w-2/3"),

            html.Div([
                html.H3(
                    "Key Insights", 
                    className="text-xl font-bold text-primary mb-4"
                ),
                html.Div([
                    html.P(
                        """The line graph visualizes three key tourism metrics across monthly intervals for your selected year. 
                        'Total Arrivals' shows absolute visitor numbers helping identify peak seasons and low periods. 
                        'Percentage Change' reveals month-over-month growth or decline trends, highlighting significant shifts in tourism patterns. 
                        'Arrivals by Region' breaks down the distribution of visitors, useful for understanding geographical impact.
                        Use the year selector to track long-term trends and the metric dropdown to switch between these different analytical views.""",
                        className="text-sm text-gray-600 leading-relaxed"
                    )
                ], className="space-y-2")
            ], className="overview-card p-6 w-1/3")
        ], className="flex gap-6 animate__animated animate__fadeIn")
    ], className="container mx-auto px-4 py-8 sl-pattern")

@app.callback(
    [Output('month-slider', 'max'),
     Output('month-slider', 'value'),
     Output('month-slider', 'marks')],
    [Input('year-selector', 'value')]
)

def update_slider(selected_year):
    months = [col for col in arrivals_data[selected_year].columns if col != 'Country']
    max_value = len(months)-2 if selected_year == '2024' else len(months)-2
    slider_value = [0, len(months)-2] if selected_year == '2024' else [0, len(months)-2]
    marks = {i: month for i, month in enumerate(months)}
    return max_value, slider_value, marks

@app.callback(
    Output('arrivals-graph', 'figure'),
    [
        Input('year-selector', 'value'),
        Input('metric-selector', 'value'),
        Input('month-slider', 'value')
    ]
)
def update_graph(selected_year, selected_metric, month_range):
    try:
        df = arrivals_data[selected_year]
        months = [col for col in df.columns if col != 'Country']
        selected_months = months[month_range[0]:month_range[1]+1]
        fig = go.Figure()
        
        if selected_metric == 'total':
            monthly_totals = [df[month].sum() for month in selected_months]
            fig.add_trace(go.Scatter(
                x=selected_months,
                y=monthly_totals,
                mode='lines+markers',
                marker_color=COLORS['secondary'],
                line_color=COLORS['secondary'],
                name='Total Arrivals',
                hovertemplate='Month: %{x}<br>Arrivals: %{y:,.0f}<extra></extra>'
            ))
            title = f'Total Monthly Tourist Arrivals ({selected_year})'
            y_axis_title = 'Number of Arrivals'
            
        elif selected_metric == 'percentage':
            monthly_totals = pd.Series([df[month].sum() for month in selected_months])
            pct_change = monthly_totals.pct_change() * 100
            fig.add_trace(go.Scatter(
                x=selected_months[1:],
                y=pct_change[1:],
                mode='lines+markers',
                marker_color=COLORS['primary'],
                line_color=COLORS['primary'],
                name='Percentage Change',
                hovertemplate='Month: %{x}<br>Change: %{y:.1f}%<extra></extra>'
            ))
            title = f'Month-over-Month Percentage Change ({selected_year})'
            y_axis_title = 'Percentage Change (%)'
            
        else:  
            region_mapping = {
                'Western Europe': ['UK', 'Germany', 'France', 'Italy', 'Netherlands'],
                'Asia': ['India', 'China', 'Japan', 'South Korea', 'Malaysia'],
                'Middle East': ['UAE', 'Saudi Arabia', 'Qatar'],
                'North America': ['USA', 'Canada'],
            }
            
            for region, countries in region_mapping.items():
                region_data = df[df['Country'].isin(countries)][selected_months].sum()
                fig.add_trace(go.Scatter(
                    x=selected_months,
                    y=region_data,
                    mode='lines+markers',
                    name=region,
                    hovertemplate=f'{region}<br>Month: %{{x}}<br>Arrivals: %{{y:,.0f}}<extra></extra>'
                ))
            title = f'Tourist Arrivals by Region ({selected_year})'
            y_axis_title = 'Number of Arrivals'
        
        fig.update_layout(
            title={
                'text': title,
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': dict(size=20, color=COLORS['text'])
            },
            xaxis_title="Month",
            yaxis_title=y_axis_title,
            template='plotly_white',
            height=600,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            paper_bgcolor='rgba(255,255,255,0)',
            plot_bgcolor='rgba(255,255,255,0.5)',
            margin=dict(t=80, r=30, b=40, l=30),
            xaxis=dict(
                tickangle=-45,
                gridcolor='rgba(0,0,0,0.1)',
                zeroline=False
            ),
            yaxis=dict(
                gridcolor='rgba(0,0,0,0.1)',
                zeroline=False
            ),
            hovermode='x unified'
        )
        
        return fig
    except Exception as e:
        print(f"Error updating graph: {e}")
        return go.Figure()

def create_arrival_dynamics_layout():
    return html.Div([
        html.H2("Arrival Dynamics Analysis",  
             style={
        'background': f'linear-gradient(to right, {COLORS["primary"]}, {COLORS["secondary"]})',
        'WebkitBackgroundClip': 'text',
        'WebkitTextFillColor': 'transparent',
        'backgroundClip': 'text',
        'fontSize': '2.25rem',
        'fontWeight': 'bold',
        'textAlign': 'center',
        'marginBottom': '0.5rem'
    }),
        html.P("Analyze travel patterns and correlations", 
               className="text-xl text-center text-gray-600 mb-8"),
        
        
        html.Div([
            html.Div([
                html.Label('Select Purpose of Visit:', 
                          className="text-2xl font-bold text-primary mb-4 block"),
                dcc.RadioItems(
                    id='purpose-selector',
                    options=[
                        {'label': 'Business Travel', 'value': 'Business'},
                        {'label': 'Pleasure/Vacation', 'value': 'Pleasure/Vacation'},
                        {'label': 'Health Tourism', 'value': 'Health'}
                    ],
                    value='Business',
                    className="purpose-radio-group",
                    inline=True,
                    inputStyle={"margin-right": "8px"},
                    labelStyle={
                        'display': 'inline-block',
                        'margin': '8px',
                        'padding': '12px 24px',
                        'border-radius': '20px',
                        'border': f'2px solid {COLORS["primary"]}',
                        'cursor': 'pointer',
                        'transition': 'all 0.3s ease',
                        'background': 'white',
                        'color': COLORS["text"],
                        'font-weight': '500',
                        'box-shadow': '0 2px 4px rgba(0,0,0,0.1)'
                    }
                )
            ], className="mb-6 animate__animated animate__fadeIn"),
        ], className="overview-card p-6 mb-6"),

        
        html.Div([
            dcc.Graph(id='dynamics-scatter')
        ], className="overview-card p-6 animate__animated animate__fadeIn"),

        html.Div([
            html.H3("🔍 Key Insights", 
                   className="text-2xl font-bold mb-4 text-primary"),
            html.Div(id='dynamics-insights', 
                    className="quick-fact-item")
        ], className="quick-facts p-6 mt-6 animate__animated animate__fadeIn")
    ], className="container mx-auto px-4 py-8 sl-pattern")

@app.callback(
    [Output('dynamics-scatter', 'figure'),
     Output('dynamics-insights', 'children')],
    [Input('purpose-selector', 'value')]
)

def update_dynamics_graph(selected_purpose):
    try:
        filtered_data = purpose_data[['Country', 'Total', selected_purpose]]
        Q1 = filtered_data['Total'].quantile(0.25)
        Q3 = filtered_data['Total'].quantile(0.75)
        IQR = Q3 - Q1
        filtered_data = filtered_data[~((filtered_data['Total'] < (Q1 - 1.5 * IQR)) | (filtered_data['Total'] > (Q3 + 1.5 * IQR)))]

        Q1 = filtered_data[selected_purpose].quantile(0.25)
        Q3 = filtered_data[selected_purpose].quantile(0.75)
        IQR = Q3 - Q1
        filtered_data = filtered_data[~((filtered_data[selected_purpose] < (Q1 - 1.5 * IQR)) | (filtered_data[selected_purpose] > (Q3 + 1.5 * IQR)))]
        colors = px.colors.qualitative.Set3  
        country_colors = {country: colors[i % len(colors)] 
                         for i, country in enumerate(filtered_data['Country'])}

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=filtered_data['Total'],
            y=filtered_data[selected_purpose],
            mode='markers',
            marker=dict(
                size=12,
                color=[country_colors[country] for country in filtered_data['Country']],
                line=dict(width=2, color='white'),
                opacity=0.8,
            ),
            text=filtered_data['Country'],
            hovertemplate="<b>%{text}</b><br>" +
                          "Total Arrivals: %{x:,.0f}<br>" +
                          selected_purpose + " Arrivals: %{y:,.0f}<br>" +
                          "<extra></extra>",
        ))
        fig.update_layout(
            title=f"Correlation between Total Arrivals and {selected_purpose} Arrivals",
            xaxis_title="Total Arrivals",
            yaxis_title=f"Number of {selected_purpose} Arrivals",
            template='plotly_white',
            height=500
        )

        
        correlation = filtered_data['Total'].corr(filtered_data[selected_purpose])
        insights = html.Div([
            html.Div([
            html.H4(f"Analysis for {selected_purpose} Travel Patterns",
                className="text-xl font-semibold mb-3 bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent"),
            html.Div([
                html.P(f"Insights between Total Arrivals and {selected_purpose} Arrivals.",
                className="inline font-medium text-gray-700 block mb-2"),
                html.P([
                html.Span(f"Correlation between total arrivals and {selected_purpose} arrivals: ",
                    className="font-medium text-gray-700"),
                html.Span(f"{correlation:.2f}",
                    className="font-bold text-secondary")
                ], className="block")
            ], className="p-4 bg-gray-50 rounded-lg shadow-sm hover:shadow-md transition-shadow duration-300")
            ], className="overview-card p-6 animate__animated animate__fadeIn")
        ], className="space-y-4")

        return fig, insights
    except Exception as e:
        print(f"Error in dynamics graph: {e}")
        return go.Figure(), html.P("Error loading insights")



def get_unique_colors(n_colors):
    """Generate a list of unique colors using plotly's color sequences"""
    colors = px.colors.qualitative.Set3 + px.colors.qualitative.Pastel + px.colors.qualitative.Bold
    while len(colors) < n_colors:
        colors += colors
    return colors[:n_colors]

def preprocess_arrivals_data(df):
    """Preprocess arrivals data by removing the last row (totals)"""
    return df.iloc[:-1]  

@app.callback(
    Output('treemap-container', 'children'),
    [Input('year-selector', 'value')])
    
def update_treemap(selected_year):
    df = arrivals_data[selected_year]
    processed_data = preprocess_arrivals_data(df)
    unique_countries = processed_data['Country'].unique()
    unique_colors = get_unique_colors(len(unique_countries))
    color_map = dict(zip(unique_countries, unique_colors))
    
    # Create treemap
    fig = px.treemap(
        processed_data,
        path=['Country'],
        values='TOTAL (Jan - Dec)',
        title=f'Tourist Arrivals by Country ({selected_year})',
        custom_data=['Country', 'TOTAL (Jan - Dec)']
    )
    
    fig.update_traces(
        marker=dict(colors=[color_map[country] for country in processed_data['Country']]),
        texttemplate='<span style="font-size: 16px">%{customdata[0]}<br>%{customdata[1]:,.0f}</span>',
        textposition='middle center',
        hovertemplate='<b>%{customdata[0]}</b><br>Arrivals: %{customdata[1]:,.0f}<extra></extra>'
    )
    
    fig.update_layout(
        height=700,
        paper_bgcolor=COLORS['background'],
        plot_bgcolor=COLORS['background'],
        font=dict(color=COLORS['text'], size=14),
        title=dict(font=dict(size=20))
    )
    
    return dcc.Graph(figure=fig)

@app.callback(
    Output('barchart-container', 'children'),
    [Input('year-selector', 'value')]
)
def update_barchart(selected_year):
    df = arrivals_data[selected_year]
    processed_data = preprocess_arrivals_data(df)
    processed_data = processed_data.sort_values('TOTAL (Jan - Dec)', ascending=False)
    top_10_data = processed_data.head(10)
    top_10_data = top_10_data.iloc[::-1]
    unique_countries = top_10_data['Country'].unique()
    unique_colors = get_unique_colors(len(unique_countries))

    fig = go.Figure(go.Bar(
        x=top_10_data['TOTAL (Jan - Dec)'],
        y=top_10_data['Country'],
        orientation='h',
        marker_color=unique_colors,
        text=top_10_data['TOTAL (Jan - Dec)'].apply(lambda x: f'{x:,.0f}'),
        textposition='auto',
    ))
    
    fig.update_layout(
        title=dict(
            text=f'Top 10 Source Markets ({selected_year})',
            font=dict(size=20)
        ),
        height=700,
        paper_bgcolor=COLORS['background'],
        plot_bgcolor=COLORS['background'],
        font=dict(color=COLORS['text'], size=14),
        xaxis_title="Number of Arrivals",
        yaxis_title="Country",
        margin=dict(l=200), 
        yaxis=dict(
            tickfont=dict(size=16),
            title_font=dict(size=16)
        ),
        xaxis=dict(
            tickfont=dict(size=14),
            title_font=dict(size=16)
        )
    )
    
    return dcc.Graph(figure=fig)

def create_countries_layout():
    return html.Div([
        html.H1(
            "Source Markets Analysis",
            style={
                'background': f'linear-gradient(to right, {COLORS["primary"]}, {COLORS["secondary"]})',
                'WebkitBackgroundClip': 'text',
                'WebkitTextFillColor': 'transparent',
                'backgroundClip': 'text',
                'fontSize': '2.25rem',
                'fontWeight': 'bold',
                'textAlign': 'center',
                'marginBottom': '0.5rem'
            },
        ),
        
        html.Div([
            html.Label(
                'Select Year:', 
                className="font-bold text-primary mb-2 block text-lg"
            ),
            dcc.Dropdown(
                id='year-selector',
                options=[{'label': year, 'value': year} for year in arrivals_data.keys()],
                value='2024',
                className="w-64"
            )
        ], className="mb-6"),
        
        html.Div([
            html.Div([
                html.H3("Insights", className="text-xl font-bold text-primary mb-4"),
                html.Ul([
                    html.Li(
                        "This tab highlights the top-performing source countries for tourism.",
                        className="mb-3 text-gray-600 flex items-center before:content-['•'] before:mr-2 before:text-primary"
                    ),
                    html.Li(
                        "Visualizations update dynamically based on the selected year.",
                        className="mb-3 text-gray-600 flex items-center before:content-['•'] before:mr-2 before:text-primary"
                    ),
                    html.Li(
                        "The treemap provides a detailed breakdown of all source markets.",
                        className="mb-3 text-gray-600 flex items-center before:content-['•'] before:mr-2 before:text-primary"
                    ),
                    html.Li(
                        "The bar chart compares the top 10 source markets for quick insights.",
                        className="mb-3 text-gray-600 flex items-center before:content-['•'] before:mr-2 before:text-primary"
                    ),
                    html.Li(
                        "Identify trends, emerging markets, or dominant countries.",
                        className="mb-3 text-gray-600 flex items-center before:content-['•'] before:mr-2 before:text-primary"
                    ),
                ], className="space-y-2")
            ], className="overview-card p-6 w-1/4 animate__animated animate__fadeIn h-[600px] sticky top-6"),
            
            html.Div([
                html.Div(
                    id='treemap-container', 
                    className="overview-card p-6 mb-6 animate__animated animate__fadeIn h-[600px]"
                ),
                html.Div(
                    id='barchart-container',
                    className="overview-card p-6 animate__animated animate__fadeIn"
                )
            ], className="w-3/4 space-y-4"),
        ], className="flex gap-6")
    ], className="container mx-auto px-4 py-8 sl-pattern") 

def load_geo_data():
    years = ['2019', '2020', '2021', '2022', '2023','2024']
    return {
        year: pd.read_csv(f'C:\\Users\\wwmsf\\Documents\\Computational Financial Analytics\\Dashboard\\Dashboard\\{year}_arrivals.csv')
        for year in years
    }

def clean_geo_data(df):
    df = df.copy()
    df['TOTAL (Jan - Dec)'] = df['TOTAL (Jan - Dec)'].astype(str).str.replace(',', '').astype(float)
    month_columns = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    for col in month_columns:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace(',', '').astype(float)
    return df

geo_yearly_dfs = load_geo_data()
geo_cleaned_data = {year: clean_geo_data(df) for year, df in geo_yearly_dfs.items()}

def create_geo_analysis_layout():
    return html.Div([

        html.Div([
            html.H2(
                "Geographic Analysis", 
                style={
        'background': f'linear-gradient(to right, {COLORS["primary"]}, {COLORS["secondary"]})',
        'WebkitBackgroundClip': 'text',
        'WebkitTextFillColor': 'transparent',
        'backgroundClip': 'text',
        'fontSize': '2.25rem',
        'fontWeight': 'bold',
        'textAlign': 'center',
        'marginBottom': '0.5rem'
    },
            ),
            html.P(
                "Explore tourist arrivals across different regions", 
                className="text-center text-gray-600 mb-6"
            )
        ], className="mb-8"),

        html.Div([
            html.Label(
                'Select Year:', 
                className="font-bold text-primary mb-2 block text-lg"
            ),
            dcc.Dropdown(
                id='year-selector',
                options=[{'label': str(year), 'value': str(year)} for year in geo_cleaned_data.keys()],
                value='2024',
                className="w-64 mx-auto"
            )
        ], className="mb-8"),


        html.Div([
            html.Div(
                dcc.Graph(id='arrivals-map', className="h-[500px]"),  
                className="overview-card p-6 animate__animated animate__fadeIn mb-6"
            ),
        
            html.Div([

                html.Div([
                    dcc.Graph(id='region-pie', className="h-[400px]"),
                    html.Div(
                        id='region-title',
                        className="text-center font-bold mt-2 text-primary"
                    )
                ], className="overview-card p-6 animate__animated animate__fadeIn w-1/2"),
                
                html.Div([
                    html.H3("Regional Insights", 
                           className="text-2xl font-bold mb-6 bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent"),
                    html.Div([
                
                        html.Div([
                            html.H4("Key Features", 
                                   className="text-lg font-semibold mb-3 text-secondary"),
                            html.Ul([
                                html.Li("Interactive world map with color-coded tourist arrivals", 
                                       className="mb-2 flex items-center before:content-['•'] before:mr-2 before:text-primary"),
                                html.Li("Dynamic monthly distribution visualization", 
                                       className="mb-2 flex items-center before:content-['•'] before:mr-2 before:text-primary")
                            ], className="mb-4 text-gray-700")
                        ], className="mb-6"),
                    
                        html.Div([
                            html.H4("How to Use", 
                                   className="text-lg font-semibold mb-3 text-secondary"),
                            html.P([
                                "Click on any country to view detailed monthly tourist distribution. ",
                                html.Br(),
                                "Color intensity indicates visitor volume:",
                                html.Br(),
                                html.Span("Dark Purple ", className="font-medium text-purple-800"),
                                "→ minimal arrivals",
                                html.Br(),
                                html.Span("Bright Yellow-Green ", className="font-medium text-green-500"),
                                "→ peak arrivals (700k+)"
                            ], className="text-gray-700 leading-relaxed")
                        ], className="mb-4")
                    ], className="bg-white rounded-lg p-6 shadow-sm hover:shadow-md transition-shadow duration-300")
                ], className="overview-card p-6 animate__animated animate__fadeIn w-1/2")
            ], className="flex gap-6")
        ])
    ], className="container mx-auto px-4 py-8 sl-pattern")

@app.callback(
    Output('arrivals-map', 'figure'),
    Input('year-selector', 'value')
)
def update_map(selected_year):
    df = geo_cleaned_data[selected_year]
    fig = px.choropleth(
        df,
        locations='Country',
        locationmode='country names',
        color='TOTAL (Jan - Dec)',
        hover_name='Country',
        color_continuous_scale='Viridis',
        hover_data={'TOTAL (Jan - Dec)': ':,.0f'},
        width=1000, 
        height=600  
    )
    
   
    fig.update_layout(
        title=f'Tourist Arrivals - {selected_year}',
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection=dict(
                type='equirectangular',
                scale=1.0  
            ),
            landcolor='rgb(242, 242, 242)',
            countrycolor="rgb(204, 204, 204)",
            coastlinecolor="rgb(255, 255, 255)",
            showland=True,
            
            lonaxis=dict(
                range=[-165, 165], 
                showgrid=False
            ),
            lataxis=dict(
                range=[-60, 85],
                showgrid=False
            ),

            domain=dict(
                x=[0, 1],
                y=[0, 1]
            )
        ),
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="Arial",
            bordercolor="black",
            align="left"
        ),
        coloraxis_colorbar_title='Total Arrivals',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=30, b=0),
        autosize=False
    )
    
    fig.update_traces(
        hoverinfo='location+z', 
        hovertemplate="<b>%{hovertext}</b><br>" +
                     "Total Arrivals: %{z:,.0f}<extra></extra>"
    )
    
    return fig

@app.callback(
    [Output('region-pie', 'figure'),
     Output('region-title', 'children')],
    [Input('arrivals-map', 'clickData'),
     Input('year-selector', 'value')]
)
def update_pie(click_data, selected_year):
    if not click_data:
        return go.Figure(), "Click a country to see monthly breakdown"
    
    clicked_country = click_data['points'][0]['location']
    df = geo_cleaned_data[selected_year]
    country_data = df[df['Country'] == clicked_country].iloc[0]

    months = ['January', 'February', 'March', 'April', 'May', 'June', 
             'July', 'August', 'September', 'October', 'November', 'December']
    monthly_data = {month: country_data[month] for month in months if month in country_data.index}
    

    fig = go.Figure(data=[go.Pie(
        labels=list(monthly_data.keys()),
        values=list(monthly_data.values()),
        hole=0.3
    )])
    
    fig.update_layout(
        title=f'Monthly Tourist Arrivals - {clicked_country}',
        height=500
    )
    
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate="Month: %{label}<br>Arrivals: %{value:,.0f}<br>Percentage: %{percent}"
    )
    
    return fig, f"Country: {clicked_country}"


app.layout = html.Div([
    dcc.Tabs(
        id="tabs",
        value="overview",
        className="dash-tabs",
        children=[
            dcc.Tab(
                label="Overview 🏠",
                value="overview",
                className="dash-tab",
                selected_className="dash-tab--selected"
            ),
            dcc.Tab(
                label="Inbound Visitors 📊",
                value="arrivals",
                className="dash-tab",
                selected_className="dash-tab--selected"
            ),
            dcc.Tab(
                label="Arrival Dynamics 💰",
                value="arrival_dynamics",
                className="dash-tab",
                selected_className="dash-tab--selected"
            ),
            dcc.Tab(
                label="Top Markets 🌏",
                value="countries",
                className="dash-tab",
                selected_className="dash-tab--selected"
            ),
            dcc.Tab(
                label="Geographic Analysis 🗺️",
                value="geography", 
                className="dash-tab",
                selected_className="dash-tab--selected"
            )
        ]
    ),
            
    html.Div(id="tab-content", className="mt-4")
], className="container mx-auto px-4 py-8")



@app.callback(
    Output("tab-content", "children"),
    [Input("tabs", "value")]
)
def update_tab(tab_name):
    if tab_name == "overview":
        return create_overview_layout()
    elif tab_name == "arrivals":
        return create_arrivals_layout()
    elif tab_name == "arrival_dynamics":
        return create_arrival_dynamics_layout()
    elif tab_name == "countries":
        return  create_countries_layout()
    elif tab_name == "geography":
        return create_geo_analysis_layout()

if __name__ == '__main__':
    app.run(debug=True)
