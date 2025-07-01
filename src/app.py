#!/usr/bin/env python3
"""This is just a simple authentication example.

Please see the `OAuth2 example at FastAPI <https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/>`_  or
use the great `Authlib package <https://docs.authlib.org/en/v0.13/client/starlette.html#using-fastapi>`_ to implement a classing real authentication system.
Here we just demonstrate the NiceGUI integration.
"""
from typing import Optional

from aiohttp import ClientResponseError
from fastapi import Request
from fastapi.responses import RedirectResponse
from pdap_access_manager.access_manager.async_ import AccessManagerAsync
from pdap_access_manager.models.auth import AuthInfo
from starlette.middleware.base import BaseHTTPMiddleware

from nicegui import app, ui

# in reality users passwords would obviously need to be hashed
passwords = {'user1': 'pass1', 'user2': 'pass2'}

unrestricted_page_routes = {'/login'}


class AuthMiddleware(BaseHTTPMiddleware):
    """This middleware restricts access to all NiceGUI pages.

    It redirects the user to the login page if they are not authenticated.
    """

    async def dispatch(self, request: Request, call_next):
        if not app.storage.user.get('authenticated', False):
            if not request.url.path.startswith('/_nicegui') and request.url.path not in unrestricted_page_routes:
                return RedirectResponse(f'/login?redirect_to={request.url.path}')
        return await call_next(request)


app.add_middleware(AuthMiddleware)


@ui.page('/')
async def main_page() -> None:
    async def logout() -> None:
        app.storage.user.clear()
        ui.navigate.to('/login')

    with ui.column().classes('absolute-center items-center'):
        try:
            username = app.storage.user.get('username')
        except KeyError:
            ui.navigate.to('/login')
        ui.label(f'Hello {username}!').classes('text-2xl')
        ui.button(on_click=logout, icon='logout').props('outline round')


@ui.page('/subpage')
async def test_page() -> None:
    ui.label('This is a sub page.')


@ui.page('/login')
async def login(redirect_to: str = '/') -> Optional[RedirectResponse]:
    async def try_login() -> None:  # local function to avoid passing username and password as arguments
        auth_info = AuthInfo(
            email=username.value,
            password=password.value
        )
        async with AccessManagerAsync(auth=auth_info) as am:
            try:
                tokens_info = await am.login()
                app.storage.user.update(
                    {
                        "username": auth_info.email,
                        "tokens": tokens_info.model_dump(mode='json'),
                        "authenticated": True
                    }
                )
                ui.navigate.to(redirect_to)  # go back to where the user wanted to go
            except ClientResponseError as e:
                ui.notify('Wrong username or password', color='negative')

    if app.storage.user.get('authenticated', False):
        return RedirectResponse('/')
    with ui.card().classes('absolute-center'):
        username = ui.input('Email').on('keydown.enter', try_login)
        password = ui.input('Password', password=True, password_toggle_button=True).on('keydown.enter', try_login)
        ui.button('Log in', on_click=try_login)
    return None


if __name__ in {'__main__', '__mp_main__'}:
    ui.run(storage_secret='THIS_NEEDS_TO_BE_CHANGED')