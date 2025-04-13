import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go

# Load preprocessed and predicted data
DATA_PATH = "data/merged_data.csv"  # Preprocessed data
MODEL_PREDICTIONS_PATH = "data/predictions.csv"  # Predictions saved from the AI model

# Read the datasets
data = pd.read_csv(DATA_PATH)
predictions = pd.read_csv(MODEL_PREDICTIONS_PATH)

# Combine actual and predicted inflation rates
data['predicted_inflation_rate'] = None
data.loc[-len(predictions):, 'predicted_inflation_rate'] = predictions['predicted_inflation_rate']

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "African Market Dashboard"

# Layout of the dashboard
app.layout = html.Div([
    html.H1("African Market Analysis Dashboard", style={'text-align': 'center'}),

    dcc.Tabs([
        dcc.Tab(label='Inflation Analysis', children=[
            html.Div([
                html.H3("Inflation Rate Over Time"),
                dcc.Graph(
                    id="inflation_graph",
                    config={"displayModeBar": True},
                ),
            ]),
            html.Div([
                html.H3("Gold Price vs Inflation Rate"),
                dcc.Graph(
                    id="gold_vs_inflation_graph",
                    config={"displayModeBar": True},
                ),
            ]),
        ]),
        dcc.Tab(label='Stock Market Trends', children=[
            html.Div([
                html.H3("Stock Index Over Time"),
                dcc.Graph(
                    id="stock_graph",
                    config={"displayModeBar": True},
                ),
            ]),
            html.Div([
                html.H3("Gold Price vs Stock Index"),
                dcc.Graph(
                    id="gold_vs_stock_graph",
                    config={"displayModeBar": True},
                ),
            ]),
        ]),
    ]),
])


# Callbacks for the interactive graphs
@app.callback(
    Output("inflation_graph", "figure"),
    [Input("inflation_graph", "id")]
)
def update_inflation_graph(_):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data['date'],
        y=data['inflation_rate'],
        mode='lines',
        name="Actual Inflation Rate"
    ))
    fig.add_trace(go.Scatter(
        x=data['date'],
        y=data['predicted_inflation_rate'],
        mode='lines',
        name="Predicted Inflation Rate",
        line=dict(dash='dash')
    ))
    fig.update_layout(
        title="Inflation Rate Over Time",
        xaxis_title="Date",
        yaxis_title="Inflation Rate",
        template="plotly_white"
    )
    return fig


@app.callback(
    Output("gold_vs_inflation_graph", "figure"),
    [Input("gold_vs_inflation_graph", "id")]
)
def update_gold_vs_inflation_graph(_):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data['gold_price'],
        y=data['inflation_rate'],
        mode='markers',
        name="Gold Price vs Inflation Rate"
    ))
    fig.update_layout(
        title="Gold Price vs Inflation Rate",
        xaxis_title="Gold Price",
        yaxis_title="Inflation Rate",
        template="plotly_white"
    )
    return fig


@app.callback(
    Output("stock_graph", "figure"),
    [Input("stock_graph", "id")]
)
def update_stock_graph(_):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data['date'],
        y=data['stock_index'],
        mode='lines',
        name="Stock Index"
    ))
    fig.update_layout(
        title="Stock Index Over Time",
        xaxis_title="Date",
        yaxis_title="Stock Index",
        template="plotly_white"
    )
    return fig


@app.callback(
    Output("gold_vs_stock_graph", "figure"),
    [Input("gold_vs_stock_graph", "id")]
)
def update_gold_vs_stock_graph(_):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data['gold_price'],
        y=data['stock_index'],
        mode='markers',
        name="Gold Price vs Stock Index"
    ))
    fig.update_layout(
        title="Gold Price vs Stock Index",
        xaxis_title="Gold Price",
        yaxis_title="Stock Index",
        template="plotly_white"
    )
    return fig


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)