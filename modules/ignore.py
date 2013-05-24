#!/usr/bin/python3
"""
ignore.py -- A simple IRC bot module
Copyright 2013, Paweł Jan Czochański
Licensed under the GPL v3 license.
"""
from action import MultiAction, action
from admin import admin_only
import ircbot


def honor_ignores(obj):
    """Decorate the function to be used only
    if the user is not on the ignored list."""

    def wrapper(*args, **kwargs):

        bot = None
        message = None

        if isinstance(args[0], type(ircbot.IRCBot)):
            bot, message = args[0:2]
        else:
            bot, message = args[1:3]

        if message.nick is not None and message.nick not in bot.ignores:
            return obj(*args, **kwargs)

    wrapper.__doc__ = obj.__doc__
    wrapper.__name__ = obj.__name__

    return wrapper


class Ignore(MultiAction):

    def __init__(self, bot, *args, **kwargs):

        if not hasattr(bot.config, 'IGNORES'):
            raise AttributeError('A IGNORES list required in the config file.')

        bot.ignores = bot.config.IGNORES
        super(Ignore, self).__init__(bot, *args, **kwargs)

    @action(name='ignore', rule=r'^\!ignore (?P<nick>\S+).*$')
    @admin_only
    def ignore(self, bot, message, match):
        """Ignore the given user.
        Usage: !ignore <nick>"""

        nick = match.group(1)
        if nick not in bot.ignores:
            bot.ignores.append(nick)
            bot.say('Ignoring {} from now on.'.format(nick), message.channel)

    @action(name='deignore', rule=r'^\!deignore (?P<nick>\S+).*$')
    @admin_only
    def deignore(self, bot, message, match):
        """Deignore the given user.
        Usage: !deignore <nick>"""

        nick = match.group(1)
        if nick in bot.ignores:
            bot.ignores.remove(nick)
            bot.say('Listening to {} again.'.format(nick), message.channel)


ircbot.register(Ignore)
