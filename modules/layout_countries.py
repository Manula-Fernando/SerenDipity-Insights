from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
from modules.data_loader import arrivals_data, COLORS # Import the clean data

# Helper to get unique colors for the chart
def get_unique_colors(n_colors):
    colors = px.colors.qualitative.Pastel
    return (colors * (n_colors // len(colors) + 1))[:n_colors]

# --- Main Layout Function ---
def create_countries_layout():
    return html.Div([
        html.H1("Source Markets Analysis", style={'background': f'linear-gradient(to right, {COLORS["primary"]}, {COLORS["secondary"]})', 'WebkitBackgroundClip': 'text', 'WebkitTextFillColor': 'transparent', 'backgroundClip': 'text', 'fontSize': '2.25rem', 'fontWeight': 'bold', 'textAlign': 'center', 'marginBottom': '0.5rem'}),
        html.Div([
            html.Label('Select Year:', className="font-bold text-primary mb-2 block text-lg"),
            dcc.Dropdown(
                id='year-selector-countries',
                options=[{'label': year, 'value': year} for year in sorted(arrivals_data.keys(), reverse=True)],
                value='2024',
                className="w-64"
            )
        ], className="mb-6 flex justify-center"),
        html.Div([
            html.Div(id='treemap-container', className="overview-card p-4 w-full lg:w-1/2"),
            html.Div(id='barchart-container', className="overview-card p-4 w-full lg:w-1/2")
        ], className="flex flex-wrap lg:flex-nowrap gap-6")
    ], className="container mx-auto px-4 py-8 sl-pattern")

# --- Callbacks for this layout ---
def register_countries_callbacks(app):
    @app.callback(
        Output('treemap-container', 'children'),
        Input('year-selector-countries', 'value')
    )
    def update_treemap(selected_year):
        # We now directly use the clean `arrivals_data`
        df = arrivals_data.get(selected_year)
        if df is None or df.empty:
            return dcc.Graph(figure=go.Figure().update_layout(title='No data available for treemap.'))

        fig = px.treemap(
            df,
            path=[px.Constant("All Countries"), 'Country'],
            values='TOTAL (Jan - Dec)',
            title=f'Arrivals by Country ({selected_year})',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig.update_traces(textinfo="label+value", hovertemplate='<b>%{label}</b><br>Arrivals: %{value:,.0f}<extra></extra>')
        fig.update_layout(height=600, paper_bgcolor='rgba(255,255,255,0)', plot_bgcolor='rgba(255,255,255,0.5)')
        return dcc.Graph(figure=fig)

    @app.callback(
        Output('barchart-container', 'children'),
        Input('year-selector-countries', 'value')
    )
    def update_barchart(selected_year):
        # We now directly use the clean `arrivals_data`
        df = arrivals_data.get(selected_year)
        if df is None or df.empty:
            return dcc.Graph(figure=go.Figure().update_layout(title='No data available for barchart.'))

        top_10_data = df.sort_values('TOTAL (Jan - Dec)', ascending=False).head(10).iloc[::-1]

        fig = go.Figure(go.Bar(
            x=top_10_data['TOTAL (Jan - Dec)'],
            y=top_10_data['Country'],
            orientation='h',
            marker_color=get_unique_colors(10),
            text=top_10_data['TOTAL (Jan - Dec)'].apply(lambda x: f'{x:,.0f}'),
            textposition='inside',
        ))
        fig.update_layout(
            title=f'Top 10 Source Markets ({selected_year})',
            height=600, paper_bgcolor='rgba(255,255,255,0)', plot_bgcolor='rgba(255,255,255,0.5)',
            xaxis_title="Number of Arrivals", yaxis_title="Country", margin=dict(l=150)
        )
        return dcc.Graph(figure=fig)