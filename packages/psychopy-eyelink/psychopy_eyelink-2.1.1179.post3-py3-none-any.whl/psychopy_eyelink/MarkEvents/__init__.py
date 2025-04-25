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


_localized.update({'trialConditionVariablesForEyeLinkLogging': _translate('Trial Condition Variables for Logging'),
                    'componentsForEyeLinkStimEventMessages': _translate('Stimulus Components for Event Marking'),
                    'includeAllEventMarkedComponentsForDVDrawingMessages': _translate('Include All Event Marked Stimulus Components For DV Drawing Messaging'),
                    'componentsForEyeLinkStimDVDrawingMessages': _translate('Stimulus Components for Data Viewer Drawing Messaging'),
                    'sendVideoFrameMessages': _translate('Send Video Frame Onset Messages to Enable Playback in Data Viewer'),
                    'includeAllEventMarkedComponentsForIAMessages': _translate('Include All Event Marked Stimulus Components For Interest Area Messaging'),
                    'componentsForEyeLinkInterestAreaMessages': _translate('Stimulus Components for Interest Area Messaging'),
                    'interestAreaMargins': _translate('Interest Area Margins'),
                    'interestAreaShape': _translate('Interest Area Shape'),
                    'componentsForEyeLinkTargetPositionMessages': _translate('Stimulus Components for Target Position Messaging'),
                    'componentsForEyeLinkRespEventMessages': _translate('Response Components for Event Marking'),
                    'sendTrialOnsetOffsetMessages': _translate('Send Trial Onset Offset Messages'),
                    'useQuitKeys': _translate('Allow Ctrl-C Quit Key to be Used')})


class MarkEvents(BaseComponent):
    """An event class for marking experimental events and for logging trial data and.
    stimulus presentation for Data Viewer integration purposes.
    """
    categories = ['Eyetracking']  # which section(s) in the components panel
    targets = ['PsychoPy']
    iconFile = Path(__file__).parent / 'MarkEvents.png'
    tooltip = _translate('Sends messages to the edf to mark events, log trial variable values,\n'
                         'and log stimulus/interest area information for analysis')
    plugin = "psychopy-eyelink"

    def __init__(self, exp, parentName, name='MarkEvents', startType='time (s)', startVal='0.0', stopVal='0.001',
                 stopType='duration (s)', trialConditionVariablesForEyeLinkLogging='', componentsForEyeLinkStimEventMessages='',
                 includeAllEventMarkedComponentsForDVDrawingMessages = True, componentsForEyeLinkStimDVDrawingMessages = '',
                 sendVideoFrameMessages = False, includeAllEventMarkedComponentsForIAMessages = True, componentsForEyeLinkInterestAreaMessages = '',
                 interestAreaMargins = '0', interestAreaShape = 'Rectangle', componentsForEyeLinkTargetPositionMessages = '',componentsForEyeLinkRespEventMessages = '',
                 sendTrialOnsetOffsetMessages = False, useQuitKeys = True):

        super(MarkEvents, self).__init__(
            exp, parentName, name, startType=startType, startVal=startVal,
            stopType=stopType, stopVal=stopVal
            )

        self.type = 'MarkEvents'
        self.url = "https://www.sr-research.com/support/thread-7525.html"

        self.params['trialConditionVariablesForEyeLinkLogging'] = Param(
            trialConditionVariablesForEyeLinkLogging, categ='Basic',
            valType='str', inputType="single",
            hint=_translate('Trial condition variables to log'),
            label=_localized['trialConditionVariablesForEyeLinkLogging'])
        
        self.params['componentsForEyeLinkStimEventMessages'] = Param(
            componentsForEyeLinkStimEventMessages, categ='Basic',
            valType='str', inputType="single",
            hint=_translate('Stimulus components for event marking'),
            label=_localized['componentsForEyeLinkStimEventMessages'])
        
        self.params['includeAllEventMarkedComponentsForDVDrawingMessages'] = Param(
            includeAllEventMarkedComponentsForDVDrawingMessages, categ='Basic',
            valType='bool', inputType="bool",
            hint=_translate('Include all event marked stimulus components for DV drawing messaging'),
            label=_localized['includeAllEventMarkedComponentsForDVDrawingMessages'])
        
        self.params['componentsForEyeLinkStimDVDrawingMessages'] = Param(
            componentsForEyeLinkStimDVDrawingMessages, categ='Basic',
            valType='str', inputType="single",
            hint=_translate('Stimulus components for DV stimulus drawing messaging'),
            label=_localized['componentsForEyeLinkStimDVDrawingMessages'])
        
        self.params['sendVideoFrameMessages'] = Param(
            sendVideoFrameMessages, categ='Basic',
            valType='bool', inputType="bool",
            hint=_translate('Send video frame onset messages to enable DV video playback'),
            label=_localized['sendVideoFrameMessages'])

        self.params['includeAllEventMarkedComponentsForIAMessages'] = Param(
            includeAllEventMarkedComponentsForIAMessages, categ='Basic',
            valType='bool', inputType="bool",
            hint=_translate('Include all event marked stimulus components for interest area messaging'),
            label=_localized['includeAllEventMarkedComponentsForIAMessages'])
        
        self.params['componentsForEyeLinkInterestAreaMessages'] = Param(
            componentsForEyeLinkInterestAreaMessages, categ='Basic',
            valType='str', inputType="single",
            hint=_translate('Stimulus components for interest area messaging'),
            label=_localized['componentsForEyeLinkInterestAreaMessages'])
        
        self.params['interestAreaMargins'] = Param(
            interestAreaMargins, categ='Basic',
            valType='str', inputType="single",
            hint=_translate('Margins to add to each side when creating interest areas'),
            label=_localized['interestAreaMargins'])
        
        self.params['interestAreaShape'] = Param(
            interestAreaShape, valType='str', inputType="choice", categ='Basic',
            allowedVals=['Rectangle','Ellipse'],
            updates='constant',
            hint=_translate("Shape of interest areas"),
            label=_localized['interestAreaShape'])
        
        self.params['componentsForEyeLinkTargetPositionMessages'] = Param(
            componentsForEyeLinkTargetPositionMessages, categ='Basic',
            valType='str', inputType="single",
            hint=_translate('Stimulus components for target position messaging'),
            label=_localized['componentsForEyeLinkTargetPositionMessages'])

        self.params['componentsForEyeLinkRespEventMessages'] = Param(
            componentsForEyeLinkRespEventMessages, categ='Basic',
            valType='str', inputType="single",
            hint=_translate('Response components for event marking'),
            label=_localized['componentsForEyeLinkRespEventMessages'])
        
        self.params['sendTrialOnsetOffsetMessages'] = Param(
            sendTrialOnsetOffsetMessages, categ='Basic',
            valType='bool', inputType="bool",
            hint=_translate('Send trial onset/offset messages within continuous recording\nUsually should be false, should be true for continuous recording with multiple trials'),
            label=_localized['sendTrialOnsetOffsetMessages'])
        
        self.params['useQuitKeys'] = Param(
            useQuitKeys, categ='Basic',
            valType='bool', inputType="bool",
            hint=_translate('Allow quit keys to be used (Esc to abort the trial, Ctrl-C to end run)'),
            label=_localized['useQuitKeys'])
        
        self.depends.append(
            {'dependsOn':'includeAllEventMarkedComponentsForDVDrawingMessages',
             'condition':'==True',
             'param':'componentsForEyeLinkStimDVDrawingMessages',
             'true':'hide',
             'false':'show'})
        
        self.depends.append(
            {'dependsOn':'includeAllEventMarkedComponentsForIAMessages',
             'condition':'==True',
             'param':'componentsForEyeLinkInterestAreaMessages',
             'true':'hide',
             'false':'show'})

    def writeInitCode(self,buff):
        code = ("%(name)s = event.Mouse(win=win)\n")
        buff.writeIndentedLines(code % self.params)



