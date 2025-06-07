from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
from modules.data_loader import arrivals_data, COLORS

# --- Layout Function ---
def create_arrivals_layout():
    return html.Div([
        html.H2("Tourist Arrivals Analysis", style={'background': f'linear-gradient(to right, {COLORS["primary"]}, {COLORS["secondary"]})', 'WebkitBackgroundClip': 'text', 'WebkitTextFillColor': 'transparent', 'backgroundClip': 'text', 'fontSize': '2.25rem', 'fontWeight': 'bold', 'textAlign': 'center', 'marginBottom': '0.5rem'}),
        html.P("Explore arrival patterns across different time periods", className="text-xl text-center text-gray-600 mb-8"),
        
        html.Div([
            html.Div([
                html.Label('Select Year:', className="font-bold text-primary mb-2 block"),
                dcc.RadioItems(
                    # UNIQUE ID
                    id='year-selector-arrivals',
                    options=[{'label': str(year), 'value': str(year)} for year in sorted(arrivals_data.keys(), reverse=True)],
                    value='2024',
                    className="year-radio-group", inline=True, inputStyle={"margin-right": "8px"},
                    labelStyle={'display': 'inline-block', 'margin': '8px', 'padding': '8px 16px', 'border-radius': '20px', 'border': f'2px solid {COLORS["primary"]}', 'cursor': 'pointer', 'transition': 'all 0.3s ease', 'background': 'white', 'color': '#2C3E50', 'font-weight': '500'}
                )
            ], className="flex-grow"),
            html.Div([
                html.Label('Select Metric:', className="font-bold text-primary mb-2 block"),
                dcc.Dropdown(
                    id='metric-selector-arrivals',
                    options=[
                        {'label': 'Total Arrivals', 'value': 'total'},
                        {'label': 'Percentage Change', 'value': 'percentage'}
                    ],
                    value='total', className="w-64"
                )
            ])
        ], className="flex flex-wrap justify-between items-end mb-6 overview-card p-6"),

        dcc.Graph(id='arrivals-graph')
    ], className="container mx-auto px-4 py-8 sl-pattern")

# --- Callbacks for this Layout ---
def register_arrivals_callbacks(app):
    @app.callback(
        Output('arrivals-graph', 'figure'),
        [Input('year-selector-arrivals', 'value'),
         Input('metric-selector-arrivals', 'value')]
    )
    def update_arrivals_graph(selected_year, selected_metric):
        try:
            df = arrivals_data.get(selected_year, pd.DataFrame())
            if df.empty:
                return go.Figure(layout={'title': 'No data available for this year.'})

            months = [col for col in df.columns if col not in ['Country', 'TOTAL (Jan - Dec)']]
            # Correctly calculate totals by summing columns from clean data
            monthly_totals = pd.Series([df[month].sum() for month in months], index=months)
            fig = go.Figure()

            if selected_metric == 'total':
                title = f'Total Monthly Tourist Arrivals ({selected_year})'
                y_axis_title = 'Number of Arrivals'
                fig.add_trace(go.Scatter(x=monthly_totals.index, y=monthly_totals.values, mode='lines+markers', marker_color=COLORS['secondary'], line_color=COLORS['secondary'], name='Total Arrivals', hovertemplate='Month: %{x}<br>Arrivals: %{y:,.0f}<extra></extra>'))
            
            elif selected_metric == 'percentage':
                pct_change = monthly_totals.pct_change() * 100
                title = f'Month-over-Month Percentage Change ({selected_year})'
                y_axis_title = 'Percentage Change (%)'
                fig.add_trace(go.Scatter(x=pct_change.index, y=pct_change.values, mode='lines+markers', marker_color=COLORS['primary'], line_color=COLORS['primary'], name='Percentage Change', hovertemplate='Month: %{x}<br>Change: %{y:.1f}%<extra></extra>'))

            fig.update_layout(title={'text': title, 'y': 0.9, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'}, xaxis_title="Month", yaxis_title=y_axis_title, template='plotly_white', height=500, paper_bgcolor='rgba(255,255,255,0)', plot_bgcolor='rgba(255,255,255,0.8)')
            return fig
        except Exception as e:
            print(f"Error updating arrivals graph: {e}")
            return go.Figure()