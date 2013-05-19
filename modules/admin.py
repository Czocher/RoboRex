#! /usr/bin/python
"""
admin.py -- A simple IRC bot module
Copyright 2013, Paweł Jan Czochański
Licensed under the GPL v3 license.
"""
from action import MultiAction, action
import ircbot


def admin_only(obj):
    """Decorate the function to be used only
    if the user is logged in as an admin."""

    def wrapper(*args, **kwargs):

        bot = None
        message = None

        if isinstance(args[0], type(ircbot.IRCBot)):
            bot, message = args[0:2]
        else:
            bot, message = args[1:3]

        if message.nick is not None and message.nick in bot.admins:
            return obj(*args, **kwargs)

    wrapper.__doc__ = obj.__doc__
    wrapper.__name__ = obj.__name__

    return wrapper


class Admin(MultiAction):
    """Control the admin functions."""

    def __init__(self, bot, *args, **kwargs):
        bot.admins = []
        super(Admin, self).__init__(bot, *args, **kwargs)

    @action(name='identify', rule=r'^\!identify\ (?P<password>\S+)$')
    def identify(self, bot, message, match, *args, **kwargs):
        """Log in an user as an admin.
        Usage: !identify <password>"""

        password = match.group(1)
        nick = message.nick

        if nick in bot.config.ADMINS \
           and password == bot.config.ADMINS[nick]:
            bot.admins.append(nick)
            bot.say('Welcome {}!'.format(nick), message.nick)

    @action(name='logout', rule=r'^\!logout(\ (?P<user>\S+))?$')
    @admin_only
    def logout(self, bot, message, match, *args, **kwargs):
        """Log out the user.
        Usage: !logout <user>"""

        user = match.group('user')
        if user is None:
            user = message.nick

        if user in bot.admins:
            bot.admins.remove(user)
            bot.say('Goodbye {}!'.format(user), message.nick)


ircbot.register(Admin)
