from __future__  import annotations
from typing import TYPE_CHECKING

import requests

from .request import Request

if TYPE_CHECKING:
    from mtrequests import PendingPool



class Session(requests.Session):
    def __init__(self, pending_pool: PendingPool | None = None):
        super().__init__()
        self.requests_count = 0
        self.pending_pool = pending_pool

    def prepare_and_send(self, request: Request, keep_cookie=False, ignore_hooks=False) -> requests.Response:
        if not ignore_hooks and self.pending_pool and self.pending_pool.on_before_request is not None:
            self.pending_pool.on_before_request(self, request)

        self.requests_count += 1
        if keep_cookie is False:
            self.cookies = requests.sessions.cookiejar_from_dict({})
        prep = self.prepare_request(request)

        proxies = request.sessionarg_proxies or {}

        settings = self.merge_environment_settings(
            prep.url, proxies, request.sessionarg_stream,
            request.sessionarg_verify, request.sessionarg_cert
        )

        send_kwargs = request.sessionarg_send_kwargs
        send_kwargs.update(settings)
        resp = self.send(prep, **send_kwargs)

        if not ignore_hooks and self.pending_pool and self.pending_pool.on_after_request is not None:
            self.pending_pool.on_after_request(self, resp)

        return resp


    @staticmethod
    def make_request(
            method,
            url,
            params=None,
            data=None,
            headers=None,
            cookies=None,
            files=None,
            auth=None,
            timeout=None,
            allow_redirects=True,
            proxies=None,
            hooks=None,
            stream=None,
            verify=None,
            cert=None,
            json=None,
    ) -> Request:
        send_kwargs = {
            "timeout": timeout,
            "allow_redirects": allow_redirects,
        }
        return Request(
            method=method.upper(),
            url=url,
            headers=headers,
            files=files,
            data=data or {},
            json=json,
            params=params or {},
            auth=auth,
            cookies=cookies,
            hooks=hooks,
            send_kwargs=send_kwargs,
            proxies=proxies,
            stream=stream,
            verify=verify,
            cert=cert,
        )
