# IMPORT DISCORD.PY. ALLOWS ACCESS TO DISCORD'S API.
import discord
from discord.ext import commands
import discord_token

# Tekken stuff
class player:
    def __init__(self, char, curr_move=None, owner=None, hp = 175, frame_adv = 0):
        self.moves = char
        self.hp = hp
        self.frame_adv = frame_adv
        self.owner = owner
        self.curr_move = curr_move

class move:
    def __init__(self, name, startup, nh_dmg, ch_dmg, trade_dmg, onNH, onCH, onBlock, onWhiff, height, cs, js, type):
        self.name = name
        self.startup = startup
        self.nh_dmg = nh_dmg
        self.ch_dmg = ch_dmg
        self.onNH = onNH
        self.onCH = onCH
        self.trade_dmg = trade_dmg
        self.onBlock = onBlock
        self.onWhiff = onWhiff
        self.height = height
        self.cs = cs
        self.js = js 
        self.type = type

# Character Movesets
djin = [
        move( "Standing Block", 1, 0, 0, None, 0, 0, 0, 0, "stand block", None, None, "defensive"),
        move( "Crouching Block", 1, 0, 0, None, 0, 0, 0, 0, "low block" , None, None, "defensive"),
        move( "Low Parry", 3, 40, 40, None, 0, 0, 0, 0, "low parry", 0, None, "defensive"),
        move( "1", 10, 7, 10, None, 8, 8, 1, -5, "high", None, None, "normal"),
        move( "112", 10, 25, 28, None, 8, 8, -1, -5, "high", None, None, "normal"),
        move( "ewgf", 14, 60, 65, 28, 0, 0, 5, -11, "high", None, None, "normal"),
        move( "df1", 13, 11, 13, None, 8, 8, -3, None, "mid", None, None, "normal"),
        move( "df1,2", 13, 11, 28, None, -8, 3, -8, None, "mid", None, None, "normal"),
        move( "df2", 15, 15, 50, 18, 4, 0, -7, None, "mid", None, None, "normal"),
        move( "b4", 17, 20, 50, 24, 6, 0, -8, None, "mid", None, None, "normal"),
        move( "uf4", 18, 21, 25, 25, 9, 9, -8, None, "mid", None, 8, "normal"),
        move( "u4", 20, 60, 64, 26, 9, 9, -26, None, "mid", None, 8, "normal"),
        move( "ss2", 26, 70, 70, 30, 9, 9, -22, None, "mid", None, None, "normal"),
        move( "d4", 12, 7, 10, None, -2, -2, -13, None, "low", 4, None, "normal"),
        move( "d3", 18, 14, 16, None, -1, 7, -12, None, "low", None, None, "normal"),
        move( "db2", 22, 15, 30, 18, 3, 8, -13, None, "low", 6, None, "normal"),
        move( "cd4,4", 19, 38, 40, 12, 4, 4, -23, None, "low", None, None, "normal")
        ]

# Player Values
start = False
players = []

p1 = player(char=djin)
p2 = player(char=djin)
# Turn Functions
def normal_hit(attacker, defender, move):
    attacker.frame_adv = move.onNH
    defender.frame_adv = 0 - move.onNH
    defender.hp -= move.nh_dmg

def counter_hit(attacker, defender, move):
    attacker.frame_adv = move.onCH
    defender.frame_adv = 0 - move.onCH
    defender.hp -= move.ch_dmg

def block(attacker, defender, move):
    attacker.frame_adv = move.onBlock
    defender.frame_adv = 0 - move.onBlock

def whiff(attacker, defender, move):
    attacker.frame_adv = move.onWhiff
    defender.frame_adv = 0 - move.onWhiff


def block_check(p1, p2, p1_move, p2_move):
    if p1_move.startup - p1.frame_adv <= p2_move.startup:
        if p1_move.height == "stand block":
            if p2_move.height == "low":
                normal_hit(p2, p1, p2_move)

            else:
                block(p2, p1, p2_move)
    
        elif p1_move.height == "low block":
            if p2_move.height == "mid":
                normal_hit(p2, p1, p2_move)

            elif p2_move.height == "high":
                whiff(p2, p1, p2_move)
        
            else:
                block(p2, p1, p2_move)

        elif p1_move.height == "low parry":
           if p2_move.height == "low":
               normal_hit(p1, p2, p1_move)
           elif p2_move.type == "defensive":
               whiff(p2, p1, p2_move)
           elif p2_move.height == "high":
               whiff(p2, p1, p2_move)
           else:
               normal_hit(p2, p1, p2_move)
    else: 
        normal_hit(p2, p1, p2_move)

