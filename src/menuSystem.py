
#   author: Respen

from creatureInfo import Creature
    
#------------------------------------------------------------------------------#

class MenuSystem:

    """
    Manager class for the SkillDnD CLI menu system.
    
    Functions:
        mainMenuDisplay()   -> returns user's choice
        runMenuSystem()
        createCharacter()
        viewCharacter()
        useCharacter()
        saveCharacter()
        loadCharacter()
    """
    
    def __init__(self):
        self.creatureList = []
    
    def mainMenuDisplay(self):
        print """
        +~~~~~~~ SkillDnD Main Menu ~~~~~~~~+
        | 1 | Create a character            |
        | 2 | View a character              |
        | 3 | Use a character's skills      |
        | 4 | Save a character to a file    |
        | 5 | Load a character from file    |
        | Q | Quit the program              |
        +~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+
        """
        
        return raw_input("  Enter your choice: ")
        
    def runMenuSystem(self):
        menuChoice = self.mainMenuDisplay()
        
        while menuChoice != 'q' or menuChoice != 'Q':
            print
            
            if menuChoice == '1':
                self.createCharacter()
            elif menuChoice == '2':
                self.viewCharacter()
            elif menuChoice == '3':
                self.useCharacter()
            elif menuChoice == '4':
                self.saveCharacter()
            elif menuChoice == '5':
                self.loadCharacter()
            elif menuChoice == 'Q' or menuChoice == 'q':
                print "  Thank you for using this program."
                print
                break
            else:
                print "  Invalid option, try again."
                
            menuChoice = self.mainMenuDisplay()
            
    def createCharacter(self):
        print "Character creation process initiated."
        
        charName = raw_input(" Enter the character's name: ")
        
        strength = input(" Enter strength score: ")
        dexterity = input(" Enter dexterity score: ")
        constitution = input(" Enter constitution score: ")
        intelligence = input(" Enter intelligence score: ")
        wisdom = input(" Enter wisdom score: ")
        charisma = input(" Enter charisma score: ")
        
        if charName != "":
            self.creatureList.append(Creature(charName, strength, dexterity, constitution, intelligence, wisdom, charisma))
        else:
            self.creatureList.append(Creature("Joe Blarg", strength, dexterity, constitution, intelligence, wisdom, charisma))
        
    def viewCharacter(self):
        print "Preparing to view a character..."
        creature = self.__creatureChooser()
        print
        print "=============================="
        print self.__creatureToString(creature)
        print "=============================="
        print
        
    def useCharacter(self):
        print "Preparing for character skill usage..."
        creature = self.__creatureChooser()
    
    def saveCharacter(self):
        print "Preparing to save a character to a file..."
        creature = self.__creatureChooser()
        
    def loadCharacter(self):
        print "Preparing to load a character from a file..."
        
    def __creatureChooser(self):
        print
        print " +=== Creature Chooser ===+"
        
        i = 1
        for creature in self.creatureList:
            print "  ", str(i) + ".", creature.get_name()
            i += 1
        print
        
        choice = input(" Enter the number of the character you want to view: ")
        while choice not in range(1,i):
            print "  Invalid option, try again."
            choice = input(" Enter the number of the character you want to view: ")
            
        return self.creatureList[choice - 1]
    
    def __creatureToString(self, creature):
        # setup the creature's name for output
        creatureNameString = " Name: " + creature.get_name()
        
        # setup the creature's ability scores for output
        abilityScores = creature.get_ability_scores()
        abilityScoresString = "\n".join([" %s: %d" % (k, v) for k, v in abilityScores.items()])
        
        # setup the creature's health for output
        healthString = " Wound Percentage: " + str(creature.get_wound_percentage()) + "%\n"
        healthString += " Fatigue Percentage: " + str(creature.get_fatigue_percentage()) + "%\n"
        healthString += " Status Effects: "
        if len(creature.get_status_effects()) == 0:
            healthString += "None"
        else:
            healthString += ",".join([" %s" % i for i in creature.get_status_effects()])
        
        # join each section and return the whole string
        return creatureNameString + "\n\n" + abilityScoresString + "\n\n" + healthString
    
#------------------------------------------------------------------------------#

if __name__ == "__main__":
    menu = MenuSystem()
    menu.runMenuSystem()
