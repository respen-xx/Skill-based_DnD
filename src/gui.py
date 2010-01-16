
#   author: Respen (respen@gmail.com)

"""
This module contains the classes necessary for the GUI to function.

Classes
    MainWindow
    SelectCreatureDialog
    CreateCreatureDialog
    ViewCreatureWindow
"""

import pygtk
pygtk.require("2.0")
import gtk
import gobject
from creatureInfo import Creature
from skillInfo import *

#------------------------------------------------------------------------------#

class MainWindow:

    """
    This class contains the information for the main gui window of the
    program.
    
    Functions:
        __init__()
        main()
        get_window()
        get_log()
    """
    
    def __init__(self, controller):
        self.__controller = controller
        
        # create the window
        self.__window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        
        # ======== window option settings ======== #
        
        # sets the title on the topbar of the window
        self.__window.set_title("SkillDnD")
        
        # sets interior padding (empty space next to the edges of the window)
        self.__window.set_border_width(10)
        
        # set default window size
        self.__window.set_default_size(600, 450)
        
        # ======== window components ======== #
        
        # file menu and it's contents
        
        fileMenu = gtk.MenuItem("File")
        fileMenu.show()
        
        menu = gtk.Menu()
        
        saveCreature = gtk.MenuItem("Save Creature")
        saveCreature.connect("activate", self.__controller.save_creature)
        saveCreature.show()
        
        loadCreature = gtk.MenuItem("Load Creature")
        loadCreature.connect("activate", self.__controller.load_creature)
        loadCreature.show()
        
        quitProgram = gtk.MenuItem("Quit")
        quitProgram.connect("activate", self.__controller.gui_destroy)
        quitProgram.show()
        
        menu.append(saveCreature)
        menu.append(loadCreature)
        menu.append(quitProgram)
        
        fileMenu.set_submenu(menu)
        
        # creature menu and it's contents
        
        creatureMenu = gtk.MenuItem("Creature")
        creatureMenu.show()
        
        menu = gtk.Menu()
        
        createCreature = gtk.MenuItem("Create")
        createCreature.connect("activate", self.__controller.create_creature)
        createCreature.show()
        
        viewCreature = gtk.MenuItem("View")
        viewCreature.connect("activate", self.__controller.view_creature)
        viewCreature.show()
        
        menu.append(createCreature)
        menu.append(viewCreature)
        
        creatureMenu.set_submenu(menu)
        
        # the menubar across the very top
        
        self.__menuBar = gtk.MenuBar()
        self.__menuBar.show()
        
        self.__menuBar.append(fileMenu)
        self.__menuBar.append(creatureMenu)
        
        # main window contents
        
        self.__log = gtk.TextBuffer()
        
        logView = gtk.TextView(self.__log)
        logView.set_editable(False)
        logView.set_cursor_visible(False)
        logView.set_wrap_mode(gtk.WRAP_WORD)
        logView.show()
        
        logViewScroller = gtk.ScrolledWindow()
        logViewScroller.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        logViewScroller.show()
        logViewScroller.add(logView)
        
        # window-level component packing
        
        vBox = gtk.VBox(False, 0)
        vBox.show()
        vBox.pack_start(self.__menuBar, False, False, 2)
        vBox.pack_end(logViewScroller, False, False, 0)
        
        self.__window.add(vBox)
        
        # ======== signal/event registering for the window ======== #
        
        # register the delete event signal
        self.__window.connect("delete_event", self.__controller.gui_delete_event)
        
        # register the destroy event
        self.__window.connect("destroy", self.__controller.gui_destroy)
        
        # display the window
        self.__window.show()
    
    def main(self):
        self.__log.insert_at_cursor("Welcome to the SkillDnD program!\n\n")
        
        # GTK now waits for an event to occur
        gtk.main()
    
    def get_window(self):
        return self.__window
    
    def get_log(self):
        return self.__log

#------------------------------------------------------------------------------#

class SelectCreatureDialog(gtk.Dialog):
    
    """
    This class is a simple dialog which allows a user to select a creature.
    """
    
    def __init__(self, parent, creatureList):
        gtk.Dialog.__init__(self, "Select a Creature", parent, gtk.DIALOG_DESTROY_WITH_PARENT)
        self.set_size_request(200, 100)
        
        # ----- dialog top area ----- #
        
        self.__comboBox = gtk.combo_box_new_text()
        self.__comboBox.show()
        self.vbox.pack_start(self.__comboBox, True, True, 0)
        
        for creature in creatureList:
            self.__comboBox.append_text(creature.get_name())
        
        # ----- dialog action (bottom) area ----- #
        
        self.add_button("Select", 1)
        self.add_button("Cancel", 0)
    
    def get_selected(self):
        model = self.__comboBox.get_model()
        active = self.__comboBox.get_active()
        if active < 0:
            return None;
        return model[active][0]

