import os

os.system('pip3 install discord')
os.system('clear')
print("Begin by creating a new bot on discord.com. Documentation:(https://discord.com/developers/docs/intro)")
token = 'token: '+input('Please Enter Your Discord Bot Token:\t')

file = open('.config', 'a')
file.write(token)
file.close()

print('Okay Everythin Set-Up, run: `python3 discord_keras.py`')