def crush_check(p1, p2, p1_move, p2_move):
    if p1_move.height == "low":
        if p2_move.js is not None and p2_move.js - p2.frame_adv <= p1_move.startup:
            if p2_move.startup - p2.frame_adv <= p1_move.startup:
                counter_hit(p2, p1, p2_move)
            else:
                normal_hit(p2, p1, p2_move)

        else:
            trade_check(p1, p2, p1_move, p2_move)
    
    elif p1_move.height == "high":
        if p2_move.cs is not None and p2_move.cs - p2.frame_adv <= p1_move.startup:
            if p2_move.startup - p2.frame_adv <= p1_move.startup:
                counter_hit(p2, p1, p2_move)
            else:
                normal_hit(p2, p1, p2_move)

        else:
            trade_check(p1, p2, p1_move, p2_move)
    
    else:
        trade_check(p1, p2, p1_move, p2_move)


def trade_check(p1, p2, p1_move, p2_move):
    if p1_move.startup - p1.frame_adv < p2_move.startup:
        counter_hit(p1, p2, p1_move)
    elif p1_move.startup - p1.frame_adv > p2_move.startup:
        counter_hit(p2, p1, p2_move)
    elif p1_move.trade_dmg != None and p2_move.trade_dmg != None:
        p1.frame_adv = 0
        p2.frame_adv = 0
        p2.hp -= p1_move.trade_dmg
        p1.hp -= p2_move.trade_dmg
    else:
        p1.frame_adv = p1_move.onCH - p2_move.onCH
        p2.frame_adv = p2_move.onCH - p1_move.onCH
        p2.hp -= p1_move.ch_dmg
        p1.hp -= p2_move.ch_dmg
        

def turn(p1_move, p2_move, p1 = p1, p2 = p2):
    if p1_move.type == "defensive":
        block_check(p1, p2, p1_move, p2_move)
    elif p2_move.type == "defensive":
        block_check(p2, p1, p2_move, p1_move)
    
    elif p1_move.cs != None or p1_move.js != None:
        crush_check(p2, p1, p2_move, p1_move)
    elif p2_move.cs != None or p2_move.js != None:
        crush_check(p1, p2, p1_move, p2_move)

    else: trade_check(p1, p2, p1_move, p2_move)

def game_over(p1=p1, p2=p2, start=start):
    p1.hp = 175
    p2.hp = 175
    p1.frame_adv = 0
    p2.frame_adv = 0
    start = False

# GETS THE CLIENT OBJECT FROM DISCORD.PY. CLIENT IS SYNONYMOUS WITH BOT.
bot = discord.Client()
bot = commands.Bot(command_prefix='!t1b ')
current_channel = None
# EVENT LISTENER FOR WHEN THE BOT HAS SWITCHED FROM OFFLINE TO ONLINE.
@bot.event
async def on_ready():
	# CREATES A COUNTER TO KEEP TRACK OF HOW MANY GUILDS / SERVERS THE BOT IS CONNECTED TO.
	guild_count = 0

	# LOOPS THROUGH ALL THE GUILD / SERVERS THAT THE BOT IS ASSOCIATED WITH.
	for guild in bot.guilds:
		# PRINT THE SERVER'S ID AND NAME.
		print(f"- {guild.id} (name: {guild.name})")

		# INCREMENTS THE GUILD COUNTER.
		guild_count = guild_count + 1

	# PRINTS HOW MANY GUILDS / SERVERS THE BOT IS IN.
	print("T1B is in " + str(guild_count) + " guilds.")

