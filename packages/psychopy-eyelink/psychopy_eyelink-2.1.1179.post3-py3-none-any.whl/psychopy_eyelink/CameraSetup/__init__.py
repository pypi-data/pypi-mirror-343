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
_localized.update({'calibrationType': _translate('Calibration Type'),'backgroundColor': _translate('Background Color'),
                   'foregroundColor': _translate('Foreground Color'),'targetType': _translate('Target Type'), 'targetSize': _translate('Target Size'),
                   'targetFilename': _translate('Target Filename'), 'calibrationSounds': _translate('Calibration/Validation Sounds'),
                   'calibrationFilenames': _translate('Calibration/Validation Filenames')})


class CameraSetup(BaseComponent):
    """An event class for configuring the EyeLink camera to calibrate participants. 
    This allows the transfer of the EyeLink camera image, the presentation of various 
    calibration target types, and the configuration of various other 
    calibration/validation properties. To read more about Camera Setup please read 
    the EyeLink Programmers Guide, or check out the SR Research Support Forum.
    """
    categories = ['Eyetracking']  # which section(s) in the components panel
    targets = ['PsychoPy']
    iconFile = Path(__file__).parent / 'CameraSetup.png'
    tooltip = _translate('Performs EyeLink camera setup, calibration, validation')
    plugin = "psychopy-eyelink"

    def __init__(self, exp, parentName, name='CameraSetup', startType='time (s)', startVal='0.0', stopVal='0.001',
                 stopType='duration (s)', calibrationType='HV9', targetType = 'circle', targetFilename = '', targetSize = '24', foregroundColor = '(1,1,1)',
                 backgroundColor = 'win.color', calibrationSounds = "defaults", calibrationFilenames = "'qbeep.wav','type.wav','error.wav'"):

        super(CameraSetup, self).__init__(
            exp, parentName, name, startType=startType, startVal=startVal,
            stopType=stopType, stopVal=stopVal
            )

        self.type = 'CameraSetup'
        self.url = "https://www.sr-research.com/support/thread-7525.html"
        # update this URL to a component specific page on anm HTML manual

        self.params['calibrationType'] = Param(
            calibrationType, valType='str', inputType="choice", categ='Basic',
            allowedVals=['H3','HV3','HV5','HV9','H13'],
            updates='constant',
            hint=_translate("Number/shape of calibration/validation targets"),
            label=_localized['calibrationType'])
        
        self.params['targetType'] = Param(
            targetType, valType='str', inputType="choice", categ='Basic',
            allowedVals=['circle', 'picture', 'movie', 'spiral'],
            updates='constant',
            hint=_translate("Calibration/Validation Target Type"),
            label=_localized['targetType'])

        self.params['targetFilename'] = Param(
            targetFilename, categ='Basic',
            valType='str', inputType="single",
            hint=_translate('Calibration/Validation target filename'),
            label=_localized['targetFilename'])
        
        self.params['targetSize'] = Param(
            targetSize, categ='Basic',
            valType='str', inputType="single",
            hint=_translate('Calibration/Validation target size (in pixels)'),
            label=_localized['targetSize'])        

        self.params['foregroundColor'] = Param(
            foregroundColor, categ='Basic',
            valType='str', inputType="single",
            hint=_translate('Calibration/Validation foreground/target color\nOnly applies to circle and spiral'),
            label=_localized['foregroundColor'])

        self.params['backgroundColor'] = Param(
            backgroundColor, categ='Basic',
            valType='str', inputType="single",
            hint=_translate("Calibration/Validation background color\nUse win.color for the window's background color"),
            label=_localized['backgroundColor'])

        self.params['calibrationSounds'] = Param(
            calibrationSounds, valType='str', inputType="choice", categ='Basic',
            allowedVals=['defaults', 'off', 'custom wav files'],
            updates='constant',
            hint=_translate("This can be set to defaults (which uses the files qbeep.wav, type.wav, and error.wav that are included in example experiments),\n"
                            "off, or to use custom wav files.  If custom wav files is selected then Calibration/Validation Filenames need to be additionally specified."),
            label=_localized['calibrationSounds'])

        self.params['calibrationFilenames'] = Param(
            calibrationFilenames, categ='Basic',
            valType='str', inputType="single",
            hint=_translate("Custom Calibration/Validation wav filenames (Target, Good, Error)\n\
                            Target -- sound to play when target moves\n\
                            Good -- sound to play on successful operation\n\
                            Error -- sound to play on failure or interruption\n\
                            Each value should specify a wav file"),
            label=_localized['calibrationFilenames'])

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
            {'dependsOn':'calibrationSounds',
             'condition':'== "custom wav files"',
             'param':'calibrationFilenames',
             'true':'show',
             'false':'hide'}) 


    def writeInitCode(self,buff):
        code = ("%(name)s = event.Mouse(win=win)\n")
        buff.writeIndentedLines(code % self.params)
 

    def writeRunOnceInitCode(self, buff):
        pass


    def writeRoutineEndCode(self,buff):
        code = ('# This section of EyeLink %s component code configures some\n' % self.params['name'].val)
        code += ('# graphics options for calibration, and then performs a camera setup\n')
        code += ('# so that you can set up the eye tracker and calibrate/validate the participant\n')
        code += ('# graphics options for calibration, and then performs a camera setup\n')
        code += ('# so that you can set up the eye tracker and calibrate/validate the participant\n')
        code += ('\n')
        code += ('# Set background and foreground colors for the calibration target\n')
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
        code += ('\n')
        code += ('# Set up the calibration/validation target\n')
        code += ('#\n')
        code += ('# The target could be a "circle" (default), a "picture", a "movie" clip,\n')
        code += ('# or a rotating "spiral". To configure the type of drift check target, set\n')
        code += ('# genv.setTargetType to "circle", "picture", "movie", or "spiral", e.g.,\n')
        code += ("genv.setTargetType('%s')\n" % self.params['targetType'].val)
        code += ('#\n')   
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
        code += ('\n')
        code += ('# Beeps to play during calibration, validation and drift correction\n')
        code += ('# parameters: target, good, error\n')
        code += ('#     target -- sound to play when target moves\n')
        code += ('#     good -- sound to play on successful operation\n')
        code += ('#     error -- sound to play on failure or interruption\n')
        code += ("# Each parameter could be ''--default sound, 'off'--no sound, or a wav file\n")
        if self.params['calibrationSounds'].val == 'off':
            code += ("genv.setCalibrationSounds('off', 'off', 'off')\n")
        elif self.params['calibrationSounds'].val == 'defaults':
            code += ("genv.setCalibrationSounds('', '', '')\n")
        elif self.params['calibrationSounds'].val == 'custom wav files':
            code += ("genv.setCalibrationSounds(" + self.params['calibrationFilenames'].val + ')\n')
        code += ('\n')
        code += ('# Choose a calibration type, H3, HV3, HV5, HV13 (HV = horizontal/vertical),\n')
        code += ('el_tracker.sendCommand("calibration_type = " ' + str(self.params['calibrationType']) + ')\n')
        code += ('#clear the screen before we begin Camera Setup mode\n')
        code += ('clear_screen(win,genv)\n')
        code += ('\n')
        code += ('\n')
        code += ('# Go into Camera Setup mode so that participant setup/EyeLink calibration/validation can be performed\n')
        code += ('# skip this step if running the script in Dummy Mode\n')
        code += ('if not dummy_mode:\n')
        code += ('    try:\n')
        code += ('        el_tracker.doTrackerSetup()\n')
        code += ('    except RuntimeError as err:\n')
        code += ("        print('ERROR:', err)\n")
        code += ('        el_tracker.exitCalibration()\n')
        code += ('    else:\n')
        code += ('        win.mouseVisible = False\n')

        buff.writeOnceIndentedLines(code)


    def writeExperimentEndCode(self, buff):
        pass



