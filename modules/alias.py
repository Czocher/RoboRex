#!/usr/bin/python3
"""
alias.py -- A simple IRC bot module
Copyright 2013, Paweł Jan Czochański
Licensed under the GPL v3 license.
"""
from action import MultiAction, action
import ircbot
import sqlite3


class Alias(MultiAction):
    """Remembering user aliases."""

    def __init__(self, bot, *args, **kwargs):

        if not hasattr(bot.config, 'ALIAS'):
            raise AttributeError('A ALIAS dict required in the config file.')

        self.connection = sqlite3.connect(bot.config.ALIAS['database'])
        self.cursor = self.connection.cursor()

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Nicks
                            (id INTEGER PRIMARY KEY, nick TEXT UNIQUE)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Aliases
                            (id INTEGER PRIMARY KEY, nickid INTEGER,
                            aliasid INTEGER,
                            FOREIGN KEY(nickid) REFERENCES Nicks(id),
                            FOREIGN KEY(aliasid) REFERENCES Nicks(id))''')
        self.connection.commit()
        super(Alias, self).__init__(bot, *args, **kwargs)

    @action(name='add_alias', events=('NICK', ))
    def add_alias(self, bot, message, match, *args, **kwargs):
        """React to a users name change."""

        oldnick = message._prefix.split('!')[0]
        newnick = message._trailing

        self.cursor.execute('''SELECT id FROM Nicks WHERE nick=?''',
                            (oldnick, ))
        oldnickid = self.cursor.fetchone()
        if not oldnickid:
            self.cursor.execute('''INSERT INTO Nicks VALUES (NULL,?)''',
                                (oldnick,))
            oldnickid = self.cursor.lastrowid
        else:
            oldnickid = oldnickid[0]

        self.cursor.execute('''SELECT id FROM Nicks WHERE nick=?''',
                            (newnick, ))
        newnickid = self.cursor.fetchone()
        if not newnickid:
            self.cursor.execute('''INSERT INTO Nicks VALUES (NULL,?)''',
                                (newnick, ))
            newnickid = self.cursor.lastrowid
        else:
            newnickid = newnickid[0]

        self.cursor.execute('''SELECT id FROM Aliases WHERE nickid=? \
                            AND aliasid=?''', (oldnickid, newnickid))

        aliasid = self.cursor.fetchone()

        if not aliasid:
            self.cursor.execute('''INSERT INTO Aliases Values (NULL,?,?),\
                                (NULL,?,?)''', (oldnickid, newnickid,
                                                newnickid, oldnickid))
        self.connection.commit()

    @action(name='alias', rule=r'^\!alias (?P<nick>\S+).*$')
    def alias(self, bot, message, match, *args, **kwargs):
        """Return a list of known alternative usernames for nick.
        Usage: !alias nick"""

        nick = match.group('nick')

        self.cursor.execute('''SELECT id FROM Nicks WHERE nick=?''', (nick, ))
        nickid = self.cursor.fetchone()

        if not nickid:
            bot.say('No other known aliases for user {}.'.format(nick))
        else:
            nickid = int(nickid[0])
            self.cursor.execute('''SELECT n1.nick FROM Nicks n1,
                                Aliases a WHERE a.nickid=?
                                AND a.aliasid=n1.id''', (nickid, ))
            aliases = [i[0] for i in self.cursor.fetchall()]
            bot.say('User also seen as {}.'.format(', '.join(aliases)),
                                                   message.channel)


ircbot.register(Alias)
