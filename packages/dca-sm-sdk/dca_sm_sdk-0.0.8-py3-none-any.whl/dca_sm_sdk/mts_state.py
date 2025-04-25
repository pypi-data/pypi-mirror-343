from dataclasses import dataclass
from datetime import datetime

import nuclio_sdk


@dataclass
class TraceInfo:
    Thread: int
    X1: float
    X2: float
    Y1: float
    Y2: float

@dataclass
class Ingot:
    Id: int
    Type: str
    TraceInfo: TraceInfo

    def __init__(self, id: int, type: str, trace_info: TraceInfo):
        self.Id = id
        self.Type = type
        self.TraceInfo = trace_info
        self._params = {}

    def __setitem__(self, key, value):
        self._params[key] = value

    def __getitem__(self, key):
        return self._params[key]


@dataclass
class MtsState:
    TrackTime: datetime
    TimeStamp: datetime
    Signals: dict[int,float]
    Ingots: dict[int,Ingot]


def UpdateMtsState(state: MtsState,  event : nuclio_sdk.Event) -> MtsState:
    return state





