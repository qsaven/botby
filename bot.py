##REPLACE THESE VALUES
bot_key="PlAcEhOlDeR"
default_role="plus"
##--------------------
import discord
import asyncio
from time import sleep
from colorsys import hls_to_rgb
from discord.ext import commands
from discord.ext.commands import Bot
import os
client = discord.Client()
dothething = {}


@client.event
async def on_ready():
	return await client.change_presence(game=discord.Game(name='+help')) 

@client.event
async def on_message(message):
        global dothething
        if message.author == client.user:
                return
        if message.content.startswith("+stop"):
                await client.send_message(message.channel,"stopped")
                try:
                        dothething[str(message.server.id)]=0
                except:
                        print("err")
        if message.content.startswith("+start"):
                await client.send_message(message.channel, "` started`:rainbow:")
                hue=0
                if message.content.strip().startswith("+start "):
                        role = discord.utils.find(lambda m: m.name == message.content[6:].strip() ,message.server.roles)
                else:
                        role = discord.utils.find(lambda m: m.name == default_role ,message.server.roles)
                try:
                        dothething[str(message.server.id)]
                except:
                        dothething[str(message.server.id)]=0
                if role and not dothething[str(message.server.id)]:
                        dothething[str(message.server.id)]=1
                        while dothething[str(message.server.id)]:
                                users = [int(str(x.status)=="online") for x in message.server.members if role in x.roles] #black magic fuckery here
                                users.append(0)
                                print(str(message.server.name)+" - "+str(users))
                                if max(users):
                                        for i in range(50): #arbitrary rate limits
                                                if not dothething[str(message.server.id)]:
                                                        break
                                                hue = (hue+7)%360
                                                rgb = [int(x*255) for x in hls_to_rgb(hue/3, 0.10, 1)]
                                                await asyncio.sleep(0.1)
                                                clr = discord.Colour(((rgb[0]<<16) + (rgb[1]<<8) + rgb[2]))
                                                try:
                                                        await client.edit_role(message.server, role, colour=clr)
                                                except:
                                                        print("no perms" + str(message.server.name))
                                                        dothething[str(message.server.id)]=0
                                else:
                                        await asyncio.sleep(0.1)
client.run(os.environ['BOT_TOKEN'])