######### PRE Experiment Event Marking/ DV Logging Function Definitions

    def writePreCode(self,buff):
        # create variables to store the conponents that need to be checked for event marking and DV logging 
        self.componentsForStimEventMarking = self.params['componentsForEyeLinkStimEventMessages'].val.replace(" ","").strip('[]')
        if self.params['includeAllEventMarkedComponentsForDVDrawingMessages'].val == True:
            self.componentsForDVDrawingMessages = self.componentsForStimEventMarking
        else:
            self.componentsForDVDrawingMessages = self.params['componentsForEyeLinkStimDVDrawingMessages'].val.replace(" ","").strip('[]')
        if self.params['includeAllEventMarkedComponentsForIAMessages'].val == True:
            self.componentsForIAMessages = self.componentsForStimEventMarking
        else:
            self.componentsForIAMessages = self.params['componentsForEyeLinkInterestAreaMessages'].val.replace(" ","").strip('[]')
        self.componentsForTargPosMessages = self.params['componentsForEyeLinkTargetPositionMessages'].val.replace(" ","").strip('[]')
        self.componentsForRespEventMarking = self.params['componentsForEyeLinkRespEventMessages'].val.replace(" ","").strip('[]')

        # if any of the variables actually have components in them then create the function.  Otherwise skip this
        if len(self.componentsForStimEventMarking) > 0 or len(self.componentsForDVDrawingMessages) > 0 or \
            len(self.componentsForIAMessages) > 0 or len(self.componentsForTargPosMessages) > 0:

            code = ('# This method, created by the EyeLink %s component code, will get called to handle\n' % self.params['name'].val)
            code += ('# sending event marking messages, logging Data Viewer (DV) stimulus drawing info, logging DV interest area info,\n')
            code += ('# sending DV Target Position Messages, and/or logging DV video frame marking info=information\n')
            code += ('def eyelink_onFlip_%s(globalClock,win,scn_width,scn_height,allStimComponentsForEyeLinkMonitoring,\\\n' % self.params['name'].val)
            if len(self.componentsForStimEventMarking) > 0:   
                code += ('    componentsForEyeLinkStimEventMessages,\\\n')
            if len(self.componentsForDVDrawingMessages) > 0:
                code += ('    componentsForEyeLinkStimDVDrawingMessages,dlf,dlf_file,\\\n')
            if len(self.componentsForIAMessages) > 0:
                code += ('    componentsForEyeLinkInterestAreaMessages,ias,ias_file,interestAreaMargins,\\\n')
            if len(self.componentsForTargPosMessages) > 0:
                code += ('    componentsForEyeLinkTargetPositionMessages,\\\n')
            if self.params['sendVideoFrameMessages'].val == True:
                code += ('    componentsForEyeLinkMovieFrameMarking')
            code = code.rstrip('\n')
            code = code.rstrip('\\')
            code = code.rstrip(',')
            code += ('):\n')

            code += ('    global eyelinkThisFrameCallOnFlipScheduled,eyelinkLastFlipTime,')
            if len(self.componentsForStimEventMarking) > 0: 
                code += ('zeroTimeDLF,sentDrawListMessage,')
            if len(self.componentsForIAMessages) > 0:
                code += ('zeroTimeIAS,sentIASFileMessage,')

            code = code.rstrip(',')
            code += ('\n')

            if len(self.componentsForDVDrawingMessages) > 0:
                code += ('    # this variable becomes true whenever a component offsets, so we can \n')
                code += ('    # send Data Viewer messgaes to clear the screen and redraw still-present \n')
                code += ('    # components.  set it to false until a screen clear is needed\n')
                code += ('    needToUpdateDVDrawingFromScreenClear = False\n')
                code += ('    # store a list of all components that need Data Viewer drawing messages \n')
                code += ('    # sent for this screen retrace\n')
                code += ('    componentsForDVDrawingList = []\n')
            
            if len(self.componentsForIAMessages) > 0:
                code += ('    # store a list of all components that need Data Viewer interest area messages \n')
                code += ('    # sent for this screen retrace\n')
                code += ('    componentsForIAInstanceMessagesList = []\n')

            if len(self.componentsForStimEventMarking) > 0 or len(self.componentsForDVDrawingMessages) > 0 or \
                len(self.componentsForIAMessages) > 0 or len(self.componentsForTargPosMessages) > 0:
                code += ('    # Log the time of the current frame onset for upcoming messaging/event logging\n')
                code += ('    currentFrameTime = float(globalClock.getTime())\n')
                
    #########################################################################################################################
    ################################################# EACH FRAME ONSET CHECKING #############################################

    #########################   GO THROUGH ALL STIM COMPONENTS FOR ALL ONSET CHECKING
                code += ('\n')
                code += ('    # Go through all stimulus components that need to be checked (for event marking,\n')
                code += ('    # DV drawing, and/or interest area logging) to see if any have just ONSET\n')
                code += ('    for thisComponent in allStimComponentsForEyeLinkMonitoring:\n')
                        
                #########################   CHECK FOR ONSET
                code += ('        # Check if the component has just onset\n')
                code += ('        if thisComponent.tStartRefresh is not None and not thisComponent.elOnsetDetected:\n')
                
                #########################   ONSET STIM MARKING
                if len(self.componentsForStimEventMarking) > 0:
                    code += ('            # Check whether we need to mark stimulus onset (and log a trial variable logging this time) for the component\n') 
                    code += ('            if thisComponent in componentsForEyeLinkStimEventMessages:\n')
                    code += ("                el_tracker.sendMessage('%s %s_ONSET' % (int(round((globalClock.getTime()-thisComponent.tStartRefresh)*1000)),thisComponent.name))\n")
                    code += ("                el_tracker.sendMessage('!V TRIAL_VAR %s_ONSET_TIME %i' % (thisComponent.name,thisComponent.tStartRefresh*1000))\n")
                code += ("                # Convert the component's position to EyeLink units and log this value under .elPos\n")
                code += ("                # Also create lastelPos/lastelSize to store pos/size of the previous position, which is needed for IAS file writing\n")  
                code += ("                if thisComponent.componentType != 'sound':\n")    
                code += ('                    thisComponent.elPos = eyelink_pos(thisComponent.pos,[scn_width,scn_height],thisComponent.units)\n')
                code += ('                    thisComponent.elSize = eyelink_size(thisComponent.size,[scn_width,scn_height],thisComponent.units)\n')
                code += ('                    thisComponent.lastelPos = thisComponent.elPos\n')
                code += ('                    thisComponent.lastelSize = thisComponent.elSize\n')

                #########################   ONSET TARGET POSIITON MESSAGING
                if len(self.componentsForTargPosMessages) > 0:
                    code += ('            # Check whether we need to send a target position message (the first) for the component\n')   
                    code += ('            if thisComponent in componentsForEyeLinkTargetPositionMessages:\n')               
                    code += ("                el_tracker.sendMessage('%s !V TARGET_POS %s (%s, %s) 1 0' % \\\n")
                    code += ('                    (int(round((globalClock.getTime()-thisComponent.tStartRefresh)*1000)),thisComponent.targLabel,\\\n')
                    code += ('                    int(round(thisComponent.elPos[0])),int(round(thisComponent.elPos[1]))))\n')

                #########################   ONSET IAS MESSAGE and INTEREST AREA LOGGING
                if len(self.componentsForIAMessages) > 0:
                    code += ('            # If this is the first interest area instance of the trial write a message pointing\n')
                    code += ('            # Data Viewer to the IAS file.  The time of the message will serve as the zero time point\n')
                    code += ('            # for interest area information (e.g., instance start/end times) that is logged to the file\n')
                    code += ('            if thisComponent in componentsForEyeLinkInterestAreaMessages:\n')
                    code += ('                if not sentIASFileMessage:\n')
                    code += ('                    # send an IAREA FILE command to let Data Viewer know where\n')
                    code += ('                    # to find the IAS file to load interest area information\n')
                    code += ('                    zeroTimeIAS = float(currentFrameTime)\n')
                    code += ("                    el_tracker.sendMessage('%s !V IAREA FILE aoi/%s' % (int(round((globalClock.getTime()-currentFrameTime)*1000)),ias))\n")
                    code += ('                    sentIASFileMessage = True\n')
                    code += ("                thisComponent.iaInstanceStartTime = currentFrameTime\n")

                #########################   ONSET DLF MESSAGE AND LOGGING FOR DRAW COMMANDS (TO BE DONE BELOW)
                if len(self.componentsForDVDrawingMessages) > 0:
                    code += ('            if not sentDrawListMessage and not dlf_file.closed:\n')
                    code += ('                # send an IAREA FILE command message to let Data Viewer know where\n')
                    code += ('                # to find the IAS file to load interest area information\n')
                    code += ('                zeroTimeDLF = float(currentFrameTime)\n')
                    code += ('                # send a DRAW_LIST command message to let Data Viewer know where\n')
                    code += ('                # to find the drawing messages to correctly present the stimuli\n')
                    code += ("                el_tracker.sendMessage('%s !V DRAW_LIST graphics/%s' % (int(round((globalClock.getTime()-currentFrameTime)*1000))-3,dlf))\n")
                    code += ("                dlf_file.write('0 CLEAR %d %d %d\\n' % eyelink_color(win.color))\n")
                    code += ('                sentDrawListMessage = True\n')
                    code += ('\n')
                    code += ('            if thisComponent in componentsForEyeLinkStimDVDrawingMessages:\n')
                    code += ('                componentsForDVDrawingList.append(thisComponent)\n')
                code += ('\n')
                code += ('            thisComponent.elOnsetDetected = True\n')
                code += ('\n')


