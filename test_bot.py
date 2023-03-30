import random
import discord
from discord.ext import commands
import datetime
import sqlite3
import pandas as pd
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
    if ctx.channel.id == 1090714380649381888 and ctx.author.id != 1053382231151878194:
        print(f'[MSG LOG] {ctx.author.name} ({ctx.author.id}): {ctx.content}')
        await bot.process_commands(ctx)

@bot.command()
async def ping(ctx):
    await ctx.channel.send('Pong! {0}ms'.format(round(bot.latency * 1000, 5)))

@bot.command()
async def test(ctx):
    rand = random.randint(40, 100)

    total = 0
    await ctx.channel.send(f'Has ganado {rand} créditos!')

@bot.command()
async def player(ctx):
    name = f"{ctx.author.name}#{ctx.author.discriminator}"
    try:
        sqliteConnection = sqlite3.connect('SQLite_Python.db')
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")

        sqlite_insert_query = f"""INSERT INTO usuarios
                            (nombre, creditos) VALUES  ('{name}', 0)"""

        count = cursor.execute(sqlite_insert_query)
        sqliteConnection.commit()
        await ctx.send(f"Jugador añadido a la base de datos: @{name}")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert data into tabla")
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
async def q(ctx):
    sqliteConnection = sqlite3.connect('SQLite_Python.db')
    query = ctx.message.content[3:]
    if not query:
        query = "SELECT * FROM tabla"
    cursor = sqliteConnection.cursor()
    result = None

    try:
        cursor.execute(query)
    except Exception as e:
        await ctx.send(f"Algo ha ido mal al ejecutar la query...\n```{query}``` ```{e}```")
        return

    if cursor.description:
        field_names = [i[0] for i in cursor.description]
        results = cursor.fetchall()
        df = pd.DataFrame(list(results), columns=field_names)
        df = df.to_string(index=False)
        await ctx.channel.send(f'```{df}```')
    else:
        sqliteConnection.commit()
        await ctx.channel.send(f"Query -> `{query}` <- successful.")

bot.run('Token')
