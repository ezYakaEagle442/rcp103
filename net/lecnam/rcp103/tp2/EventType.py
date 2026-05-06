from enum import Enum

# EventType – SEND_MSG, RECV_MSG, MSG_DEPT
class EventType(Enum):
    SEND_MSG = 1
    RECV_MSG = 2
    MSG_DEPT = 3