
class Status(object):

    def __init__(self, code, message):
        self.code = code
        self.message = message


class CoreBaseMessage(object):

    SUCCESS = Status(200, 'Success')
    FAILURE = Status(500, 'Failure')
    UNIMPLIMENTED = Status(405, 'Unimplimented')