#########################################################################################################################
################################################# EACH FRAME POSITION CHANGE CHECKING ###################################
            
            if len(self.componentsForTargPosMessages) > 0 or len(self.componentsForIAMessages) > 0 or len(self.componentsForDVDrawingMessages) > 0:
                code += ('    # Check whether any components that are being monitored for EyeLink purposes have changed position\n')
                code += ('    for thisComponent in allStimComponentsForEyeLinkMonitoring:\n')
                code += ("        if thisComponent.componentType != 'sound':\n")
                code += ('            # Get the updated position in EyeLink Units\n')
                code += ('            thisComponent.elPos = eyelink_pos(thisComponent.pos,[scn_width,scn_height],thisComponent.units)\n')
                code += ('            if thisComponent.elPos[0] != thisComponent.lastelPos[0] or thisComponent.elPos[1] != thisComponent.lastelPos[1]\\\n')
                code += ('                and thisComponent.elOnsetDetected:\n')
                code += ('                # Only get an updated size if position has changed\n')
                code += ('                thisComponent.elSize = eyelink_size(thisComponent.size,[scn_width,scn_height],thisComponent.units)\n')
            #########################   CHECK FOR NEED TO UPDATE DV TRIAL VIEW
            if len(self.componentsForDVDrawingMessages) > 0:
                code += ('                # log that we need to update the screen drawing with a clear command\n')
                code += ('                # and a redrawing of all still-present components\n')
                code += ('                if thisComponent in componentsForEyeLinkStimDVDrawingMessages:\n')
                code += ('                    needToUpdateDVDrawingFromScreenClear = True\n')
                code += ('\n')
            if len(self.componentsForIAMessages) > 0:
                code += ('                # log that we need to send an interest area instance message to the EDF\n')
                code += ('                # to mark the presentation that just ended\n')
                code += ('                if thisComponent in componentsForEyeLinkInterestAreaMessages:\n')
                code += ('                    thisComponent.iaInstancePos = thisComponent.lastelPos\n')
                code += ('                    thisComponent.iaInstanceSize = thisComponent.lastelSize\n')
                code += ('                    componentsForIAInstanceMessagesList.append(thisComponent)\n')
                code += ('\n')
            code += ('                # update the position (in EyeLink coordinates) for upcoming usage\n')
            code += ("        if thisComponent.componentType != 'sound':\n")
            code += ('            thisComponent.lastelPos = thisComponent.elPos\n')
            code += ('            thisComponent.lastelSize = thisComponent.elSize\n')

            #########################   CHECK FOR NEED TO UPDATE TARGET POS MESSAGE
            if len(self.componentsForTargPosMessages) > 0:
                code += ('            # Check whether we need to send a target position messagew for Data Viewer integration\n')
                code += ('            if thisComponent in componentsForEyeLinkTargetPositionMessages:\n')
                code += ("                el_tracker.sendMessage('%s !V TARGET_POS %s (%s, %s) 1 1' % (int(round((globalClock.getTime()-currentFrameTime)*1000)),thisComponent.targLabel,\\\n")
                code += ('                    int(round(thisComponent.elPos[0])),int(round(thisComponent.elPos[1]))))\n')
            

#########################################################################################################################
################################################# EACH FRAME OFFSET CHECKING ############################################

#########################   GO THROUGH ALL STIM COMPONENTS FOR ALL OFFSET CHECKING
            code += ('    # Go through all stimulus components that need to be checked (for event marking,\n')
            code += ('    # DV drawing, and/or interest area logging) to see if any have just OFFSET\n')
            code += ('    for thisComponent in allStimComponentsForEyeLinkMonitoring:\n')

#########################   CHECK FOR STIM OFFSET
            code += ('        # Check if the component has just offset\n')
            code += ('        if thisComponent.tStopRefresh is not None and thisComponent.tStartRefresh is not None and \\\n')
            code += ('            not thisComponent.elOffsetDetected:\n')

            #########################   OFFSET STIM MARKING
            if len(self.componentsForStimEventMarking) > 0:
                code += ("            # send a message marking that component's offset in the EDF\n")
                code += ('            if thisComponent in componentsForEyeLinkStimEventMessages:\n')
                code += ("                el_tracker.sendMessage('%s %s_OFFSET' % (int(round((globalClock.getTime()-thisComponent.tStopRefresh)*1000)),thisComponent.name))\n")

            #########################   OFFSET DV DRAWING
            if len(self.componentsForDVDrawingMessages) > 0:
                code += ('            # log that we need to update the screen drawing with a clear command\n')
                code += ('            # and a redrawing of all still-present components\n')
                code += ('            if thisComponent in componentsForEyeLinkStimDVDrawingMessages:\n')
                code += ('                needToUpdateDVDrawingFromScreenClear = True\n')

            #########################   OFFSET IA Messaging
            if len(self.componentsForIAMessages) > 0:
                code += ('            # log that we need to send an interest area instance message to the EDF\n')
                code += ('            # to mark the presentation that just ended\n')
                code += ('            if thisComponent in componentsForEyeLinkInterestAreaMessages:\n')
                code += ('                thisComponent.iaInstancePos = thisComponent.lastelPos\n')
                code += ('                thisComponent.iaInstanceSize = thisComponent.lastelSize\n')
                code += ('                componentsForIAInstanceMessagesList.append(thisComponent)\n')
            code += ('            thisComponent.elOffsetDetected = True \n')



