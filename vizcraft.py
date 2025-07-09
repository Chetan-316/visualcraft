# Import libraries
import dash
from dash import dcc, html, Input, Output, State, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import base64
import io
from fpdf import FPDF
import os
import tempfile
import time

# Initialize Dash app with Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "VizCraft: Data Visualization Tool"
server = app.server  # For deployment

# Limit upload size to 5 MB
app.server.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5 MB max

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
            'textAlign': 'center',
            'backgroundColor': '#f8f9fa'
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
                {'label': 'Pie Chart', 'value': 'pie'},
                {'label': 'Scatter Plot', 'value': 'scatter'},
                {'label': 'Area Plot', 'value': 'area'},
            ],
            value='bar',
            placeholder="Select Chart Type"
        ), width=4),
    ], className='my-3'),

    # Help text for special charts
    html.Div(id='chart-help-text', className='mb-3'),

    # Graph
    dcc.Graph(id='graph-output'),

    # Download Buttons
    dbc.Row([
        dbc.Col([
            html.Button("⬇️ Download Chart as PNG", id="btn-download-chart", n_clicks=0, className="btn btn-primary"),
            dcc.Download(id="download-chart")
        ]),
        dbc.Col([
            html.Button("⬇️ Download Report as PDF", id="btn-download-pdf", n_clicks=0, className="btn btn-secondary"),
            dcc.Download(id="download-pdf")
        ]),
        dbc.Col([
            html.Button("⬇️ Download Data as CSV", id="btn-download-csv", n_clicks=0, className="btn btn-success"),
            dcc.Download(id="download-csv")
        ]),
    ], className="my-3 text-center"),

    html.Footer("✨ Made by Chetan", className="text-center text-muted my-4")
], fluid=True)

# Parse uploaded CSV file
def parse_contents(contents):
    try:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        buffer = io.BytesIO(decoded)
        df = pd.read_csv(buffer, low_memory=False)
        return df
    except Exception as e:
        return None

# Store data and figure
app.data_store = {}

# Helper function to determine column types
def get_column_types(df):
    numeric_cols = []
    categorical_cols = []
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            numeric_cols.append(col)
        else:
            categorical_cols.append(col)
    return numeric_cols, categorical_cols

# Safe file deletion function
def safe_delete(filepath, max_attempts=5):
    for attempt in range(max_attempts):
        try:
            if os.path.exists(filepath):
                os.unlink(filepath)
            return True
        except PermissionError:
            time.sleep(0.1 * (attempt + 1))
    return False

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
    if df is None:
        return [], [], dbc.Alert("⚠️ Error reading file. Please upload a valid CSV file.", color="danger")

    app.data_store['df'] = df  # Save data in memory

    # Get column types
    numeric_cols, categorical_cols = get_column_types(df)
    app.data_store['numeric_cols'] = numeric_cols
    app.data_store['categorical_cols'] = categorical_cols

    options = [{'label': col, 'value': col} for col in df.columns]
    return options, options, html.Div([
        html.H5("Preview of Uploaded File:"),
        dash_table.DataTable(
            data=df.head().to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns],
            page_size=5
        )
    ])

# Callback to show help text based on chart type
@app.callback(
    Output('chart-help-text', 'children'),
    Input('chart-type', 'value')
)
def update_help_text(chart_type):
    if chart_type == 'pie':
        return dbc.Alert(
            "📝 For Pie Chart: Select a categorical column for X-axis (labels) and a numerical column for Y-axis (values).",
            color="info"
        )
    elif chart_type == 'scatter':
        return dbc.Alert(
            "📝 For Scatter Plot: Select numeric columns for both X and Y axes.",
            color="info"
        )
    elif chart_type == 'area':
        return dbc.Alert(
            "📝 For Area Plot: Works best with time-series or continuous data.",
            color="info"
        )
    return ""

