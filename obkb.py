#!/usr/bin/env python
# coding=utf-8

# This script reads the keybinds configuration file (".config/openbox/rc.xml")
# and writes them to a text file (".config/openbox/kbinds.txt"). This file is read
# and displayed on screen in a zenity text-info dialog
#
# Keyboard shorcuts without commands are not displayed
#
# Based on a script by wlourf 07/03/2010
# <http://u-stripts.blogspot.com/2010/03/how-to-display-openboxs-shortcuts.html>
#
# The original script parsed the keyboard and mouse commands from
# rc.xml, and passed them to Conkys to display on screen
#
# March 2014 by damo    <damo.linux@gmail.com>
#   : This version just outputs the keyboard keybinds
#
########################################################################
#
#   USAGE:  Output formatted keyboard shortcuts to the terminal with "python path/to/obkb.py"
#            (or make executable and put in $PATH)
#
#           If run in a terminal the keybinds are also echoed to screen
#
#
#   ****If Openbox xml version changes then the xml root will need
#        changing as well (line 51)********
#
########################################################################
import sys,os
import datetime
import subprocess

try:
    from lxml import etree
except ImportError:
    import xml.etree.ElementTree as etree

#######################################################
# path and name of the rc.xml and saved keybinds files
rc_fpath = os.environ["HOME"] + "/.config/openbox/rc.xml"
kb_fpath = os.environ["HOME"] + "/.config/openbox/kbinds.txt"
#######################################################
arrShortcut=[]

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
        if action_element!=None:
            arrShortcut.append((key,"",""))
            if action_element.get("name")=="Execute":
                name_element=action_element.find(strRoot + "name")
                command_element=action_element.find(strRoot + "command")
                exec_element=action_element.find(strRoot + "execute")

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

            arrShortcut[len(arrShortcut)-1]=(key,strTxt)


def output_keybinds(arrShortcut):
    """loop through array, and format output
        then write to file"""
    print str(datetime.date.today()) + "\trc.xml KEYBINDS"
    print "-------------------------------\n"
    for i in range(0,len(arrShortcut)):
        keybinding=str(arrShortcut[i][0])
        execute=str(arrShortcut[i][1])
        if len(execute)>80 :
            execute=execute[:75]+"....."
        line = "{:2}".format(i) + "\t" + "{:<15}".format(keybinding)\
        + "\t" + execute
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
    """Create Text file to store keybinds
        write date/time heading"""
    try:
        f = open(kb_fpath,'w')
    except IOError as e:
        return False
    return True
    f = open(kb_fpath,'a')
    f.write(datetime.date.today() + "\trc.xml KEYBINDS\n")
    f.write("-------------------------------\n")
    f.close()

if __name__ == "__main__":

    check_txtfile(kb_fpath)

    if check_rcfile(rc_fpath,"r"):
        keyboard()
        output_keybinds(arrShortcut)
    else:
        msg = "\nCan't open rc.xml for parsing\n\
        Check the filepath given: " + rc_fpath + "\n"
        print msg
        sys.exit(1)

    os.system("zenity --text-info --filename=.config/openbox/kbinds.txt --width=700 --height=700")


