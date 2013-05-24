#!/usr/bin/python3
"""
alias.py -- A simple IRC bot module
Copyright 2013, Paweł Jan Czochański
Licensed under the GPL v3 license.
"""
from action import MultiAction, action
import ircbot


class Alias(MultiAction):
    """Remembering user aliases."""

    def __init__(self, bot, *args, **kwargs):
        bot.aliaslist = []
        super(Alias, self).__init__(bot, *args, **kwargs)

    @action(name='add_alias', events=('NICK', ))
    def add_alias(self, bot, message, match, *args, **kwargs):
        """React to a users name change."""

        oldnick = message._prefix.split('!')[0]
        newnick = message._trailing

        for aliases in bot.aliaslist:
            if oldnick in aliases:
                break
        else:
            bot.aliaslist.append([oldnick, ])

        for aliases in bot.aliaslist:
            if oldnick in aliases and newnick not in aliases:
                aliases.append(newnick)

    @action(name='alias', rule=r'^\!alias (?P<user>\S+).*$')
    def alias(self, bot, message, match, *args, **kwargs):
        """Return a list of known user names for the user.
        Usage: !alias user"""

        user = match.group('user')

        for aliases in bot.aliaslist:
            if user in aliases:
                bot.say('User also seen as {}.'.format(', '.join(aliases)),
                        message.channel)
                break
        else:
            bot.say('No other known aliases for user {}.'.format(user))

ircbot.register(Alias)
