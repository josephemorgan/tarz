# tarz.py
import os
import logging
import discord
import time
from dotenv import load_dotenv

def test(num):
    print(num)

async def purge(arg, channel):
    print(arg)
    if arg == 'all':
        await channel.send("https://c.tenor.com/BDfaxXA3WfAAAAAM/thanos-thanos-dance.gif");
        time.sleep(10)
        await channel.purge()
    elif arg.isnumeric():
        await channel.purge(limit=int(arg))
    else:
        if len(arg) == 22 and client.get_user(int(arg[3:-1])):
            async for m in channel.history():
                if m.author == client.get_user(int(arg[3:-1])):
                    await m.delete()

async def man(command):
    if command == "purge":
        purge_man_string = """Usage: purge NUM | purge @USER | purge all
          NUM : Can be any number, controls how far back into a channel's history purge searches
          @USER : tags a user, deletes messeges sent by them
          all : Purges all messages in a channel"""



logging.basicConfig(filename='/home/joe/dev/tarz/tarz.log', level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

command_prefix = "?"
commands = {"test" : test,
            "purge" : purge}

rules_message_id = 750078591374721235
message_ids_for_class_roles = {
        803318558218125312: "csc131-chidella",
        799000805629100083: "csc133-muyan",
        799000339634323487: "csc133-posnett",
        803099185524113418: "csc133-gordon",
        803099343993307147: "csc134-applebaum",
        803099421356458014: "csc134-jin",
        803319040964820992: "csc134-sabzevary",
        798992437858795520: "csc135-krovets",
        803099634275713034: "csc135-lu",
        803099748440735794: "csc137-posnett",
        803319438354022461: "csc137-singh",
        803099809447280672: "csc138-dai",
        803099889445634098: "csc138-sun",
        803104759383851078: "csc138-wang",
        803099943056441365: "csc139-cheng",
        803107039106695239: "csc139-shobaki",
        803319740201304194: "csc139-mayer",
        803111599362539531: "csc140-phoulady",
        803100413133062175: "csc142-arad",
        803106704026763274: "csc152-krovets",
        803100466530746369: "csc154-dai",
        803100805543755786: "csc155-gordon",
        803320024512069632: "csc170-chidella",
        803320458522263562: "csc171-chen",
        803105872111861770: "csc173-baynes",
        803100892810313768: "csc174-applebaum",
        803100980840890418: "csc177-lu",
        803113969136173148: "csc180-chen",
        803320816682532874: "csc192-rajiyah",
        803321230429651035: "csc194-gordon",
        803114383210315796: "math45-mathur"
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

@client.event
async def on_message(message):
    try:
        content = message.content
        sourceChannelName = message.channel.name;
        sourceChannelId = message.channel.id
        sourceAuthor = message.author
        sourceAdmin = message.author.guild_permissions.administrator
        print(f'{sourceChannelName}, {sourceChannelId} : {sourceAuthor} > {content}')
    except AttributeError:
        print(f'AttributeError')
    command = message.content.split();
    if command[0].startswith(command_prefix) and command[0][1:] in commands.keys():
        if len(command) == 2:
            await commands[command[0][1:]](command[1], message.channel)
        elif len(command) == 1:
            commands[command[0][1:]](message.channel)

client.run(TOKEN)