#------------------------------------------------------------------------------#

class CreateCreatureDialog:
    
    """
    This class contains the form for inputting creature information to
    create a new creature.
    
    Functions:
        create_creature(widget,[data])
        close_dialog(widget,[data])
    """
    
    def __init__(self, parent, creatureList, log):
        self.__creatureList = creatureList
        self.__mainLog = log
        
        skills = SkillList()
        
        self.__dialog = gtk.Dialog("Create a Creature", parent, gtk.DIALOG_DESTROY_WITH_PARENT)
        self.__dialog.set_size_request(400, 400)
        
        # ----- dialog top area ----- #
        
        scrolledWindow = gtk.ScrolledWindow()
        scrolledWindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrolledWindow.show()
        self.__dialog.vbox.pack_start(scrolledWindow, True, True, 0)
        
        table = gtk.Table(rows=(8 + 1 + len(skills)), columns=2)
        table.set_row_spacings(5)
        table.set_col_spacings(10)
        table.show()
        scrolledWindow.add_with_viewport(table)
        
        currentRow = 0
        currentCol = 0
        
        nameLabel = gtk.Label("Creature Name")
        nameLabel.show()
        table.attach(nameLabel, currentCol, currentCol + 1, currentRow, currentRow + 1, xoptions = gtk.SHRINK, yoptions = gtk.SHRINK)
        currentCol += 1
        
        self.__nameEntry = gtk.Entry(max=50)
        self.__nameEntry.set_text("Joe")
        self.__nameEntry.select_region(0, 2)
        self.__nameEntry.show()
        table.attach(self.__nameEntry, currentCol, currentCol + 1, currentRow, currentRow + 1, xpadding=5, xoptions = gtk.SHRINK, yoptions = gtk.SHRINK)
        currentRow += 1
        currentCol = 0
        
        strengthLabel = gtk.Label("Strength")
        strengthLabel.show()
        table.attach(strengthLabel, currentCol, currentCol + 1, currentRow, currentRow + 1, xoptions = gtk.SHRINK, yoptions = gtk.SHRINK)
        currentCol += 1
        
        self.__strSpin = gtk.SpinButton(gtk.Adjustment(value=10, lower=0, upper=100, step_incr=1))
        self.__strSpin.set_numeric(True)
        self.__strSpin.set_max_length(3)
        self.__strSpin.show()
        table.attach(self.__strSpin, currentCol, currentCol + 1, currentRow, currentRow + 1, xoptions = gtk.SHRINK, yoptions = gtk.SHRINK)
        currentRow += 1
        currentCol = 0
        
        dexterityLabel = gtk.Label("Dexterity")
        dexterityLabel.show()
        table.attach(dexterityLabel, currentCol, currentCol + 1, currentRow, currentRow + 1, xoptions = gtk.SHRINK, yoptions = gtk.SHRINK)
        currentCol += 1
        
        self.__dexSpin = gtk.SpinButton(gtk.Adjustment(value=10, lower=0, upper=100, step_incr=1))
        self.__dexSpin.set_numeric(True)
        self.__dexSpin.set_max_length(3)
        self.__dexSpin.show()
        table.attach(self.__dexSpin, currentCol, currentCol + 1, currentRow, currentRow + 1, xoptions = gtk.SHRINK, yoptions = gtk.SHRINK)
        currentRow += 1
        currentCol = 0
        
        constitutionLabel = gtk.Label("Constitution")
        constitutionLabel.show()
        table.attach(constitutionLabel, currentCol, currentCol + 1, currentRow, currentRow + 1, xoptions = gtk.SHRINK, yoptions = gtk.SHRINK)
        currentCol += 1
        
        self.__conSpin = gtk.SpinButton(gtk.Adjustment(value=10, lower=0, upper=100, step_incr=1))
        self.__conSpin.set_numeric(True)
        self.__conSpin.set_max_length(3)
        self.__conSpin.show()
        table.attach(self.__conSpin, currentCol, currentCol + 1, currentRow, currentRow + 1, xoptions = gtk.SHRINK, yoptions = gtk.SHRINK)
        currentRow += 1
        currentCol = 0
        
        intelligenceLabel = gtk.Label("Intelligence")
        intelligenceLabel.show()
        table.attach(intelligenceLabel, currentCol, currentCol + 1, currentRow, currentRow + 1, xoptions = gtk.SHRINK, yoptions = gtk.SHRINK)
        currentCol += 1
        
        self.__intSpin = gtk.SpinButton(gtk.Adjustment(value=10, lower=0, upper=100, step_incr=1))
        self.__intSpin.set_numeric(True)
        self.__intSpin.set_max_length(3)
        self.__intSpin.show()
        table.attach(self.__intSpin, currentCol, currentCol + 1, currentRow, currentRow + 1, xoptions = gtk.SHRINK, yoptions = gtk.SHRINK)
        currentRow += 1
        currentCol = 0
        
        wisdomLabel = gtk.Label("Wisdom")
        wisdomLabel.show()
        table.attach(wisdomLabel, currentCol, currentCol + 1, currentRow, currentRow + 1, xoptions = gtk.SHRINK, yoptions = gtk.SHRINK)
        currentCol += 1
        
        self.__wisSpin = gtk.SpinButton(gtk.Adjustment(value=10, lower=0, upper=100, step_incr=1))
        self.__wisSpin.set_numeric(True)
        self.__wisSpin.set_max_length(3)
        self.__wisSpin.show()
        table.attach(self.__wisSpin, currentCol, currentCol + 1, currentRow, currentRow + 1, xoptions = gtk.SHRINK, yoptions = gtk.SHRINK)
        currentRow += 1
        currentCol = 0
        
        charismaLabel = gtk.Label("Charisma")
        charismaLabel.show()
        table.attach(charismaLabel, currentCol, currentCol + 1, currentRow, currentRow + 1, xoptions = gtk.SHRINK, yoptions = gtk.SHRINK)
        currentCol += 1
        
        self.__chaSpin = gtk.SpinButton(gtk.Adjustment(value=10, lower=0, upper=100, step_incr=1))
        self.__chaSpin.set_numeric(True)
        self.__chaSpin.set_max_length(3)
        self.__chaSpin.show()
        table.attach(self.__chaSpin, currentCol, currentCol + 1, currentRow, currentRow + 1, xoptions = gtk.SHRINK, yoptions = gtk.SHRINK)
        currentRow += 1
        currentCol = 0
        
        # skills section
        currentRow += 1
        self.__skillsAndSpins = []
        
        for skill in skills:
            l = gtk.Label(skill.get_name())
            l.show()
            table.attach(l, currentCol, currentCol + 1, currentRow, currentRow + 1, xoptions = gtk.SHRINK, yoptions = gtk.SHRINK)
            currentCol += 1
            
            s = gtk.SpinButton(gtk.Adjustment(value=0, lower=0, upper=100, step_incr=1))
            s.set_numeric(True)
            s.set_max_length(3)
            s.show()
            table.attach(s, currentCol, currentCol + 1, currentRow, currentRow + 1, xoptions = gtk.SHRINK, yoptions = gtk.SHRINK)
            currentRow += 1
            currentCol = 0
            
            self.__skillsAndSpins.append((skill, s))
        
        # ----- dialog action (bottom) area ----- #
        
        create = gtk.Button("Create")
        create.connect("clicked", self.create_creature)
        create.show()
        
        cancel = gtk.Button("Cancel")
        cancel.connect("clicked", self.close_dialog)
        cancel.show()
        
        self.__dialog.action_area.pack_start(create, True, True, 0)
        self.__dialog.action_area.pack_start(cancel, True, True, 0)
        
        # ----- show the dialog ----- #
        
        self.__dialog.show()
    
    def create_creature(self, widget, data = None):
        sks = SkillList(empty = True)
        for pair in self.__skillsAndSpins:
            sks.append(Skill( pair[0].get_name(), pair[0].get_associated_attributes(),
                              pair[0].get_opposing_skill(), pair[1].get_value_as_int() ))
            
        self.__creatureList.append( Creature(self.__nameEntry.get_text(), self.__strSpin.get_value_as_int(),
                                    self.__dexSpin.get_value_as_int(), self.__conSpin.get_value_as_int(),
                                    self.__intSpin.get_value_as_int(), self.__wisSpin.get_value_as_int(),
                                    self.__chaSpin.get_value_as_int(), skills = sks)
                                   )
        
        print "    %s created." % self.__nameEntry.get_text()
        self.__mainLog.insert_at_cursor("  Creature: %s created.\n" % self.__nameEntry.get_text())
        
        self.close_dialog(widget, "completed")
    
    def close_dialog(self, widget, data = None):
        print "    Creature creation Dialog closed."
        if data is not None:
            self.__mainLog.insert_at_cursor("Creature creation process %s.\n\n" % data)
        else:
            self.__mainLog.insert_at_cursor("Creature creation process aborted.\n\n")
        
        self.__dialog.destroy()

