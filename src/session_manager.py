
from flask import session
from pdap_access_manager.models.tokens import TokensInfo


class SessionManager:

    @property
    def logged_in(self):
        return session.get("logged_in")

    @logged_in.setter
    def logged_in(self, value):
        session["logged_in"] = value

    @property
    def tokens(self) -> TokensInfo:
        d = session.get("tokens")
        return TokensInfo(**d)

    @tokens.setter
    def tokens(self, value: TokensInfo):
        session["tokens"] = value.model_dump(mode="json")