class UserFacingError(Exception):
    def __init__(self, user_message):
        super().__init__(user_message)
        self.user_message = user_message

class UnsupportedMediaType(UserFacingError):
    pass


class UnsupportedUrl(UserFacingError):
    pass


class MediaTooLong(UserFacingError):
    pass


class SendFailed(UserFacingError):
    pass
