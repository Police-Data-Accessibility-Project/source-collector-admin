# Import packages
import asyncio

from aiohttp import ClientResponseError
from dash import Dash, html, dcc, Output, Input, State
from flask import Flask, redirect, session
from pdap_access_manager import AccessManager
from pdap_access_manager.models.auth import AuthInfo
from pdap_access_manager.models.tokens import TokensInfo

from src.layouts.login import login_layout
from src.layouts.main import main_layout
from src.session_manager import SessionManager

# Initialize the app - incorporate css
server = Flask(__name__)
server.secret_key = "LugubriousLugnutLitigants"  # Needed for session management

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(
    __name__,
    server=server,
    suppress_callback_exceptions=True,
    external_stylesheets=external_stylesheets
)

# Dummy route to simulate redirecting
@app.server.route("/")
def redirect_to_dash():
    return redirect("/dash")


# Full Layout Wrapper
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    html.Div(id="page-content")
])

# Routing callback
@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def display_page(pathname):
    if session.get("logged_in"):
        return main_layout()
    return login_layout()

# Login handler
@app.callback(
    Output("login-output", "children"),
    Input("login-button", "n_clicks"),
    State("username", "value"),
    State("password", "value"),
    prevent_initial_call=True
)
def handle_login(n_clicks, username, password):
    if not username or not password:
        return "Username and password required."

    try:
        # Send credentials to external auth API
        am = AccessManager(
            auth=AuthInfo(
                email=username,
                password=password
            )
        )
        tokens: TokensInfo = asyncio.run(am.login())
        session_manager = SessionManager()
        session_manager.logged_in = True
        session_manager.tokens = tokens
        return dcc.Location(pathname="/dash", id="login-redirect")
    except ClientResponseError as e:
        return f"Error: {str(e)}"

# Logout handler
@app.callback(
    Output("url", "pathname"),
    Input("logout-button", "n_clicks"),
    prevent_initial_call=True
)
def logout(n):
    session.clear()
    return "/dash"

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
