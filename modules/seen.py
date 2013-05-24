#!/usr/bin/python3
"""
seen.py -- A simple IRC bot module
Copyright 2013, Paweł Jan Czochański
Licensed under the GPL v3 license.
"""
from action import MultiAction, action
from ignore import honor_ignores
import ircbot
from datetime import datetime


class Seen(MultiAction):
    """Bot seen command."""

    def __init__(self, bot, *args, **kwargs):
        self.seendb = {}
        super(Seen, self).__init__(bot, *args, **kwargs)

    @action(name='populate_seen', events=('PRIVMSG', 'JOIN'))
    def populate_seen(self, bot, message, match, *args, **kwargs):
        """Populates the seen database."""

        user = message.nick
        msg = message._trailing
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.seendb[user] = (msg, date)

    @action(name='seen', rule=r'^\!seen (?P<user>\S+).*$')
    @honor_ignores
    def seen(self, bot, message, match, *args, **kwargs):
        """Tells when the user was last seen on the channel.
        Usage: !seen user"""

        user = match.group('user')

        if user in self.seendb:
            msg = self.seendb[user][0]
            date = self.seendb[user][1]
            bot.say('{} last seen saying {} on {}.'.format(user, msg, date))
        else:
            bot.say('I haven\'t seen {} around.'.format(user), message.channel)


ircbot.register(Seen)