#########################################################################################################################
################################################# IAS AND DLF FILE WRITING ##############################################         

            ######################### IAS FILE WRITING          
            if len(self.componentsForIAMessages) > 0:
                code += ('    # send an interest area message to the IAS file\n')
                code += ('    # see the section of the Data Viewer User Manual \n')
                code += ('    # Protocol for EyeLink Data to Viewer Integrations -> Interest Area Commands\n')
                code += ('    if not ias_file.closed:\n')
                code += ('        for thisComponent in componentsForIAInstanceMessagesList:\n')
                if self.params['interestAreaShape'].val == 'Rectangle':
                    shapeText = 'RECTANGLE'
                elif self.params['interestAreaShape'].val == 'Ellipse':
                    shapeText = 'ELLIPSE'
                if self.params['interestAreaMargins'].val.isdigit():        
                    code += ("            ias_file.write('%i %i IAREA %s %i %i %i %i %i %s\\n' % \\\n")
                    code += ('                (int(round((zeroTimeIAS - thisComponent.iaInstanceStartTime)*1000)),\n')
                    code += ('                int(round((zeroTimeIAS - currentFrameTime)*1000 + 1)),"%s",thisComponent.iaIndex,\n' % shapeText)
                    code += ('                thisComponent.iaInstancePos[0]-(thisComponent.iaInstanceSize[0]/2+interestAreaMargins),\n')
                    code += ('                thisComponent.iaInstancePos[1]-(thisComponent.iaInstanceSize[1]/2+interestAreaMargins),\n')
                    code += ('                thisComponent.iaInstancePos[0]+(thisComponent.iaInstanceSize[0]/2+interestAreaMargins),\n')
                    code += ('                thisComponent.iaInstancePos[1]+(thisComponent.iaInstanceSize[1]/2+interestAreaMargins),thisComponent.name))\n')
                else:
                    code += ("            ias_file.write('%i %i IAREA %s %i %i %i %i %i %s\\n' % \\\n")
                    code += ('                (int(round((zeroTimeIAS - thisComponent.iaInstanceStartTime)*1000)),\n')
                    code += ('                int(round((zeroTimeIAS - currentFrameTime)*1000 + 1)),"%s",thisComponent.iaIndex,\n' % shapeText)
                    code += ('                thisComponent.iaInstancePos[0]-thisComponent.iaInstanceSize[0]/2,\n')
                    code += ('                thisComponent.iaInstancePos[1]-thisComponent.iaInstanceSize[1]/2,\n')
                    code += ('                thisComponent.iaInstancePos[0]+thisComponent.iaInstanceSize[0]/2,\n')
                    code += ('                thisComponent.iaInstancePos[1]+thisComponent.iaInstanceSize[1]/2,thisComponent.name))\n')
                code += ('            thisComponent.iaInstanceStartTime = currentFrameTime\n')


            ######################### DLF FILE WRITING
            if len(self.componentsForDVDrawingMessages) > 0:

                ######################### CLEAR COMMAND DLF FILE WRITING
                code += ('    # Send drawing messages to the draw list file so that the stimuli/placeholders can be viewed in \n')
                code += ("    # Data Viewer's Trial View window\n")
                code += ('    # See the Data Viewer User Manual, sections:\n')
                code += ('    # Protocol for EyeLink Data to Viewer Integration -> Image Commands/Simple Drawing Commands\n')
                code += ('    # If any component has offsetted on this frame then send a clear message\n')
                code += ('    # followed by logging to send draw commands for all still-present components\n')
                code += ('    if needToUpdateDVDrawingFromScreenClear and not dlf_file.closed:\n')
                code += ("        dlf_file.write('%i CLEAR ' % (int(round((zeroTimeDLF - currentFrameTime)*1000)))\n")
                code += ("            + '%d %d %d\\n' % eyelink_color(win.color))\n")
                code += ('\n')
                code += ('        for thisComponent in componentsForEyeLinkStimDVDrawingMessages:\n')
                code += ('            if thisComponent.elOnsetDetected and not thisComponent.elOffsetDetected and thisComponent not in componentsForDVDrawingList:\n')
                code += ('                componentsForDVDrawingList.append(thisComponent)\n')
                code += ('\n')

                ######################### IMAGE AND DRAW COMMAND DLF FILE WRITING
                code += ('    for thisComponent in componentsForDVDrawingList:\n')
                code += ('        if not dlf_file.closed:\n')
                code += ('            # If it is an image component then send an image loading message\n')
                code += ('            if thisComponent.componentType == "Image":\n')
                code += ("                dlf_file.write('%i IMGLOAD CENTER ../../%s %i %i %i %i\\n' % \n")
                code += ('                    (int(round((zeroTimeDLF - currentFrameTime)*1000)),\n')
                code += ('                   thisComponent.image,thisComponent.elPos[0],\n')
                code += ('                    thisComponent.elPos[1],thisComponent.elSize[0],thisComponent.elSize[1]))\n')
                code += ('            # If it is a sound component then skip the stimulus drawing message\n')
                code += ('            elif thisComponent.componentType == "sound" or thisComponent.componentType == "MovieStim3" or thisComponent.componentType == "MovieStimWithFrameNum":\n')
                code += ('                pass\n')
                code += ('            # If it is any other non-movie visual stimulus component then send\n')
                code += ("            # a draw command to provide a placeholder box in Data Viewer's Trial View window\n")
                code += ('            else:\n')
                code += ("                dlf_file.write('%i DRAWBOX 255 0 0 %i %i %i %i\\n' % \n")
                code += ('                    (int(round((zeroTimeDLF - currentFrameTime)*1000)),\n')
                code += ('                    thisComponent.elPos[0]-thisComponent.elSize[0]/2,\n')
                code += ('                    thisComponent.elPos[1]-thisComponent.elSize[1]/2,\n')
                code += ('                    thisComponent.elPos[0]+thisComponent.elSize[0]/2,\n')
                code += ('                    thisComponent.elPos[1]+thisComponent.elSize[1]/2))\n')

            ######################### DLF FILE WRITING
            if self.params['sendVideoFrameMessages'] == True:
                code += ('\n')
                code += ('    # Send movie frame event messages and video frame draw messages for Data Viewer\n')
                code += ('    # integration.  # See the Data Viewer User Manual, section\n')
                code += ('    # Protocol for EyeLink Data to Viewer Integration -> Video Commands\n')
                code += ('    for thisComponent in componentsForEyeLinkMovieFrameMarking:\n')
                code += ('        sendFrameMessage = 0\n')
                code += ('        #Check whether the movie playback has begun yet\n')
                code += ('        if thisComponent.tStartRefresh is not None:\n')
                code += ('            # Check the movie class type to identify the frame identifier\n')
                code += ('            # MovieStim3 does not provide the frame index, so we need to determine\n')
                code += ('            # it manually based on the value of the current frame time\n')
                code += ('            if thisComponent.componentType == "MovieStim3":\n')
                code += ('                # MovieStim3 does not report the frame number or index, but does provide the \n')
                code += ('                # frame onset time for the current frame. We can use this to identify each\n')
                code += ('                # frame increase\n')
                code += ('                vidFrameTime = thisComponent.getCurrentFrameTime()\n')
                code += ('                # Wait until the video has begun and define frame_index\n')
                code += ('                if not thisComponent.firstFramePresented:\n')
                code += ('                    # reset frame_index to 0\n')
                code += ('                    thisComponent.elMarkingFrameIndex = 0\n')
                code += ('                    # log that we will have sent the video onset marking message\n')
                code += ('                    # for future iterations/frames\n')
                code += ('                    thisComponent.firstFramePresented = True\n')
                code += ('                    # log that we need to send a message marking the current frame onset\n')
                code += ('                    sendFrameMessage = 1\n')
                code += ('                # check whether we have started playback and are on a new frame and if \n')
                code += ('                # so then update our variables\n')
                code += ('                if thisComponent.elMarkingFrameIndex >= 0 and vidFrameTime > thisComponent.previousFrameTime:\n')
                code += ('                    thisComponent.elMarkingFrameIndex = thisComponent.elMarkingFrameIndex + 1\n')
                code += ('                    sendFrameMessage = 1\n')
                code += ('                    thisComponent.previousFrameTime = vidFrameTime\n')
                code += ('            # else if we are using a movie stim class that provides the current\n')
                code += ('            # frame number then we can grab the frame number directly\n')
                code += ('            else:\n')
                code += ('                # Other movie players have access to the frame number\n')
                code += ('                frameNum = thisComponent.getCurrentFrameNumber()\n')
                code += ('                vidFrameTime = currentFrameTime\n')
                code += ('                # If we have a new frame then update the frame number and log\n')
                code += ('                # that we need to send a frame-marking message\n')
                code += ('                if frameNum >= 0 and frameNum is not thisComponent.elMarkingFrameIndex:\n')
                code += ('                    thisComponent.elMarkingFrameIndex = frameNum\n')
                code += ('                    sendFrameMessage = 1\n')
                code += ('            # If we need to mark a frame onset, then with the above frame_index and \n')
                code += ('            # currentTime variables defined, update the times, frame level messages and \n')
                code += ('            # interest are information\n')
                code += ('            if sendFrameMessage == 1:\n')
                code += ('                # send a message to mark the onset of each frame\n')
                code += ("                el_tracker.sendMessage('%s %s_Frame %d' % (int(round((globalClock.getTime()-vidFrameTime)*1000)),thisComponent.name,thisComponent.elMarkingFrameIndex))\n")
                code += ('                # Write a VFRAME message to mark the onset of each frame\n')
                code += ('                # Format: VFRAME frame_num pos_x, pos_y, path_to_file\n')
                code += ('                # See the Data Viewer User Manual, section:\n')
                code += ('                # Protocol for EyeLink Data to Viewer Integration -> Video Commands\n')
                code += ('                if not dlf_file.closed:\n')
                code += ('                    if thisComponent.componentType == "MovieStim3":\n')
                code += ('                        vidFrameTime = currentFrameTime\n')             
                code += ("                        dlf_file.write('%i VFRAME %d %d %d ../../%s\\n' % (int(round((zeroTimeDLF - vidFrameTime)*1000+3)),\n")
                code += ('                            thisComponent.elMarkingFrameIndex,\n')
                code += ('                            int(round(thisComponent.elPos[0]-thisComponent.elSize[0]/2.0)),\n')
                code += ('                            int(round(thisComponent.elPos[1]-thisComponent.elSize[1]/2.0)),\n')
                code += ('                            thisComponent.filename))\n')
                code += ('                    else:\n')
                code += ("                        dlf_file.write('%i VFRAME %d %d %d ../../%s\\n' % (int(round((zeroTimeDLF - vidFrameTime)*1000+3)),\n")
                code += ('                            thisComponent.elMarkingFrameIndex,\n')
                code += ('                            int(round(thisComponent.elPos[0]-thisComponent.elSize[0]/2.0)),\n')
                code += ('                            int(round(thisComponent.elPos[1]-thisComponent.elSize[1]/2.0)),\n')
                code += ('                            thisComponent.filename))\n')
                code += ("                # Log that we don't need to send a new frame message again\n")
                code += ('                # until a new frame is actually drawn/detected\n')
                code += ('                sendFrameMessage = 0\n')
            code += ('    # This logs whether a call to this method has already been scheduled for the upcoming retrace\n')
            code += ('    # And is used to help ensure we schedule only one callOnFlip call for each retrace\n')
            code += ('    eyelinkThisFrameCallOnFlipScheduled = False\n')
            code += ('    # This stores the time of the last retrace and can be used in Code components to \n')
            code += ('    # check the time of the previous screen flip\n')
            code += ('    eyelinkLastFlipTime = float(currentFrameTime)\n')
            buff.writeOnceIndentedLines(code)

