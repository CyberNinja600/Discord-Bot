import discord
import os
import json
import asyncio 
from itertools import cycle
import time
from keep_alive import keep_alive
from discord.ext import commands, tasks
from discord.ext.commands import CommandNotFound


#--------------------------------Get Prefix------------------------------------#

def get_prefix(client, message):

  with open('./cogs/Data/prefixes.json', 'r') as f:
    prefixes = json.load(f)

  return prefixes[str(message.guild.id)]


def server_count():

  with open('./cogs/Data/prefixes.json', 'r') as f:
    prefixes = json.load(f)

  count = 0
  for i in prefixes:
    count += 1  

  return count

#---------------------------------INFO-----------------------------------------#


version = '0.5'
client = commands.Bot(command_prefix = get_prefix, intents = discord.Intents.all())

client.remove_command('help')

status = cycle(['Objective: Make people GAY!', 'Cyka Blyat!', f'in {server_count()} servers'])

@client.event
async def on_ready():
  
  change_status.start()
  print('Logged in as {0.user}'.format(client))

@tasks.loop(seconds=10)
async def change_status():

  await client.change_presence(activity=discord.Game(next(status)))
  

#-----------------------------Prefix Setup--------------------------------------#


@client.event
async def on_guild_join(guild):

  with open('./cogs/Data/prefixes.json', 'r') as f:
    prefixes = json.load(f)

  prefixes[str(guild.id)] = '$$'

  with open('./cogs/Data/prefixes.json', 'w') as f:
    json.dump(prefixes, f, indent=4)

@client.event
async def on_guild_remove(guild):

  with open('./cogs/Data/prefixes.json', 'r') as f:
    prefixes = json.load(f)

  prefixes.pop(str(guild.id))

  with open('./cogs/Data/prefixes.json', 'w') as f:
    json.dump(prefixes, f, indent=4)

  

@client.command(aliases=['changeprefix'])
async def prefix(ctx, change_prefix):

  with open('./cogs/Data/prefixes.json', 'r') as f:
    prefixes = json.load(f)

  prefixes[str(ctx.guild.id)] = change_prefix

  with open('./cogs/Data/prefixes.json', 'w') as f:
    json.dump(prefixes, f, indent=4)

  await ctx.channel.send(f'Prefix changed to: `{change_prefix}`')

#--------------------------------Invite----------------------------------------#

@client.command()
@commands.has_permissions(administrator=True)
async def invite(ctx):
  
  invite = 'https://discord.com/api/oauth2/authorize?client_id=894627029717237800&permissions=0&scope=bot'

  embedVar = discord.Embed(title="Invitation Link", description=invite, color=0x00ff00)

  await ctx.channel.send(embed=embedVar)
    
#--------------------------------PING------------------------------------------#
@client.command()
async def ping(ctx):

  before = time.monotonic()
  message = await ctx.send("Pong!")
  ping = (time.monotonic() - before) * 1000
  # await message.edit(content=f"Pong!  `{int(ping)}ms`")  

  # latency = (round(client.latency) * 1000)

  latency = int(ping)

  if latency <= 60:
    clr = 0x00ff00

  elif latency > 60 and latency <= 150:
    clr = 0xffff00

  else:
    clr = 0xff0000

  

  embedVar = discord.Embed(title="Latency", description=f'Pong! {latency}ms', color=clr)
  embedVar.set_footer(text = f'Requested by {ctx.author}' ,icon_url = ctx.author.avatar_url)

  await asyncio.sleep(1)
  await message.edit(embed=embedVar)
#-----------------------Error Handler------------------------------------------#
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    raise error
##------------------Access Files---------------------------------


for filename in os.listdir('./cogs'):
  if filename.endswith('py') and filename != 'new_leveling.py':

    client.load_extension(f'cogs.{filename[:-3]}')

# for filename in os.listdir('./cogs/level system'):
#   if filename.endswith('py'):

#     client.load_extension(f'cogs.{filename[:-3]}')


##---------------------------------------------------
def setup(client):
    # Every extension should have this function
    client.add_command(prefix)
    client.add_command(invite)
    
##------------------RUN------------------------------
keep_alive()
my_secret = os.environ['TOKEN']
client.run(my_secret)
##---------------------------------------------------
