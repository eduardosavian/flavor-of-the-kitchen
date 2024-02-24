class UserException(Exception):
    ...


class UserNotFoundError(UserException):
    def __init__(self):
        self.status_code = 404
        self.detail = "User doesn't exist error"


class UserAlreadyExistError(UserException):
    def __init__(self):
        self.status_code = 409
        self.detail = "Email already exists error"


class RecipeException(Exception):
    ...


class RecipeNotFoundError(RecipeException):
    def __init__(self):
        self.status_code = 404
        self.detail = "Recipe doesn't exist error"


class CommentException(Exception):
    ...


class CommentNotFoundError(CommentException):
    def __init__(self):
        self.status_code = 404
        self.detail = "Common doesn't exist error"
