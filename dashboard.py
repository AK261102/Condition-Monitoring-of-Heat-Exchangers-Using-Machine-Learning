import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import requests

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the layout of the dashboard
app.layout = html.Div([
    html.H1("Heat Exchanger Condition Monitoring Dashboard"),
    html.Div([
        html.Label("Inlet Temperature:"),
        dcc.Input(id='inlet-temp', type='number', value=60),
        html.Label("Outlet Temperature:"),
        dcc.Input(id='outlet-temp', type='number', value=50),
        html.Label("Flow Rate:"),
        dcc.Input(id='flow-rate', type='number', value=10),
        html.Label("Specific Heat Capacity:"),
        dcc.Input(id='specific-heat', type='number', value=4.18),
        html.Button('Predict Fouling Factor', id='predict-button', n_clicks=0)
    ]),
    html.Hr(),
    html.Div(id='prediction-result', style={'fontSize': 24}),
    dcc.Graph(id='heat-duty-graph')
])

# Callback for updating prediction and graph
@app.callback(
    [Output('prediction-result', 'children'),
     Output('heat-duty-graph', 'figure')],
    [Input('predict-button', 'n_clicks')],
    [Input('inlet-temp', 'value'),
     Input('outlet-temp', 'value'),
     Input('flow-rate', 'value'),
     Input('specific-heat', 'value')]
)
def update_output(n_clicks, inlet_temp, outlet_temp, flow_rate, specific_heat):
    if n_clicks > 0:
        # Prepare data for prediction
        input_data = {
            'inlet_temperature': inlet_temp,
            'outlet_temperature': outlet_temp,
            'flow_rate': flow_rate,
            'specific_heat_capacity': specific_heat,
            'temp_diff': inlet_temp - outlet_temp,
            'heat_duty': flow_rate * specific_heat * (inlet_temp - outlet_temp)
        }
        
        # Make a prediction request to the Flask backend
        try:
            response = requests.post('http://127.0.0.1:5001/predict', json=input_data)
            response.raise_for_status()  # Check if the request was successful
            fouling_factor = response.json().get('fouling_factor', 'N/A')
        except requests.exceptions.RequestException as e:
            fouling_factor = f"Error: {e}"

        # Create a graph to show heat duty
        heat_duty = input_data['heat_duty']
        figure = {
            'data': [go.Bar(
                x=['Heat Duty'],
                y=[heat_duty],
                name='Heat Duty',
                marker=dict(color='blue')
            )],
            'layout': go.Layout(
                title='Heat Duty of Heat Exchanger',
                xaxis={'title': 'Parameter'},
                yaxis={'title': 'Value'},
                barmode='group'
            )
        }

        return f"Predicted Fouling Factor: {fouling_factor:.2f}" if isinstance(fouling_factor, (int, float)) else fouling_factor, figure

    return "Enter values and click 'Predict Fouling Factor'", {}

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True, port=8050)