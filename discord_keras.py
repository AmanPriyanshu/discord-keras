import discord
from discord.ext import commands
from preprocessing import preprocess as pre
import os
import time
import pandas as pd

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

name = ""

@client.command()
async def define(ctx, *msg):
	global name
	msg = list(msg)
	msg = msg[1:-1]
	model_def = []
	text = ""
	for m in msg:
		if m.endswith(';'):
			model_def.append(text+m[:-1])
			text = ""
		else:
			text += m + ' '
	model_def = [m if m!='model' else '\nmodel:' for m in model_def]
	name = model_def[0][len('name: '):]
	model_def = model_def[1:]
	model_def = [m+'\n' for m in model_def]

	file = open(name+'.txt', 'w')
	file.writelines(model_def)
	file.close()

@client.command()
@commands.has_permissions(manage_messages = True)
async def execute(ctx, *msg):
	await ctx.send("Starting model execution...")
	if len(msg) == 0:
		patience = 1
		number = 2
	elif len(msg) == 1:
		number = int(msg[0])
		patience = 1
	else:
		number = int(msg[0])
		patience = int(msg[1])
	global name
	os.system('nohup python3 -u ./script_to_model.py '+name+' > live.txt & ')
	#pkill -f script_to_model.py
	prev_config = None
	first = True
	while(1):
		time.sleep(number)
		try:
			files = os.listdir('./output_'+name+'/')
			if len(files) == 3:
				break
			path = './output_'+name+'/per_epoch.csv'
			data = pd.read_csv(path)
			columns = data.columns
			data = data.values
			row = data[-1]
			row = [i for i in row]
			output = ' -- '.join([str(i)+' '+str(round(j, 4)) if type(j)!=str else str(i)+' '+str(j) for i,j in zip(columns, row)])
			await ctx.send(output)
		except:
			continue
	
	await ctx.send("Completed model execution!")

	path = './output_'+name+'/final_output.csv'
	data = pd.read_csv(path)
	columns = data.columns
	data = data.values
	row = data[0]
	output = ' -- '.join([str(i)+' '+str(round(j, 4)) if type(j)!=str else str(i)+' '+str(j) for i,j in zip(columns, row)])
	await ctx.send(output)
	row = data[1]

	output = ' -- '.join([str(i)+' '+str(round(j, 4)) if type(j)!=str else str(i)+' '+str(j) for i,j in zip(columns, row)])
	await ctx.send(output)

@client.command()
@commands.has_permissions(manage_messages = True)
async def clear(ctx, *msg):
	files = ['test', 'discord_keras.py', '.config','.gitignore', 'README.md', '.git', 'setup.py', 'script_to_model.py', 'data', '__pycache__', 'preprocessing.py']
	c_files = os.listdir()
	r_files = [i for i in c_files if i not in files]
	for f in r_files:
		try:
			if f.index('.')!=-1:
				os.system('rm '+f)
		except:
			os.system('rm -r '+f)

client.run(token)