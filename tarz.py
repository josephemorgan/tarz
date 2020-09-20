# tarz.py
import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_member_join(member):
    intro_string = f'Hi {member.name}, welcome to the CSUS Computer Science class-specific Discord Server! Please start by heading over to the rules channel. ' \
            f'For now, you\'re unable to comment in any channels. To fix that, please head over to the rules channel and react with a :thumbs_up: emoji to ' \
            f'show that you accept the rules. Once you do that, you\'ll be given the "accepted_rules" role, and you\'ll be able to participate. Thanks!'
    await member.create_dm()
    await member.dm_channel.send(intro_string)
    return

@client.event
async def on_raw_reaction_add(payload):
    rulesMessageId = 750078591374721235
    print(f'User added reaction...\n' \
            f'message_id: {payload.message_id}\n' \
            f'user_id: {payload.user_id}\n' \
            f'emoji: {payload.emoji}\n' \
            f'member: {payload.member}\n')

    if payload.message_id == rulesMessageId:
        if str(payload.emoji) == '👍':
            await payload.member.add_roles(discord.utils.get(payload.member.guild.roles, name="accepted_rules"))

    return

client.run(TOKEN)
