
#   author: Respen (respen@gmail.com)

"""
This module contains classes to describe a creature.

Classes:
    Creature
    Health
    CreatureList
"""

from skillInfo import SkillList
    
#------------------------------------------------------------------------------#

class Creature:

    """
    The SkillDnD class which holds and manages a creature.
    
    Functions:
        get_name()                -> returns the creature's name string
        get_attributes()           -> returns a dictionary with keys of attribute
                                    name, and values equal to the attribute's value
        get_skills([string:whatToReturn]) -> returns a list of the creature's skills
        get_wound_percentage()    -> returns the value for the creature's wound
                                    point percentage
        get_status_effects()      -> returns a list of status effects affecting
                                    the creature
        get_fatigue_percentage()  -> returns the value for the creature's fatigue
                                    percentage
        use_skill(string:skillName[,int:difficulty,Creature:target, int:modifiers]) -> returns a
                                    value indicating the degree of success of
                                    the action
    """
    
    def __init__(self, name, strength = 0, dexterity = 0, constitution = 0,
                 intelligence = 0, wisdom = 0, charisma = 0, wp = -1, fatigue = -1,
                 status = ["None"], skills = None):
        self.__name = name
        self.__attributes = { "Strength"     : strength,
                              "Dexterity"    : dexterity,
                              "Constitution" : constitution,
                              "Intelligence" : intelligence,
                              "Wisdom"       : wisdom,
                              "Charisma"     : charisma }
                             
        self.__health = Health(self.__attributes["Constitution"],
                               self.__attributes["Strength"],
                               status, wp, fatigue)
        
        if skills is not None:
            self.__skills = skills
        else:
            self.__skills = SkillList()
                           
    def get_name(self):
        return self.__name
        
    def get_attributes(self):
        return self.__attributes
    
    def get_skills(self, whatToReturn = "all names"):
        if whatToReturn == "list of Skill":
            return self.__skills
        else:
            return self.__skills.get_all_skill_names()
    
    def get_wound_percentage(self):
        return self.__health.get_wound_percentage()
        
    def get_status_effects(self):
        return self.__health.get_status()
    
    def get_fatigue_percentage(self):
        return self.__health.get_fatigue_percentage()
        
    def use_skill(self, skillName, difficulty = 0, target = None, modifiers = 0):
        # set initial variables
        skill = self.__skills.get_skill(skillName)
        attributeBonus = 0
        for i in skill.get_associated_attributes():
            attributeBonus += int((self.__attributes[i] - 10) / 2)
        
        return skill.use(attributeBonus, difficulty, target, modifiers)
            
#------------------------------------------------------------------------------#

from math import sqrt

class Health:

    """
    A management class controlling a creature's health.
    
    Functions:
        get_max_wp()                            -> returns the max wound point value
        get_current_wp()                        -> returns the current wp value
        get_wound_percentage()                  -> returns percent of wounds in int
        get_status()                            -> returns a list of status effects
        get_max_fatigue()                       -> returns max fatigue value
        get_current_fatigue()                   -> returns current fatigue value
        get_fatigue_percentage()                -> returns percent of fatigue in int
        damage_wp(int:amount)                   -> returns modified wp,
                                                    and raises death exception if
                                                    health goes to zero or past
        heal_wp(int:amount)                     -> returns modifed wp
        add_status_effect(string:effect)        -> adds effect to status listing
        remove_status_effect(string:effect)     -> returns the effect removed
        recover_fatigue(int:amount)             -> returns modified fatigue value
        drain_fatigue(int:amount)               -> returns modified fatigue value
    """
    
    def __init__(self, conScore, strScore, status = ["None"], curWP = -1, curFatigue = -1):
        self.__maxWoundPoints = conScore
        
        if curWP == -1:
            self.__currentWoundPoints = self.__maxWoundPoints
        else:
            self.__currentWoundPoints = curWP
        
        self.__status = status
        
        self.__maxFatigue = self.__maxWoundPoints + strScore
        
        if curFatigue == -1:
            self.__currentFatigue = self.__maxFatigue
        else:
            self.__currentFatigue = curFatigue
        
    def get_max_wp(self):
        return self.__maxWoundPoints
        
    def get_current_wp(self):
        return self.__currentWoundPoints
    
    def get_wound_percentage(self):
        percentage = 100
        
        try:
            percentage = int( 100.0 * ( float(self.__currentWoundPoints) / float(self.__maxWoundPoints) ) )
        except ZeroDivisionError:
            pass
        
        return percentage
    
    def get_status(self):
        return self.__status
        
    def get_max_fatigue(self):
        return self.__maxFatigue
    
    def get_current_fatigue(self):
        return self.__currentFatigue
    
    def get_fatigue_percentage(self):
        percentage = 100
        
        try:
            percentage = int( 100.0 * ( float(self.__currentFatigue) / float(self.__maxFatigue) ) )
        except ZeroDivisionError:
            pass
        
        return percentage
    
    def damage_wp(self, amount = 1):
        self.__currentWoundPoints -= amount
        
        if self.__currentWoundPoints <= 0:
            # raise death exception
            pass
            
        return self.__currentWoundPoints
    
    def heal_wp(self, amount = 1, fullRecover = False):
        if fullRecover:
            self.__currentWoundPoints = self.__maxWoundPoints
        else:
            self.__currentWoundPoints += amount
        
            if self.__currentWoundPoints > self.__maxWoundPoints:
                self.__currentWoundPoints = self.__maxWoundPoints
        
        return self.__currentWoundPoints
    
    def add_status_effect(self, effect):
        if self.__status.find("None") > 0:
            self.__status.remove("None")
        
        self.__status.append(effect)
    
    def remove_status_effect(self, effect):
        returnee = self.__status.remove(effect)
        
        if len(self.__status) == 0:
            self.__status.append("None")
        
        return returnee
    
    def recover_fatigue(self, amount = 1, fullRecover = False):
        if fullRecover:
            self.__currentFatigue = self.__maxFatigue
        else:
            self.__currentFatigue += amount
        
            if self.__currentFatigue > self.__maxFatigue:
                self.__currentFatigue = self.__maxFatigue
        
        return self.__currentFatigue
    
    def drain_fatigue(self, amount = 1):
        self.__currentFatigue -= amount
        
        if self.__currentFatigue < 0:
            pastAmount = -1 * self.__currentFatigue
            self.__currentFatigue = 0
            # raise exception, passing on pastAmount
        
        return self.__currentFatigue
    
#------------------------------------------------------------------------------#

class CreatureList(list):
    """
    A subclass of the list type which manages a list of creatures.
    
    Functions:
        remove_by_name(string:name)
        get_by_name(string:name)
        find_index_by_name(string:name)
    """
    
    def __init__(self):
        list.__init__(self)
    
    def remove_by_name(self, name):
        index = self.find_index_by_name(name)
        
        # remove the creature from the list if it was found
        if index >= 0:
            return self.pop(index)
    
    def get_by_name(self, name):
        return self[self.find_index_by_name(name)]
    
    def find_index_by_name(self, name):
        for i in range(len(self)):
            if self[i].get_name() == name:
                return i
                
        # if creature not found return a value beyond bounds of the list
        return -1
    
#------------------------------------------------------------------------------#

if __name__ == "__main__":
    print
    l = CreatureList()
    l.append(Creature("Bob"))
    l.append(Creature("Joe"))
    l.append(Creature("Woof"))
    l.append(Creature("Rawr!"))
    print l
    print
    print l.find_index_by_name("Woof")
    print l.get_by_name("Woof")
    print
    print l.find_index_by_name("Joe")
    print l.remove_by_name("Joe")
    print
    print l
    print
