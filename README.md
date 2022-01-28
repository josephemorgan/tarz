# Tarz - The CSUS CS Classes Discord Bot

Tarz is the special-purpose discord bot written to assist in the administration of the CSUS CS Classes Discord Server.

# Using the Bot

There are a number of commands available, including the following:

- reset_roles: Removes all class-specific roles that you've added using the `addme` command.
- addme: Tarz will grant you the role associated with the class channel that the command was sent in. Only works in class channels, which are under a channel category that contains "CLASSES"
- removeme: Functions as the opposite of addme. Removes the role associated with the class channel that the command was sent in.

# Setting up your own instance

You can set up your own instance of Tarz to run on any server that you have permissions for. This can be helpful if you're interested in contribution to Tarz, or if you just want to see how it works.

## Creating a Bot Account

You need to create a Discord account that your bot will use. Because our instance of Tarz has permissions to administer the CSUS CS Classes server, you'll need to create your own bot account to test on your testing server.

Head to the [Discord website](discord.com) and log in. Go the the [applications page](https://discord.com/developers/applications) and click New Application. Give the application a name (we called ours Tarz), and then navigate to the "Bot" tab on the left. Click "Add Bot," and you're done with creating a bot account!

On the bot page, you'll be given a token that you want to keep track of. This token is secret, so don't share it with anyone. You'll use it in the next step.

## Cloning and setting up the repository

Your next step is to clone this repository. Once you've done so, create a file in the root directory of the repo named ".env" without quotes, and without any file extension. There should be one line in this file that says:

>DISCORD_TOKEN = "<your token here>"

Replace <your token here> with the token from the bots tab of the discord applications page.

## Running your instance of Tarz

To run Tarz, simply execute the following command in the root directory of your Tarz repo:

`python3 ./main.py`

# Contributing

Because Tarz is meant to be an educational project for CS students in our server, contributions are very welcome. Feel free to create issues with suggestions that you might have, and make pull requests with your ideas.
