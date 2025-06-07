from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
from modules.data_loader import geo_cleaned_data, COLORS

# Layout Function
def create_geo_analysis_layout():
    return html.Div([
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
            }
        ),
        html.P(
            "Explore tourist arrivals across different regions",
            className="text-center text-gray-600 mb-6"
        ),
        html.Div([
            html.Label(
                'Select Year:',
                className="font-bold text-primary mb-2 block text-lg"
            ),
            dcc.Dropdown(
                id='year-selector-geo',
                options=[
                    {'label': str(year), 'value': str(year)}
                    for year in sorted(geo_cleaned_data.keys(), reverse=True)
                ],
                value='2024',
                className="w-64 mx-auto"
            )
        ], className="mb-8"),
        html.Div([
            dcc.Graph(id='arrivals-map', className="h-full"),
        ], className="overview-card p-2 animate__animated animate__fadeIn mb-6 h-[600px]"),
        html.Div(
            id='pie-chart-container',
            className="overview-card p-4 animate__animated animate__fadeIn",
            style={'min-height': '400px'}
        )
    ], className="container mx-auto px-4 py-8 sl-pattern")

# Callbacks for this layout
def register_geo_callbacks(app):
    # Callback to update the map based on selected year
    @app.callback(
        Output('arrivals-map', 'figure'),
        Input('year-selector-geo', 'value')
    )
    def update_map(selected_year):
        df = geo_cleaned_data[selected_year]
        if df.empty:
            return go.Figure()
        fig = px.choropleth(
            df,
            locations='Country',
            locationmode='country names',
            color='TOTAL (Jan - Dec)',
            hover_name='Country',
            color_continuous_scale=px.colors.sequential.Plasma,
            projection="natural earth",
            title=f'Global Tourist Arrivals in {selected_year}'
        )
        fig.update_layout(
            geo=dict(
                showframe=False,
                showcoastlines=False,
                landcolor='rgb(217, 217, 217)',
                bgcolor='rgba(0,0,0,0)'
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin={"r": 0, "t": 40, "l": 0, "b": 0},
            coloraxis_colorbar=dict(title='Total Arrivals')
        )
        return fig

    # Callback to update the pie chart when a country is clicked
    @app.callback(
        Output('pie-chart-container', 'children'),
        [Input('arrivals-map', 'clickData'), Input('year-selector-geo', 'value')]
    )
    def update_pie(click_data, selected_year):
        if not click_data:
            return html.Div(
                "Click a country on the map to see its monthly breakdown.",
                className="flex items-center justify-center h-full text-gray-500"
            )
        clicked_country = click_data['points'][0]['location']
        df = geo_cleaned_data[selected_year]
        country_data = df[df['Country'] == clicked_country].iloc[0]

        # List of months to extract data for the pie chart
        months = [
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ]
        valid_months = [m for m in months if m in country_data.index]
        monthly_values = [country_data[month] for month in valid_months]

        fig = go.Figure(data=[go.Pie(
            labels=valid_months,
            values=monthly_values,
            hole=0.4,
            marker_colors=px.colors.sequential.RdBu
        )])
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(
            title_text=f'Monthly Arrival Distribution for {clicked_country} ({selected_year})',
            showlegend=False,
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        return dcc.Graph(figure=fig)