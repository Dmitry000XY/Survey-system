class RepositoryError(Exception):
    """Base exception for failures inside the persistence layer."""

    def __init__(self, entity: str, operation: str) -> None:
        self.entity = entity
        self.operation = operation
        super().__init__(f"Could not {operation} {entity}")


class RepositoryConflictError(RepositoryError):
    """Raised when a database constraint rejects a write operation."""
