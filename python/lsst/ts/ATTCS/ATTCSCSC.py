#
# Developed for the LSST Telescope and Site Systems.
# This product includes software developed by the LSST Project
# (https://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from lsst.ts.salobj import *
import asyncio
import contextlib
import os
import random
import socket
import string
import time
import warnings

import numpy as np

try:
    import SALPY_ATTCS
except ImportError:
    warnings.warn("Could not import SALPY_ATTCS; ATTCS will not work")


class ATTCSCsc(base_csc.BaseCsc):
    """A skeleton implementation of ATTCS
    Supported commands:


    Parameters
    ----------
    initial_state : `salobj.State` (optional)
        The initial state of the CSC. Typically one of:
        - State.ENABLED if you want the CSC immediately usable.
        - State.STANDBY if you want full emulation of a CSC.
    """
    def __init__(self, index, initial_state=base_csc.State.STANDBY):
        if initial_state not in base_csc.State:
            raise ValueError(f"intial_state={initial_state} is not a salobj.State enum")
        super().__init__(SALPY_ATTCS, index)
        print('initialized super')
        
        self.summary_state = initial_state

        self.telTask = None
        #
        # set up event data structures
        #
        self.evt_detailedState_data = self.evt_detailedState.DataType()
        # etc

        # set up telemetry data structures

        self.tel_loopTime_data = self.tel_loopTime.DataType()
        # etc

        #
        print('summary state: ', self.summary_state)
        #
        # start the telemetry loop as a task. It won't actually send telemetry
        # unless the CSC is in the STANDBY or ENABLED states

        print('starting telemetryLoop')
        asyncio.ensure_future(self.telemetryLoop())

    def end_standby(self):
        if self.telTask and not self.telTask.done():
            self.telTask.cancel()
        super().end_standby()
    
    async def telemetryLoop(self):
        if self.telTask and not self.telTask.done():
            self.telTask.cancel()
        
        while self.summary_state in (base_csc.State.STANDBY, base_csc.State.ENABLED):
            self.telTask = await asyncio.sleep(self.conf.telemetryInterval)
            self.sendTelemetry()

    def sendTelemetry(self):
        print('sendTelemetry: ', '{:.4f}'.format(time.time()))
        # stuff some fake data into self.tel_actuatorPositions_data before doing the put
        # these will come from stateATHexapod
#        self.tel_actuatorPositions_data.raw[0] = self.simState.xpos
#        print('telemetry xpos:', self.simState.xpos)
#        self.tel_actuatorPositions.put(self.tel_actuatorPositions_data)
        
    async def do_target(self, id_data):


        self.assert_enabled("target")
        
    
    async def do_offset(self, id_data):

        self.assert_enabled("offset")


    def do_spectrographSetup(self, id_data):

        self.assert_enabled("spectrographSetup")

    
