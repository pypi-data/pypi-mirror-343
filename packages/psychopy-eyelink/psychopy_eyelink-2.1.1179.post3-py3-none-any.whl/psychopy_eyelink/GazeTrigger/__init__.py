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
_localized.update({'gazeWindowPosition':_translate('Position'),
                   'gazeWindowSize':_translate('Size'),
                   'screenUnitType':_translate('Screen Unit Type'),
                   'within':_translate('Within'),
                   'minimumDuration':_translate('Minimum Duration'),
                   'sendHostBackdropDrawCommand':_translate('Send Draw Command to Host PC')})


class GazeTrigger(BaseComponent):
    """An event class for trgigering actions or end routines with link EyeLink gaze data
    defined within a defined area for a specified duration.
    """
    categories = ['Eyetracking']  # which section(s) in the components panel
    targets = ['PsychoPy']
    iconFile = Path(__file__).parent / 'GazeTrigger.png'
    tooltip = _translate('Defines a gaze-contingent triggering region')
    plugin = "psychopy-eyelink"

    def __init__(self, exp, parentName, name='GazeTrigger', startType='time (s)', startVal='0.0', stopVal='3.0',
                 stopType='duration (s)', gazeWindowPosition = '', gazeWindowSize = '', screenUnitType = 'pix', minimumDuration = 0,
                 within = True, sendHostBackdropDrawCommand = True):


        super(GazeTrigger, self).__init__(
            exp, parentName, name, startType=startType, startVal=startVal,
            stopType=stopType, stopVal=stopVal
            )

        self.type = 'GazeTrigger'
        self.url = "https://www.sr-research.com/support/thread-7525.html"
        # update this URL to a component specific page on an HTML manual

        self.params['gazeWindowPosition'] = Param(
            gazeWindowPosition, categ='Basic',
            valType='str', inputType="single",
            hint=_translate('X,Y position of the gaze-triggered region (in PsychoPy project units,\n'
                            'as specified in the EyeLink Initialize Connection Component)'),
            label=_localized['gazeWindowPosition'])
        
        self.params['gazeWindowSize'] = Param(
            gazeWindowSize, categ='Basic',
            valType='str', inputType="single",
            hint=_translate('Height and width of the gaze-triggered region (in PsychoPy project units,\n'
                            'as specified in the EyeLink Initialize Connection Component)'),
            label=_localized['gazeWindowSize'])
                 
        self.params['screenUnitType'] = Param(
            screenUnitType, valType='str', inputType="choice", categ='Basic',
            allowedVals=['pix','norm','height'],
            updates='constant',
            hint=_translate("PsychoPy Screen Unit Type"),
            label=_localized['screenUnitType'])
        
        self.params['within'] = Param(
            within, categ='Basic',
            valType='bool', inputType="bool",
            hint=_translate('Whether the requirement is for gaze to be \ninside the defined region (checked) or outside the defined region (unchecked)'),
            label=_localized['within'])
        
        self.params['minimumDuration'] = Param(
            minimumDuration, categ='Basic',
            valType='str', inputType="single",
            hint=_translate('Minimum duration that gaze must be in the triggering region consecutively'),
            label=_localized['minimumDuration'])
        
        self.params['sendHostBackdropDrawCommand'] = Param(
            sendHostBackdropDrawCommand, categ='Basic',
            valType='bool', inputType="bool",
            hint=_translate('Send a draw command to the Host PC backdrop\ncorresponding to the gaze trigger window'),
            label=_localized['sendHostBackdropDrawCommand'])
        

    def writeInitCode(self,buff):
        code = ("%(name)s = event.Mouse(win=win)\n")
        code += ('from math import fabs')
        buff.writeIndentedLines(code % self.params)

 
    def writeRoutineStartCode(self,buff):
        code = ('# This section of EyeLink %s component code sets some variables that specify the gaze window characteristics, \n')
        code += ('# including gaze window position, size, minimum duration, within (whether gaze should be inside or outside the region),\n')
        code += ('# and resets some variables that help keep track of whether the gaze criteria, in relation to the window, have been met\n')
        code += ('%s.gazeWinPos = eyelink_pos(%s,[scn_width,scn_height],%s)\n' % (self.params['name'].val,
                                                                                  self.params['gazeWindowPosition'].val,self.params['screenUnitType']))
        code += ('%s.gazeWinSize = eyelink_size(%s,[scn_width,scn_height],%s)\n' % (self.params['name'].val,
                                                                                    self.params['gazeWindowSize'].val,self.params['screenUnitType']))
        code += ('# the width of the gaze window in pixels\n')
        code += ('%s.gazeWinWidth = %s.gazeWinSize[0]\n'% (self.params['name'].val,self.params['name'].val))
        code += ('#the height of the fixation window in pixels\n')
        code += ('%s.gazeWinHeight = %s.gazeWinSize[1]\n' % (self.params['name'].val,self.params['name'].val))
        code += ('#the X and Y location of the gaze window\n')
        code += ('%s.gazeWinX, %s.gazeWinY = (%s.gazeWinPos[0], %s.gazeWinPos[1])\n' % (self.params['name'].val,self.params['name'].val,\
                                                                                   self.params['name'].val,self.params['name'].val))
        if self.params['sendHostBackdropDrawCommand'].val == True:
            leftString = "int(round(%s.gazeWinX - %s.gazeWinWidth/2))" % (self.params['name'].val,self.params['name'].val)
            topString = "int(round(%s.gazeWinY - %s.gazeWinHeight/2))" % (self.params['name'].val,self.params['name'].val)
            rightString = "int(round(%s.gazeWinX + %s.gazeWinWidth/2))" % (self.params['name'].val,self.params['name'].val)
            bottomString = "int(round(%s.gazeWinY + %s.gazeWinHeight/2))" % (self.params['name'].val,self.params['name'].val)
            code += ('# Send a command to the Host PC to draw a box on its backdrop corresponding to the gaze trigger window\n')
            code += ('el_tracker.sendCommand("draw_box %s %s %s %s 2" % (\\\n')
            code += ('                        %s,\\\n' % leftString)
            code += ('                        %s,\\\n' % topString)
            code += ('                        %s,\\\n' % rightString)
            code += ('                        %s))\n' % bottomString)
        code += ('# the minimum consecutive time that gaze must be within the gaze triggering region\n')
        code += ("%s.minimumDuration = %s\n" % (self.params['name'].val,self.params['minimumDuration'].val))
        code += ('# keeps track of the time when the eye most recently entered triggering region\n')
        code += ('%s.gazeInHitRegionStartTime = -1\n' % self.params['name'].val)
        code += ('# keeps track of whether gaze is currently in the triggering region\n')
        code += ('%s.inHitRegion = False\n' % self.params['name'].val)
        code += ('# keeps track of whether the gaze criteria have been met\n')
        code += ('%s.gazeWindowGazeCompletedStatus = False\n' % self.params['name'].val)
        code += ('# will log time when gaze criteria were met\n')
        code += ('%s.gazeWindowGazeCompletedTime = -1\n' % self.params['name'].val)
        code += ('# keeps track of time whether gaze criteria checking period has started\n')
        code += ('%s.elFixCheckOnsetDetected = False\n' % self.params['name'].val)
        code += ('# keeps track of time whether gaze criteria checking period has ended\n')
        code += ('%s.elFixCheckOffsetDetected = False\n' % self.params['name'].val)
        code += ('# stores the time of the last (i.e., previous) sample\n')
        code += ('%s.lastSampleTime = -1\n' % self.params['name'].val)
        code += ('\n')
        buff.writeOnceIndentedLines(code) 

    def writeFrameCode(self, buff):

        code = ('# This section of EyeLink %s component code checks to see whether the gaze checking\n' % self.params['name'].val)
        code += ('# period has started (and marks it with a message when it\n')
        code += ('# does), grabs the gaze data online, and uses it to check whether the\n')
        code += ('# gaze window criteria have been satisfied\n')
        code += ('# Checks whether it is the first frame of the gaze trigger checking period\n')
        code += ('if %s.status == NOT_STARTED and tThisFlip >= %s-frameTolerance and not %s.elFixCheckOnsetDetected:\n' \
                 % (self.params['name'].val,self.params['startVal'].val,self.params['name'].val))
        code += ('    # mark the onset of the EyeLink %s gaze checking period and log some data about it\n' % self.params['name'].val)																						  
        code += ('    el_tracker.sendMessage("%s_ONSET")\n' % self.params['name'].val)
        code += ('    %s.tStartRefresh = tThisFlipGlobal\n' % self.params['name'].val)													
        code += ('    %s.elFixCheckOnsetDetected = True\n' % self.params['name'].val)
        code += ('    %s.status = STARTED\n' % self.params['name'].val)
                # if fixation is stopping this frame...
        if len(self.params['stopVal'].val) > 0:
            code += ('if %s.status == STARTED:\n' % self.params['name'].val)
            # is it time to stop? (based on global clock, using actual start)
            code += ('    # Checks whether it is the last frame of the  % sgaze trigger checking period\n' % self.params['name'].val)
            code += ('    if tThisFlipGlobal > %s.tStartRefresh + %s - frameTolerance:\n' % (self.params['name'].val,self.params['stopVal'].val))
            code += ('        # mark the offset of the EyeLink %s gaze checking period and log some data about it\n' % self.params['name'].val)																						  
            code += ('        el_tracker.sendMessage("%s_OFFSET")\n' % self.params['name'].val)
            code += ('        %s.elFixCheckOffsetDetected = True\n' % self.params['name'].val)
            code += ('        %s.status = FINISHED\n' % self.params['name'].val)
            code += ('\n')
        code += ('# Gaze/Trigger Region checking section\n')
        code += ('# Do we have a sample in the sample buffer?\n')
        code += ("# and does it differ from one we've seen before?\n")
        code += ('if %s.status == STARTED:\n' % self.params['name'].val)
        code += ('    new_sample = el_tracker.getNewestSample()\n')
        code += ('    if new_sample is not None:\n')
        code += ('        if new_sample.getTime() != %s.lastSampleTime and %s.tStartRefresh is not None:\n' % (self.params['name'].val,self.params['name'].val))
        code += ('            %s.lastSampleTime = new_sample.getTime()\n' % self.params['name'].val)
        code += ('            # check if the new sample has data for the eye\n')
        code += ('            # currently being tracked; if so, we retrieve the current\n')
        code += ('            # gaze position and PPD (how many pixels correspond to 1\n')
        code += ('            # deg of visual angle, at the current gaze position)\n')
        code += ('            if eye_used == 1 and new_sample.isRightSample():\n')
        code += ('                eyelinkGazeX, eyelinkGazeY = new_sample.getRightEye().getGaze()\n')
        code += ('            if eye_used == 0 and new_sample.isLeftSample():\n')
        code += ('                eyelinkGazeX, eyelinkGazeY = new_sample.getLeftEye().getGaze()\n')
        code += ('\n')
        if self.params['within'].val == True:
            code += ('            # check if gaze is insde (within) the triggering region\n')
            code += ('            if fabs(eyelinkGazeX - %s.gazeWinX) < %s.gazeWinWidth/2 and fabs(eyelinkGazeY - %s.gazeWinY) < %s.gazeWinHeight/2:\n' %\
                    (self.params['name'].val,self.params['name'].val,self.params['name'].val,self.params['name'].val))
        else:
            code += ('            # check if gaze is outside (not within) the triggering region\n')
            code += ('            if fabs(eyelinkGazeX - %s.gazeWinX) >= %s.gazeWinWidth/2 or fabs(eyelinkGazeY - %s.gazeWinY) >= %s.gazeWinHeight/2:\n' %\
                    (self.params['name'].val,self.params['name'].val,self.params['name'].val,self.params['name'].val))
        code += ('                # record gaze start time\n')
        code += ('                if not %s.inHitRegion:\n' % self.params['name'].val)
        code += ('                    if %s.gazeInHitRegionStartTime == -1:\n' % self.params['name'].val)
        code += ('                        %s.gazeInHitRegionStartTime = globalClock.getTime()\n' % self.params['name'].val)
        code += ('                        %s.inHitRegion = True\n' % self.params['name'].val)
        code += ('                # check the gaze duration and fire\n')
        code += ('                if %s.inHitRegion:\n' % self.params['name'].val)
        code += ('                    %s.gazeDur = globalClock.getTime() - %s.gazeInHitRegionStartTime\n' % (self.params['name'].val,self.params['name'].val))
        code += ('                    if %s.gazeDur > %s:\n' % (self.params['name'].val,self.params['minimumDuration'].val))
        code += ('                        %s.gazeWindowGazeCompletedTime = globalClock.getTime()\n' % self.params['name'].val)
        code += ('                        %s.gazeWindowGazeCompletedStatus = True\n' % self.params['name'].val)
        code += ('            else:  # gaze outside the hit region, reset variables\n')
        code += ('                %s.inHitRegion = False\n' % self.params['name'].val)
        code += ('                %s.gazeInHitRegionStartTime = -1\n' % self.params['name'].val)
        code += ('\n')
        code += ('    # if the gaze criteria have been met then send an event marking message \n')
        code += ('    # and log the time of occurrence as a trial variable for Data Viewer\n')
        code += ('    if %s.gazeWindowGazeCompletedStatus == True and continueRoutine == True:\n' % self.params['name'].val)
        code += ("        el_tracker.sendMessage('%s_FIX_WINDOW_GAZE_COMPLETED')\n" % self.params['name'].val)
        code += ("        el_tracker.sendMessage('!V TRIAL_VAR %s.gazeWindowGazeCompletedTime ' + str(%s.gazeWindowGazeCompletedTime))\n" % (self.params['name'].val,self.params['name'].val))
        code += ('        continueRoutine = False\n')

        buff.writeOnceIndentedLines(code) 
