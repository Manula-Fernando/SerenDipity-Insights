# Filename: modules/layout_overview.py

import pandas as pd
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import requests
from modules.data_loader import arrivals_data, COLORS # Import the clean data

# --- Helper Functions ---
def create_overview_card(title, value, icon, description):
    # This function is correct and needs no changes.
    return html.Div([
        html.Div([
            html.I(className=f"fas {icon} sl-icon animate__animated animate__fadeIn"),
            html.H3(title, className="text-xl font-semibold mb-2 text-gray-700"),
            html.Div(value, className="stat-value animate__animated animate__fadeInUp"),
            html.P(description, className="text-sm text-gray-600 mt-2")
        ], className="p-6")
    ], className="overview-card")

def get_exchange_rate():
    # This function is correct and needs no changes.
    try:
        url = "https://api.exchangerate-api.com/v4/latest/USD"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return round(response.json().get('rates', {}).get('LKR', 'N/A'), 2)
        return 'N/A'
    except requests.RequestException:
        return 'N/A'

def get_current_year_total_arrivals():
    # Corrected function to sum the clean data
    try:
        df = arrivals_data.get('2024', pd.DataFrame())
        if df.empty:
            return 0
        return int(df['TOTAL (Jan - Dec)'].sum())
    except Exception as e:
        print(f"Error in get_current_year_total_arrivals: {e}")
        return 0

def create_highlights_chart(data):
    # Corrected function to sum clean monthly data
    try:
        if data.empty:
            return go.Figure()
        
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

# --- Main Layout Function ---
def create_overview_layout():
    try:
        current_year_data = arrivals_data.get('2024', pd.DataFrame())
        
        if current_year_data.empty:
            return html.Div("Data for 2024 is not available.", className="text-center text-red-500 text-2xl p-10")

        # Use corrected functions and logic that relies on clean data
        total_arrivals = get_current_year_total_arrivals()
        
        months = [col for col in current_year_data.columns if col not in ['Country', 'TOTAL (Jan - Dec)']]
        latest_month = months[-1] if months else "N/A"
        latest_arrivals = current_year_data[latest_month].sum() if latest_month in current_year_data.columns else 0
        
        top_country = current_year_data.loc[current_year_data['TOTAL (Jan - Dec)'].idxmax()]['Country'] if not current_year_data.empty else "N/A"

        return html.Div([
            dcc.Interval(id='interval-component', interval=24*60*60*1000, n_intervals=0),
            html.Div([
                html.H1("🏖️ SerenDipity InsiGhts 🌴", className="text-4xl font-bold text-center mb-2"),
                html.P("Experience the Wonder of Asia 🇱🇰", className="text-xl text-center text-gray-600")
            ], className="mb-8 animate__animated animate__fadeIn"),
            html.Div([
                create_overview_card("Total Tourist Arrivals", f"{total_arrivals:,.0f}", "fa-plane-arrival", "Cumulative arrivals for the current year"),
                create_overview_card(f"Latest Month ({latest_month})", f"{latest_arrivals:,.0f}", "fa-calendar-alt", "Most recent monthly arrivals"),
                create_overview_card("Top Source Market", top_country, "fa-globe-asia", "Leading tourist origin country"),
                html.Div(id='exchange-rate-card')
            ], className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8"),
            html.Div([
                dcc.Graph(id='tourism-highlights', figure=create_highlights_chart(current_year_data))
            ], className="chart-container")
        ], className="container mx-auto px-4 py-8 sl-pattern")
    except Exception as e:
        # Provide a more user-friendly error message
        return html.Div(f"An error occurred while loading the overview: {str(e)}", className="text-center text-red-500 text-2xl p-10")

# --- Callbacks for this Layout ---
def register_overview_callbacks(app):
    @app.callback(
        Output('exchange-rate-card', 'children'),
        Input('interval-component', 'n_intervals')
    )
    def update_exchange_rate_card(n):
        rate = get_exchange_rate()
        return create_overview_card("LKR to USD Rate", f"{rate} LKR", "fa-money-bill-wave", "Live exchange rate updated daily")