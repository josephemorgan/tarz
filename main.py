import discord
import logging
from tarz import Tarz

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
tarz = Tarz(attached_client = client, guild_id = 714930784045105173, rules_message_id = 750078591374721235, command_prefix = "?")

# this is a ready function
@client.event
async def on_ready():
    print("Ready!")
    logging.info('Connected')

# this is a member join function
@client.event
async def on_member_join(member):
    await tarz.greet(member)

# this is a raw reaction add function
@client.event
async def on_raw_reaction_add(payload):
    await tarz.handle_reaction_add(payload)

# this is a on message function
@client.event
async def on_message(message):
    await tarz.handle_message(message)



client.run(tarz.token)
