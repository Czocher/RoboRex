"""
bot.py -- A simple IRC bot example module
Copyright 2013, Paweł Jan Czochański
Licensed under the GPL v3 license.
"""

from action import action, MultiAction
import ircbot


# Execute when someone joins a channel
@ircbot.register
@action(events=('JOIN', ))
def greeting(bot, message, *args, **kwargs):
    """Greet a joining person."""  # Help for the function (it is required)

    # Get the persons nick
    nick = message.nick

    # Get the channel on which the JOIN event occured
    channel = message.channel

    # Greet the person on the given channel
    bot.say('Welcome {}!'.format(nick), channel)


# RegExp rule for function execution, name is a aditional parameter
# defining the function human-readable name (displayed in help messages)
@ircbot.register
@action(rule=r'^\!simonSay (.*)$', name='simonSay')
def say_something(bot, message, match, *args, **kwargs):
    """Say the sentence after the command.
    Usage: !say sentence"""

    # Get the message from the previously defined RegExp
    msg = match.group(1)

    # Get the channel
    channel = message.channel

    # Say the message
    bot.say(msg, channel)


class ClassModuleExample(MultiAction):
    """An example MultiAction module class."""

    def __init__(self, bot, *args, **kwargs):

        # Create a new bot public field
        bot.usersWhoSaidNi = []

        # Run the superclass constructor
        super(ClassModuleExample, self).__init__(bot, *args, **kwargs)

    @action(name='grepNiSayers', rule=r'Ni!|ni!')
    def niSayersShallBeRemebered(self, bot, message, *args, **kwargs):
        """Remember users who said Ni! or ni!"""

        # Add the user who matched the rule to the list
        if not message.nick in bot.usersWhoSaidNi:
            bot.usersWhoSaidNi.append(message.nick)

        # Say something for fun
        bot.say('Ni sayer!', message.channel)


# Register the module in the bot
ircbot.register(ClassModuleExample)
