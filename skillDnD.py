#! /usr/bin/env python

#   author: Respen (respen@gmail.com)

from gui import *
from creatureInfo import CreatureList
import cPickle

import pygtk
pygtk.require("2.0")
import gtk

"""
This module contains the controller for the SkillDnD program.  It
is run in order to run the program.

Classes
    Controller
"""
    
#------------------------------------------------------------------------------#

class Controller:

    """
    Class which handles engine data manipulation for the user interface.
    
    Functions:
        start_session()
        add_creature(creature)
        remove_creature(name)
        
        create_creature()
        view_creature()
        save_creature()
        load_creature()
        gui_delete_event(widget,event,[data])
        gui_destroy(widget,[data])
    """
    
    def __init__(self):
        self.__mainWindow = MainWindow(self)
        self.__creatureList = CreatureList()
    
    def start_session(self):
        self.__mainWindow.main()
    
    def add_creature(self, creature):
        self.__creatureList.append(creature)
    
    def remove_creature(self, name):
        self.__creatureList.remove_by_name(name)
    
    # ----- gui callback functions ----- #
    
    def create_creature(self, widget, data = None):
        print "  Creature creation process initiated."
        self.__mainWindow.get_log().insert_at_cursor("Creature creation process initiated.\n")
        dialog = CreateCreatureDialog(self.__mainWindow.get_window(), self.__creatureList, self.__mainWindow.get_log())
    
    def view_creature(self, widget, data = None):
        print "  Starting to view a creature."
        self.__mainWindow.get_log().insert_at_cursor("Viewing a creature...\n")
        window = ViewCreatureWindow(self.__creatureList, self.__mainWindow.get_log())
    
    def save_creature(self, widget, data = None):
        print "  Starting to save a creature."
        print "    Selecting a creature..."
        dialog = SelectCreatureDialog(self.__mainWindow.get_window(), self.__creatureList)
        response = dialog.run()
        creature = None
        if response == 1:
            creature = dialog.get_selected()
            print "    %s selected." % creature
        else:
            print "  Saving aborted."
        dialog.destroy()
        
        if creature != None:
            with open("./" + creature + ".creature", "w") as f:
                cPickle.dump(self.__creatureList.get_by_name(creature), f)
                print "  %s saved." % creature
    
    def load_creature(self, widget, data = None):
        print "  Starting to load a creature."
        print "    Selecting a creature..."
        dialog = gtk.FileChooserDialog()
        dialog.add_button("Load", 1)
        dialog.add_button("Cancel", 0)
        response = dialog.run()
        creature = None
        if response == 1:
            creature = dialog.get_filename()
            print "    %s selected." % creature
        else:
            print "  Loading aborted."
        dialog.destroy()
        
        if creature != None:
            with open(creature, "r") as f:
                self.__creatureList.append(cPickle.load(f))
                print "  %s loaded." % creature
    
    def gui_delete_event(self, widget, event, data = None):
        print "  Signal received to terminate program."
        # return False to destroy gui, True to not destroy gui
        return False
    
    def gui_destroy(self, widget, data = None):
        print "  Thank you for using SkillDnD!"
        gtk.main_quit()
    
#------------------------------------------------------------------------------#

if __name__ == "__main__":
    controller = Controller()
    controller.start_session()

