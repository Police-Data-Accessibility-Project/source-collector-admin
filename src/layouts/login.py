from dash import html, dcc


def login_layout():
    return html.Div([
        html.H2("Login"),
        dcc.Input(id="username", type="text", placeholder="Username"),
        dcc.Input(id="password", type="password", placeholder="Password"),
        html.Button("Login", id="login-button"),
        html.Div(id="login-output"),
    ])
