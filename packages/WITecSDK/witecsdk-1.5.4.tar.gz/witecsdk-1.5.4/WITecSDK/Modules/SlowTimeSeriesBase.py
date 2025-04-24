﻿"""Module containing the bases classes for the Slow Series"""

from typing import Callable
from WITecSDK.Parameters import (COMIntParameter, COMFloatParameter, COMEnumParameter, COMTriggerParameter, COMStringParameter, COMBoolParameter,
                                 COMStringFillStatusParameter, COMFloatFillStatusParameter, ParameterNotAvailableException)
from WITecSDK.Modules.HelperStructs import DataChannelDescription, specchannelpath, userparam

statuspath = "Status|Software|Sequencers|SequencerTimeSeriesSlow|"

class SlowSeriesBase:
    """Base class for all Slow Series"""

    _parampath = userparam + "SequencerTimeSeriesSlow|"

    def __init__(self, aGetParameter: Callable):
        self._numberOfAccumulationsCOM: COMIntParameter = aGetParameter(self._parampath + "SpectrumAcquisition|Accumulations")
        self._integrationTimeCOM: COMFloatParameter = aGetParameter(self._parampath + "SpectrumAcquisition|IntegrationTime")

    @property
    def NumberOfAccumulations(self) -> int:
        """Defines the number of accumulations"""
        return self._numberOfAccumulationsCOM.Value

    @NumberOfAccumulations.setter
    def NumberOfAccumulations(self, numberOfAccumulations: int):
        self._numberOfAccumulationsCOM.Value = numberOfAccumulations

    @property
    def IntegrationTime(self) -> float:
        """Defines the integration time in seconds"""
        return self._integrationTimeCOM.Value

    @IntegrationTime.setter
    def IntegrationTime(self, integrationTime: float):
        self._integrationTimeCOM.Value = integrationTime
        
class SlowTimeSeriesBase(SlowSeriesBase):
    """Base class for Slow Time Series"""

    def __init__(self, aGetParameter: Callable):
        super().__init__(aGetParameter)
        self._numberOfMeasurementsCOM: COMIntParameter = aGetParameter(self._parampath + "AmountOfMeasurements")
        self._measurementModeCOM: COMEnumParameter = aGetParameter(self._parampath + "MeasurementMode")
        self._startTimeSeriesCOM: COMTriggerParameter = aGetParameter(self._parampath + "Start")
        self._processScriptCommandCOM: COMStringParameter = aGetParameter("UserParameters|SequencerProcessScript|CommandLine")
        self._subSequenceCOM: COMEnumParameter = aGetParameter(self._parampath + "SubSequence|SubSequencerName")
        self._readUserDataCOM: COMBoolParameter = aGetParameter(self._parampath + "UserData|ReadUserData")
        self._userDataCaptionsCOM: COMStringFillStatusParameter = aGetParameter(statuspath + "UserDataCaptions")
        self._userDataUnitsCOM: COMStringFillStatusParameter = aGetParameter(statuspath + "UserDataUnits")
        self._userDataValuesCOM: COMFloatFillStatusParameter = aGetParameter(statuspath + "UserDataValues")
        self._nextIndexCOM: COMIntParameter = aGetParameter(self._parampath + "IndexOfNextMeasurement")
        self._showSpectrum1COM: COMBoolParameter = aGetParameter(specchannelpath + "SpectralCamera1Data|TimeSeriesSlow|Show")
        self._showSpectrum2COM: COMBoolParameter = None
        self._showSpectrum3COM: COMBoolParameter = None
        try:
            self._showSpectrum2COM = aGetParameter(specchannelpath + "SpectralCamera2Data|TimeSeriesSlow|Show")
            self._showSpectrum3COM = aGetParameter(specchannelpath + "SpectralCamera3Data|TimeSeriesSlow|Show")
        except ParameterNotAvailableException:
            pass
        except Exception as e:
            raise e

    def Initialize(self, numberOfMeasurements: int, numberOfAccumulations: int, integrationTime: float):
        """Initializes a Slow Time Series with the necessary acquisition parameters."""
        self.NumberOfMeasurements = numberOfMeasurements
        self.NumberOfAccumulations = numberOfAccumulations
        self.IntegrationTime = integrationTime
        self.UseAutoFocus(False)
        self._readUserDataCOM.Value = False
    
    @property
    def NumberOfMeasurements(self) -> int:
        """Defines the number of datapoints for the measurement"""
        return self._numberOfMeasurementsCOM.Value
    
    @NumberOfMeasurements.setter
    def NumberOfMeasurements(self, numberOfMeasurements: int):
        self._numberOfMeasurementsCOM.Value = numberOfMeasurements

    def UseAutoFocus(self, aUse: bool):
        """Expects a bool value to activate (True) or deactivate (False) a spectral Autofocus before each acquisition.
        (The Autofocus has to be defined in the SpectralAutofocus module)"""
        if aUse:
            self._processScriptCommandCOM.Value = "AutoFocus"
            self._subSequenceCOM.Value = 1
        else:
            self._subSequenceCOM.Value = 0

    def CreateDataChannels(self, dataChannels: list[DataChannelDescription]):
        """Defines caption and unit of additional datachannels that should be recorded with the measurement"""
        self._readUserDataCOM.Value = True
        captionlist = [i.Caption for i in dataChannels]
        unitlist = [i.Unit for i in dataChannels]
        self._userDataCaptionsCOM.WriteArray(captionlist)
        self._userDataUnitsCOM.WriteArray(unitlist)

    def WriteDataToDataChannels(self, data: list[float]):
        """Writes values to the defined additional datachannels"""
        self._userDataValuesCOM.WriteArray(data)

    @property
    def NextIndex(self) -> int:
        """Retrieves the index of the next measurement"""
        return self._nextIndexCOM.Value
    
    def DeactivateShowSpectrum(self) -> bool:
        """Deactivates that a Graph viewer is opened for each measurement.
        Is valid until the configuration is reloaded"""
        self._showSpectrum1COM.Value = False
        if self._showSpectrum2COM is not None:
            self._showSpectrum2COM.Value = False
        if self._showSpectrum3COM is not None:
            self._showSpectrum3COM.Value = False

    def Start(self):
        """Starts the Slow Time Series"""
        self._startTimeSeriesCOM.ExecuteTrigger()


class SlowTimeSeriesAdd52:
    """Extension class with features available for version 5.2 and higher"""

    def __init52__(self, aGetParameter: Callable):
        self._stateBetweenMeasureCOM: COMStringParameter = aGetParameter(self._parampath + "MicroscopeStateAfterSingleMeasurement")
        
    def setWaitWithShutterClosed(self):
        """This mode will close the laser shutter after each single acquisition"""
        self._stateBetweenMeasureCOM.Value = "Laser|Selected|Shutter:SetValue:False"
    
    def setWaitWithShutterOpen(self):
        """This mode will leave the laser shutter open after each single acquisition"""
        self._stateBetweenMeasureCOM.Value = ""