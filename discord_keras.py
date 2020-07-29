import discord
from discord.ext import commands
from preprocessing import preprocess as pre

client = commands.Bot(command_prefix=">")
file = open('.config', 'r')
config = file.readlines()
file.close()

token = config[0][len('token: '):]

@client.event
async def on_ready():
	print("Bot is Ready")

@client.command()
async def preprocess(ctx):
	await ctx.send("Running preprocessing...")
	try:
		pre()
	except Exception as e:
		await ctx.send('ERROR:\n'+str(e))
	await ctx.send("Completed running preprocessing.")

@client.command()
async def define(ctx):
	print(ctx)

client.run(token)