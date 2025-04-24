from time import sleep
from threading import Lock

from . import Session, Request
from .pending_response import PendingResponse


class PendingRequest:
    def __init__(self, session: Session, request: Request, lock: Lock, keep_cookies: bool, parent):
        self.session = session
        self.request = request
        self.lock = lock
        self.keep_cookies = keep_cookies
        self.parent = parent

    def send(self, repeats=0, delay=0.1, ignore_hooks=False) -> PendingResponse | None:
        with self.lock:
            while repeats >= 0:
                if self.parent.alive is False:
                    return
                try:
                    response = self.session.prepare_and_send(self.request, self.keep_cookies, ignore_hooks)
                    rsp = PendingResponse(response, None, self)
                except Exception as exc:
                    rsp = PendingResponse(None, exc, self)
                    rsp.request = self.request
                if rsp.is_valid():
                    return rsp
                repeats -= 1
                sleep(delay)
            return rsp
