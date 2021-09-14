class BaseServiceError(Exception):
    pass


class ClientError(BaseServiceError):
    pass


class ServerError(BaseServiceError):
    pass


class EntityConflictError(ClientError):
    pass


class EntityDoesNotExistError(ClientError):
    pass
