#bot.py
import os
import random
import discord
from mafia import game
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='mafia ')
mafiaGame = None
players = {}

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='usage', help='Displays the various commands and their usage')
async def usage(ctx):
    output = ''
    output += 'mafia open - Opens a new game, must be done before any other commands\n'
    output += 'mafia join - Adds you to the current open game, there must be a game open to work\n'
    output += 'mafia add_role \{role_name\} \{role_quantity\} - Adds a role to the game defaulted to mafia with quanitity of 1\n'
    output += 'mafia start - assigns the roles set to everyone in the lobby and dm\'s everyone their role\n'
    output += 'mafia update_role \{role_name\} \{role_quantity\} - Updates a role already in the game, defaults to mafia with quanitity of 1\n'
    output += 'mafia vote \{player_name\} \{player_role\} - Checks if that person has the role (default mafia) and dm\'s the result to you\n'
    output += 'mafia output - Sends a message showing the current values for players and roles\n'
    output += 'mafia close - Closes the current game, must use mafia open before anything else can be done'
    await ctx.send(output)

@bot.command(name='open', help='Opens up a game for people to join')
async def open(ctx):
    global mafiaGame

    mafiaGame = game()
    await ctx.send('You have opened up a game! Use mafia join to join the game')

@bot.command(name='join', help='adds you to the game')
async def open(ctx):
    global mafiaGame
    global players

    if mafiaGame is not None:
        id = str(ctx.message.author)
        idx = id.find('#')
        id = id.split('#',1)[0]
        mafiaGame.addPlayer(id)
        players[id] = ctx.message.author
        await ctx.send(id +  ' has joined the game')
    else:
        await ctx.send('A game is not open! Use mafia open to start a game')

@bot.command(name='add_role', help='Adds a role to the game')
async def add_role(ctx, role_name='mafia', role_num=1):
    global mafiaGame

    if mafiaGame is not None:
        err = mafiaGame.addRole(role_name, role_num)
        if err == -1:
            await ctx.send("Not enough players to have that amount of roles")
        else:
            await ctx.send("Successfully added " + role_name + " with a quantity of " + str(role_num))
    else:
        await ctx.send('A game is not open! Use mafia open to start a game')

@bot.command(name='update_role', help='Updates a role currently in the game')
async def update_role(ctx, role_name='mafia', role_num=1):
    global mafiaGame

    if mafiaGame is not None:
        err = mafiaGame.updateRole(role_name, role_num)
        if err is not None:
            await ctx.send('Error: ' + err)
        else:
            await ctx.send("Successfully updated " + role_name + " to the quantity of " + str(role_num))
    else:
        await ctx.send('A game is not open! Use mafia open to start a game')

@bot.command(name='start', help='Assigns everyone in the game a role from the list of roles and dm\'s them their result.')
async def assign_roles(ctx):
    global mafiaGame
    global players

    # If a role other than villager doesn't exist, add a mafia
    roles = mafiaGame.getRoles()
    if len(roles) <= 1:
        mafiaGame.addRole('mafia', 1)

    # Assign roles
    mafiaGame.assignRoles()

    # Send a DM to everyone in the game and tell them their role
    for player in players:
        num = 0
        role = mafiaGame.getRole(player)
        await players[player].send(player + ' you are a ' + role)
        # if role == 'mafia':
        #     await players[player].send(mafiaGame.getGame())
        #     if num == 1:
        #         await players[player].send('Can\'t save')
        #     else:
        #         await players[player].send('Can\'t score')
        #     num += 1


@bot.command(name='vote', help='checks the role of a player and sends the result to you')
async def vote(ctx, player_name=None, role_name='mafia'):
    global mafiaGame

    if player_name is None:
        await ctx.send('You didn\'t set a player name, usage for mafia vote is as follows: mafia vote player_name role_name (role_name is optional)')
    elif mafiaGame is not None:
        retVal = mafiaGame.getRole(player_name)
        if retVal == -1:
            await ctx.send('The player with the name ' + player_name + ' doesn\'t not exist in this game. Use mafia output to see the current game values.')
        elif retVal == role_name:
            await ctx.author.send(player_name + ' is ' + role_name + ', good job.')
        else:
            await ctx.author.send(player_name + ' is not ' + role_name + ', idiot.')
    else:
        await ctx.send('A game is not open! Use mafia open to start a game')

@bot.command(name='output', help='sends a message showing the current game state')
async def output(ctx):
    global mafiaGame

    if mafiaGame is not None:
        await ctx.send(mafiaGame.getGame())
    else:
        await ctx.send('A game is not open! Use mafia open to start a game')

@bot.command(name='close', help='Ends an open game')
async def close(ctx):
    global mafiaGame

    mafiaGame = None
    await ctx.send('Game has been closed! See you sometime soon hopefully :)')

bot.run(TOKEN)