import discord
import logging
from tarz import Tarz

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
tarz = Tarz(client, "?", 750078591374721235)

@client.event
async def on_ready():
    print("Ready!")
    logging.info('Connected')

@client.event
async def on_member_join(member):
    await tarz.greet(member)

@client.event
async def on_raw_reaction_add(payload):
    await tarz.handle_reaction_add(payload)

@client.event
async def on_message(message):
    await tarz.handle_message(message)



client.run(tarz.token)
