# File that contains the logic necessary to create and have a mafia game
# Author - Oscar Filson
# Date - 11/15/2020

import random

class game(object):

    def __init__(self):
        self.players = {}
        self.roles = {}
        self.roles['villager'] = 0

    # Adds a new player with the role of villager
    def addPlayer(self, id):
        self.players[id] = 'villager'
        self.roles['villager'] = self.roles.get('villager') + 1

    # Returns the role of the player whose id was specified
    def getRole(self, id):
        if self.players.get(id) is None:
            print("That player doesn't exist")
            return -1
        else:
            return self.players.get(id)

    def getRoles(self):
        return self.roles

    # Removes player with matching ID
    def removePlayer(self, id):
        if self.players.get(id) is None:
            print("That player not found")
        elif self.players.get(id) == 'villager':
            del self.players[id]
            self.roles['villager'] = self.roles.get('villager') - 1
        else:
            del self.players[id]
            self.roles['villager'] = self.roles.get('villager') - 1
            self.assignRoles()

    # Removes all players in the dict, and sets roles to 0
    def removeAllPlayers(self):
        self.players.clear()
        for role in self.roles.keys():
            self.roles[role] = 0

    # Adds a role and its quantity to the roles dict
    def addRole(self, name, quantity):
        if quantity >= len(self.players):
            print("Not enough players to have that amount of roles")
            return -1
        else:
            self.roles[name] = quantity
            self.roles['villager'] = self.roles.get('villager') - quantity
            return 0

    # Removes a role from the dictionary
    def removeRole(self, name):
        if self.roles.get(name) is None:
            print("Role doesn't exist")
        else:
            self.roles['villager'] = self.roles.get('villager') + self.roles.get(name)
            del self.roles[name]

    # Updates the quantity of a role, and updates villagers to keep overall amount
    def updateRole(self, name, newNum):
        if newNum >= len(self.players):
            return "Not enough players to have that amount of roles"
        elif self.roles.get(name) is None:
            return "Role doesn't exist"
        else:
            currNum = self.roles.get(name)
            dif = currNum - newNum
            if dif == 0:
                return "Same number as before, no change"
            else:
                self.roles['villager'] = self.roles.get('villager') + dif
                self.roles[name] = newNum

    # Removes all roles in the dictionary
    def removeAllRoles(self):
        self.roles.clear()

    # Clears both players and roles from the dictionary
    def clearAll(self):
        self.removeAllPlayers()
        self.removeAllRoles()

    def resetRoles(self):
        for key in self.players.keys():
            self.players[key] = 'villager'

    # Assigns the roles in roles to the players in players randomly.
    def assignRoles(self):
        self.resetRoles()
        if self.roles != {} and self.players != {}:
            for role in self.roles.keys():
                if role == 'villager':
                    continue
                for x in range(self.roles.get(role)):
                    oldRole = ''
                    while oldRole != 'villager':
                        id, oldRole = random.choice(list(self.players.items()))
                    self.players[id] = role
        else:
            print("roles or players is empty")

    # Outputs a string representing the current values in the game.
    def printGame(self):
        print(self.roles)
        print(self.players)

    # Returns a string representing the current values in the game.
    def getGame(self):
        return ('Roles:' + str(self.roles) + '\nPlayers' + str(self.players))
