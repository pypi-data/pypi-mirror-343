import re
from dataclasses import dataclass
from datetime import datetime

import nuclio_sdk
from dataclasses import dataclass
from datetime import datetime

import nuclio_sdk

from dca_sm_sdk.Exceptions import PathException


@dataclass
class TraceInfo:
    thread: int
    x1: float
    x2: float
    y1: float
    y2: float
    xCentre: float
    yCentre: float
    length: float
    width: float


@dataclass
class Ingot(dict):
    id: int
    type: str
    traceInfo: TraceInfo

    def __init__(self, id: int, type: str):
        super().__init__()
        self.type = type
        self.id = id

    @classmethod
    def CreateIngot(cls, json: dict) -> 'Ingot':
        ingot = cls(json["id"], json["type"])
        ingot.traceInfo = TraceInfo(json["traceInfo"]["thread"], json["traceInfo"]["x1"], json["traceInfo"]["x2"],
                                    json["traceInfo"]["y1"], json["traceInfo"]["y2"], json["traceInfo"]["xCentre"],
                                    json["traceInfo"]["yCentre"], json["traceInfo"]["length"],
                                    json["traceInfo"]["width"])
        del json["id"]
        del json["type"]
        del json["traceInfo"]
        for paramName in json:
            ingot[paramName] = json[paramName]
        return ingot


