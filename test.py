# File that contains the logic necessary to create and have a mafia game
# Author - Oscar Filson
# Date - 11/15/2020

from mafia import game

game = game()
for x in range(6):
    name = 'Player' + str(x+1)
    game.addPlayer(name)
game.printGame()
game.addRole('mafia', 1)
game.printGame()
game.updateRole('mafia', 2)
game.printGame()
game.addPlayer('Player7')
game.printGame()
# game.removePlayer('Player8')
# game.printGame()
# game.removeRole('mafia')
# game.printGame()
# game.clearAll()
# game.printGame()
game.assignRoles()
game.printGame()
print(game.getRole("Player1"))
print(game.getQuantity("mafia"))
game.removePlayer("Player1")
game.printGame()
game.assignRoles()
game.printGame()
game.assignRoles()
game.printGame()
print(game.getGame())