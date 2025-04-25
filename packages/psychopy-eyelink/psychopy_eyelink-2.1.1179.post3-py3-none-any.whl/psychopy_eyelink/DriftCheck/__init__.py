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
_localized.update({'backgroundColor': _translate('Background Color'),
                   'foregroundColor': _translate('Foreground Color'),
                   'targetType': _translate('Target Type'),
                   'targetSize': _translate('Target Size'),
                   'targetFilename': _translate('Target Filename'),
                   'driftCheckSounds': _translate('Drift Check Sounds'),
                   'driftCheckFilenames': _translate('Drift Check WAV Filenames'),
                   'targetPosition': _translate('Target Position'),
                   'screenUnitType':_translate('Screen Unit Type'),
                   })


class DriftCheck(BaseComponent):
    """An event class for performing a Drift Check or Drift Correction with
    and EyeLink eye tracker. This wil show a single calibration target at
    a fixed location, with the option to press ESC to enter camera setup and
    relcalibrate where necessary. For further detail please see the EyeLink
    Programmers Guide or visit the SR Research Support Forum.
    """
    categories = ['Eyetracking']  # which section(s) in the components panel
    targets = ['PsychoPy']
    iconFile = Path(__file__).parent / 'DriftCheck.png'
    tooltip = _translate('Performs an EyeLink drift check or drift correct')
    plugin = "psychopy-eyelink"

    def __init__(self, exp, parentName, name='DriftCheck', startType='time (s)', startVal='0.0', stopVal='0.001',
                 stopType='duration (s)', targetPosition = '[0,0]', screenUnitType = 'pix', targetType = 'circle', targetFilename = '', 
                 targetSize = '24', foregroundColor = '(1,1,1)', backgroundColor = 'win.color', driftCheckSounds = "defaults", 
                 driftCheckFilenames = "'qbeep.wav','type.wav','error.wav'"):

        super(DriftCheck, self).__init__(
            exp, parentName, name, startType=startType, startVal=startVal,
            stopType=stopType, stopVal=stopVal
            )

        self.type = 'DriftCheck'
        self.url = "https://www.sr-research.com/support/thread-7525.html"
        # update this URL to a component specific page on anm HTML manual

        self.params['targetPosition'] = Param(
            targetPosition, categ='Basic',
            valType='str', inputType="single",
            hint=_translate('Drift Check target position (in PsychoPy project units,\n'
                            'as specified in the EyeLink Initialize Connection Component)\n'),
            label=_localized['targetPosition'])
        
        self.params['screenUnitType'] = Param(
            screenUnitType, valType='str', inputType="choice", categ='Basic',
            allowedVals=['pix','norm','height'],
            updates='constant',
            hint=_translate("PsychoPy Screen Unit Type"),
            label=_localized['screenUnitType'])
         
        self.params['targetType'] = Param(
            targetType, valType='str', inputType="choice", categ='Basic',
            allowedVals=['circle', 'picture', 'movie', 'spiral'],
            updates='constant',
            hint=_translate("Target type"),
            label=_localized['targetType'])

        self.params['targetFilename'] = Param(
            targetFilename, categ='Basic',
            valType='str', inputType="single",
            hint=_translate('Drift Check target filename'),
            label=_localized['targetFilename'])
        
        self.params['targetSize'] = Param(
            targetSize, categ='Basic',
            valType='str', inputType="single",
            hint=_translate('Drift Check target size (in pixels)\n'),
            label=_localized['targetSize'])        

        self.params['foregroundColor'] = Param(
            foregroundColor, categ='Basic',
            valType='str', inputType="single",
            hint=_translate('Drift Check foreground color\nonly applies to circle and spiral'),
            label=_localized['foregroundColor'])

        self.params['backgroundColor'] = Param(
            backgroundColor, categ='Basic',
            valType='str', inputType="single",
            hint=_translate("Drift Check background color\nUse win.color for the window's background color"),
            label=_localized['backgroundColor'])

        self.params['driftCheckSounds'] = Param(
            driftCheckSounds, valType='str', inputType="choice", categ='Basic',
            allowedVals=['defaults', 'off', 'custom wav files'],
            updates='constant',
            hint=_translate("Drift Check Sounds"),
            label=_localized['driftCheckSounds'])

        self.params['driftCheckFilenames'] = Param(
            driftCheckFilenames, categ='Basic',
            valType='str', inputType="single",
            hint=_translate("Custom Drift Check wav filenames (Target, Good, Error)\n\
                            Target -- sound to play when target moves\n\
                            Good -- sound to play on successful operation\n\
                            Error -- sound to play on failure or interruption\n\
                            Each value should specify a wav file"),
            label=_localized['driftCheckFilenames'])

        self.depends.append(
            {'dependsOn':'targetType',
             'condition':'in ["picture","movie"]',
             'param':'targetFilename',
             'true':'show',
             'false':'hide'})        
        
        self.depends.append(
            {'dependsOn':'targetType',
             'condition':'in ["circle","spiral"]',
             'param':'foregroundColor',
             'true':'show',
             'false':'hide'})   
        
        self.depends.append(
            {'dependsOn':'targetType',
             'condition':'in ["circle","spiral","movie"]',
             'param':'targetSize',
             'true':'show',
             'false':'hide'})   
        
        self.depends.append(
            {'dependsOn':'driftCheckSounds',
             'condition':'== "custom wav files"',
             'param':'driftCheckFilenames',
             'true':'show',
             'false':'hide'}) 

        #self.order += ['forceEndRoutine']

    def writeInitCode(self,buff):
        code = ("%(name)s = event.Mouse(win=win)\n")
        buff.writeIndentedLines(code % self.params)
 
    #def writeInitCode(self,buff):
    def writeRunOnceInitCode(self, buff):
        pass


    def writeRoutineEndCode(self,buff):
        code = ('# This section of EyeLink %s component code configures some\n' % self.params['name'].val)
        code += ('# graphics options for drift check, and then performs the drift check')
        code += ('\n')
        code += ('# Set background and foreground colors for the drift check target\n')
        code += ('# in PsychoPy, (-1, -1, -1)=black, (1, 1, 1)=white, (0, 0, 0)=mid-gray\n')
        if len(str(self.params['backgroundColor'])) == 0 or str(self.params['backgroundColor']) == "win.color":
            code += ('background_color = tuple(win.color)\n')
        else:
            code += ('background_color = ' + self.params['backgroundColor'].val + '\n')

        if len(str(self.params['foregroundColor'])) == 0:
            code += ('foreground_color = (-1, -1, -1)\n')
        else:
            code += ('foreground_color = ' + self.params['foregroundColor'].val + '\n')
          
        code += ('genv.setCalibrationColors(foreground_color, background_color)\n')
        code += ('# Set up the drift check target\n')
        code += ('# The target could be a "circle" (default), a "picture", a "movie" clip,\n')
        code += ('# or a rotating "spiral". To configure the type of drift check target, set\n')
        code += ('# genv.setTargetType to "circle", "picture", "movie", or "spiral", e.g.,\n')
        code += ("genv.setTargetType('%s')\n" % self.params['targetType'].val)
        if self.params['targetType'].val == "movie":
            code += ('# Use a movie as the drift check target\n')
            code += ('# Use genv.setMovieTarget() to set a "movie" target\n')
            code += ("genv.setMovieTarget(os.path.normpath(" + str(self.params['targetFilename']).replace('\\','/') + "))\n")
        elif self.params['targetType'].val == "picture":
            code += ('# Use a picture as the drift check target\n')
            code += ('# Use genv.setPictureTarget() to set a "movie" target\n')
            code += ("genv.setPictureTarget(os.path.normpath(" + str(self.params['targetFilename']).replace('\\','/') + "))\n")
        if self.params['targetType'].val == "circle" or self.params['targetType'].val == "spiral" or self.params['targetType'].val == "movie":
            code += ('genv.setTargetSize(' + str(int(round(float(self.params['targetSize'].val)))) + ')\n')
        code += ('# Beeps to play during calibration, validation and drift correction\n')
        code += ('# parameters: target, good, error\n')
        code += ('#     target -- sound to play when target moves\n')
        code += ('#     good -- sound to play on successful operation\n')
        code += ('#     error -- sound to play on failure or interruption\n')
        code += ("# Each parameter could be ''--default sound, 'off'--no sound, or a wav file\n")
        if self.params['driftCheckSounds'].val == 'off':
            code += ("genv.setCalibrationSounds('off', 'off', 'off')\n")
        elif self.params['driftCheckSounds'].val == 'defaults':
            code += ("genv.setCalibrationSounds('', '', '')\n")
        elif self.params['driftCheckSounds'].val == 'custom wav files':
            code += ("genv.setCalibrationSounds(" + self.params['driftCheckFilenames'].val + ')\n')
        code += ('\n')
        code += ('# drift check\n')
        code += ('# the doDriftCorrect() function requires target position in integers\n')
        code += ('# the last two arguments:\n')
        code += ('# draw_target (1-default, 0-draw the target then call doDriftCorrect)\n')
        code += ('# allow_setup (1-press ESCAPE to recalibrate, 0-not allowed)\n')
        code += ('\n')
        code += ('# Skip drift-check if running the script in Dummy Mode\n')
        code += ('while not dummy_mode:\n')
        code += ('    # terminate the task if no longer connected to the tracker or\n')
        code += ('    # user pressed Ctrl-C to terminate the task\n')
        code += ('    if (not el_tracker.isConnected()) or el_tracker.breakPressed():\n')
        code += ('        terminate_task(win,genv,edf_file,session_folder,session_identifier)\n')
        code += ('    # drift-check and re-do camera setup if ESCAPE is pressed\n')
        code += ('    dcX,dcY = eyelink_pos(%s,[scn_width,scn_height],%s)\n' % (self.params['targetPosition'].val,self.params['screenUnitType']))
        code += ('    try:\n')
        code += ('        error = el_tracker.doDriftCorrect(int(round(dcX)),int(round(dcY)),1,1)\n')
        code += ('        # break following a success drift-check\n')
        code += ('        if error is not pylink.ESC_KEY:\n')
        code += ('            break\n')
        code += ('    except:\n')
        code += ('        pass\n')

        buff.writeOnceIndentedLines(code)




    def writeExperimentEndCode(self, buff):
        pass


