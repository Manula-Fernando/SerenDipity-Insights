# Dinil Bandara - 003
# Manula Fernando - 004

import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Import layout and callback registration functions from modules
from modules.layout_overview import create_overview_layout, register_overview_callbacks
from modules.layout_arrivals import create_arrivals_layout, register_arrivals_callbacks
from modules.layout_dynamics import create_arrival_dynamics_layout, register_dynamics_callbacks
from modules.layout_countries import create_countries_layout, register_countries_callbacks
from modules.layout_geo import create_geo_analysis_layout, register_geo_callbacks

# --- APP INITIALIZATION ---
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

# --- HTML TEMPLATE ---
# We use the external CSS file in /assets now, so the <style> block is removed.
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
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

# --- MAIN LAYOUT ---
app.layout = html.Div([
    dcc.Tabs(
        id="tabs",
        value="overview",
        className="dash-tabs",
        children=[
            dcc.Tab(label="Overview 🏠", value="overview", className="dash-tab", selected_className="dash-tab--selected"),
            dcc.Tab(label="Inbound Visitors 📊", value="arrivals", className="dash-tab", selected_className="dash-tab--selected"),
            dcc.Tab(label="Arrival Dynamics 💰", value="arrival_dynamics", className="dash-tab", selected_className="dash-tab--selected"),
            dcc.Tab(label="Top Markets 🌏", value="countries", className="dash-tab", selected_className="dash-tab--selected"),
            dcc.Tab(label="Geographic Analysis 🗺️", value="geography", className="dash-tab", selected_className="dash-tab--selected")
        ]
    ),
    html.Div(id="tab-content", className="mt-4")
], className="container mx-auto px-4 py-8")


# --- TAB ROUTING CALLBACK ---
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
        return create_countries_layout()
    elif tab_name == "geography":
        return create_geo_analysis_layout()
    return html.P("This is an example of a Dash app with dynamic content.")

# --- REGISTER ALL CALLBACKS ---
register_overview_callbacks(app)
register_arrivals_callbacks(app)
register_dynamics_callbacks(app)
register_countries_callbacks(app)
register_geo_callbacks(app)

# --- RUN THE APP ---
if __name__ == '__main__':
    app.run(debug=True)