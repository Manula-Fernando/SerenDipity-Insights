# Filename: modules/layout_dynamics.py

import pandas as pd
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px
from modules.data_loader import purpose_data, COLORS

# --- Layout Function (no changes needed here) ---
def create_arrival_dynamics_layout():
    # ... (This function is fine as it is) ...
    return html.Div([
        html.H2("Arrival Dynamics Analysis",
            style={'background': f'linear-gradient(to right, {COLORS["primary"]}, {COLORS["secondary"]})', 'WebkitBackgroundClip': 'text', 'WebkitTextFillColor': 'transparent', 'backgroundClip': 'text', 'fontSize': '2.25rem', 'fontWeight': 'bold', 'textAlign': 'center', 'marginBottom': '0.5rem'}),
        html.P("Analyze travel patterns and correlations", className="text-xl text-center text-gray-600 mb-8"),
        
        html.Div([
            html.Div([
                html.Label('Select Purpose of Visit:', className="text-2xl font-bold text-primary mb-4 block"),
                dcc.RadioItems(
                    id='purpose-selector-dynamics', # UNIQUE ID
                    options=[{'label': 'Business Travel', 'value': 'Business'}, {'label': 'Pleasure/Vacation', 'value': 'Pleasure/Vacation'}, {'label': 'Health Tourism', 'value': 'Health'}],
                    value='Business',
                    className="purpose-radio-group", inline=True, inputStyle={"margin-right": "8px"},
                    labelStyle={'display': 'inline-block', 'margin': '8px', 'padding': '12px 24px', 'border-radius': '20px', 'border': f'2px solid {COLORS["primary"]}', 'cursor': 'pointer', 'transition': 'all 0.3s ease', 'background': 'white', 'color': COLORS["text"], 'font-weight': '500', 'box-shadow': '0 2px 4px rgba(0,0,0,0.1)'}
                )
            ], className="mb-6 animate__animated animate__fadeIn"),
        ], className="overview-card p-6 mb-6"),
        
        html.Div([dcc.Graph(id='dynamics-scatter')], className="overview-card p-6 animate__animated animate__fadeIn"),
        
        html.Div([
            html.H3("🔍 Key Insights", className="text-2xl font-bold mb-4 text-primary"),
            html.Div(id='dynamics-insights', className="quick-fact-item")
        ], className="quick-facts p-6 mt-6 animate__animated animate__fadeIn")
    ], className="container mx-auto px-4 py-8 sl-pattern")

# --- Callbacks for this layout ---
def register_dynamics_callbacks(app):
    @app.callback(
        [Output('dynamics-scatter', 'figure'),
         Output('dynamics-insights', 'children')],
        [Input('purpose-selector-dynamics', 'value')] # Match UNIQUE ID
    )
    def update_dynamics_graph(selected_purpose):
        try:
            filtered_data = purpose_data[['Country', 'Total', selected_purpose]].copy()
            filtered_data = filtered_data[(filtered_data['Total'] > 0) & (filtered_data[selected_purpose] > 0)]

            for col in ['Total', selected_purpose]:
                Q1, Q3 = filtered_data[col].quantile(0.25), filtered_data[col].quantile(0.75)
                IQR = Q3 - Q1
                lower, upper = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
                filtered_data = filtered_data[(filtered_data[col] >= lower) & (filtered_data[col] <= upper)]

            if filtered_data.empty:
                return go.Figure().update_layout(title_text=f"No data for {selected_purpose} after filtering."), html.P("Not enough data.")

            # Correctly use px.scatter with color and custom_data
            fig = px.scatter(
                filtered_data,
                x='Total',
                y=selected_purpose,
                color='Country',  # Assign color by country for multi-colored dots
                custom_data=['Country'],
                title=f"Correlation: Total Arrivals vs {selected_purpose} Arrivals"
            )

            # Set correct hover template using custom_data for country name
            fig.update_traces(
                mode='markers',
                hovertemplate="<b>%{customdata[0]}</b><br>" +
                              "Total Arrivals: %{x:,.0f}<br>" +
                              selected_purpose + "Arrivals: %{y:,.0f}<br>" +
                              "<extra></extra>",
            )

            fig.update_layout(template='plotly_white', height=500, showlegend=False)

            correlation = filtered_data['Total'].corr(filtered_data[selected_purpose])
            insights = html.P([
                html.Span(f"Correlation for {selected_purpose}: ", className="font-medium text-gray-700"),
                html.Span(f"{correlation:.2f}", className="font-bold text-lg text-secondary")
            ])
            return fig, insights
        except Exception as e:
            print(f"Error in dynamics graph: {e}")
            return go.Figure(), html.P("An error occurred.")