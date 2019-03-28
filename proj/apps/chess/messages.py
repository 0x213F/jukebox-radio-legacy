
from proj.core.management.responses import CoreBaseMessage
from proj.core.management.responses import Status


class ChessGameMessage(CoreBaseMessage):

    INVALID_MOVE = Status(401, 'Invalid move')
