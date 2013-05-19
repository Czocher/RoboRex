#! /usr/bin/python
"""
utils.py -- A simple IRC bot module
Copyright 2013, Paweł Jan Czochański
Licensed under the GPL v3 license.
"""
from action import MultiAction, action
from admin import admin_only
from ignore import honor_ignores
import ircbot
import random


class Utils(MultiAction):
    """Random useful bot utilities."""

    def __init__(self, bot, *args, **kwargs):

        if not hasattr(bot.config, 'GREETINGS'):
            raise AttributeError('A GREETINGS dict required\
                    in the config file.')

        self.seendb = {}

        self.welcome = bot.config.GREETINGS['welcome']
        self.name_react = bot.config.GREETINGS['name-react']
        self.bot_react = bot.config.GREETINGS['bot-react']

        super(Utils, self).__init__(bot, *args, **kwargs)

    @action(name='autogreet', rule=r'$botnick|bot', events=('JOIN', ))
    @honor_ignores
    def autogreet(self, bot, message, match, *args, **kwargs):
        """Automatically greets a user."""

        nick = message.nick
        msg = getattr(message, 'content', '')
        cmd = message._command

        if (cmd == 'JOIN' and self.welcome and nick != bot.nick) or\
                (cmd == 'PRIVMSG' and self.name_react and bot.nick in msg) or\
                (cmd == 'PRIVMSG' and self.bot_react and 'bot' in msg):
            greeting = random.choice(bot.config.GREETINGS['greetings'])

            action = False
            if greeting.startswith(r'\me '):
                greeting = greeting[4:]
                action = True

            channel = message.channel
            bot.say(greeting.format(message.nick), channel, action=action)

    @action(name='say', rule=r'^\!say(\ \#(?P<channel>\S+))?\ (?P<what>.+)$')
    @admin_only
    def say(self, bot, message, match, *args, **kwargs):
        """Repeats after the user on the given channel.
        Usage: !say <channel> what"""

        what = match.group('what')
        channel = match.group('channel')

        action = False
        if what.startswith('/me '):
            what = what[4:]
            action = True

        if channel is not None:
            bot.say(what, '#'+channel, action=action)
        else:
            bot.say(what, action=action)

    @action(name='help', rule=r'^\!help(\ (?P<action>\S+))?$')
    @admin_only
    def help(self, bot, message, match, *args, **kwargs):
        """Returns the help for the given action or a list of actions.
        Usage: !help <action>"""

        action = match.group('action')

        if action is not None:
            for a in bot._actions:
                if a.name == action:
                    bot.say(a.help, message.channel)
                    break
            else:
                bot.say('No such command.', message.channel)
        else:
            actions = [ac.name for ac in bot._actions]
            bot.say(', '.join(actions), message.channel)


ircbot.register(Utils)
