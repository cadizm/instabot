
class InstaBotException(Exception):
    pass

class InvalidUsernamePasswordError(InstaBotException):
    pass

class LoginError(InstaBotException):
    pass