######### ROUTINE START CODE

    def writeRoutineStartCode(self, buff):

        ############ MAKE LIST OF VARIABLES, STIM COMPONENTS, DV DRAWING, DV INTEREST AREAS, DV TARGET POS, and RESPONSE COMPONENTS
        ############ TO MONITOR
        trialVariablesForLogging = self.params['trialConditionVariablesForEyeLinkLogging'].val.replace(" ","").strip('[]')
        trialVariableNamesForLogging = trialVariablesForLogging.split(',')

        code = ('# This section of EyeLink %s component code initializes some variables that will help with\n' % self.params['name'].val)
        code += ('# sending event marking messages, logging Data Viewer (DV) stimulus drawing info, logging DV interest area info,\n')
        code += ('# sending DV Target Position Messages, and/or logging DV video frame marking info\n')
        code += ('# information\n')
        code += ('\n')
        if self.params["sendTrialOnsetOffsetMessages"].val == True:
            code += ('# When we  have multiple trials within one continuous recording we should send a \n')
            code += ('# new TRIALID (for all trials after the first trial of the recording; the first \n')
            code += ("# trial's TRIALID message is sent before recording begins)\n")
            code += ('if trial_index > trialIDAtRecordingStart:\n')
            code += ("    el_tracker.sendMessage('TRIALID %d' % trial_index)\n")
        code += ('\n')
        if len(trialVariablesForLogging) > 0:
            code += ("# log trial variables' values to the EDF data file, for details, see Data\n")
            code += ('# Viewer User Manual, "Protocol for EyeLink Data to Viewer Integration"\n')
            code += ('trialConditionVariablesForEyeLinkLogging = [%s]\n' % trialVariablesForLogging)
            code += ('trialConditionVariableNamesForEyeLinkLogging = %s\n' % trialVariableNamesForLogging)
            code += ('for i in range(len(trialConditionVariablesForEyeLinkLogging)):\n')
            code += ("    el_tracker.sendMessage('!V TRIAL_VAR %s %s'% (trialConditionVariableNamesForEyeLinkLogging[i],trialConditionVariablesForEyeLinkLogging[i]))\n")
            code += ('    #add a brief pause after every 5 messages or so to make sure no messages are missed\n')
            code += ('    if i % 5 == 0:\n')
            code += ('        time.sleep(0.001)\n')
            code += ('\n')
        if len(self.componentsForStimEventMarking) > 0:
            code += ('# list of all stimulus components whose onset/offset will be marked with messages\n')
            code += ('componentsForEyeLinkStimEventMessages = [%s]\n' % self.componentsForStimEventMarking)
        if len(self.componentsForDVDrawingMessages) > 0:
            code += ('# list of all stimulus components for which Data Viewer draw commands will be sent\n')
            code += ('componentsForEyeLinkStimDVDrawingMessages = [%s]\n' % self.componentsForDVDrawingMessages)
        if len(self.componentsForIAMessages) > 0:
            code += ('# list of all stimulus components which will have interest areas automatically created for them\n')
            code += ('componentsForEyeLinkInterestAreaMessages = [%s]\n' % self.componentsForIAMessages)
        if len(self.componentsForTargPosMessages) > 0:
            code += ('# list of all stimulus components which will have their ongoing positions marked with target position messages\n')
            code += ('componentsForEyeLinkTargetPositionMessages = [%s]\n' % self.componentsForTargPosMessages)

        code += ('# create list of all components to be monitored for EyeLink Marking/Messaging\n')
        code += ('allStimComponentsForEyeLinkMonitoring = ')
        if len(self.componentsForStimEventMarking) > 0:
            code += ('componentsForEyeLinkStimEventMessages + ')
        if len(self.componentsForDVDrawingMessages) > 0:
            code += ('componentsForEyeLinkStimDVDrawingMessages + ')
        if len(self.componentsForIAMessages) > 0:
            code += ('componentsForEyeLinkInterestAreaMessages + ')
        if len(self.componentsForTargPosMessages) > 0:
            code += ('componentsForEyeLinkTargetPositionMessages + ')
        code = code.rstrip(' + ')
        code += ('# make sure each component is only in the list once\n')
        code += ('allStimComponentsForEyeLinkMonitoring = [*set(allStimComponentsForEyeLinkMonitoring)]\n')
        if self.params["sendVideoFrameMessages"].val == True:
            code += ('# list of all movie components whose individual frame onsets need to be marked\n')
            code += ('componentsForEyeLinkMovieFrameMarking = []\n')
        code += ('# list of all response components whose onsets need to be marked and values\n')
        code += ('# need to be logged\n')
        if len(self.componentsForRespEventMarking) > 0:
            code += ('componentsForEyeLinkRespEventMessages = [%s]\n' % self.componentsForRespEventMarking)
        code += ('\n')

        ##### STIM COMPONENT INITIALIZATION    
        if len(self.componentsForStimEventMarking) > 0 or len(self.componentsForDVDrawingMessages) > 0 or \
            len(self.componentsForIAMessages) > 0 or len(self.componentsForTargPosMessages) > 0:
            code += ('# Initialize stimulus components whose occurence needs to be monitored for event\n')
            code += ('# marking, Data Viewer integration, and/or interest area messaging\n')
            code += ('# to the EDF (provided they are supported stimulus types)\n')
            code += ('for thisComponent in allStimComponentsForEyeLinkMonitoring:\n')
            code += ('    componentClassString = str(thisComponent.__class__)\n')
            code += ('    supportedStimType = False\n')
            code += ('    for stimType in ["Aperture","Text","Dot","Shape","Rect","Grating","Image","MovieStim3","Movie","sound"]:\n')
            code += ('        if stimType in componentClassString:\n')
            code += ('            supportedStimType = True\n')
            code += ('            thisComponent.elOnsetDetected = False\n')
            code += ('            thisComponent.elOffsetDetected = False\n')
            if len(self.componentsForIAMessages) > 0:
                code += ('            if thisComponent in componentsForEyeLinkInterestAreaMessages:\n')    
                code += ('                thisComponent.iaInstanceStartTime = -1\n')
                code += ('                thisComponent.iaIndex = componentsForEyeLinkInterestAreaMessages.index(thisComponent) + 1\n')
            code += ('            if stimType != "sound":\n')
            code += ('                thisComponent.elPos = eyelink_pos(thisComponent.pos,[scn_width,scn_height],thisComponent.units)\n')
            code += ('                thisComponent.elSize = eyelink_size(thisComponent.size,[scn_width,scn_height],thisComponent.units)\n')      
            code += ('                thisComponent.lastelPos = thisComponent.elPos\n')
            code += ('                thisComponent.lastelSize = thisComponent.elSize\n')            
            if len(self.componentsForTargPosMessages) > 0:
                code += ('                if thisComponent in componentsForEyeLinkTargetPositionMessages:\n') 
                code += ('                    thisComponent.targLabel = "Targ" + str(componentsForEyeLinkTargetPositionMessages.index(thisComponent) + 1)\n')   
            code += ('            if stimType == "MovieStim3":\n')
            code += ('                thisComponent.componentType = "MovieStim3"\n')
            code += ('                thisComponent.elMarkingFrameIndex = -1\n')
            code += ('                thisComponent.previousFrameTime = 0\n')
            code += ('                thisComponent.firstFramePresented = False\n')
            if self.params["sendVideoFrameMessages"].val == True:
                code += ('                componentsForEyeLinkMovieFrameMarking.append(thisComponent)   \n')
            code += ('            elif stimType == "Movie":\n')
            code += ('                thisComponent.componentType = "MovieStimWithFrameNum"\n')
            code += ('                thisComponent.elMarkingFrameIndex = -1\n')
            code += ('                thisComponent.firstFramePresented = False\n')
            if self.params["sendVideoFrameMessages"].val == True:
                code += ('                componentsForEyeLinkMovieFrameMarking.append(thisComponent)\n')
            code += ('            else:\n')
            code += ('                thisComponent.componentType = stimType\n')
            code += ('            break   \n')
            code += ('    if not supportedStimType:\n')
            code += ('        print("WARNING:  Stimulus component type " + str(thisComponent.__class__) + " not supported for EyeLink event marking")\n')
            code += ('        print("          Event timing messages and/or Data Viewer drawing messages")\n')
            code += ('        print("          will not be marked for this component")\n')
            code += ('        print("          Consider marking the component via code component")\n')
            code += ('        # remove unsupported types from our monitoring lists\n')
            code += ('        allStimComponentsForEyeLinkMonitoring.remove(thisComponent)\n')
            code += ('        componentsForEyeLinkStimEventMessages.remove(thisComponent)\n')
            code += ('        componentsForEyeLinkStimDVDrawingMessages.remove(thisComponent)\n')
            code += ('        componentsForEyeLinkInterestAreaMessages.remove(thisComponent)\n')
            code += ('\n')
            if len(self.componentsForIAMessages) > 0:
                code += ('# Set Interest Area Margin -- this value will be added to all four edges of the components\n')
                code += ('# for which interest areas will be created\n')
                code += ('interestAreaMargins = %s\n' % self.params['interestAreaMargins'].val)
                code += ('\n')
        if len(self.componentsForRespEventMarking) > 0:
            code += ('# Initialize response components whose occurence needs to be marked with \n')
            code += ('# a message to the EDF (provided they are supported stimulus types)\n')
            code += ('# Supported types include mouse, keyboard, and any response component with an RT or time property\n')
            code += ('for thisComponent in componentsForEyeLinkRespEventMessages:\n')
            code += ('    componentClassString = str(thisComponent.__class__)\n')
            code += ('    componentClassDir = dir(thisComponent)\n')
            code += ('    supportedRespType = False\n')
            code += ('    for respType in ["Mouse","Keyboard"]:\n')
            code += ('        if respType in componentClassString:\n')
            code += ('            thisComponent.componentType = respType\n')
            code += ('            supportedRespType = True\n')
            code += ('            break\n')
            code += ('    if not supportedRespType:\n')
            code += ('        if "rt" in componentClassDir:\n')
            code += ('            thisComponent.componentType = "OtherRespWithRT"\n')
            code += ('            supportedRespType = True\n')
            code += ('        elif "time" in componentClassDir:\n')
            code += ('            thisComponent.componentType = "OtherRespWithTime"\n')
            code += ('            supportedRespType = True\n')
            code += ('    if not supportedRespType:    \n')
            code += ('            print("WARNING:  Response component type " + str(thisComponent.__class__) + " not supported for EyeLink event marking")\n')
            code += ('            print("          Event timing will not be marked for this component")\n')
            code += ('            print("          Please consider marking the component via code component")\n')
            code += ('            # remove unsupported response types\n')
            code += ('            componentsForEyeLinkRespEventMessages.remove(thisComponent)\n')
            code += ('\n')
        if len(self.componentsForDVDrawingMessages) > 0:
            code += ('# Open a draw list file (DLF) to which Data Viewer drawing information will be logged\n')
            code += ('# The commands that will be written to this DLF file will enable\n')
            code += ('# Data Viewer to reproduce the stimuli in its Trial View window\n')
            code += ('sentDrawListMessage = False\n')
            code += ('# create a folder for the current testing session in the "results" folder\n')
            code += ('drawList_folder = os.path.join(results_folder, session_identifier,"graphics")\n')
            code += ('if not os.path.exists(drawList_folder):\n')
            code += ('    os.makedirs(drawList_folder)\n')
            code += ('# open a DRAW LIST file to save the frame timing info for the video, which will\n')
            code += ("# help us to be able to see the video in Data Viewer's Trial View window\n")
            code += ('# See the Data Viewer User Manual section:\n')
            code += ('# "Procotol for EyeLink Data to Viewer Integration -> Simple Drawing Commands"\n')
            code += ("dlf = 'TRIAL_%04d_ROUTINE_%02d.dlf' % (trial_index,routine_index)\n")
            code += ("dlf_file = open(os.path.join(drawList_folder, dlf), 'w')\n")
            code += ('\n')
        if len(self.componentsForIAMessages) > 0:
            code += ('# Open an Interest Area Set (IAS) file to which interest area information will be logged\n')
            code += ('# Interest Areas will appear in Data Viewer and assist with analysis\n')
            code += ('# See the Data Viewer User Manual section: \n')
            code += ('# "Procotol for EyeLink Data to Viewer Integration -> Interest Area Commands"\n')
            code += ('sentIASFileMessage = False\n')
            code += ('interestAreaSet_folder = os.path.join(results_folder, session_identifier,"aoi")\n')
            code += ('if not os.path.exists(interestAreaSet_folder):\n')
            code += ('    os.makedirs(interestAreaSet_folder)\n')
            code += ('# open the IAS file to save the interest area info for the stimuli\n')
            code += ("ias = 'TRIAL_%04d_ROUTINE_%02d.ias' % (trial_index,routine_index)\n")
            code += ("ias_file = open(os.path.join(interestAreaSet_folder, ias), 'w')\n")
            
        if len(self.componentsForDVDrawingMessages) > 0 or len(self.componentsForIAMessages) > 0:
            code += ('# Update a routine index for EyeLink IAS/DLF file logging -- \n')
            code += ('# Each routine will have its own set of IAS/DLF files, as each will have its own  Mark Events component\n')
            code += ('routine_index = routine_index + 1\n')
        code += ('# Send a Data Viewer clear screen command to clear its Trial View window\n')
        code += ('# to the window color\n')
        code += ("el_tracker.sendMessage('!V CLEAR %d %d %d' % eyelink_color(win.color))\n")

        if self.params["useQuitKeys"].val == True:
            code += ('# create a keyboard instance and reinitialize a kePressNameList, which\n')
            code += ('# will store list of key names currently being pressed (to allow Ctrl-C abort)\n')
            code += ('kb = keyboard.Keyboard()\n')
            code += ('keyPressNameList = []\n')
        code += ('eyelinkThisFrameCallOnFlipScheduled = False\n')
        code += ('eyelinkLastFlipTime = 0.0\n')
        if self.params['sendTrialOnsetOffsetMessages'].val == False:
            code += ('routineTimer.reset()\n')
        buff.writeOnceIndentedLines(code)