# EVENT LISTENER FOR WHEN A NEW MESSAGE IS SENT TO A CHANNEL.
@bot.command()
async def play(ctx):
	# CHECKS IF THE MESSAGE THAT WAS SENT IS EQUAL TO "HELLO".
            if len(players) == 2:
                await ctx.send("Two people are already playing.")

            elif len(players) == 0:
                players.append(ctx.author)
                await ctx.send(f"{ctx.author} has been set to Player 1.")

            
            elif len(players) == 1:
                #if ctx.author in players:
                #    await ctx.send(f"{ctx.author} is already playing.")
                #else:
                    players.append(ctx.author)
                    await ctx.send(f"{ctx.author} has been set to Player 2. \"Type !t1b start\" to begin.")

@bot.command()
async def remove(ctx):
            if ctx.author in players:
                global start
                if start == True:
                    await ctx.send(f"Game has been stopped due to {ctx.author} leaving.")
                    start = False
                players.remove(ctx.author)
                await ctx.send(f"{ctx.author} has been removed from the game.")
            else:
                await ctx.send(f"{ctx.author} is not playing currently.")

@bot.command()
async def remove_all(ctx):
            global start
            if start == True:
                await ctx.send(f"Game is currently in progress.")
            else:
                players.clear()
                await ctx.send(f"All players have been removed from the queue.")

@bot.command()
async def start(ctx):
        if ctx.author in players:
            if len(players) == 2:
                await ctx.send(f"Starting: {players[0]} VS {players[1]}")
                global start
                start = True
                
                if ctx.channel.type is not discord.ChannelType.private:
                    global current_channel 
                    current_channel = ctx.channel

                p1.owner = players[0]
                p2.owner = players[1]

                for player in [p1, p2]:
                    movelist = []
                    for moves in player.moves:
                        movelist.append(moves.name)
                    await player.owner.send(f"Use '!t1b move your_move_here' to do a move!\nAvailable Moves: {movelist}\n{p1.owner} HP: {player.hp}, {p2.owner} HP: {p2.hp}, Frame Advantage: {player.frame_adv}")

            else:
                await ctx.send("Not enough players.")
        else:
            await ctx.send("Only a player can start the match.")

@bot.command()
async def move(ctx, arg):
    if start == False:
        await ctx.send("Match has not started yet.")

    elif ctx.author in players:
        for player in [p1, p2]:
            if player.owner == ctx.author:
                for moves in player.moves:
                    if arg == moves.name:
                        player.curr_move = moves
                        await ctx.send(f"{ctx.author} chose to do {arg}.")
                        break
                if player.curr_move == None:
                    await ctx.send(f"The move {arg} was not found.")
                break

        if p1.curr_move != None and p2.curr_move != None:
            turn(p1.curr_move, p2.curr_move)
            await p1.owner.send(f"{p1.owner} did {p1.curr_move.name}! \n{p2.owner} did {p2.curr_move.name}!\n{p1.owner} HP: {p1.hp}, {p2.owner} HP: {p2.hp}, Frame Advantage: {p1.frame_adv}")
            await p2.owner.send(f"{p1.owner} did {p1.curr_move.name}! \n{p2.owner} did {p2.curr_move.name}!\n{p1.owner} HP: {p1.hp}, {p2.owner} HP: {p2.hp}, Frame Advantage: {p2.frame_adv}")

            if current_channel != None:
                await current_channel.send(f"{p1.owner} did {p1.curr_move.name}! \n{p2.owner} did {p2.curr_move.name}!\n{p1.owner} HP: {p1.hp}, {p2.owner} HP: {p2.hp}, Frame Advantage: {p1.frame_adv}")

            p1.curr_move = None
            p2.curr_move = None

            if p1.hp <= 0 and p2.hp <= 0:
                await p1.owner.send("Draw!")
                await p2.owner.send("Draw!")
                game_over()

            elif p1.hp <= 0:
                await p1.owner.send(f"{p1.owner} lost to {p2.owner}!")
                await p2.owner.send(f"{p1.owner} lost to {p2.owner}!")
                game_over()

            elif p2.hp <= 0:
                await p1.owner.send(f"{p2.owner} lost to {p1.owner}!")
                await p2.owner.send(f"{p2.owner} lost to {p1.owner}!")
                game_over()

    else:
        await ctx.send("You are not a player.")

bot.run(discord_token.token)
