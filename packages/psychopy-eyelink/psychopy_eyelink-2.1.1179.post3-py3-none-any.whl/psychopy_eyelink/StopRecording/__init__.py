#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Copyright (c) 1996-2024, SR Research Ltd., All Rights Reserved
#
# For use by SR Research licencees only. Redistribution and use in source
# and binary forms, with or without modification, are NOT permitted.
#
# Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in
# the documentation and/or other materials provided with the distribution.
#
# Neither name of SR Research Ltd nor the name of contributors may be used
# to endorse or promote products derived from this software without
# specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS ``AS
# IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
# TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE REGENTS OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from pathlib import Path

from psychopy.experiment.components import BaseComponent, Param, _translate
from psychopy.experiment import CodeGenerationException, valid_var_re

_localized = {}
__author__ = 'Marcus Johnson, Jono Batten, Brian Richardson'


class StopRecording(BaseComponent):
    """An event class for stopping EyeLink eye tracker recording
    """
    categories = ['Eyetracking']  # which section(s) in the components panel
    targets = ['PsychoPy']
    iconFile = Path(__file__).parent / 'StopRecording.png'
    tooltip = _translate('Stops an EyeLink eye tracker recording')
    plugin = "psychopy-eyelink"

    def __init__(self, exp, parentName, name='StopRecord', startType='time (s)', startVal='0.0', stopVal='0.001',
                 stopType='duration (s)'):

        super(StopRecording, self).__init__(
            exp, parentName, name, startType=startType, startVal=startVal,
            stopType=stopType, stopVal=stopVal
            )

        self.type = 'StopRecording'
        self.url = "https://www.sr-research.com/support/thread-7525.html"
        

    def writeInitCode(self,buff):
        code = ("%(name)s = event.Mouse(win=win)\n")
        buff.writeIndentedLines(code % self.params)
 
    def writeRunOnceInitCode(self, buff):
        pass


    def writeRoutineEndCode(self,buff):
        # This Begin Routine tab of the elStartRecord component draws some feedback \n')
        # This End Routine tab of the elStopRecord component clears the \n')
        code = ('# This section of EyeLink %s component code stops recording, sends a trial end (TRIAL_RESULT)\n' % self.params['name'].val)
        code += ('# message to the EDF, and updates the trial_index variable \n')
        code += ('el_tracker.stopRecording()\n')
        code += ('\n')
        code += ("# send a 'TRIAL_RESULT' message to mark the end of trial, see Data\n")
        code += ('# Viewer User Manual, "Protocol for EyeLink Data to Viewer Integration"\n')
        code += ("el_tracker.sendMessage('TRIAL_RESULT %d' % 0)\n")
        code += ('\n')
        code += ('# update the trial counter for the next trial\n')
        code += ('trial_index = trial_index + 1\n')
 

        buff.writeOnceIndentedLines(code)




    def writeExperimentEndCode(self, buff):
        pass



