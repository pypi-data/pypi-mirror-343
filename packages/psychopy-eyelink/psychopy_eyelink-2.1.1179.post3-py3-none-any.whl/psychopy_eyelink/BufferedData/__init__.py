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
_localized.update({'eventDataTypesToInclude':_translate('Event Data Types to Include'),
                   'localEventListsMaxLength':_translate('Maximum Local Event List Length'),
                   'includeSampleData':_translate('Include Sample Data'),
                   'localSampleListMaxLength':_translate('Maximum Local Sample List Length'),
                   'includeSpannedEvents':_translate('Include Spanned End Events')
                   })


class BufferedData(BaseComponent):
    """An event class for accessing buffered EyeLink data across the
    link from the Host PC

    Further details on the data available can be found in the 
    EyeLink Programmers Guide, and on the SR Research Support Forum.
    """
    categories = ['Eyetracking']  # which section(s) in the components panel
    targets = ['PsychoPy']
    iconFile = Path(__file__).parent / 'BufferedData.png'
    tooltip = _translate('Provides buffered EyeLink event data')
    plugin = "psychopy-eyelink"

    def __init__(self, exp, parentName, name='BufferedData', startType='time (s)', startVal='0.0', stopVal='3.0',
                 stopType='duration (s)', eventDataTypesToInclude = '', localEventListsMaxLength = '100', includeSampleData = False, includeSpannedEvents = False,
                 localSampleListMaxLength = 5000):

        super(BufferedData, self).__init__(
            exp, parentName, name, startType=startType, startVal=startVal,
            stopType=stopType, stopVal=stopVal
            )

        self.type = 'BufferedData'
        self.url = "https://www.sr-research.com/support/thread-7525.html"
        # update this URL to a component specific page on anm HTML manual
                 
        self.params['eventDataTypesToInclude'] = Param(
            eventDataTypesToInclude, categ='Basic',
            valType='str', inputType="single",
            hint=_translate('Event Data Types to Include - include any of the following, separated by commas:\n'
                            'STARTBLINK -- start of blink events\n'
                            'ENDBLINK -- end of blink events\n'
                            'STARTSACC -- start of saccade events\n'
                            'ENDSACC -- end of saccade events\n'
                            'STARTFIX -- start of fixation events\n'
                            'ENDFIX -- end of fixations\n'
                            'FIXUPDATE -- fixation update events\n'
                            'MESSAGEEVENT -- message events\n'
                            'BUTTONEVENT -- button events\n'
                            'INPUTEVENT -- input events\n'
                            'These events will be saved in a variable of the component which will be called EVENTNAME_LIST,\n'
                            'e.g., BufferedData.ENDSACC_LIST will be the list of end saccade events for a component named BufferedData'),
            label=_localized['eventDataTypesToInclude'])
        
        self.params['localEventListsMaxLength'] = Param(
            localEventListsMaxLength, categ='Basic',
            valType='str', inputType="single",
            hint=_translate('Maximum number of events to be stored in local PsychoPy list for each event data type'),
            label=_localized['localEventListsMaxLength'])
        
        self.params['includeSpannedEvents'] = Param(
            includeSpannedEvents, categ='Basic',
            valType='bool', inputType="bool",
            hint=_translate('Include end eye events for events that span the start/stop time of the component:\n'
                            'If unchecked, then the component will not include 1) end saccade, end fixation, and end blink events\n'
                            "that occur between the component's start/stop times but whose start was before the component's\n"
                            "start time and 2) end saccade, end fixation, and end blink events that occur after the component's\n"
                            "stop time but whose start time was between the component's start/stop times.\n"
                            "If checked then those events will be included."),
            label=_localized['includeSpannedEvents'])
        
        self.params['includeSampleData'] = Param(
            includeSampleData, categ='Basic',
            valType='bool', inputType="bool",
            hint=_translate('Whether to retrieve sample data from the EyeLink link data buffer'),
            label=_localized['includeSampleData'])
        
        self.params['localSampleListMaxLength'] = Param(
            localSampleListMaxLength, categ='Basic',
            valType='str', inputType="single",
            hint=_translate('Maximum number of samples to be stored in local PsychoPy list'),
            label=_localized['localSampleListMaxLength'])

        self.depends.append(
            {'dependsOn':'includeSampleData',
             'condition':'==True',
             'param':'localSampleListMaxLength',
             'true':'show',
             'false':'hide'})       

    def writeInitCode(self,buff):
        code = ("%(name)s = event.Mouse(win=win)\n")
        buff.writeIndentedLines(code % self.params)
 
    def writeRoutineStartCode(self,buff):

        code = ('# This section of EyeLink %s component code resets some variables \n' % self.params['name'].val)
        code += ('# that log information about the data access period and creates LIST variables\n')
        code += ("# (stored within the component's data structure) that will store the buffered data for each type locally\n")
        code += ('# these keep track of whether the buffered data access period has started/stopped\n')
        code += ('%s.bufferedDataPeriodOnsetDetected = False\n' % self.params['name'].val)
        code += ('%s.bufferedDataPeriodOffsetDetected = False\n' % self.params['name'].val)

        if len(self.params['eventDataTypesToInclude'].val) > 0:
            eventDataTypesToInclude = self.params['eventDataTypesToInclude'].val.replace(" ","").split(',')
            self.eventDataTypesToMonitor = []
            for eventDataType in eventDataTypesToInclude:
                if eventDataType in ["STARTBLINK","ENDBLINK","STARTSACC","ENDSACC","STARTFIX","ENDFIX",
                                     "FIXUPDATE","MESSAGEEVENT","BUTTONEVENT","INPUTEVENT"]:
                    code += ('# %s.%s_LIST will store the EyeLink %s data\n' % (self.params['name'].val,eventDataType,eventDataType))
                    code += ('%s.%s_LIST = []\n' % (self.params['name'].val,eventDataType))
                    self.eventDataTypesToMonitor.append(eventDataType)
                else:
                    print("WARNING: Event data type %s not supported.  Will not attempt to access data for that type.")

        if self.params['includeSampleData'].val == True:
            code += ('# %s.SAMPLE_LIST list will store the EyeLink sample data\n' % self.params['name'].val)
            code += ('%s.SAMPLE_LIST = []\n' % self.params['name'].val)

        buff.writeOnceIndentedLines(code) 

    def writeFrameCode(self, buff):
        code = ('\n')
        code += ('# This section of EyeLink %s component code grabs data from the EyeLink buffer \n' % self.params['name'].val)
        code += ('# within its start/stop time speicifications, marks the access period with \n')
        code += ('# ONSET/OFFSET messages, and makes the link data available to the rest \n')
        code += ('# of the experiment via a list for each data type included/accessed.\n')
        code += ('# Checks whether it is the first frame of the data access period\n')
        code += ('if %s.status == NOT_STARTED and tThisFlip >= %s-frameTolerance and not %s.bufferedDataPeriodOnsetDetected:\n' \
                 % (self.params['name'].val,self.params['startVal'].val,self.params['name'].val))
        code += ('    # log the Host PC time when we start accessing eye data, send a message marking\n')
        code += ('    # the time when the data access period begins, and log some data about the start of the access period\n')
        code += ('    %s.startMonitoringTimeHostPC = pylink.getEYELINK().trackerTime()\n' % self.params['name'].val)
        code += ('    el_tracker.sendMessage("%s_ONSET")\n' % self.params['name'].val)
        code += ('    %s.tStartRefresh = tThisFlipGlobal\n' % self.params['name'].val)
        code += ('    %s.status = STARTED\n' % self.params['name'].val)
        code += ('    %s.bufferedDataPeriodOnsetDetected = True\n' % self.params['name'].val)
                # if fixation is stopping this frame...
        if len(self.params['stopVal'].val) > 0:       
            code += ('if %s.status == STARTED:\n' % self.params['name'].val)
            # is it time to stop? (based on global clock, using actual start)
            code += ('    # Checks whether it is the last frame of the EyeLink data access period\n')
            code += ('    if tThisFlipGlobal > %s.tStartRefresh + %s - frameTolerance:\n' % (self.params['name'].val,self.params['stopVal'].val))
            code += ('        # log the Host PC time when we stop accessing eye data, send a message marking\n')
            code += ('        # the time when the data access period ends, and log some data about the end of the access period\n')
            code += ('        %s.endMonitoringTimeHostPC = pylink.getEYELINK().trackerTime()\n' % self.params['name'].val)
            code += ('        el_tracker.sendMessage("%s_OFFSET")\n' % self.params['name'].val)
            code += ('        %s.bufferedDataPeriodOffsetDetected = True\n' % self.params['name'].val)
            code += ('        %s.status = FINISHED\n' % self.params['name'].val)
            code += ('\n')
        code += ('# grab the events in the buffer until we are caught up and no more data remains in the EyeLink buffer\n')
        code += ('while True:\n')
        code += ('    eventType = el_tracker.getNextData()\n')
        code += ('    if not eventType:\n')
        code += ('        break\n')
        code += ('    else:\n')
        # this variable helps us in writing the if/elif series (we used if if the var is true, elif if false)
        firstEventTypeToBeChecked = True
        for eventTypeToMonitor in self.eventDataTypesToMonitor:
            if firstEventTypeToBeChecked == True:
                code += ('        # Check whether the next data type in the EyeLink buffer matches one of the types we are monitoring\n')
                code += ('        if eventType == pylink.%s:\n' % eventTypeToMonitor)
                firstEventTypeToBeChecked = False
            else:    
                code += ('        elif eventType == pylink.%s:\n' % eventTypeToMonitor)
            code += ('            eventData = el_tracker.getFloatData()\n')
            code += ('            eventStartTime = eventData.getStartTime()\n')
            code += ('            includeEvent = False\n')
            if "END" in eventTypeToMonitor:
                code += ('            # Check the timing of the END event to see whether it should be added to the local LIST\n')
                code += ('            eventEndTime = eventData.getEndTime()\n')
                if self.params['includeSpannedEvents'].val == True:
                    code += ('            if %s.status == STARTED:\n' % self.params['name'].val)
                    code += ('                if eventStartTime >= %s.startMonitoringTimeHostPC:\n')
                    code += ('                    includeEvent = True\n')
                    code += ('				    elif %s.status == FINISHED:\n' % self.params['name'].val)
                    code += ('					    if eventEndTime <= %s.endMonitoringTimeHostPC and eventStartTime <= %s.endMonitoringTimeHostPC:\n' % (self.params['name'].val,self.params['name'].val))
                    code += ('						    includeEvent = True\n')
                else:
                    code += ('            if %s.status == STARTED:\n' % self.params['name'].val)
                    code += ('                if eventEndTime >= %s.startMonitoringTimeHostPC:\n' % self.params['name'].val)
                    code += ('                    includeEvent = True\n')
                    code += ('            elif %s.status == FINISHED:\n' % self.params['name'].val)
                    code += ('                if eventStartTime <= %s.endMonitoringTimeHostPC:\n' % self.params['name'].val)
                    code += ('                    includeEvent = True\n')
            else:
                code += ('            # Check the timing of the event to see whether it should be added to the local LIST\n')
                code += ('            if %s.status == STARTED:\n' % self.params['name'].val)
                code += ('                if eventStartTime >= %s.startMonitoringTimeHostPC:\n' % self.params['name'].val)
                code += ('                    includeEvent = True\n')
                code += ('            elif %s.status == FINISHED:\n' % self.params['name'].val)
                code += ('                if eventStartTime <= %s.endMonitoringTimeHostPC:\n' % self.params['name'].val)
                code += ('                    includeEvent = True\n')
            code += ('            # if the event should be included then add it to the local LIST:\n')   
            code += ('            if includeEvent:\n')
            code += ('                %s.%s_LIST.append(eventData)\n' % (self.params['name'].val,eventTypeToMonitor))
            code += ('                if len(%s.%s_LIST) > %s:\n' % (self.params['name'].val,eventTypeToMonitor,self.params['localEventListsMaxLength'].val))
            code += ('                    del %s.%s_LIST[0]\n' % (self.params['name'].val,eventTypeToMonitor))
        if self.params['includeSampleData'].val == True:
            code += ('        # Check for sample data -- if a new sample is found check its timing to see\n')
            code += ('        # whether it should be added to the local SAMPLE_LIST\n')
            if firstEventTypeToBeChecked:
                code += ('        if eventType == pylink.SAMPLE_TYPE:\n')
            else:
                code += ('        elif eventType == pylink.SAMPLE_TYPE:\n')
            code += ('            # grab the sample data and log it to the SAMPLE_LIST if we are within the EyeLink data access period\n')
            code += ('            sampleData = el_tracker.getFloatData()\n')
            code += ('            sampleTime = sampleData.getTime()\n')
            code += ('            includeSample = False\n')
            code += ('            if %s.status == STARTED:\n' % self.params['name'].val)
            code += ('                if sampleTime >= %s.startMonitoringTimeHostPC:\n' % self.params['name'].val)
            code += ('                    includeSample = True\n')
            code += ('            elif %s.status == FINISHED:\n' % self.params['name'].val)
            code += ('                if sampleTime <= %s.endMonitoringTimeHostPC:\n' % self.params['name'].val)
            code += ('                    includeSample = True\n')
            code += ('            if includeSample:\n')
            code += ('                %s.SAMPLE_LIST.append(sampleData)\n' % self.params['name'].val)
            code += ('                # if the local PsychoPy SAMPLE_LIST buffer has filled up, remove the oldest/first item in the buffer\n')
            code += ('                if len(%s.SAMPLE_LIST) > %s:\n' % (self.params['name'].val,self.params['localSampleListMaxLength'].val))
            code += ('                    del %s.SAMPLE_LIST[0]\n' % self.params['name'].val)
            code += ('\n')

        buff.writeOnceIndentedLines(code) 

    def writeRoutineEndCode(self,buff):
        # code = ('# this section of EyeLink %s component code writes the buffered data for the trial to text files\n' % self.params['name'].val)
        # code += ('onlineDataCheckFolder = os.path.join(results_folder, session_identifier,"onlineDataCheck")\n')
        # code += ('if not os.path.exists(onlineDataCheckFolder):\n')
        # code += ('    os.makedirs(onlineDataCheckFolder)\n')

        # for eventTypeToMonitor in self.eventDataTypesToMonitor:

        #     code += ('# WRITE THE BUFFFERED EVENT DATA TO TEXT FILES FOR CHECKING\n')
        #     code += ('writeFileName = "%s_DATA_TRIAL_" + str(trial_index)\n' % (eventTypeToMonitor))
        #     code += ("writeFile = open(os.path.join(onlineDataCheckFolder, writeFileName), 'w')\n")
        #     code += ('for i in range(len(%s.%s_LIST)):\n' % (self.params['name'].val,eventTypeToMonitor))
        #     code += ('    writeFile.write(str(%s.%s_LIST[i]) + "\\n")\n' % (self.params['name'].val,eventTypeToMonitor))
        #     code += ('writeFile.close')
        #     code += ('\n')

        # if self.params['includeSampleData'].val == True:
        #     code += ('# WRITE THE BUFFFERED SAMPLE DATA TO TEXT FILE FOR CHECKING\n')
        #     code += ('writeFileName = "SAMPLE_DATA_TRIAL_" + str(trial_index)\n')
        #     code += ("writeFile = open(os.path.join(onlineDataCheckFolder, writeFileName), 'w')\n")
        #     code += ('for i in range(len(%s.SAMPLE_LIST)):\n' % self.params['name'].val)
        #     code += ('    writeFile.write(str(%s.SAMPLE_LIST[i]) + "\\n")\n' % self.params['name'].val)
        #     code += ('writeFile.close')
        #     code += ('\n')
        pass
        # buff.writeOnceIndentedLines(code) 
