__all__ = ["SheetDataNotFoundError"]
class SheetDataNotFoundError(Exception):
    def __init__(self, message: str):
        super().__init__(message)