import discord
import os
import logging
from dotenv import load_dotenv
from UserRunnableCommand import UserRunnableCommand


class Tarz:
    client: discord.Client
    guild_id: int
    rules_message_id: int
    command_prefix: str


    def __init__(self, attached_client: discord.Client, guild_id, rules_message_id, command_prefix: str):
        load_dotenv()
        self.token = os.getenv('DISCORD_TOKEN')
        Tarz.client = attached_client
        Tarz.guild_id = guild_id
        Tarz.rules_message_id = rules_message_id
        Tarz.command_prefix = command_prefix;

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
        if UserRunnableCommand.is_command(message.content):
            command = UserRunnableCommand(self, message);
            await command.run()
