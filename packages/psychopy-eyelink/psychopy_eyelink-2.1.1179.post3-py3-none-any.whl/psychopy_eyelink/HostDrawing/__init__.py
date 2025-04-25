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
_localized.update({'imagesToHostBackdrop':_translate('Images for Host PC Backdrop'),
                   'componentsForDrawingToHostBackdrop':_translate('Components for Draw Commands to Host PC Backdrop'),
                   'additionalDrawCommands':_translate('Additional Draw Commands for Host PC Backdrop'),'drawCommands': _translate('Draw Commands'),
                   'recordStatusMessage':_translate('Record Status Message')})


class HostDrawing(BaseComponent):
    """An event class for populating the Host PC backdrop before recording
    """
    categories = ['Eyetracking']  # which section(s) in the components panel
    targets = ['PsychoPy']
    iconFile = Path(__file__).parent / 'HostDrawing.png'
    tooltip = _translate('Populates the Host PC backdrop with stimuli/landmarks')
    plugin = "psychopy-eyelink"

    def __init__(self, exp, parentName, name='HostDrawing', startType='time (s)', startVal='0.0', stopVal='0.001',
                 stopType='duration (s)', imagesToHostBackdrop = '', componentsForDrawingToHostBackdrop = '',
                 additionalDrawCommands = '', recordStatusMessage = ''):

        super(HostDrawing, self).__init__(
            exp, parentName, name, startType=startType, startVal=startVal,
            stopType=stopType, stopVal=stopVal
            )

        self.type = 'HostDrawing'
        self.url = "https://www.sr-research.com/support/thread-7525.html"

        self.params['imagesToHostBackdrop'] = Param(
            imagesToHostBackdrop, categ='Basic',
            valType='str', inputType="single",
            hint=_translate('Images and their corresponding components that should be sent To Host PC Backdrop\n'
                            'Each pair should provide the image filename (or a variable specifying it) followed by\n'
                            'the component handling its presentation (separated by comma).  Pairs should be separated by semicolon\n'
                            'E.g., targImage,targImageComponent;distImage,distImageComponent'),
            label=_localized['imagesToHostBackdrop'])
        
        self.params['componentsForDrawingToHostBackdrop'] = Param(
            componentsForDrawingToHostBackdrop, categ='Basic',
            valType='str', inputType="single",
            hint=_translate('Components for which to send simple draw commands to Host PC backdrop\n'
                            'These components will be represented by a rectangle on the Host PC backdrop'),
            label=_localized['componentsForDrawingToHostBackdrop'])
     
        self.params['additionalDrawCommands'] = Param(
            additionalDrawCommands, categ='Basic',
            valType='str', inputType="single",
            hint=_translate('Additional Host PC Backdrop drawing commands to send\n'
                            'Commands should be separated by semicolon'),
            label=_localized['additionalDrawCommands'])
        
        self.params['recordStatusMessage'] = Param(
            recordStatusMessage, categ='Basic',
            valType='str', inputType="single",
            hint=_translate('Record status message string to send to Host PC\n'
                            'This string will be shown at the bottom of the Host PC during recording'),
            label=_localized['recordStatusMessage'])
        

    def writeInitCode(self,buff):
        code = ("%(name)s = event.Mouse(win=win)\n")
        buff.writeIndentedLines(code % self.params)
 

    def writeRunOnceInitCode(self, buff):
        pass


    def writeRoutineEndCode(self,buff):
        code = ('# This section of EyeLink %s component code provides options for sending images/shapes\n' % self.params['name'].val)
        code += ('# representing stimuli to the Host PC backdrop for real-time gaze monitoring\n')
        code += ('\n')
        code += ('# get a reference to the currently active EyeLink connection\n')
        code += ('el_tracker = pylink.getEYELINK()\n')
        code += ('# put the tracker in the offline mode first\n')
        code += ('el_tracker.setOfflineMode()\n')
        code += ('# clear the host screen before we draw the backdrop\n')
        code += ("el_tracker.sendCommand('clear_screen 0')\n")
        if len(self.params['imagesToHostBackdrop'].val) > 0:
            imagesAndComponentsStringList = self.params['imagesToHostBackdrop'].val.strip('[]').split(';')
            code += ('# imagesAndComponentsStringList value = %s\n' % imagesAndComponentsStringList)
            imagesAndComponentsList = []
            for subList in imagesAndComponentsStringList:
                subList = subList.strip('$')
                imageComponentList = subList.split(',')
                imagesAndComponentsList.append([imageComponentList[0],imageComponentList[1]])
                imagesAndComponentsListString = str(imagesAndComponentsList).replace("'","")
            code += ('# Send image components to the Host PC backdrop to serve as landmarks during recording\n')
            code += ('# The method bitmapBackdrop() requires a step of converting the\n')
            code += ('# image pixels into a recognizable format by the Host PC.\n')
            code += ('# pixels = [line1, ...lineH], line = [pix1,...pixW], pix=(R,G,B)\n')
            code += ('# the bitmapBackdrop() command takes time to return, not recommended\n')
            code += ('# for tasks where the ITI matters, e.g., in an event-related fMRI task\n')
            code += ('# parameters: width, height, pixel, crop_x, crop_y,\n')
            code += ('#             crop_width, crop_height, x, y on the Host, drawing options\n')
            code += ('imagesAndComponentsListForHostBackdrop = %s\n' % imagesAndComponentsListString)
            code += ('# get the array of blank pixels where each pixel corresponds to win.color\n')
            code += ('pixels = blankHostPixels[::]\n')
            code += ('# go through each image and replace the pixels in the blank array with the image pixels\n')
            code += ('for thisImage in imagesAndComponentsListForHostBackdrop:\n')
            code += ('    thisImageFile = thisImage[0]\n')
            code += ('    thisImageComponent = thisImage[1]\n')
            code += ('    thisImageComponent.setImage(thisImageFile)\n')
            code += ('    if "Image" in str(thisImageComponent.__class__):\n')
            code += ('        # Use the code commented below to convert the image and send the backdrop\n')
            code += ('        im = Image.open(script_path + "/" + thisImageFile)\n')
            code += ('        thisImageComponent.elPos = eyelink_pos(thisImageComponent.pos,[scn_width,scn_height],thisImageComponent.units)\n')
            code += ('        thisImageComponent.elSize = eyelink_size(thisImageComponent.size,[scn_width,scn_height],thisImageComponent.units)\n')
            code += ('        imWidth = int(round(thisImageComponent.elSize[0]))\n')
            code += ('        imHeight = int(round(thisImageComponent.elSize[1]))\n')
            code += ('        imLeft = int(round(thisImageComponent.elPos[0]-thisImageComponent.elSize[0]/2))\n')
            code += ('        imTop = int(round(thisImageComponent.elPos[1]-thisImageComponent.elSize[1]/2))\n')
            code += ('        im = im.resize((imWidth,imHeight))\n')
            code += ('        # Access the pixel data of the image\n')
            code += ('        img_pixels = list(im.getdata())\n')
            code += ('        # Check to see if the image goes off the screen\n')
            code += ('        # If so, adjust the coordinates appropriately\n')
            code += ('        if imLeft < 0:\n')
            code += ('            imTransferLeft = 0\n')
            code += ('        else:\n')
            code += ('            imTransferLeft = imLeft\n')
            code += ('        if imTop < 0:\n')
            code += ('            imTransferTop = 0\n')
            code += ('        else:\n')
            code += ('            imTransferTop = imTop\n')
            code += ('        if imLeft + imWidth > scn_width:\n')
            code += ('            imTransferRight = scn_width\n')
            code += ('        else:\n')
            code += ('            imTransferRight = imLeft+imWidth\n')
            code += ('        if imTop + imHeight > scn_height:\n')
            code += ('            imTransferBottom = scn_height\n')
            code += ('        else:\n')
            code += ('            imTransferBottom = imTop+imHeight    \n')
            code += ('        imTransferImageLineStartX = imTransferLeft-imLeft\n')
            code += ('        imTransferImageLineEndX = imTransferRight-imTransferLeft+imTransferImageLineStartX\n')
            code += ('        imTransferImageLineStartY = imTransferTop-imTop\n')
            code += ('        for y in range(imTransferBottom-imTransferTop):\n')
            code += ('            pixels[imTransferTop+y][imTransferLeft:imTransferRight] = \\\n')
            code += ('                img_pixels[(imTransferImageLineStartY + y)*imWidth+imTransferImageLineStartX:\\\n')
            code += ('                (imTransferImageLineStartY + y)*imWidth + imTransferImageLineEndX]\n')
            code += ('    else:\n')
            code += ('        print("WARNING: Image Transfer Not Supported For non-Image Component %s)" % str(thisComponent.__class__))\n')
            code += ('# transfer the full-screen pixel array to the Host PC\n')
            code += ('el_tracker.bitmapBackdrop(scn_width,scn_height, pixels,\\\n')
            code += ('    0, 0, scn_width, scn_height, 0, 0, pylink.BX_MAXCONTRAST)\n')

        if len(self.params['componentsForDrawingToHostBackdrop'].val) > 0:
            code += ('# Draw rectangles along the edges of components to serve as landmarks on the Host PC backdrop during recording\n')
            code += ('# For a list of supported draw commands, see the "COMMANDS.INI" file on the Host PC\n')
            code += ('componentDrawListForHostBackdrop = [%s]\n' % self.params['componentsForDrawingToHostBackdrop'].val)
            code += ('for thisComponent in componentDrawListForHostBackdrop:\n')
            code += ('        thisComponent.elPos = eyelink_pos(thisComponent.pos,[scn_width,scn_height],thisComponent.units)\n')
            code += ('        thisComponent.elSize = eyelink_size(thisComponent.size,[scn_width,scn_height],thisComponent.units)\n')
            code += ('        drawColor = 4\n')
            code += ('        drawCommand = "draw_box = %i %i %i %i %i" % (thisComponent.elPos[0] - thisComponent.elSize[0]/2,\n')
            code += ('            thisComponent.elPos[1] - thisComponent.elSize[1]/2, thisComponent.elPos[0] + thisComponent.elSize[0]/2,\n')
            code += ('            thisComponent.elPos[1] + thisComponent.elSize[1]/2, drawColor)\n')
            code += ("        el_tracker.sendCommand(drawCommand)\n")
        if len(self.params['additionalDrawCommands'].val) > 0:
             drawCommandsToDo = self.params['additionalDrawCommands'].val.replace(', ',',').strip('][').split(';')
             code += ('# Draw additional shapes to serve as landmarks on the Host PC backdrop during recording\n')
             code += ('# For a list of supported draw commands, see the "COMMANDS.INI" file on the Host PC\n')
             for drawCommand in drawCommandsToDo: 
                 code += ('el_tracker.sendCommand(%s)\n' % drawCommand)
        if len(self.params['recordStatusMessage'].val) > 0:
            code += ('# record_status_message -- send a messgae string to the Host PC that will be present during recording\n')
            code += ('el_tracker.sendCommand("record_status_message ' + "'%s'" + '" % (' + self.params['recordStatusMessage'].val + '))\n')
 
        buff.writeOnceIndentedLines(code)


    def writeExperimentEndCode(self, buff):
        pass


