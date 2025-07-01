from pdap_access_manager import AccessManager
from pdap_access_manager.enums import DataSourcesNamespaces, RequestType
from pdap_access_manager.models.request import RequestInfo

from src.session_manager import SessionManager


def get_notifications_preview():
    session_manager = SessionManager()
    tokens_info = session_manager.tokens
    am = AccessManager(tokens=tokens_info)
    am.make_request(
        ri=RequestInfo(
            url=am.build_url(
                namespace=DataSourcesNamespaces.NOTIFICATIONS,
                subdomains=["preview"]
            ),
            type_=RequestType.GET,
            headers=am.jwt_header()

        )
    )