import discord
from discord.ext import commands
import datetime
import sqlite3
import traceback
import sys

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='-', case_insensitive=True, description='sanic_bot', help_command=None, intents=intents)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Prefix: -"))

@bot.event
async def on_message(ctx):
    print(f'[MSG LOG] {ctx.author.name} ({ctx.author.id}): {ctx.content}')
    await bot.process_commands(ctx)

@bot.command()
async def ping(ctx):
    print('{} - {} ({}) in {} -> {}'.format(datetime.datetime.now(), ctx.author.name, ctx.author.id, ctx.guild, 'Ping'))
    await ctx.send('Pong! {0}ms'.format(round(bot.latency*1000, 5)))

@bot.command()
async def player(ctx):
    name = f"{ctx.author.name}{ctx.author.discriminator}"
    
    try:
        sqliteConnection = sqlite3.connect('SQLite_Python.db')
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")

        sqlite_insert_query = f"""INSERT INTO usuarios
                            (nombre, creditos) VALUES  ('{name}', 0)"""

        count = cursor.execute(sqlite_insert_query)
        sqliteConnection.commit()
        print("Record inserted successfully.", cursor.rowcount)
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table")
        print("Exception class is: ", error.__class__)
        print("Exception is", error.args)
        print('Printing detailed SQLite exception traceback: ')
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(traceback.format_exception(exc_type, exc_value, exc_tb))
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("The SQLite connection is closed")

@bot.command()
async def battle(ctx):

bot.run('Token')


# ======================================================
# CLASSES:
# ======================================================

class jugador:
    
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"{self.name}"



class batalla:

    def __init__(self, j1, j2 = "", j3 = "", j4 = ""):
        self.j1 = j1
        self.j2 = j2
        self.j3 = j3
        self.j4 = j4

    def __str__(self):
        return f"{self.j1}, {self.j2}, {self.j3}, {self.j4}"