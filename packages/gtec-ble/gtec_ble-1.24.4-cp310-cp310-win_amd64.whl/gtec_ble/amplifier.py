from enum import Enum
from .lib.gtec_ble_wrapper import GtecBLEWrapper


class Amplifier():

    class ChannelType(Enum):
        EXG = 1
        ACC = 2
        GYR = 3
        BAT = 4
        CNT = 5
        LINK = 6
        SATURATION = 7
        FLAG = 8
        VALID = 9
        OTHER = 10

    class Error(Enum):
        NONE = 0
        INVALID_HANDLE = 1
        BLUETOOTH_ADAPTER = 2
        BLUETOOTH_DEVICE = 3
        GENERAL = 4294967295

    _imp: GtecBLEWrapper

    @staticmethod
    def GetApiVersion():
        return GtecBLEWrapper.GetApiVersion()

    @staticmethod
    def Register(key: str):
        GtecBLEWrapper.Register(key=key)

    @staticmethod
    def StartScanning():
        GtecBLEWrapper.StartScanning()

    @staticmethod
    def StopScanning():
        GtecBLEWrapper.StopScanning()

    @staticmethod
    def AddDevicesDiscoveredEventhandler(handler):
        GtecBLEWrapper.AddDevicesDiscoveredEventhandler(handler)

    @staticmethod
    def RemoveDevicesDiscoveredEventhandler():
        GtecBLEWrapper.RemoveDevicesDiscoveredEventhandler()

    def __init__(self, serial):
        self._imp = GtecBLEWrapper(self, serial)

    def AddDataAvailableEventhandler(self, handler):
        self._imp.AddDataAvailableEventhandler(self, handler)

    def RemoveDataAvailableEventhandler(self):
        self._imp.RemoveDataAvailableEventhandler(self)

    @property
    def ModelNumber(self):
        return self._imp.ModelNumber

    @property
    def SerialNumber(self):
        return self._imp.SerialNumber

    @property
    def FirmwareRevision(self):
        return self._imp.FirmwareRevision

    @property
    def HardwareRevision(self):
        return self._imp.HardwareRevision

    @property
    def ManufacturerName(self):
        return self._imp.ManufacturerName

    @property
    def ChannelTypes(self):
        return self._imp.ChannelTypes

    @property
    def NumberOfAcquiredChannels(self):
        return self._imp.NumberOfAcquiredChannels

    @property
    def SamplingRate(self):
        return self._imp.SamplingRate
