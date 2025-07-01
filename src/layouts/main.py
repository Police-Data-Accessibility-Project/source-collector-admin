from dash import html, dcc


def main_layout():
    return html.Div([
        html.H2("Welcome! You're logged in."),
        html.Button("Logout", id="logout-button"),
        dcc.Location(id="url", refresh=True),
    ])
