# tarz.py
import os
import logging
import discord
from dotenv import load_dotenv

logging.basicConfig(filename='tarz.log', level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

rules_message_id = 750078591374721235
message_ids_for_class_roles = {
        798992437858795520: "csc135-krovets",
        799000339634323487: "csc133-posnett", 
        799000805629100083: "csc133-muyan"
        }


@client.event
async def on_ready():
    print("Ready!")
    logging.info('Connected')

@client.event
async def on_member_join(member):
    logging.info(f'{member.name} has joined the server')
    intro_string = f'Hi {member.name}, welcome to the CSUS Computer Science class-specific Discord Server! ' \
            f'For now, you\'re unable to comment in any channels. To fix that, please head over to the rules channel and react with a thumbs_up emoji to ' \
            f'show that you accept the rules. Once you do that, you\'ll be given the "accepted_rules" role, and you\'ll be able to participate. Thanks!'
    await member.send(intro_string)
    return

@client.event
async def on_raw_reaction_add(payload):
    if payload.message_id == rules_message_id:
        if str(payload.emoji) == '👍':
            await payload.member.add_roles(discord.utils.get(payload.member.guild.roles, name="accepted_rules"))
            logging.info(f'{payload.member.name} has accepted the rules: granting accepted_rules role.')

    if payload.message_id in message_ids_for_class_roles:
        await payload.member.add_roles(discord.utils.get(payload.member.guild.roles, name=message_ids_for_class_roles[payload.message_id]))
        logging.info(f'{payload.member.name} is being added to {message_ids_for_class_roles[payload.message_id]}')

    return

@client.event
async def on_raw_reaction_remove(payload):
    if payload.message_id in message_ids_for_class_roles:
        guild = client.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        await member.remove_roles(discord.utils.get(guild.roles, name=message_ids_for_class_roles[payload.message_id]))
        logging.info(f'{member.name} is being removed from {message_ids_for_class_roles[payload.message_id]}')

client.run(TOKEN)
