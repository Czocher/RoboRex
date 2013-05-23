#! /usr/bin/python
"""
userlists.py -- A simple IRC bot module
Copyright 2013, Paweł Jan Czochański
Licensed under the GPL v3 license.
"""
from action import MultiAction, action
import ircbot


def userPresent(bot, user, channel):
    """Return true if user is present on the channel, else false."""

    if channel in bot.userlists and user in bot.userlists[channel]:
        return True
    else:
        return False


class UserLists(MultiAction):
    """Managind the channel userlists for the bot."""

    def __init__(self, bot, *args, **kwargs):
        bot.userlists = {channel: [] for channel in bot.channels}
        super(UserLists, self).__init__(bot, *args, **kwargs)

    @action(name='fetch_userlists', rule=r'.*')
    def fetch_userlists(self, bot, message, match, *args, **kwargs):
        """Fetch the channel userlist."""

        if message._parameters:
            msg = message._parameters.split()

            if len(msg) == 3 and msg[-1].startswith('#'):
                bot.userlists[msg[-1]] = [u for u in message._trailing.split()]

    @action(name='populate_userlist', events=('JOIN', ))
    def populate_userlists(self, bot, message, match, *args, **kwargs):
        """Populates the channel userlist."""

        bot.userlists[message.channel].append(message.nick)

    @action(name='namechange_react', events=('NICK', ))
    def namechange_react(self, bot, message, match, *args, **kwargs):
        """React to a users name change."""

        oldnick = message._prefix.split('!')[0]
        newnick = message._trailing

        for channel in bot.userlists.values():
            if oldnick in channel:
                channel.remove(oldnick)
                channel.append(newnick)

    @action(name='depopulate_userlist', events=('PART', 'QUIT'))
    def depopulate_userlists(self, bot, message, match, *args, **kwargs):
        """Depopulates the channel userlist when someone quits."""

        for c in bot.userlists.values():
            if message.nick in c:
                c.remove(message.nick)


ircbot.register(UserLists)