######### EACH FRAME CODE

    def writeFrameCode(self, buff):
        code = ('# This section of EyeLink %s component code checks whether to send (and sends/logs when appropriate)\n' % self.params['name'].val)
        code += ('# event marking messages, log Data Viewer (DV) stimulus drawing info, log DV interest area info,\n')
        code += ('# send DV Target Position Messages, and/or log DV video frame marking info\n')
        
        # if any of the variables actually have components in them then create the function.  Otherwise skip this
        if len(self.componentsForStimEventMarking) > 0 or len(self.componentsForDVDrawingMessages) > 0 or \
            len(self.componentsForIAMessages) > 0 or len(self.componentsForTargPosMessages) > 0:
   
            code += ('if not eyelinkThisFrameCallOnFlipScheduled:\n')
            code += ('    # This method, created by the EyeLink %s component code will get called to handle\n' % self.params['name'].val)
            code += ('    # sending event marking messages, logging Data Viewer (DV) stimulus drawing info, logging DV interest area info,\n')
            code += ('    # sending DV Target Position Messages, and/or logging DV video frame marking info=information\n')
            code += ('    win.callOnFlip(eyelink_onFlip_%s,globalClock,win,scn_width,scn_height,allStimComponentsForEyeLinkMonitoring,\\\n' % self.params['name'].val)
            if len(self.componentsForStimEventMarking) > 0:   
                code += ('        componentsForEyeLinkStimEventMessages,\\\n')
            if len(self.componentsForDVDrawingMessages) > 0:
                code += ('        componentsForEyeLinkStimDVDrawingMessages,dlf,dlf_file,\\\n')
            if len(self.componentsForIAMessages) > 0:
                code += ('        componentsForEyeLinkInterestAreaMessages,ias,ias_file,interestAreaMargins,\\\n')
            if len(self.componentsForTargPosMessages) > 0:
                code += ('        componentsForEyeLinkTargetPositionMessages,\\\n')
            if self.params['sendVideoFrameMessages'].val == True:
                code += ('    componentsForEyeLinkMovieFrameMarking')
            code = code.rstrip('\n')
            code = code.rstrip('\\')
            code = code.rstrip(',')
            code += (')\n')
            code += ('    eyelinkThisFrameCallOnFlipScheduled = True\n')

        code += ('\n')
        code += ('# abort the current trial if the tracker is no longer recording\n')
        code += ('error = el_tracker.isRecording()\n')
        code += ('if error is not pylink.TRIAL_OK:\n')
        code += ("    el_tracker.sendMessage('tracker_disconnected')\n")
        code += ('    abort_trial(win,genv)\n')
        code += ('\n')

        if self.params["useQuitKeys"].val == True:
            code += ('# check keyboard events for experiment abort key combination\n')
            code += ("keyPressList = kb.getKeys(keyList = ['lctrl','rctrl','c'], waitRelease = False, clear = False)\n")
            code += ('for keyPress in keyPressList:\n')
            code += ('    keyPressName = keyPress.name\n')
            code += ('    if keyPressName not in keyPressNameList:\n')
            code += ('        keyPressNameList.append(keyPress.name)\n')     
            code += ("if ('lctrl' in keyPressNameList or 'rctrl' in keyPressNameList) and 'c' in keyPressNameList:\n")
            code += ("    el_tracker.sendMessage('terminated_by_user')\n")
            code += ('    terminate_task(win,genv,edf_file,session_folder,session_identifier)\n')
            code += ('#check for key releases\n')
            code += ("keyReleaseList = kb.getKeys(keyList = ['lctrl','rctrl','c'], waitRelease = True, clear = False)\n")
            code += ('for keyRelease in keyReleaseList:\n')
            code += ('    keyReleaseName = keyRelease.name\n')
            code += ('    if keyReleaseName in keyPressNameList:\n')
            code += ('        keyPressNameList.remove(keyReleaseName)\n')
            
        buff.writeOnceIndentedLines(code)  

    def writeRoutineEndCode(self,buff):
        code = ('\n')
        if len(self.componentsForStimEventMarking) > 0 or len(self.componentsForRespEventMarking) > 0 or len(self.componentsForIAMessages) > 0 \
            or len(self.componentsForDVDrawingMessages) > 0:
            code += ('# This section of EyeLink %s component code does some event cleanup at the end of the routine\n' % self.params['name'].val)