#------------------------------------------------------------------------------#

class ViewCreatureWindow:

    """
    This dialog allows the user to view the information for
    a chosen creature.
    
    Functions:
        close_window(widget,[data])
        __box_update(widget,[data])
    """
    
    def __init__(self, creatureList, log):
        self.__creatureList = creatureList
        self.__mainLog = log
        
        # create the window and set its options
        
        self.__window = gtk.Window()
        self.__window.set_title("View a Creature")
        self.__window.set_border_width(5)
        self.__window.set_size_request(410, 400)
        
        # create the window's contents
        
        ## top combo box holding creatureList
        
        self.__comboBox = gtk.combo_box_new_text()
        self.__comboBox.connect("changed", self.__box_update)
        self.__comboBox.show()
        
        for creature in self.__creatureList:
            self.__comboBox.append_text(creature.get_name())
        
        ## scrolled window contents
        
        scrolledWindow = gtk.ScrolledWindow()
        scrolledWindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrolledWindow.show()
        
        labels = []
        
        labels.append(gtk.Label("Creature Name"))
        
        labels.append(gtk.Label("Strength"))
        labels.append(gtk.Label("Dexterity"))
        labels.append(gtk.Label("Constitution"))
        labels.append(gtk.Label("Intelligence"))
        labels.append(gtk.Label("Wisdom"))
        labels.append(gtk.Label("Charisma"))
        
        labels.append(gtk.Label("Wound %"))
        labels.append(gtk.Label("Fatigue %"))
        labels.append(gtk.Label("Status Effect(s)"))
        
        skills = SkillList()
        for skill in skills:
            labels.append(gtk.Label(skill.get_name()))
        
        for label in labels:
            label.show()
        
        self.__values = []
        
        for i in range(len(labels)):
            width = 0
            if i == 0:
                width = 20
            elif i < 9 or i > 9:
                width = 3
            else:
                width = 20
            
            entry = gtk.Entry(0)
            entry.set_width_chars(width)
            entry.set_editable(False)
            entry.show()
            self.__values.append(entry)
        
        ### place labels and values on the table
        
        table = gtk.Table(rows=len(labels), columns=2)
        table.set_row_spacings(5)
        table.set_col_spacings(10)
        table.show()
        scrolledWindow.add_with_viewport(table)
        
        for i in range(len(labels)):
            labelAlign = gtk.Alignment(0.0, 0.5)
            labelAlign.show()
            labelAlign.add(labels[i])
            table.attach(labelAlign, 0, 1, i, i + 1, xpadding = 5)
            
            valueAlign = gtk.Alignment(0.0, 0.5)
            valueAlign.show()
            valueAlign.add(self.__values[i])
            table.attach(valueAlign, 1, 2, i, i + 1, xpadding = 5)
        
        ## bottom close button
        
        close = gtk.Button("Close")
        close.connect("clicked", self.close_window)
        close.show()
        
        buttonHBox = gtk.HBox(False, 0)
        buttonHBox.show()
        buttonHBox.pack_end(close, False, False, 0)
        
        # pack the window's contents into the window
        
        vbox = gtk.VBox(False, 0)
        vbox.show()
        vbox.pack_start(self.__comboBox, False, False, 0)
        vbox.pack_start(scrolledWindow, True, True, 5)
        vbox.pack_end(buttonHBox, False, False, 0)
        
        self.__window.add(vbox)
        
        # show the window
        
        self.__window.show()
    
    def close_window(self, widget, data = None):
        print "    Creature view window closed."
        self.__mainLog.insert_at_cursor("Creature view window closed.\n\n")
        
        self.__window.destroy()
    
    def __box_update(self, widget, data = None):
        creature = self.__creatureList.get_by_name(self.__get_combobox_active(widget))
        
        # set name
        self.__values[0].set_text(creature.get_name())
        
        # set ability scores
        scores = creature.get_attributes()
        self.__values[1].set_text(str(scores['Strength']))
        self.__values[2].set_text(str(scores['Dexterity']))
        self.__values[3].set_text(str(scores['Constitution']))
        self.__values[4].set_text(str(scores['Intelligence']))
        self.__values[5].set_text(str(scores['Wisdom']))
        self.__values[6].set_text(str(scores['Charisma']))
        
        # set health stats
        self.__values[7].set_text(str(creature.get_wound_percentage()))
        self.__values[8].set_text(str(creature.get_fatigue_percentage()))
        self.__values[9].set_text(", ".join(["%s" % k for k in creature.get_status_effects()]))
        
        # set skill values
        skills = creature.get_skills("list of Skill")
        s = 0
        for i in range(10, len(self.__values)):
            self.__values[i].set_text(str(skills[s].get_level()))
            s += 1
        
        
        
    def __get_combobox_active(self, comboBox):
        model = comboBox.get_model()
        active = comboBox.get_active()
        if active < 0:
            return None;
        return model[active][0]

#------------------------------------------------------------------------------#