class MtsState:
    trackTime: datetime
    timeStamp: datetime
    signals: dict[int, float]
    ingots: dict[int, Ingot]

    def __init__(self):
        self.trackTime = datetime.min
        self.timeStamp = datetime.min
        self.signals = {}
        self.ingots = {}

    def UpdateMtsState(self, event: nuclio_sdk.Event):
        if "MessageType" in event.body:
            if event.body["MessageType"] == 2:
                self._PathDiff(event.body["Diff"])
            elif event.body["MessageType"] == 1:
                self._SetState(event.body["State"])
    def _SetState(self, state: dict):

        # self.timeStamp = datetime.strptime(state["timeStamp"][:26]+ state["timeStamp"][27:], "%Y-%m-%dT%H:%M:%S.%f%z")
        # self.trackTime = datetime.strptime(state["trackTime"][:26]+ state["timeStamp"][27:], "%Y-%m-%dT%H:%M:%S.%f%z")
        cleaned_timestamp = re.sub('(\d{6})\d(\+\d{2})(:)(\d{2})', r'\1\2\4', state["timeStamp"])
        self.timeStamp = datetime.strptime(cleaned_timestamp, "%Y-%m-%dT%H:%M:%S.%f%z")
        cleaned_timestamp = re.sub('(\d{6})\d(\+\d{2})(:)(\d{2})', r'\1\2\4', state["trackTime"])
        self.trackTime = datetime.strptime(cleaned_timestamp, "%Y-%m-%dT%H:%M:%S.%f%z")
        self.ingots = {}
        self.signals = {}

        if state["signals"]:
            for signalKey in state["signals"]:
                self.signals[int(signalKey)] = float(state["signals"][signalKey])

        if state["ingots"]:
            for ingot in state["ingots"].values():
                newIngot = Ingot.CreateIngot(ingot)
                self.ingots[newIngot.id] = newIngot

    def _PathDiff(self, diff: dict):
        if "timeStamp" in diff:
            cleaned_timestamp = re.sub('(\d{6})\d(\+\d{2})(:)(\d{2})', r'\1\2\4', diff["timeStamp"][1])
            self.timeStamp = datetime.strptime(cleaned_timestamp, "%Y-%m-%dT%H:%M:%S.%f%z")

        if "trackTime" in diff:
            cleaned_trackTime = re.sub('(\d{6})\d(\+\d{2})(:)(\d{2})', r'\1\2\4', diff["trackTime"][1])
            self.trackTime = datetime.strptime(cleaned_trackTime, "%Y-%m-%dT%H:%M:%S.%f%z")
        if "signals" in diff:
            for signalKey in diff["signals"]:
                self.signals[int(signalKey)] = diff["signals"][signalKey][0]

        if "ingots" in diff:
            for ingot_key in diff["ingots"]:
                diff_ingot = diff["ingots"][ingot_key]
                int_ingot_key = int(ingot_key)
                if isinstance(diff_ingot, dict):
                    if int_ingot_key not in self.ingots:
                        raise PathException(f"Ingot key {int_ingot_key} does not exist in state")
                    for diff_key in diff_ingot:
                        diff_value = diff_ingot[diff_key]
                        if diff_key == "id":
                            self.ingots[int_ingot_key].id = diff_ingot[diff_key]
                        elif diff_key == "type":
                            self.ingots[int_ingot_key].type = diff_ingot[diff_key]
                        elif diff_key == "traceInfo":
                            if isinstance(diff_ingot[diff_key], dict):
                                for traceInfo_key in diff_ingot[diff_key]:
                                    if traceInfo_key == "thread":
                                        self.ingots[int_ingot_key].traceInfo.thread = \
                                        diff_ingot[diff_key][traceInfo_key][0]
                                    elif traceInfo_key == "x1":
                                        self.ingots[int_ingot_key].traceInfo.x1 = diff_ingot[diff_key][traceInfo_key][0]
                                    elif traceInfo_key == "x2":
                                        self.ingots[int_ingot_key].traceInfo.x2 = diff_ingot[diff_key][traceInfo_key][0]
                                    elif traceInfo_key == "y1":
                                        self.ingots[int_ingot_key].traceInfo.y1 = diff_ingot[diff_key][traceInfo_key][0]
                                    elif traceInfo_key == "y2":
                                        self.ingots[int_ingot_key].traceInfo.y2 = diff_ingot[diff_key][traceInfo_key][0]
                                    elif traceInfo_key == "xCentre":
                                        self.ingots[int_ingot_key].traceInfo.xCentre = \
                                        diff_ingot[diff_key][traceInfo_key][0]
                                    elif traceInfo_key == "yCentre":
                                        self.ingots[int_ingot_key].traceInfo.yCentre = \
                                        diff_ingot[diff_key][traceInfo_key][0]
                                    elif traceInfo_key == "length":
                                        self.ingots[int_ingot_key].traceInfo.length = \
                                        diff_ingot[diff_key][traceInfo_key][0]
                                    elif traceInfo_key == "width":
                                        self.ingots[int_ingot_key].traceInfo.width = \
                                        diff_ingot[diff_key][traceInfo_key][0]

                            elif isinstance(diff_ingot[diff_key], list):
                                if len(diff_ingot[diff_key]) == 3:
                                    del self.ingots[int_ingot_key][diff_key]
                                elif len(diff_ingot[diff_key]) == 2:
                                    self.ingots[int_ingot_key].traceInfo = TraceInfo(diff_ingot[diff_key][1]["thread"],
                                                                                     diff_ingot[diff_key][1]["x1"],
                                                                                     diff_ingot[diff_key][1]["x2"],
                                                                                     diff_ingot[diff_key][1]["y1"],
                                                                                     diff_ingot[diff_key][1]["y2"],
                                                                                     diff_ingot[diff_key][1]["xCentre"],
                                                                                     diff_ingot[diff_key][1]["yCentre"],
                                                                                     diff_ingot[diff_key][1]["length"],
                                                                                     diff_ingot[diff_key][1]["width"])
                                elif len(diff_ingot[diff_key]) == 1:
                                    self.ingots[int_ingot_key].traceInfo = TraceInfo(diff_ingot[diff_key][0]["thread"],
                                                                                     diff_ingot[diff_key][0]["x1"],
                                                                                     diff_ingot[diff_key][0]["x2"],
                                                                                     diff_ingot[diff_key][0]["y1"],
                                                                                     diff_ingot[diff_key][0]["y2"],
                                                                                     diff_ingot[diff_key][0]["xCentre"],
                                                                                     diff_ingot[diff_key][0]["yCentre"],
                                                                                     diff_ingot[diff_key][0]["length"],
                                                                                     diff_ingot[diff_key][0]["width"])


                        else:
                            if isinstance(diff_ingot[diff_key], list):
                                if len(diff_ingot[diff_key]) == 2:
                                    self.ingots[int_ingot_key][diff_key] = diff_ingot[diff_key][1]
                                elif len(diff_ingot[diff_key]) == 3:
                                    del self.ingots[int_ingot_key][diff_key]
                                elif len(diff_ingot[diff_key]) == 1:
                                    self.ingots[int_ingot_key][diff_key] = diff_ingot[diff_key][0]




                elif isinstance(diff_ingot, list):
                    if len(diff_ingot) == 3:
                        del self.ingots[int_ingot_key]
                    elif len(diff_ingot) == 2:
                        self.ingots[int_ingot_key] = Ingot.CreateIngot(diff_ingot[1])
                    elif len(diff_ingot) == 1:
                        self.ingots[int_ingot_key] = Ingot.CreateIngot(diff_ingot[0])
