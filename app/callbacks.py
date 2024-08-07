import os
import pickle
import tempfile
import uuid
import dash
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import dash_uploader as du
from dash import ALL
from dash import MATCH
from dash import Dash
from dash import Input
from dash import Output
from dash import State
from dash import callback_context as ctx
from dash import clientside_callback
from dash import dcc
from dash import html


dash._dash_renderer._set_react_version("18.2.0")


dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
app = Dash(__name__, external_stylesheets=[dbc.themes.UNITED, dbc_css, dbc.icons.FONT_AWESOME])
# Configure the upload folder
TEMP_DIR = tempfile.mkdtemp()
du.configure_upload(app, TEMP_DIR)

clientside_callback(
    """
    (switchOn) => {
    document.documentElement.setAttribute('data-bs-theme', switchOn ? 'light' : 'dark');
    return window.dash_clientside.no_update
    }
    """,
    Output("color-mode-switch", "id"),
    Input("color-mode-switch", "value"),
)


@du.callback(
    id="dash-uploader",
    output=[Output("dash-uploader-output", "children"), Output("file-store", "data")],
)
def upload_data(status: du.UploadStatus):  # noqa: D103
    if status.is_completed:
        latest_file = status.latest_file
        with open(status.latest_file, "rb") as f:
            pickle.load(f)
        return (
            f"Successfully uploaded: {os.path.basename(latest_file)} [{round(status.uploaded_size_mb, 2)} MB]",
            str(latest_file),
        )
    return "No file uploaded", None


@app.callback(
    [
        Output("gm-tab", "disabled"),
        Output("gm-accordion-control", "disabled"),
        Output("mg-tab", "disabled"),
    ],
    [Input("file-store", "data")],
    prevent_initial_call=True,
)
def disable_tabs(file_name):  # noqa: D103
    if file_name is None:
        # Disable the tabs
        return True, True, True
    # Enable the tabs
    return False, False, False


# Define another callback to access the stored file path and read the file
@app.callback(
    Output("file-content-mg", "children"),
    [Input("file-store", "data")],
)
def display_file_contents(file_path):  # noqa: D103
    if file_path is not None:
        with open(file_path, "rb") as f:
            data = pickle.load(f)
        # Process and display the data as needed
        content = f"File contents: {data[0][:2]}"
        return content  # Display same content in both tabs
    return "No data available"


@app.callback(
    Output("blocks-id", "data"),
    Input({"type": "gm-add-button", "index": ALL}, "n_clicks"),
    State("blocks-id", "data"),
)
def add_block(n_clicks, blocks_id):  # noqa: D103
    if not any(n_clicks):
        raise dash.exceptions.PreventUpdate
    # Create a unique ID for the new block
    new_block_id = str(uuid.uuid4())
    blocks_id.append(new_block_id)
    return blocks_id


@app.callback(
    Output("blocks-container", "children"),
    Input("blocks-id", "data"),
    State("blocks-container", "children"),
)
def display_blocks(blocks_id, existing_blocks):  # noqa: D103
    new_block_id = blocks_id[-1]

    new_block = dmc.Grid(
        id={"type": "gm-block", "index": new_block_id},
        children=[
            dmc.GridCol(
                dbc.Button(
                    [html.I(className="fas fa-plus")],
                    id={"type": "gm-add-button", "index": new_block_id},
                    className="btn-primary",
                ),
                span=1,
            ),
            dmc.GridCol(
                dcc.Dropdown(
                    options=[
                        {"label": "GCF ID", "value": "GCF_ID"},
                        {"label": "BGC Class", "value": "BGC_CLASS"},
                    ],
                    value="GCF_ID",
                    id={"type": "gm-dropdown-menu", "index": new_block_id},
                    clearable=False,
                ),
                span=6,
            ),
            dmc.GridCol(
                [
                    dmc.TextInput(
                        id={"type": "gm-dropdown-ids-text-input", "index": new_block_id},
                        placeholder="1, 2, 3, ...",
                        className="custom-textinput",
                    ),
                    dcc.Dropdown(
                        id={"type": "gm-dropdown-bgc-class-dropdown", "index": new_block_id},
                        options=[
                            {"label": "NRP", "value": "NRP"},
                            {"label": "Polyketide", "value": "POLYKETIDE"},
                            {"label": "RiPP", "value": "RIPP"},
                            {"label": "Terpene", "value": "TERPENE"},
                            {"label": "Saccharide", "value": "SAACCHARIDE"},
                            {"label": "Alkaloid", "value": "ALKALOID"},
                            {"label": "Other", "value": "OTHER"},
                            {"label": "Unknown", "value": "UNKNOWN"},
                        ],
                        multi=True,
                        style={"display": "none"},
                    ),
                ],
                span=5,
            ),
        ],
        gutter="md",
    )

    # Hide the add button on the previous last block
    existing_blocks[-1]["props"]["children"][0]["props"]["children"]["props"]["style"] = {
        "display": "none"
    }

    return existing_blocks + [new_block]


@app.callback(
    Output({"type": "gm-dropdown-ids-text-input", "index": MATCH}, "style"),
    Output({"type": "gm-dropdown-bgc-class-dropdown", "index": MATCH}, "style"),
    Output({"type": "gm-dropdown-ids-text-input", "index": MATCH}, "placeholder"),
    Output({"type": "gm-dropdown-bgc-class-dropdown", "index": MATCH}, "placeholder"),
    Output({"type": "gm-dropdown-ids-text-input", "index": MATCH}, "value"),
    Output({"type": "gm-dropdown-bgc-class-dropdown", "index": MATCH}, "value"),
    Input({"type": "gm-dropdown-menu", "index": MATCH}, "value"),
)
def update_placeholder(selected_value):  # noqa: D103
    if not ctx.triggered:
        # Callback was not triggered by user interaction, don't change anything
        raise dash.exceptions.PreventUpdate
    if selected_value == "GCF_ID":
        return {"display": "block"}, {"display": "none"}, "1, 2, 3, ...", "", "", []
    elif selected_value == "BGC_CLASS":
        return (
            {"display": "none"},
            {"display": "block"},
            "",
            "Select one or more BGC classes",
            "",
            [],
        )
