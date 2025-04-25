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


_localized.update({'dummyMode': _translate('Dummy Mode'),'useCustomHostIP': _translate('Use Custom Host IP Address'),'hostAddress': _translate('Host IP Address'),
                   'disableEyeLinkAudio': _translate('Disable EyeLink Audio')})


class InitializeConnection(BaseComponent):
    """An event class for initializing a connection to the EyeLink Host PC, setting Host PC
    parameters, and defining helper functions that may be called later in the script
    """
    categories = ['Eyetracking']  # which section(s) in the components panel
    targets = ['PsychoPy']
    iconFile = Path(__file__).parent / 'Initialize.png'
    tooltip = _translate('Makes a connection to the EyeLink system and '
                         'sets some initial parameters')
    plugin = "psychopy-eyelink"

    def __init__(self, exp, parentName, name='Initialize', startType='time (s)', startVal='0.0', stopVal='0.001',
                 stopType='duration (s)', dummyMode=False, useCustomHostIP=True, hostAddress='100.1.1.1', disableEyeLinkAudio=False):

        super(InitializeConnection, self).__init__(
            exp, parentName, name, startType=startType, startVal=startVal,
            stopType=stopType, stopVal=stopVal
            )

        self.type = 'Initialize'
        self.url = "https://www.sr-research.com/support/thread-7525.html"

        self.params['dummyMode'] = Param(
            dummyMode, categ='Basic',
            valType='bool', inputType="bool",
            hint=_translate('Run Experiment in Dummy Mode'),
            label=_localized['dummyMode'])
        
        self.params['useCustomHostIP'] = Param(
            dummyMode, categ='Basic',
            valType='bool', inputType="bool",
            hint=_translate('Use custom Host IP address (will use default 100.1.1.1 if false)'),
            label=_localized['useCustomHostIP'])
        
        self.params['hostAddress'] = Param(
            hostAddress, categ='Basic',
            valType='str', inputType="single",
            hint=_translate('The custom IP address of the Host PC (i.e., eye tracking) computer'),
            label=_localized['hostAddress'])
        
        self.params['disableEyeLinkAudio'] = Param(
            disableEyeLinkAudio, categ='Basic',
            valType='bool', inputType="bool",
            hint=_translate('Disable EyeLink audio (may be useful when running experiments where audio is presented)'),
            label=_localized['disableEyeLinkAudio'])
        
        self.depends.append(
            {'dependsOn':'useCustomHostIP',
             'condition':'== True',
             'param':'hostAddress',
             'true':'show',
             'false':'hide'}) 

    def writePreCode(self,buff):
        code = ('# This section of the EyeLink %s component code imports some\n' % self.params['name'].val)
        code += ('# modules we need, manages data filenames, allows for dummy mode configuration\n')
        code += ('# (for testing experiments without an eye tracker), connects to the tracker,\n') 
        code += ('# and defines some helper functions (which can be called later)\n')   
        code += ('import pylink\n')
        code += ('import time\n')
        code += ('import platform\n')
        code += ('from PIL import Image  # for preparing the Host backdrop image\n')
        code += ('from EyeLinkCoreGraphicsPsychoPy import EyeLinkCoreGraphicsPsychoPy\n')
        code += ('from string import ascii_letters, digits\n')
        code += ('from psychopy import gui\n')
        # removed due to plugin folder structure changes in 2024.1.x
        #code += ("plugins.loadPlugin('psychopy-eyelink')\n")
        code += ('\n')
        code += ('import psychopy_eyelink\n')
        code += ("print('EyeLink Plugin For PsychoPy Version = ' + str(psychopy_eyelink.__version__))\n")
        code += ('\n')
        code += ('script_path = os.path.dirname(sys.argv[0])\n')
        code += ('if len(script_path) != 0:\n')
        code += ('    os.chdir(script_path)\n')
        code += ('\n')
        code += ('# Set this variable to True if you use the built-in retina screen as your\n')
        code += ('# primary display device on macOS. If have an external monitor, set this\n')
        code += ('# variable True if you choose to "Optimize for Built-in Retina Display"\n')
        code += ('# in the Displays preference settings.\n')
        code += ('use_retina = False\n')
        code += ('\n')
        code += ('# Set this variable to True to run the script in "Dummy Mode"\n')
        code += ('dummy_mode = %s\n' % self.params['dummyMode'].val)
        code += ('\n')
        # Updated May 2024 to fix dialog changes in 2024.1.x
        code += ('# Prompt user to specify an EDF data filename\n')
        code += ('# before we open a fullscreen window\n')
        code += ('dlg_title = "Enter EDF Filename"\n')
        code += ('dlg_prompt = "Please enter a file name with 8 or fewer characters [letters, numbers, and underscore]."\n')
        code += ('# loop until we get a valid filename\n')
        code += ('while True:\n')
        code += ('    dlg = gui.Dlg(dlg_title)\n')
        code += ('    dlg.addText(dlg_prompt)\n')
        code += ('    dlg.addField("Filename",initial="Test",label="EDF Filename")\n')
        code += ('    # show dialog and wait for OK or Cancel\n')
        code += ('    ok_data = dlg.show()\n')
        code += ('    if dlg.OK:  # if ok_data is not None\n')
        code += ('        print("EDF data filename: {}".format(ok_data["Filename"]))\n')
        code += ('    else:\n')
        code += ('        print("user cancelled")\n')
        code += ('        core.quit()\n')
        code += ('        sys.exit()\n')
        code += ('\n')
        code += ('    # get the string entered by the experimenter\n')
        code += ('    tmp_str = ok_data["Filename"]\n')
        code += ('    # strip trailing characters, ignore the ".edf" extension\n')
        code += ('    edf_fname = tmp_str.rstrip().split(".")[0]\n')
        code += ('\n')
        code += ('    # check if the filename is valid (length <= 8 & no special char)\n')
        code += ('    allowed_char = ascii_letters + digits + "_"\n')
        code += ('    if not all([c in allowed_char for c in edf_fname]):\n')
        code += ('        print("ERROR: Invalid EDF filename")\n')
        code += ('    elif len(edf_fname) > 8:\n')
        code += ('        print("ERROR: EDF filename should not exceed 8 characters")\n')
        code += ('    else:\n')
        code += ('        break')

        code += ('# Set up a folder to store the EDF data files and the associated resources\n')
        code += ('# e.g., files defining the interest areas used in each trial\n')
        code += ('results_folder = "results"\n')
        code += ('if not os.path.exists(results_folder):\n')
        code += ('    os.makedirs(results_folder)\n')
        code += ('\n')
        code += ('# We download EDF data file from the EyeLink Host PC to the local hard\n')
        code += ('# drive at the end of each testing session, here we rename the EDF to\n')
        code += ('# include session start date/time\n')
        code += ('time_str = time.strftime("_%Y_%m_%d_%H_%M", time.localtime())\n')
        code += ('session_identifier = edf_fname + time_str\n')
        code += ('\n')
        code += ('# create a folder for the current testing session in the "results" folder\n')
        code += ('session_folder = os.path.join(results_folder, session_identifier)\n')
        code += ('if not os.path.exists(session_folder):\n')
        code += ('    os.makedirs(session_folder)\n')
        code += ('\n')
        code += ('# For macOS users check if they have a retina screen\n')
        code += ("if 'Darwin' in platform.system():\n")
        code += ('    dlg = gui.Dlg("Retina Screen?")\n')
        code += ('    dlg.addText("What type of screen will the experiment run on?")\n')
        code += ('    dlg.addField("Screen Type", choices=["High Resolution (Retina, 2k, 4k, 5k)", "Standard Resolution (HD or lower)"])\n')
        code += ('    # show dialog and wait for OK or Cancel\n')
        code += ('    ok_data = dlg.show()\n')
        code += ('    if dlg.OK:\n')
        code += ('        if dlg.data["Screen Type"] == "High Resolution (Retina, 2k, 4k, 5k)":  \n')
        code += ('            use_retina = True\n')
        code += ('        else:\n')
        code += ('            use_retina = False\n')
        code += ('    else:\n')
        code += ("        print('user cancelled')\n")
        code += ('        core.quit()\n')
        code += ('        sys.exit()\n')
        code += ('\n')
        code += ('# Connect to the EyeLink Host PC\n')
        code += ('# The Host IP address, by default, is "100.1.1.1".\n')
        code += ('# the "el_tracker" objected created here can be accessed through the Pylink\n')
        code += ('# Set the Host PC address to "None" (without quotes) to run the script\n')
        code += ('# in "Dummy Mode"\n')
        code += ('if dummy_mode:\n')
        code += ('    el_tracker = pylink.EyeLink(None)\n')
        code += ('else:\n')
        code += ('    try:\n')
        if self.params['useCustomHostIP'].val == True:
            code += ('        el_tracker = pylink.EyeLink(' + str(self.params['hostAddress']) + ')\n')
        else:
            code += ('        el_tracker = pylink.EyeLink("100.1.1.1")\n')
        code += ('    except RuntimeError as error:\n')
        if self.params['useCustomHostIP'].val == True:
            code += ('        dlg = gui.Dlg("Dummy Mode?")\n')
            code += ('        dlg.addText("Could not connect to tracker at " '+ str(self.params['hostAddress']) + '" -- continue in Dummy Mode?")\n')
        else:
            code += ('        dlg = gui.Dlg("Dummy Mode?")\n')
            code += ('        dlg.addText("Could not connect to tracker at 100.1.1.1 -- continue in Dummy Mode?")\n')
        code += ('        # show dialog and wait for OK or Cancel\n')
        code += ('        ok_data = dlg.show()\n')
        code += ('        if dlg.OK:  # if ok_data is not None\n')
        code += ('            dummy_mode = True\n')
        code += ('            el_tracker = pylink.EyeLink(None)\n')
        code += ('        else:\n')
        code += ('            print("user cancelled")\n')
        code += ('            core.quit()\n')
        code += ('            sys.exit()\n')
        code += ('\n')
        code += ('eyelinkThisFrameCallOnFlipScheduled = False\n')
        code += ('eyelinkLastFlipTime = 0.0\n')
        code += ('zeroTimeIAS = 0.0\n')
        code += ('zeroTimeDLF = 0.0\n')
        code += ('sentIASFileMessage = False\n')
        code += ('sentDrawListMessage = False\n')

        
                ## HELPER FUNCTIONS
        code += ('\n')
        code += ('def clear_screen(win,genv):\n')
        code += ('    """ clear up the PsychoPy window"""\n')
        code += ('    win.fillColor = genv.getBackgroundColor()\n')
        code += ('    win.flip()\n')
        code += ('\n')
        code += ('def show_msg(win, genv, text, wait_for_keypress=True):\n')
        code += ('    """ Show task instructions on screen"""\n')
        code += ('    scn_width, scn_height = win.size\n')
        code += ('    msg = visual.TextStim(win, text,\n')
        code += ('                          color=genv.getForegroundColor(),\n')
        code += ('                          wrapWidth=scn_width/2)\n')
        code += ('    clear_screen(win,genv)\n')
        code += ('    msg.draw()\n')
        code += ('    win.flip()\n')
        code += ('\n')
        code += ('    # wait indefinitely, terminates upon any key press\n')
        code += ('    if wait_for_keypress:\n')
        code += ('        kb = keyboard.Keyboard()\n')
        code += ('        waitKeys = kb.waitKeys(keyList=None, waitRelease=True, clear=True)\n')
        code += ('        clear_screen(win,genv)\n')
        code += ('\n')
        code += ('def terminate_task(win,genv,edf_file,session_folder,session_identifier):\n')
        code += ('    """ Terminate the task gracefully and retrieve the EDF data file\n')
        code += ('    """\n')
        code += ('    el_tracker = pylink.getEYELINK()\n')
        code += ('\n')
        code += ('    if el_tracker.isConnected():\n')
        code += ('        # Terminate the current trial first if the task terminated prematurely\n')
        code += ('        error = el_tracker.isRecording()\n')
        code += ('        if error == pylink.TRIAL_OK:\n')
        code += ('            abort_trial(win,genv)\n')
        code += ('\n')
        code += ('        # Put tracker in Offline mode\n')
        code += ('        el_tracker.setOfflineMode()\n')
        code += ('\n')
        code += ('        # Clear the Host PC screen and wait for 500 ms\n')
        code += ("        el_tracker.sendCommand('clear_screen 0')\n")
        code += ('        pylink.msecDelay(500)\n')
        code += ('\n')
        code += ('        # Close the edf data file on the Host\n')
        code += ('        el_tracker.closeDataFile()\n')
        code += ('\n')
        code += ('        # Show a file transfer message on the screen\n')
        code += ("        msg = 'EDF data is transferring from EyeLink Host PC...'\n")
        code += ('        show_msg(win, genv, msg, wait_for_keypress=False)\n')
        code += ('\n')
        code += ('        # Download the EDF data file from the Host PC to a local data folder\n')
        code += ('        # parameters: source_file_on_the_host, destination_file_on_local_drive\n')
        code += ("        local_edf = os.path.join(session_folder, session_identifier + '.EDF')\n")
        code += ('        try:\n')
        code += ('            el_tracker.receiveDataFile(edf_file, local_edf)\n')
        code += ('        except RuntimeError as error:\n')
        code += ("            print('ERROR:', error)\n")
        code += ('\n')
        code += ('        # Close the link to the tracker.\n')
        code += ('        el_tracker.close()\n')
        code += ('\n')
        code += ('    # close the PsychoPy window\n')
        code += ('    win.close()\n')
        code += ('\n')
        code += ('    # quit PsychoPy\n')
        code += ('    core.quit()\n')
        code += ('    sys.exit()')
        code += ('\n')
        code += ('\n')
        code += ('def abort_trial(win,genv):\n')
        code += ('    """Ends recording """\n')
        code += ('    el_tracker = pylink.getEYELINK()\n')
        code += ('\n')
        code += ('    # Stop recording\n')
        code += ('    if el_tracker.isRecording():\n')
        code += ('        # add 100 ms to catch final trial events\n')
        code += ('        pylink.pumpDelay(100)\n')
        code += ('        el_tracker.stopRecording()\n')
        code += ('\n')
        code += ('    # clear the screen\n')
        code += ('    clear_screen(win,genv)\n')
        code += ('    # Send a message to clear the Data Viewer screen\n')
        code += ('    bgcolor_RGB = (116, 116, 116)\n')
        code += ("    el_tracker.sendMessage('!V CLEAR %d %d %d' % bgcolor_RGB)\n")
        code += ('\n')
        code += ('    # send a message to mark trial end\n')
        code += ("    el_tracker.sendMessage('TRIAL_RESULT %d' % pylink.TRIAL_ERROR)\n")
        code += ('    return pylink.TRIAL_ERROR\n')
        code += ('\n')
        code += ('# this method converts PsychoPy position values to EyeLink position values\n')
        code += ('# EyeLink position values are in pixel units and are such that 0,0 corresponds \n')
        code += ('# to the top-left corner of the screen and increase as position moves right/down\n')
        code += ('def eyelink_pos(pos,winSize,unitType):\n')
        code += ('    screenUnitType = unitType\n')
        code += ('    scn_width,scn_height = winSize\n')
        code += ("    if screenUnitType == 'pix':\n")
        code += ('        elPos = [pos[0] + scn_width/2,scn_height/2 - pos[1]]\n')
        code += ("    elif screenUnitType == 'height':\n")
        code += ('        elPos = [scn_width/2 + pos[0] * scn_height,scn_height/2 + pos[1] * scn_height]\n')
        code += ('    elif screenUnitType == "norm":\n')
        code += ('        elPos = [(scn_width/2 * pos[0]) + scn_width/2,scn_height/2 + pos[1] * scn_height]\n')
        code += ('    else:\n')
        code += ('        print("ERROR:  Only pixel, height, and norm units supported for conversion to EyeLink position units")\n')
        code += ('    return [int(round(elPos[0])),int(round(elPos[1]))]\n')
        code += ('\n')
        code += ('# this method converts PsychoPy size values to EyeLink size values\n')
        code += ('# EyeLink size values are in pixels\n')
        code += ('def eyelink_size(size,winSize,unitType):\n')
        code += ('    screenUnitType = unitType\n')
        code += ('    scn_width,scn_height = winSize\n')
        code += ('    if len(size) == 1:\n')
        code += ('        size = [size[0],size[0]]\n')
        code += ("    if screenUnitType == 'pix':\n")
        code += ('        elSize = [size[0],size[1]]\n')
        code += ("    elif screenUnitType == 'height':\n")
        code += ('        elSize = [int(round(scn_height*size[0])),int(round(scn_height*size[1]))]\n')
        code += ('    elif screenUnitType == "norm":\n')
        code += ('        elSize = [size[0]/2 * scn_width,size[1]/2 * scn_height]\n')
        code += ('    else:\n')
        code += ('        print("ERROR:  Only pixel, height, and norm units supported for conversion to EyeLink position units")\n')
        code += ('    return [int(round(elSize[0])),int(round(elSize[1]))]\n')
        code += ('\n')
        code += ('# this method converts PsychoPy color values to EyeLink color values\n')
        code += ('def eyelink_color(color):\n')
        code += ('    elColor = (int(round((win.color[0]+1)/2*255)),int(round((win.color[1]+1)/2*255)),int(round((win.color[2]+1)/2*255)))\n')
        code += ('    return elColor\n')
        code += ('\n')
        code += ('\n')
        
        buff.writeOnceIndentedLines(code)

    def writeInitCode(self,buff):
        code = ("%(name)s = event.Mouse(win=win)\n")
        buff.writeIndentedLines(code % self.params)
 

    def writeRunOnceInitCode(self, buff):
        code = ('# This section of the EyeLink %s component code opens an EDF file,\n' % self.params['name'].val)
        code += ('# writes some header text to the file, and configures some tracker settings\n')
        code += ('el_tracker = pylink.getEYELINK()\n')
        code += ('global edf_fname\n')
        code += ('# Open an EDF data file on the Host PC\n')
        code += ('edf_file = edf_fname + ".EDF"\n')
        code += ('try:\n')
        code += ('    el_tracker.openDataFile(edf_file)\n')
        code += ('except RuntimeError as err:\n')
        code += ('    print("ERROR:", err)\n')
        code += ('    # close the link if we have one open\n')
        code += ('    if el_tracker.isConnected():\n')
        code += ('        el_tracker.close()\n')
        code += ('    core.quit()\n')
        code += ('    sys.exit()\n')
        code += ('\n')
        code += ('# Add a header text to the EDF file to identify the current experiment name\n')
        code += ('# This is OPTIONAL. If your text starts with "RECORDED BY " it will be\n')
        code += ("# available in DataViewer's Inspector window by clicking\n")
        code += ('# the EDF session node in the top panel and looking for the "Recorded By:"\n')
        code += ('# field in the bottom panel of the Inspector.\n')
        code += ("preamble_text = 'RECORDED BY %s EyeLink Plugin Version %s ' % (os.path.basename(__file__),psychopy_eyelink.__version__)\n")
        code += ('el_tracker.sendCommand("add_file_preamble_text ' + "'%s'" + '" % preamble_text)\n')
        code += ('\n')
        code += ('# Configure the tracker\n')
        code += ('#\n')
        code += ('# Put the tracker in offline mode before we change tracking parameters\n')
        code += ('el_tracker.setOfflineMode()\n')
        code += ('\n')
        code += ('# Get the software version:  1-EyeLink I, 2-EyeLink II, 3/4-EyeLink 1000,\n')
        code += ('# 5-EyeLink 1000 Plus, 6-Portable DUO\n')
        code += ('eyelink_ver = 0  # set version to 0, in case running in Dummy mode\n')
        code += ('if not dummy_mode:\n')
        code += ('    vstr = el_tracker.getTrackerVersionString()\n')
        code += ('    eyelink_ver = int(vstr.split()[-1].split(".")[0])\n')
        code += ('    # print out some version info in the shell\n')
        code += ('    print("Running experiment on %s, version %d" % (vstr, eyelink_ver))\n')
        code += ('\n')
        code += ('# File and Link data control\n')
        code += ('# what eye events to save in the EDF file, include everything by default\n')
        code += ("file_event_flags = 'LEFT,RIGHT,FIXATION,SACCADE,BLINK,MESSAGE,BUTTON,INPUT'\n")
        code += ('# what eye events to make available over the link, include everything by default\n')
        code += ("link_event_flags = 'LEFT,RIGHT,FIXATION,SACCADE,BLINK,BUTTON,FIXUPDATE,INPUT'\n")
        code += ('# what sample data to save in the EDF data file and to make available\n')
        code += ("# over the link, include the 'HTARGET' flag to save head target sticker\n")
        code += ('# data for supported eye trackers\n')
        code += ('if eyelink_ver > 3:\n')
        code += ("    file_sample_flags = 'LEFT,RIGHT,GAZE,HREF,RAW,AREA,HTARGET,GAZERES,BUTTON,STATUS,INPUT'\n")
        code += ("    link_sample_flags = 'LEFT,RIGHT,GAZE,GAZERES,AREA,HTARGET,STATUS,INPUT'\n")
        code += ('else:\n')
        code += ("    file_sample_flags = 'LEFT,RIGHT,GAZE,HREF,RAW,AREA,GAZERES,BUTTON,STATUS,INPUT'\n")
        code += ("    link_sample_flags = 'LEFT,RIGHT,GAZE,GAZERES,AREA,STATUS,INPUT'\n")
        code += ('el_tracker.sendCommand("file_event_filter = %s" % file_event_flags)\n')
        code += ('el_tracker.sendCommand("file_sample_data = %s" % file_sample_flags)\n')
        code += ('el_tracker.sendCommand("link_event_filter = %s" % link_event_flags)\n')
        code += ('el_tracker.sendCommand("link_sample_data = %s" % link_sample_flags)\n')
        code += ('# Set a gamepad button to accept calibration/drift check target\n')
        code += ('# You need a supported gamepad/button box that is connected to the Host PC\n')
        code += ('el_tracker.sendCommand("button_function 5 ' + "'accept_target_fixation'" + '")\n')
        code += ('\n')
        code += ('global eyelinkThisFrameCallOnFlipScheduled,eyelinkLastFlipTime,zeroTimeDLF,sentDrawListMessage,zeroTimeIAS,sentIASFileMessage\n')
        buff.writeOnceIndentedLines(code)


    def writeRoutineEndCode(self,buff):
        code = ('# This section of the EyeLink %s component code gets graphic \n' % self.params['name'].val)
        code += ('# information from Psychopy, sets the screen_pixel_coords on the Host PC based\n')
        code += ('# on these values, and logs the screen resolution for Data Viewer via \n')  
        code += ('# a DISPLAY_COORDS message\n')
        code += ('\n')
        code += ('# get the native screen resolution used by PsychoPy\n')
        code += ('scn_width, scn_height = win.size\n')
        code += ('# resolution fix for Mac retina displays\n')
        code += ("if 'Darwin' in platform.system():\n")
        code += ('    if use_retina:\n')
        code += ('        scn_width = int(scn_width/2.0)\n')
        code += ('        scn_height = int(scn_height/2.0)\n')
        code += ('\n')
        code += ('# Pass the display pixel coordinates (left, top, right, bottom) to the tracker\n')
        code += ('# see the EyeLink Installation Guide, "Customizing Screen Settings"\n')
        code += ('el_coords = "screen_pixel_coords = 0 0 %d %d" % (scn_width - 1, scn_height - 1)\n')
        code += ('el_tracker.sendCommand(el_coords)\n')
        code += ('\n')
        code += ('# Write a DISPLAY_COORDS message to the EDF file\n')
        code += ('# Data Viewer needs this piece of info for proper visualization, see Data\n')
        code += ('# Viewer User Manual, "Protocol for EyeLink Data to Viewer Integration"\n')
        code += ('dv_coords = "DISPLAY_COORDS  0 0 %d %d" % (scn_width - 1, scn_height - 1)\n')
        code += ('el_tracker.sendMessage(dv_coords)')
        code += ('# This Begin Experiment tab of the elTrial component just initializes\n')
        code += ('# a trial counter variable at the beginning of the experiment\n')
        code += ('trial_index = 1\n')
        code += ('# Configure a graphics environment (genv) for tracker calibration\n')
        code += ('genv = EyeLinkCoreGraphicsPsychoPy(el_tracker, win, %s)\n' % self.params['disableEyeLinkAudio'].val)
        code += ('print(genv)  # print out the version number of the CoreGraphics library\n')
        code += ('\n')
        code += ('# resolution fix for macOS retina display issues\n')
        code += ('if use_retina:\n')
        code += ('    genv.fixMacRetinaDisplay()\n')
        code += ('# Request Pylink to use the PsychoPy window we opened above for calibration\n')
        code += ('pylink.openGraphicsEx(genv)\n')
        code += ('# Create an array of pixels to assist in transferring content to the Host PC backdrop\n')
        code += ('rgbBGColor = eyelink_color(win.color)\n')
        code += ('blankHostPixels = [[rgbBGColor for i in range(scn_width)]\n')
        code += ('    for j in range(scn_height)]\n')

        buff.writeOnceIndentedLines(code)


    def writeExperimentEndCode(self, buff):
        code = ('# This section of the Initialize component calls the \n')
        code += ('# terminate_task helper function to get the EDF file and close the connection\n')
        code += ('# to the Host PC\n')
        code += ('\n')
        code += ('# Disconnect, download the EDF file, then terminate the task\n')
        code += ('terminate_task(win,genv,edf_file,session_folder,session_identifier)')

        buff.writeOnceIndentedLines(code)


