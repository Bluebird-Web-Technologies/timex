class ModelAlreadyExistsError(Exception):
    def __init__(self, name: str):
        model_str = str(name)
        self.message = f"A model record with name {model_str} already exists"
        super().__init__(self.message)


class ActivityAlreadyActiveError(Exception):
    def __init__(self):
        self.message: str = "There is already an active activity"
        super().__init__(self.message)


class ModelNotFoundError(Exception):
    def __init__(self) -> None:
        self.message: str = "No instance found"
        super().__init__(self.message)