# Callback to update chart
@app.callback(
    Output('graph-output', 'figure'),
    [Input('chart-type', 'value'),
     Input('x-axis', 'value'),
     Input('y-axis', 'value')]
)
def update_graph(chart_type, x_col, y_col):
    df = app.data_store.get('df')
    if df is None or x_col is None or y_col is None:
        return {}

    try:
        if chart_type == 'bar':
            fig = px.bar(df, x=x_col, y=y_col, title=f"Bar Chart: {y_col} vs {x_col}")
        elif chart_type == 'line':
            fig = px.line(df, x=x_col, y=y_col, title=f"Line Chart: {y_col} vs {x_col}")
        elif chart_type == 'scatter':
            fig = px.scatter(df, x=x_col, y=y_col, title=f"Scatter Plot: {y_col} vs {x_col}", color=x_col, size=y_col)
        elif chart_type == 'area':
            fig = px.area(df, x=x_col, y=y_col, title=f"Area Plot: {y_col} over {x_col}")
        elif chart_type == 'pie':
            pie_data = df.groupby(x_col)[y_col].sum().reset_index()
            fig = px.pie(pie_data, names=x_col, values=y_col, title=f"Pie Chart: {y_col} by {x_col}")

        fig.update_layout(
            showlegend=True,
            height=500,
            margin=dict(t=50, b=50, l=50, r=50)
        )
        app.data_store['fig'] = fig
        return fig

    except Exception as e:
        return {
            'data': [],
            'layout': {
                'title': f'Error creating chart: {str(e)}',
                'xaxis': {'visible': False},
                'yaxis': {'visible': False},
                'annotations': [{
                    'text': '⚠️ Check your data and column selections.',
                    'showarrow': False,
                    'xref': 'paper',
                    'yref': 'paper',
                    'x': 0.5,
                    'y': 0.5,
                    'font': {'size': 16}
                }]
            }
        }

# Download callbacks
@app.callback(
    Output("download-csv", "data"),
    Input("btn-download-csv", "n_clicks"),
    prevent_initial_call=True
)
def download_csv(n_clicks):
    if app.data_store.get('df') is not None:
        df = app.data_store['df']
        return dcc.send_data_frame(df.to_csv, "data.csv", index=False)

@app.callback(
    Output("download-chart", "data"),
    Input("btn-download-chart", "n_clicks"),
    prevent_initial_call=True
)
def download_chart(n_clicks):
    if app.data_store.get('fig') is not None:
        fig = app.data_store['fig']
        img_bytes = fig.to_image(format="png", width=1200, height=800)
        return dcc.send_bytes(img_bytes, "chart.png")

@app.callback(
    Output("download-pdf", "data"),
    Input("btn-download-pdf", "n_clicks"),
    prevent_initial_call=True
)
def download_pdf(n_clicks):
    if app.data_store.get('fig') is not None and app.data_store.get('df') is not None:
        fig = app.data_store['fig']
        df = app.data_store['df']
        img_bytes = fig.to_image(format="png", width=1200, height=800)
        tmp_img_path, tmp_pdf_path = None, None

        try:
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_img:
                tmp_img_path = tmp_img.name
                tmp_img.write(img_bytes)
                tmp_img.flush()

            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=16)
            pdf.cell(0, 10, txt="VizCraft: Data Visualization Report", ln=True, align='C')
            pdf.ln(10)
            pdf.image(tmp_img_path, x=10, y=30, w=190)
            pdf.ln(120)

            pdf.set_font("Arial", size=12)
            pdf.cell(0, 10, txt="Data Preview:", ln=True, align='L')
            pdf.ln(5)
            col_width = 190 / len(df.columns)
            for col in df.columns:
                pdf.cell(col_width, 8, txt=str(col)[:15], border=1, align='C')
            pdf.ln()
            for _, row in df.head(10).iterrows():
                for val in row.values:
                    pdf.cell(col_width, 8, txt=str(val)[:15], border=1, align='C')
                pdf.ln()

            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_pdf:
                tmp_pdf_path = tmp_pdf.name
                pdf.output(tmp_pdf_path)

            with open(tmp_pdf_path, 'rb') as f:
                pdf_data = f.read()
            return dcc.send_bytes(pdf_data, "report.pdf")

        finally:
            if tmp_img_path:
                safe_delete(tmp_img_path)
            if tmp_pdf_path:
                safe_delete(tmp_pdf_path)
# Run app
if __name__ == "__main__":
    app.run(debug=True)
