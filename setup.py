import os

os.system('pip3 install discord')
print("Begin by creating a new bot on discord.com. Documentation:(https://discord.com/developers/docs/intro)")
token = 'token: '+input('Please Enter Your Discord Bot Token:\t')

file = open('.config', 'a')
file.write(token)
file.close()

os.system()