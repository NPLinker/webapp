import uuid
import dash_bootstrap_components as dbc
import dash_uploader as du
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
    ],
    className="p-5 ml-5 mr-5",
)


# ------------------ Tabs ------------------ #
# gcfs ids dropdown menu items
gcf_ids_dropdown_menu_items = [
    dbc.DropdownMenuItem("Clear", id="gcf-ids-dropdown-clear"),
]
gcf_ids_input_group = dbc.InputGroup(
    [
        dbc.DropdownMenu(
            gcf_ids_dropdown_menu_items, id="gcf-ids-dropdown-menu", label="GCF ID", disabled=True
        ),
        dbc.Input(
            id="gcf-ids-dropdown-input", placeholder="Enter one or more GCF IDs", disabled=True
        ),
    ]
)
# gcfs bigscape class dropdown menu items
gcf_bigscape_dropdown_menu_items = [
    dbc.DropdownMenuItem("Clear", id="gcf-bigscape-dropdown-clear"),
]
gcf_bigscape_input_group = dbc.InputGroup(
    [
        dbc.DropdownMenu(
            gcf_bigscape_dropdown_menu_items,
            id="gcf-bigscape-dropdown-menu",
            label="BiG-SCAPE Class",
            disabled=True,
        ),
        dbc.Input(
            id="gcf-bigscape-dropdown-input",
            placeholder="Enter one or more GCF BiG-SCAPE classes",
            disabled=True,
        ),
    ]
)
# gm tab content
gm_content = dbc.Row(
    dbc.Col(
        dbc.Card(
            dbc.CardBody(
                [
                    gcf_ids_input_group,
                    gcf_bigscape_input_group,
                ]
            ),
        )
    )
)
# mg tab content
mg_content = dbc.Row(
    dbc.Col(
        dbc.Card(
            dbc.CardBody([html.Div(id="file-content-mg")]),
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
                    className="disabled-tab",
                ),
                dbc.Tab(
                    mg_content,
                    label="Metabolomics -> Genomics",
                    activeTabClassName="fw-bold",
                    disabled=True,
                    id="mg-tab",
                    className="disabled-tab",
                ),
            ],
        ),
    ),
    className="p-5",
)


def create_layout():  # noqa: D103
    return dbc.Container([navbar, uploader, tabs], fluid=True, className="p-0 dbc")
