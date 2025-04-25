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

# only use _localized values for label values, nothing functional:


_localized.update({})


class StartRecording(BaseComponent):
    """An event class for starting EyeLink eye tracker recording
    """
    categories = ['Eyetracking']  # which section(s) in the components panel
    targets = ['PsychoPy']
    iconFile = Path(__file__).parent / 'StartRecording.png'
    tooltip = _translate('Starts an EyeLink eye tracker recording')
    plugin = "psychopy-eyelink"

    def __init__(self, exp, parentName, name='StartRecord', startType='time (s)', startVal='0.0', stopVal='0.001',
                 stopType='duration (s)'):

        super(StartRecording, self).__init__(
            exp, parentName, name, startType=startType, startVal=startVal,
            stopType=stopType, stopVal=stopVal
            )

        self.type = 'StartRecording'
        self.url = "https://www.sr-research.com/support/thread-7525.html"

 
    def writeInitCode(self,buff):
        code = ("%(name)s = event.Mouse(win=win)\n")
        buff.writeIndentedLines(code % self.params)
 

    def writeRunOnceInitCode(self, buff):
        pass


    def writeRoutineEndCode(self,buff):
        code = ('# This section of EyeLink %s component code starts eye tracker recording,\n' % self.params['name'].val)
        code += ("# sends a trial start (i.e., TRIALID) message to the EDF, \n")
        code += ('# and logs which eye is tracked\n')
        code += ('\n')
        code += ('# get a reference to the currently active EyeLink connection\n')
        code += ('el_tracker = pylink.getEYELINK()\n')
        code += ('# Send a "TRIALID" message to mark the start of a trial, see the following Data Viewer User Manual:\n')
        code += ('# "Protocol for EyeLink Data to Viewer Integration -> Defining the Start and End of a Trial"\n')
        code += ("el_tracker.sendMessage('TRIALID %d' % trial_index)\n")
        code += ('# Log the trial index at the start of recording in case there will be multiple trials within one recording\n')
        code += ('trialIDAtRecordingStart = int(trial_index)\n')
        code += ('# Log the routine index at the start of recording in case there will be multiple routines within one recording\n')
        code += ('routine_index = 1\n')
        code += ('# put tracker in idle/offline mode before recording\n')
        code += ('el_tracker.setOfflineMode()\n')
        code += ('# Start recording, logging all samples/events to the EDF and making all data available over the link\n')
        code += ('# arguments: sample_to_file, events_to_file, sample_over_link, events_over_link (1-yes, 0-no)\n')
        code += ('try:\n')
        code += ('    el_tracker.startRecording(1, 1, 1, 1)\n')
        code += ('except RuntimeError as error:\n')
        code += ('    print("ERROR:", error)\n')
        code += ('    abort_trial(genv)\n')
        code += ('# Allocate some time for the tracker to cache some samples before allowing\n')
        code += ('# trial stimulus presentation to proceed\n')
        code += ('pylink.pumpDelay(100)\n')
        code += ('# determine which eye(s) is/are available\n')
        code += ('# 0-left, 1-right, 2-binocular\n')
        code += ('eye_used = el_tracker.eyeAvailable()\n')
        code += ('if eye_used == 1:\n')
        code += ('    el_tracker.sendMessage("EYE_USED 1 RIGHT")\n')
        code += ('elif eye_used == 0 or eye_used == 2:\n')
        code += ('    el_tracker.sendMessage("EYE_USED 0 LEFT")\n')
        code += ('    eye_used = 0\n')
        code += ('else:\n')
        code += ('    print("ERROR: Could not get eye information!")\n')
        code += ('#routineForceEnded = True\n')
        
 
        buff.writeOnceIndentedLines(code)


    def writeExperimentEndCode(self, buff):
        pass


