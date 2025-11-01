class ClientError(Exception):
    def __init__(self, reason: str, request_url: str, *args, **kwargs) -> None:
        super().__init__(reason, *args, **kwargs)
        self.request_url = request_url


class ClientStatusError(ClientError):
    def __init__(
        self, reason: str, request_url: str, status: int, *args, **kwargs
    ) -> None:
        super().__init__(reason, request_url, *args, **kwargs)
        self.status = status


class ClientRequestTimeoutError(ClientError):
    pass


__all__ = [
    "ClientError",
    "ClientStatusError",
    "ClientRequestTimeoutError",
]
