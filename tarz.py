import discord
from typing import Union
import os
import logging
import time
from dotenv import load_dotenv


class Tarz:
    command_prefix: str
    commands: dict
    token: Union[str,  None]
    client: discord.Client
    rules_message_id: int


    def __init__(self, attached_client: discord.Client, command_prefix: str, rules_message_id: int):
        load_dotenv()
        self.commands = {"man" : self.man, "purge" : self.purge}
        self.command_prefix = command_prefix
        self.token = os.getenv('DISCORD_TOKEN')
        self.client = attached_client
        self.rules_message_id = rules_message_id
        logging.basicConfig(filename='/home/joe/dev/tarz/tarz.log', level=logging.INFO, format='%(asctime)-15s : %(levelname)s :: %(message)s')


    async def greet(self, member: discord.User) -> None:
        logging.info(f'JOIN - {member.name} has joined the server')
        intro_string = f'Hi {member.name}, welcome to the CSUS Computer Science class-specific Discord Server! ' \
            f'For now, you\'re unable to comment in any channels. To fix that, please head over to the rules channel and react with a thumbs_up emoji to ' \
            f'show that you accept the rules. Once you do that, you\'ll be given the "accepted_rules" role, and you\'ll be able to participate. Thanks!'
        await member.send(intro_string)


    async def handle_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.message_id == self.rules_message_id:
            if str(payload.emoji) == '👍' and payload.member != None:
                await payload.member.add_roles(discord.utils.get(payload.member.guild.roles, name="accepted_rules"))
                logging.info(f'ACCAPTED RULES - {payload.member.name} has accepted the rules: granting accepted_rules role.')


    async def handle_message(self, message: discord.Message) -> None:
        try:
            logging.info(f'MSG - {message.channel.name} : {message.author} > {message.content}')
        except AttributeError:
            logging.error(f'AttributeError')
        command = message.content.split();
        if command[0].startswith(self.command_prefix):
            if command[0][1:] == "purge":
                await self.purge(command[1], message.channel)
            elif command[0][1:] == "man":
                await self.man(command[1], message.channel);
            elif command[0][1:] == "addme":
                if "CLASSES" in message.channel.category.name:
                    await self.add_class_role(message.author, message.channel.name)
            elif command[0][1:] == "removeme":
                if "CLASSES" in message.channel.category.name:
                    await self.remove_class_role(message.author, message.channel.name)
            elif command[0][1:] == "reset_roles":
                await self.reset_class_roles(message.author)


    async def purge(self, arg: str, channel: discord.TextChannel) -> None:
        """ Purges messages from a channel based on an argument """
        if arg == 'all':
            await channel.send("https://c.tenor.com/BDfaxXA3WfAAAAAM/thanos-thanos-dance.gif");
            time.sleep(10)
            await channel.purge()
        elif arg.isnumeric():
            await channel.purge(limit=int(arg) + 1)
        elif len(arg) == 22 and self.client.get_user(int(arg[3:-1])):
            async for m in channel.history(limit=1000):
                if m.author == self.client.get_user(int(arg[3:-1])):
                    await m.delete()
        else:
            await channel.send(f"That doesn't seem to be a valid purge command. Try {self.command_prefix}man purge")


    async def add_class_role(self, user: discord.Member, channel_name: str) -> None:
        guild = self.client.get_guild(714930784045105173)
        role_to_add = None
        if (guild) != None:
            for existing_role in guild.roles:
                if existing_role.name == channel_name:
                    role_to_add = existing_role
                    break
            if role_to_add == None:
                role_to_add = await guild.create_role(name=channel_name, mentionable=True)
            await user.add_roles(role_to_add)


    async def remove_class_role(self, user: discord.Member, channel_name: str) -> None:
        guild = self.client.get_guild(714930784045105173)
        try:
            for assigned_role in user.roles:
                if assigned_role.name == channel_name:
                    await user.remove_roles(assigned_role)
                    break
        except discord.HTTPException:
            logging.exception(f"Failed to remove {channel_name} role from {user.display_name}")


    async def reset_class_roles(self, user:discord.Member) -> None:
        for assigned_role in user.roles:
            if "csc" in assigned_role.name or "math" in assigned_role.name or "phil" in assigned_role.name:
                await user.remove_roles(assigned_role)


    async def man(self, arg: str, channel: discord.TextChannel) -> None:
        tarz_man_string = '''Tarz is the friendly unpaid intern responsible for helping with things here in the CSUS discord server \n
        A number of comands are available, including the following:\n
        addme : Tarz will grant you the role associated with the class channel that the command was sent in.\n
        removeme : Tarz will remove the role associated with the class channel that the command was sent in from the user who sent the command.\n
        reset_roles : Tarz will remove all roles that are associated with a class channel from the user who sent the command.\n
        purge : Tarz will purge messages from the channel history. <requires admin>\n
        man [COMMAND] : Tarz will tell you how to use a certain command'''
        purge_man_string = '''Purges messages from a channel's history
        Usage :: purge [NUMBER] | purge @[USER] | purge all
        NUMBER : Can be any number, controls how far back into a channel's history purge searches
        @USER : tags a user, deletes messeges sent by them
        all : Purges all messages in a channel'''
        addme_man_string = '''Tarz will assign the command issuer the role associated with the channel that the command was issued in, if it's a class channel.
        Usage :: addme'''
        removeme_man_string = '''Tarz will remove from the command issuer the role associated with the channel that the command was issued in, if it's a class channel.
        Usage :: removeme'''
        reset_roles_man_string = '''Tarz will remove from the command issuer ALL roles associated with any class channel.
        Usage :: removeme'''
        if arg == "purge":
            await channel.send(purge_man_string)
        elif arg == "tarz":
            await channel.send(tarz_man_string)
        elif arg == "addme":
            await channel.send(addme_man_string)
        elif arg == "removeme":
            await channel.send(removeme_man_string)
        elif arg == "reset_roles":
            await channel.send(reset_roles_man_string)
