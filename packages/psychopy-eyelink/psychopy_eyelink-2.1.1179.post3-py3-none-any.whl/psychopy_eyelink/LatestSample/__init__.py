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

#_localized = {}
__author__ = 'Marcus Johnson, Jono Batten, Brian Richardson'


class LatestSample(BaseComponent):
    """An event class for accessing the latest sample data over the EyeLink link.
    For further information on types of link data please see the EyeLink Programmers
    Guide or visit the SR Research Support Forum.
    """
    categories = ['Eyetracking']  # which section(s) in the components panel
    targets = ['PsychoPy']
    iconFile = Path(__file__).parent / 'LatestSample.png'
    tooltip = _translate('Provides the latest EyeLink sample data')
    plugin = "psychopy-eyelink"

    def __init__(self, exp, parentName, name='LatestSample', startType='time (s)', startVal='0.0', stopVal='3.0',
                 stopType='duration (s)'):

        super(LatestSample, self).__init__(
            exp, parentName, name, startType=startType, startVal=startVal,
            stopType=stopType, stopVal=stopVal
            )

        self.type = 'LatestSample'
        self.url = "https://www.sr-research.com/support/thread-7525.html"


    def writeInitCode(self,buff):
        code = ("%(name)s = event.Mouse(win=win)\n")
        buff.writeIndentedLines(code % self.params)
 
    def writeRoutineStartCode(self,buff):

        code = ('# This section of EyeLink %s component code resets some variables \n' % self.params['name'].val)
        code += ('# that log information about the data access period, checks which eye(s) is/are available to track, \n')
        code += ("# and creates a variables that will store the latest sample data locally\n")
        code += ('# these keep track of whether the buffered data access period has started/stopped\n')
        code += ('%s.latestSamplePeriodOnsetDetected = False\n' % self.params['name'].val)
        code += ('%s.latestSamplePeriodOffsetDetected = False\n' % self.params['name'].val)
        code += ('%s.lastSampleTime = -1\n' % self.params['name'].val)
        code += ("# this variable will store the latest sample data locally\n")
        code += ('%s.latestSample = None\n' % self.params['name'].val)
        code += ('\n')
        buff.writeOnceIndentedLines(code) 

    def writeFrameCode(self, buff):
        code = ('\n')
        code += ('# This section of EyeLink %s component code grabs the most recent sample \n' % self.params['name'].val)
        code += ('# once its start time period has started (and marks it with a message when it\n')
        code += ('# starts grabbing), grabs the latest sample on each iteration of the routine loop, and makes it available\n')
        code += ('# to the rest of the experiment\n')
        code += ('# Checks whether it is the first frame of the latest sample access period\n')
        code += ('if %s.status == NOT_STARTED and tThisFlip >= %s-frameTolerance and not %s.latestSamplePeriodOnsetDetected:\n' \
                 % (self.params['name'].val,self.params['startVal'].val,self.params['name'].val))
        code += ('    # log the Host PC time when we start accessing latest sample data, send a message marking\n')
        code += ('    # the time when the data access period begins, and log some data about the start of the access period\n')
        code += ('    el_tracker.sendMessage("%s_ONSET")\n' % self.params['name'].val)
        code += ('    %s.tStartRefresh = tThisFlipGlobal\n' % self.params['name'].val)
        code += ('    %s.status = STARTED\n' % self.params['name'].val)
        code += ('    %s.latestSamplePeriodOnsetDetected = True\n' % self.params['name'].val)
        code += ('if %s.status == STARTED:\n' % self.params['name'].val)
        code += ('    if tThisFlipGlobal > %s.tStartRefresh + %s - frameTolerance:\n' % (self.params['name'].val,self.params['stopVal'].val))
        code += ('        # log the Host PC time when we stop accessing latest sample data, send a message marking\n')
        code += ('        # the time when the data access period ends, and log some data about the end of the access period\n')
        code += ('        el_tracker.sendMessage("%s_OFFSET")\n' % self.params['name'].val)
        code += ('        %s.latestSamplePeriodOffsetDetected = True\n' % self.params['name'].val)
        code += ('        %s.status = FINISHED\n' % self.params['name'].val)
        code += ('\n')
        code += ('# Gaze checking\n')
        code += ('# Do we have a sample available\n')
        code += ("# and does it differ from one we've seen before?\n")
        code += ('if %s.status == STARTED:\n' % self.params['name'].val)
        code += ('    new_sample = el_tracker.getNewestSample()\n')
        code += ('    if new_sample is not None:\n')
        code += ('        if new_sample.getTime() != %s.lastSampleTime and %s.tStartRefresh is not None:\n' % (self.params['name'].val,self.params['name'].val))
        code += ('            %s.lastSampleTime = new_sample.getTime()\n' % self.params['name'].val)
        code += ('            %s.latestSample = new_sample\n' % self.params['name'].val)
        code += ('\n')

        buff.writeOnceIndentedLines(code) 

