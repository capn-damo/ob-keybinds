#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This script reads the keybinds configuration file ("$HOME/.config/openbox/rc.xml")
# and writes them to a text file ("$HOME/.config/openbox/kbinds.txt").
# The script is used by bl-kb-pipemenu to pipe the output to the Openbox menu
#
# Based on a script by wlourf 07/03/2010
# <http://u-stripts.blogspot.com/2010/03/how-to-display-openboxs-shortcuts.html>
#
# The original script parsed the keyboard and mouse commands from
# rc.xml, and passed them to Conkys to display on screen
#
# April 2015
#   : This script outputs the keyboard keybinds to terminal or
#     with a "--gui" argument will display the output in a text window
#   : Written for use by BunsenLabs Linux bl-kb-pipemenu by <damo>
#
########################################################################
#
#   ****If Openbox xml version changes then the xml root will need
#        changing as well (line 55)********
#
########################################################################
import sys,os
import datetime
import subprocess

try:
    from lxml import etree
except ImportError:
    import xml.etree.ElementTree as etree

# path and name of the rc.xml and saved keybinds files
rc_fpath = os.environ["HOME"] + "/.config/openbox/rc.xml"
kb_fpath = os.environ["HOME"] + "/.config/openbox/kbinds.txt"
arrShortcut=[]
gui=False

def cmdargs():
    """get command arguments"""
    if  len(sys.argv) > 1:
        if sys.argv[1] == "--gui":
            gui=True
            return gui
        else:
            msg = "\n\n\tUSAGE: to display keybinds in a text window use 'bl-kb.py --gui'\n\n"
            msg = msg + "\tRunning the script without args will send output to the terminal\n\n"
            print(msg)
            sys.exit()

def keyboard():
    """read keyboard shorcuts"""
    # Parse xml
    strRoot="{http://openbox.org/3.4/rc}"
    tree = etree.parse(rc_fpath)
    root = tree.getroot()

    for k in root.findall(strRoot+"keyboard/" + strRoot + "keybind"):
        key = k.get("key")
        action_element = k.find(strRoot+"action")
        strTxt=""
        strType="o "        # flag for pipemenu: Openbox window command
        if action_element!=None:
            arrShortcut.append((key,"",""))
            if action_element.get("name")=="Execute":
                name_element=action_element.find(strRoot + "name")
                command_element=action_element.find(strRoot + "command")
                exec_element=action_element.find(strRoot + "execute")
                strType="x "  # flag for pipemenu: Run command

                if name_element != None:
                    strTxt=name_element.text
                elif command_element != None:
                    strTxt=command_element.text
                elif exec_element != None:
                    strTxt=exec_element.text
            elif action_element.get("name")=="ShowMenu":
                menu_element=action_element.find(strRoot + "menu")
                if menu_element != None: strTxt=menu_element.text
            else:
                action_name=action_element.get("name")
                if action_name!=None:
                    strTxt=action_name
            arrShortcut[len(arrShortcut)-1]=(strType,key,strTxt)

def output_keybinds(arrShortcut,gui):
    """loop through array, and format output then write to file"""
    for i in range(0,len(arrShortcut)):
        exe=str(arrShortcut[i][0])
        keybinding=str(arrShortcut[i][1])
        execute=str(arrShortcut[i][2])
        if gui:     #format output for text window
            if len(execute)>80 :
                execute=execute[:75]+"....."
            line = "{:2}".format(i) + "\t" + "{:<15}".format(keybinding)\
            + "\t" + execute
        else:   #format text for pipemenu
            line = exe + "{:<15}".format(keybinding) + "\t" + execute
        print(line)
        write_file(line)

def check_rcfile(fpath,mode):
    """Check if rc.xml exists, and is accessible"""
    try:
        f = open(fpath,mode)
    except IOError as e:
        return False
    return True

def write_file(line):
    """Text file to store keybinds"""
    f = open(kb_fpath,'a')
    f.write(line + "\n")
    f.close()

def check_txtfile(kb_fpath):
    """Create Text file to store keybinds"""
    try:
        f = open(kb_fpath,'w')
    except IOError as e:
        return False
    return True

if __name__ == "__main__":
    gui=cmdargs()
    check_txtfile(kb_fpath)
    if gui:      # output formatted keybinds text in text window
        write_file(str(datetime.date.today()) + "\trc.xml KEYBINDS")
        write_file("---------------------------------------\n")

    if check_rcfile(rc_fpath,"r"):
        keyboard()
        output_keybinds(arrShortcut,gui)
    else:
        msg = "\nCan't open rc.xml for parsing\n\
        Check the filepath given: " + rc_fpath + "\n"
        print msg
        sys.exit(1)

    if gui:     # output formatted keybinds text in text window
        os.system("zenity --text-info --filename=$HOME/.config/openbox/kbinds.txt --width=700 --height=700")

