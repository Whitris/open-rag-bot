class CollectionError(RuntimeError):
    """Raised when the collection loading fails."""

    def __init__(self):
        super().__init__("Error while loading the collection.")


class MissingCSVColumnError(RuntimeError):
    """Raised when one or more required columns are missing from a CSV file."""

    def __init__(self, missing: set[str]):
        super().__init__(f"Missing columns in CSV: {missing}")


class MissingProviderAPIKeyError(RuntimeError):
    """Raised when a required provider API key is missing."""

    def __init__(self, provider: str):
        super().__init__(f"{provider.upper()}_API_KEY not set in environment or .env")


class UnknownProviderError(RuntimeError):
    """Raised when an unknown provider is set."""

    def __init__(self, task: str, provider: str):
        super().__init__(f"Unknown {task} provider: {provider}")
