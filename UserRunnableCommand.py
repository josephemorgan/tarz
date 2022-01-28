import logging
import time
import discord
from tarz import Tarz

class UserRunnableCommand:
    command_prefix = "?"


    def __init__(self, bot_instance: Tarz, message: discord.Message):
        self.bot = bot_instance
        # Store reference to message
        self.message_reference = discord.MessageReference.from_message(message)

        # Store content of command
        self.content = message.content

        # Identify user running command
        self.author = message.author

        # Identify channel that command was run in
        self.channel = message.channel

        # Store the associated function
        command = discord.Message.content.split()
        if command[0][1:] == "purge":
            self.command = self.__purge;
        elif command[0][1:] in ["man", "help"]:
            self.command = self.__man
        elif command[0][1:] == "addme":
            self.command = self.__add_class_role
        elif command[0][1:] == "removeme":
            self.command = self.__remove_class_role
        elif command[0][1:] == "reset_roles":
            self.command = self.__reset_class_roles

        # Set list of arguments to command
        self.args = message.content.split()[1:]

        # Cache the help text
        readme = open("./README.md", "r")
        self.help_text = readme.read()


    async def run(self) -> None:
        await self.command()


    async def __man(self) -> None:
        await self.channel.send("```" + self.help_text + "```")


    async def __purge(self) -> None:
        """ Purges messages from a channel based on an argument """
        if self.args == 'all':
            await self.channel.send("https://c.tenor.com/BDfaxXA3WfAAAAAM/thanos-thanos-dance.gif");
            time.sleep(10)
            await self.channel.purge()
        elif self.args.isnumeric():
            await self.channel.purge(limit=int(self.args) + 1)
        else:
            await self.channel.send(f"That doesn't seem to be a valid purge command.")


    async def __add_class_role(self) -> None:
        if "CLASSES" in self.channel.category.name:
            guild = Tarz.client.get_guild(Tarz.guild_id)
            role_to_add = None
            if (guild) != None:
                for existing_role in guild.roles:
                    if existing_role.name == self.channel.name:
                        role_to_add = existing_role
                        break
                if role_to_add == None:
                    role_to_add = await guild.create_role(name=self.channel.name, mentionable=True)
                await self.author.add_roles(role_to_add)


    async def __remove_class_role(self) -> None:
        if "CLASSES" in self.channel.category.name:
            try:
                for assigned_role in self.author.roles:
                    if assigned_role.name == self.channel.name:
                        await self.author.remove_roles(assigned_role)
                        break
            except discord.HTTPException:
                logging.exception(f"Failed to remove {self.channel.name} role from {self.author.display_name}")


    async def __reset_class_roles(self) -> None:
        for assigned_role in self.channel.roles:
            if "csc" in assigned_role.name or "math" in assigned_role.name or "phil" in assigned_role.name:
                await self.author.remove_roles(assigned_role)


    @classmethod
    def is_command(cls, message_text: str):
        if message_text[0].startswith(cls.command_prefix):
            return True
        else:
            return False
