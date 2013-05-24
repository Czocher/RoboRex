#!/usr/bin/python3
"""
randquote.py -- A simple IRC bot module
Copyright 2013, Paweł Jan Czochański
Licensed under the GPL v3 license.
"""
from action import MultiAction, action
from ignore import honor_ignores
from admin import admin_only
import random
import ircbot
import sqlite3


class RandQuote(MultiAction):
    """Throw a random quote from the database at the given moment."""

    def __init__(self, bot, *args, **kwargs):

        if not hasattr(bot.config, 'RANDQUOTE'):
            raise AttributeError('A RANDQUOTE dict\
                    required in the config file.')

        self.connection = sqlite3.connect(bot.config.RANDQUOTE['database'])
        self.cursor = self.connection.cursor()

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Quotes
                (id INTEGER PRIMARY KEY, quote TEXT)''')
        self.connection.commit()

        self.gatherprob = bot.config.RANDQUOTE['gather']
        self.throwprob = bot.config.RANDQUOTE['throw']
        self.namereact = bot.config.RANDQUOTE['name-react']
        self.botreact = bot.config.RANDQUOTE['bot-react']

        super(RandQuote, self).__init__(bot, *args, **kwargs)

    @action(name='gather', events=('PRIVMSG', ))
    @honor_ignores
    def gather(self, bot, message, match, *args, **kwargs):
        """Gathers quotes to the database with a given probability."""

        nick = message.nick
        msg = message.content

        if random.randint(1, 100) <= self.gatherprob\
                and nick != bot.nick and not msg.startswith('!')\
                and not bot.nick in msg and not ' bot ' in msg:

            self.cursor.execute('''INSERT INTO Quotes
                    VALUES (NULL,?)''', (msg, ))
            self.connection.commit()

    @action(name='throw', events=('PRIVMSG', ))
    @honor_ignores
    def throw(self, bot, message, match, *args, **kwargs):
        """Throws a random quote from the database
        with a given probability."""

        nick = message.nick
        msg = message.content

        if (random.randint(1, 100) <= self.throwprob or
            (bot.nick in msg and self.namereact) or
            (message.channel == bot.nick) or
            ('bot' in msg and self.botreact)) and not \
           (msg.startswith('!') or nick == bot.nick):

            self.cursor.execute("""SELECT quote FROM Quotes
            ORDER BY RANDOM() LIMIT 1""")
            quote = self.cursor.fetchone()

            if quote:
                bot.say(quote[0], message.channel)

    @action(name='throwprobchange', rule=r'^\!throw(\ (?P<prob>\d+))?$')
    @admin_only
    def throwprobchange(self, bot, message, match, *args, **kwargs):
        """Change the quote throw probability.
        Usage: !throw <prob>"""

        prob = match.group('prob')

        if prob:
            self.throwprob = int(prob)
            bot.say('Changed the quote throw probability'
                    ' to {}.'.format(self.throwprob), message.channel)
        else:
            bot.say('Current throw probability is {}.'.format(self.throwprob),
                    message.channel)

    @action(name='gatherprobchange', rule=r'^\!gather(\ (?P<prob>\d+))?$')
    @admin_only
    def gatherprobchange(self, bot, message, match, *args, **kwargs):
        """Change the quote gather probability.
        Usage: !gather <prob>"""

        prob = match.group('prob')

        if prob:
            self.gatherprob = int(prob)
            bot.say('Changed the quote gather probability'
                    ' to {}.'.format(self.gatherprob), message.channel)
        else:
            bot.say('Current gather probability is {}.'
                    .format(self.gatherprob), message.channel)


ircbot.register(RandQuote)