#########################   END ROUTINE OFFSET STIM MARKING
        if len(self.componentsForStimEventMarking) > 0:
            code += ('# Go through all stimulus components that need to be checked for event marking,\n')
            code += ('#  to see if the trial ended before PsychoPy reported OFFSET detection to mark their offset from trial end\n')
            code += ('for thisComponent in componentsForEyeLinkStimEventMessages:\n')
            code += ('    if thisComponent.elOnsetDetected and not thisComponent.elOffsetDetected:\n')
            code += ('        # Check if the component had onset but the trial ended before offset\n')
            code += ("        el_tracker.sendMessage('%s_OFFSET' % (thisComponent.name))\n")
            # commented out to fix IA issue (sometimes IA was missing if response component event ended trial)
            #code += ("         thisComponent.elOffsetDetected = True\n")

        if len(self.componentsForRespEventMarking) > 0:
            code += ('# Go through all response components whose occurence/data\n')
            code += ('# need to be logged to the EDF and marks their occurence with a message (using an offset calculation that backstam\n')
            code += ('for thisComponent in componentsForEyeLinkRespEventMessages:\n')
            code += ('    if thisComponent.componentType == "Keyboard" or thisComponent.componentType == "OtherRespWithRT":\n')
            code += ('        if not isinstance(thisComponent.rt,list):\n')
            code += ('            offsetValue = int(round((globalClock.getTime() - \\\n')
            code += ('                (thisComponent.tStartRefresh + thisComponent.rt))*1000))\n')
            code += ("            el_tracker.sendMessage('%i %s_EVENT' % (offsetValue,thisComponent.componentType,))\n")
            code += ('            # if sending many messages in a row, add a 1 msec pause between after\n')
            code += ('            # every 5 messages or so\n')
            code += ('        if isinstance(thisComponent.rt,list) and len(thisComponent.rt) > 0:\n')
            code += ('            for i in range(len(thisComponent.rt)):\n')
            code += ('                offsetValue = int(round((globalClock.getTime() - \\\n')
            code += ('                    (thisComponent.tStartRefresh + thisComponent.rt[i]))*1000))\n')
            code += ("                el_tracker.sendMessage('%i %s_EVENT_%i' % (offsetValue,thisComponent.componentType,i+1))\n")
            code += ('                if i % 4 == 0:\n')
            code += ('                    # if sending many messages in a row, add a 1 msec pause between after \n')
            code += ('                    # every 5 messages or so\n')
            code += ('                    time.sleep(0.001)\n')
            code += ("        el_tracker.sendMessage('!V TRIAL_VAR %s.rt(s) %s' % (thisComponent.componentType,thisComponent.rt))\n")
            code += ('        if "corr" in dir(thisComponent):\n')
            code += ("            el_tracker.sendMessage('!V TRIAL_VAR %s.corr %s' % (thisComponent.componentType,thisComponent.corr))\n")
            code += ('        if "keys" in dir(thisComponent):\n')
            code += ("            el_tracker.sendMessage('!V TRIAL_VAR %s.keys %s' % (thisComponent.componentType,thisComponent.keys))\n")
            code += ('    elif thisComponent.componentType == "Mouse" or thisComponent.componentType == "OtherRespWithTime":\n')
            code += ('        if not isinstance(thisComponent.time,list):\n')
            code += ('            offsetValue = int(round((globalClock.getTime() - \\\n')
            code += ('                (thisComponent.tStartRefresh + thisComponent.time))*1000))\n')
            code += ("            el_tracker.sendMessage('%i %s_EVENT' % (thisComponent.componentType,offsetValue))\n")
            code += ('            # if sending many messages in a row, add a 1 msec pause between after \n')
            code += ('            # every 5 messages or so\n')
            code += ('            time.sleep(0.0005)\n')
            code += ('        if isinstance(thisComponent.time,list) and len(thisComponent.time) > 0:\n')
            code += ('            for i in range(len(thisComponent.time)):\n')
            code += ('                offsetValue = int(round((globalClock.getTime() - \\\n')
            code += ('                    (thisComponent.tStartRefresh + thisComponent.time[i]))*1000))\n')
            code += ("                el_tracker.sendMessage('%i %s_EVENT_%i' % (offsetValue,thisComponent.componentType,i+1))\n")
            code += ('                if i % 4 == 0:\n')
            code += ('                    # if sending many messages in a row, add a 1 msec pause between after \n')
            code += ('                    # every 5 messages or so\n')
            code += ('                    time.sleep(0.001)\n')
            code += ("        el_tracker.sendMessage('!V TRIAL_VAR %s.time(s) %s' % (thisComponent.componentType,thisComponent.time))\n")
            code += ('    time.sleep(0.001)\n')            
            code += ('\n')
            
        if len(self.componentsForIAMessages) > 0:
            code += ('# log any remaining interest area commands to the IAS file for stimuli that \n')
            code += ('# were still being presented when the routine ended\n')
            code += ('for thisComponent in componentsForEyeLinkInterestAreaMessages:\n')
            code += ('    if not thisComponent.elOffsetDetected and thisComponent.tStartRefresh is not None:\n')

            if self.params['interestAreaShape'].val == 'Rectangle':
                shapeText = 'RECTANGLE'
            elif self.params['interestAreaShape'].val == 'Ellipse':
                shapeText = 'ELLIPSE'
            if self.params['interestAreaMargins'].val.isdigit():        
                code += ("        ias_file.write('%i %i IAREA %s %i %i %i %i %i %s\\n' % \\\n")
                code += ('            (int(round((zeroTimeIAS - thisComponent.iaInstanceStartTime)*1000)),\n')
                code += ('            int(round((zeroTimeIAS - globalClock.getTime())*1000 - 1)),"%s",thisComponent.iaIndex,\n' % shapeText)
                code += ('            thisComponent.elPos[0]-(thisComponent.elSize[0]/2+interestAreaMargins),\n')
                code += ('            thisComponent.elPos[1]-(thisComponent.elSize[1]/2+interestAreaMargins),\n')
                code += ('            thisComponent.elPos[0]+(thisComponent.elSize[0]/2+interestAreaMargins),\n')
                code += ('            thisComponent.elPos[1]+(thisComponent.elSize[1]/2+interestAreaMargins),thisComponent.name))\n')
            else:
                code += ("        ias_file.write('%i %i IAREA %s %i %i %i %i %i %s\\n' % \\\n")
                code += ('            (int(round((zeroTimeIAS - thisComponent.iaInstanceStartTime)*1000)),\n')
                code += ('            int(round((zeroTimeIAS - globalClock.getTime())*1000 - 1)),"%s",thisComponent.iaIndex,\n' % shapeText)
                code += ('            thisComponent.elPos[0]-thisComponent.elSize[0]/2,\n')
                code += ('            thisComponent.elPos[1]-thisComponent.elSize[1]/2,\n')
                code += ('            thisComponent.elPos[0]+thisComponent.elSize[0]/2,\n')
                code += ('            thisComponent.elPos[1]+thisComponent.elSize[1]/2,thisComponent.name))\n')
            code += ('# Close the interest area set file and draw list file for the trial\n')
            code += ('ias_file.close()\n')
        
        if len(self.componentsForDVDrawingMessages) > 0:
            code += ('# close the drawlist file (which is used in Data Viewer stimulus presntation re-creation)\n')
            code += ('dlf_file.close()\n')
            code += ('\n')       
        if self.params["sendTrialOnsetOffsetMessages"].val == True:
            code += ('# Mark the end of the trial for Data Viewer trial parsing\n')
            code += ('el_tracker.sendMessage("TRIAL_RESULT 0")\n')
            code += ('# Update the EyeLink trial counter\n')
            code += ('trial_index = trial_index + 1\n')

        buff.writeOnceIndentedLines(code)
