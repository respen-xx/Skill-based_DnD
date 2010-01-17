
#   author: Respen (respen@gmail.com)

from random import randint
from math import sqrt

"""
This module contains the classes for skills.

Classes
    Skill
    SkillList
"""
    
#------------------------------------------------------------------------------#

class Skill:

    """
    A class which defines the behavior of skills.
    
    Functions:
        get_level()                         -> returns the level value
        get_exp()                           -> returns the experience value
        get_description()                   -> returns the description string
        get_name()                          -> returns the name string
        get_associated_attributes()         -> returns list of attribute names
        get_opposing_skill()                -> returns the opposing skill's name
        set_description(string:newDesc)     -> sets description to newDesc
        level_up(int:numOfLevels)           -> levels up this skill by numOfLevels and resets experience to zero
        gain_exp(int:skillCheckResult)      -> 
        use(int:attributeBonus[, int:difficulty, Creature:target, int:modifiers])    -> returns an int rating the success
    """

    def __init__(self, name, associatedAttributes, oppSk = None, lvl = 0, exp = 0, description = "No description given."):
        self.__level = lvl
        self.__experience = exp
        self.__description = description
        self.__name = name
        self.__associatedAttributes = associatedAttributes
        self.__opposingSkill = oppSk
        
    def get_level(self):
        return self.__level
        
    def get_exp(self):
        return self.__experience
        
    def get_description(self):
        return self.__description
    
    def get_name(self):
        return self.__name
    
    def get_associated_attributes(self):
        return self.__associatedAttributes
    
    def get_opposing_skill(self):
        return self.__opposingSkill
    
    def set_description(self, newDesc):
        self.__description = newDesc
        
    def level_up(self, numOfLevels = 1):
        self.__level += numOfLevels
        self.__experience = 0
        
    def gain_exp(self, skillCheckResult):
        # determine gained experience using the skill check's result
        expGain = 0
        if skillCheckResult >= 0:
            expGain = 15 - skillCheckResult
        elif skillCheckResult < 0 and skillCheckResult >= -5:
            expGain = 6 + skillCheckResult
        
        # apply gained experience
        self.__experience += expGain
        
        # check for a level up, and perform it if necessary
        if self.__experience >= 100:
            self.__level_up()
    
    def use(attributeBonus, dc = 0, target = None, modifiers = 0):
        # perform creature's roll
        roll = self.__level + attributeBonus + modifiers + randint(1, 20)
        
        # determine the result
        if target is not None and self.__opposingSkill is not None:
            # determine difficulty for the target and then call for their response
            result = target.use_skill(self.__opposingSkill, roll)
        else:
            result = roll - dc
        
        # gain experience for using the skill
        self.gain_exp(result)
            
        # return a rating of the success (int for now)
        return result
                
#------------------------------------------------------------------------------#

class SkillList(list):

    """
    A subclass of the list datatype which displays different types of skills.
    
    Functions:
        get_all_skill_names()          -> returns a list of names of all of the
                                        skills in the master list
        get_skill(string:name)       -> returns the skill whose name is passed
    """
    
    def __init__(self, empty = False):
        list.__init__(self)
        
        if not empty:
            # now add all known skills to self's list
            self.append(Skill("Attack", ["Strength", "Dexterity"], "Defense"))
            self.append(Skill("Defense", ["Dexterity", "Constitution"]))
            self.append(Skill("Magic", ["Constitution", "Intelligence", "Wisdom"]))
    
    def get_all_skill_names(self):
        allSkillNames = []
        for i in self:
            allSkillNames.append(i.get_name())
            
        return allSkillNames
    
    def get_skill(self, name):
        return self[self.index(name)]
    
#------------------------------------------------------------------------------#

