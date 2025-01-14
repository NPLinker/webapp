import uuid
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import dash_uploader as du
from dash import dash_table
from dash import dcc
from dash import html


# ------------------ Nav Bar ------------------ #
color_mode_switch = html.Span(
    [
        dbc.Label(className="fa fa-moon", html_for="color-mode-switch"),
        dbc.Switch(
            id="color-mode-switch",
            value=False,
            className="d-inline-block ms-1",
            persistence=True,
        ),
        dbc.Label(className="fa fa-sun", html_for="color-mode-switch"),
    ],
    className="p-2",
)
navbar = dbc.Row(
    dbc.Col(
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink("Doc", href="https://nplinker.github.io/nplinker/latest/")),
                dbc.NavItem(
                    dbc.NavLink("About", href="https://github.com/NPLinker/nplinker-webapp"),
                ),
                dbc.NavItem(
                    color_mode_switch,
                    className="mt-1 p-1",
                ),
            ],
            brand="NPLinker Webapp",
            color="primary",
            className="p-3 mb-2",
            dark=True,
        ),
    ),
)


# ------------------ Uploader ------------------ #
uploader = html.Div(
    [
        dbc.Row(
            dbc.Col(
                du.Upload(
                    id="dash-uploader",
                    text="Import Data",
                    text_completed="Uploaded: ",
                    filetypes=["pkl", "pickle"],
                    upload_id=uuid.uuid1(),  # Unique session id
                    cancel_button=True,
                    max_files=1,
                ),
            )
        ),
        dbc.Row(
            dbc.Col(
                html.Div(children="No file uploaded", id="dash-uploader-output", className="p-4"),
                className="d-flex justify-content-center",
            )
        ),
        dcc.Store(id="file-store"),  # Store to keep the file contents
        dcc.Store(id="processed-data-store"),  # Store to keep the processed data
        dcc.Store(id="processed-links-store"),  # Store to keep the processed links
    ],
    className="p-5 ml-5 mr-5",
)


# ------------------ Tabs ------------------ #
# gm filter dropdown menu items
gm_filter_input_group = html.Div(
    [
        dcc.Store(id="gm-filter-blocks-id", data=[]),  # Start with one block
        html.Div(
            id="gm-filter-blocks-container",
            children=[],
        ),
    ]
)
# gm filter (accordion) card
gm_filter_accordion = dmc.Accordion(
    [
        dmc.AccordionItem(
            [
                dmc.AccordionControl(
                    "Genomics filter",
                    disabled=True,
                    id="gm-filter-accordion-control",
                    className="mt-5 mb-3",
                ),
                dmc.AccordionPanel(
                    [
                        gm_filter_input_group,
                        html.Div(
                            dbc.Button(
                                "Apply Filters",
                                id="gm-filter-apply-button",
                                color="primary",
                                className="mt-3",
                            ),
                            className="d-flex justify-content-center",
                        ),
                    ]
                ),
            ],
            value="gm-filter-accordion",
        ),
    ],
    className="mt-5 mb-3",
)
# gm graph
gm_graph = dcc.Graph(id="gm-graph", className="mt-5 mb-3", style={"display": "none"})
# gm_table
gm_table = dbc.Card(
    [
        dbc.CardHeader(
            [
                "Data",
            ],
            id="gm-table-card-header",
            style={"color": "#888888"},
        ),
        dbc.CardBody(
            [
                html.Div(
                    dcc.Checklist(
                        options=[{"label": "", "value": "disabled"}],
                        id="gm-table-select-all-checkbox",
                        style={
                            "position": "absolute",
                            "top": "4px",
                            "left": "10px",
                            "zIndex": "1000",
                        },
                    ),
                    style={"position": "relative", "height": "0px"},
                ),
                dash_table.DataTable(
                    id="gm-table",
                    columns=[],
                    data=[],
                    tooltip_data=[],
                    editable=False,
                    filter_action="none",
                    sort_action="none",
                    sort_mode="multi",
                    column_selectable=False,
                    row_deletable=False,
                    row_selectable="multi",
                    selected_columns=[],
                    selected_rows=[],
                    page_action="native",
                    page_current=0,
                    page_size=10,
                    style_cell={"textAlign": "left", "padding": "5px"},
                    style_header={
                        "backgroundColor": "#FF6E42",
                        "fontWeight": "bold",
                        "color": "white",
                    },
                    style_data={"border": "1px solid #ddd"},
                    style_data_conditional=[
                        {
                            "if": {"state": "selected"},
                            "backgroundColor": "white",
                            "border": "1px solid #ddd",
                        }
                    ],
                    style_cell_conditional=[{"if": {"column_id": "selector"}, "width": "30px"}],
                    tooltip_delay=0,
                    tooltip_duration=None,
                    css=[
                        {
                            "selector": ".dash-table-tooltip",
                            "rule": """
                                background-color: #ffd8cc;
                                font-family: monospace;
                                font-size: 12px;
                                max-width: none !important;
                                white-space: pre-wrap;
                                padding: 8px;
                                border: 1px solid #FF6E42;
                                box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
                            """,
                        }
                    ],
                    tooltip={"type": "markdown"},
                ),
            ],
            id="gm-table-card-body",
            style={"display": "none"},
        ),
        html.Div(id="gm-table-output1", className="p-4"),
        html.Div(id="gm-table-output2", className="p-4"),
    ]
)
# gm scoring dropdown menu items
gm_scoring_input_group = html.Div(
    [
        dcc.Store(id="gm-scoring-blocks-id", data=[]),  # Start with one block
        html.Div(
            id="gm-scoring-blocks-container",
            children=[],
        ),
    ]
)
# gm score (accordion) card
gm_scoring_accordion = dmc.Accordion(
    [
        dmc.AccordionItem(
            [
                dmc.AccordionControl(
                    "Scoring",
                    disabled=True,
                    id="gm-scoring-accordion-control",
                    className="mt-5 mb-3",
                ),
                dmc.AccordionPanel(
                    [
                        gm_scoring_input_group,
                        html.Div(
                            dbc.Button(
                                "Set Scoring",
                                id="gm-scoring-apply-button",
                                color="primary",
                                className="mt-3",
                            ),
                            className="d-flex justify-content-center",
                        ),
                    ]
                ),
            ],
            value="gm-scoring-accordion",
        ),
    ],
    className="mt-5 mb-3",
)
# gm tab content
gm_content = dbc.Row(
    [
        dbc.Col(gm_filter_accordion, width=10, className="mx-auto dbc"),
        dbc.Col(gm_graph, width=10, className="mx-auto"),
        dbc.Col(gm_table, width=10, className="mx-auto"),
        dbc.Col(gm_scoring_accordion, width=10, className="mx-auto dbc"),
    ]
)
# mg tab content
mg_content = dbc.Row(
    dbc.Col(
        dbc.Card(
            dbc.CardBody([html.Div(id="mg-file-content")]),
        )
    ),
)
# tabs
tabs = dbc.Row(
    dbc.Col(
        dbc.Tabs(
            [
                dbc.Tab(
                    gm_content,
                    label="Genomics -> Metabolomics",
                    activeTabClassName="fw-bold",
                    disabled=True,
                    id="gm-tab",
                ),
                dbc.Tab(
                    mg_content,
                    label="Metabolomics -> Genomics",
                    activeTabClassName="fw-bold",
                    disabled=True,
                    id="mg-tab",
                ),
            ],
        ),
    ),
    className="p-5",
)


def create_layout():  # noqa: D103
    return dmc.MantineProvider(
        [dbc.Container([navbar, uploader, tabs], fluid=True, className="p-0")]
    )
