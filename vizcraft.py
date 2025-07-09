# Import libraries
import dash
from dash import dcc, html, Input, Output, State, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import base64
import io
from fpdf import FPDF

# Initialize Dash app with Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Expose Flask server for deployment
server = app.server  # <-- This line is IMPORTANT for hosting

# App Layout
app.layout = dbc.Container([
    html.H1("📊 VizCraft: Data Visualization Tool", className="text-center my-4"),
    html.P("Turn raw data into insights & download beautiful reports", className="text-center mb-4 text-muted"),

    # Upload Section
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            '📂 Drag & Drop or ',
            html.A('Select CSV File')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '2px',
            'borderStyle': 'dashed',
            'borderRadius': '10px',
            'textAlign': 'center'
        },
        multiple=False
    ),
    html.Div(id='output-data-upload', className='my-3'),

    # Dropdowns
    dbc.Row([
        dbc.Col(dcc.Dropdown(id='x-axis', placeholder="Select X-axis"), width=4),
        dbc.Col(dcc.Dropdown(id='y-axis', placeholder="Select Y-axis"), width=4),
        dbc.Col(dcc.Dropdown(
            id='chart-type',
            options=[
                {'label': 'Bar Chart', 'value': 'bar'},
                {'label': 'Line Chart', 'value': 'line'},
                {'label': 'Pie Chart', 'value': 'pie'}
            ],
            value='bar',
            placeholder="Select Chart Type"
        ), width=4),
    ], className='my-3'),

    # Graph
    dcc.Graph(id='graph-output'),

    # Download Buttons
    dbc.Row([
        dbc.Col(html.Button("⬇️ Download Chart as PNG", id="btn-download-chart", n_clicks=0, className="btn btn-primary")),
        dbc.Col(html.Button("⬇️ Download Report as PDF", id="btn-download-pdf", n_clicks=0, className="btn btn-secondary")),
        dbc.Col(html.A("⬇️ Download Data as CSV", id="download-data-link", href="", target="_blank", className="btn btn-success")),
    ], className="my-3 text-center")
], fluid=True)

# Parse uploaded CSV file
def parse_contents(contents):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
    return df

# Store data and figure
app.data_store = {}

# Callbacks for dropdowns
@app.callback(
    [Output('x-axis', 'options'),
     Output('y-axis', 'options'),
     Output('output-data-upload', 'children')],
    Input('upload-data', 'contents')
)
def update_dropdowns(contents):
    if contents is None:
        return [], [], ''
    df = parse_contents(contents)
    app.data_store['df'] = df  # Save data in memory
    options = [{'label': col, 'value': col} for col in df.columns]
    return options, options, html.Div([
        html.H5("Preview of Uploaded File:"),
        dash_table.DataTable(
            data=df.head().to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns],
            page_size=5
        )
    ])

# Callback to update chart
@app.callback(
    Output('graph-output', 'figure'),
    [Input('chart-type', 'value'),
     Input('x-axis', 'value'),
     Input('y-axis', 'value')],
)
def update_graph(chart_type, x_col, y_col):
    df = app.data_store.get('df')
    if df is None or x_col is None or y_col is None:
        return {}
    if chart_type == 'bar':
        fig = px.bar(df, x=x_col, y=y_col, title=f"{chart_type.title()} of {y_col} vs {x_col}")
    elif chart_type == 'line':
        fig = px.line(df, x=x_col, y=y_col, title=f"{chart_type.title()} of {y_col} vs {x_col}")
    elif chart_type == 'pie':
        fig = px.pie(df, names=x_col, values=y_col, title=f"{chart_type.title()} of {y_col} vs {x_col}")
    app.data_store['fig'] = fig  # Save current figure
    return fig

# Callback to download dataset as CSV
@app.callback(
    Output("download-data-link", "href"),
    Input('upload-data', 'contents'),
)
def update_csv_download(contents):
    if contents is None:
        return ""
    df = parse_contents(contents)
    csv_string = df.to_csv(index=False, encoding='utf-8')
    b64 = base64.b64encode(csv_string.encode()).decode()
    return f"data:text/csv;base64,{b64}"

# Callback to save chart as PNG
@app.callback(
    Output('btn-download-chart', 'children'),
    Input('btn-download-chart', 'n_clicks')
)
def save_chart_png(n_clicks):
    if n_clicks > 0 and app.data_store.get('fig') is not None:
        app.data_store['fig'].write_image("chart.png")
        return "✅ Chart Saved as chart.png"
    return "⬇️ Download Chart as PNG"

# Callback to save chart and data as PDF
@app.callback(
    Output('btn-download-pdf', 'children'),
    Input('btn-download-pdf', 'n_clicks')
)
def save_report_pdf(n_clicks):
    if n_clicks > 0 and app.data_store.get('fig') is not None:
        # Save chart as PNG
        app.data_store['fig'].write_image("chart_temp.png")
        df = app.data_store.get('df')

        # Create PDF report
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="📊 VizCraft: Data Visualization Report", ln=True, align='C')
        pdf.ln(10)
        pdf.image("chart_temp.png", w=170)
        pdf.ln(10)
        pdf.cell(200, 10, txt="Data Preview:", ln=True, align='L')
        for i, row in df.head().iterrows():
            pdf.cell(200, 10, txt=str(row.values), ln=True, align='L')
        pdf.output("report.pdf")
        return "✅ Report Saved as report.pdf"
    return "⬇️ Download Report as PDF"

# Run app
if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8080)
