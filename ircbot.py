#! /usr/bin/python
"""
ircbot.py -- A simple IRC bot base class
Copyright 2013, Paweł Jan Czochański
Licensed under the GPL v3 license.
"""

import asyncore
import socket
import re
from inspect import isfunction, isclass
from singleton import Singleton
from message import Message


def register(obj):
    """Register the given object with the bot."""
    IRCBot().register(obj)


@Singleton
class IRCBot(asyncore.dispatcher):
    """Main bot class."""

    def __init__(self, *args, **kwargs):
        self._inbuf = ''
        self._outbuf = ''
        self._actions = []

    def setup(self, config):
        self.config = config
        self.nick = config.BOT['nick']
        self.realname = config.BOT['realname']
        self.channels = [c.lower() for c in config.BOT['channels']]
        self.host = config.SERVER['host']
        self.port = config.SERVER['port']

        self.irc_message = re.compile(r'^(:(?P<prefix>\S+) )?'
                                      '(?P<command>\S+)( (?!:)'
                                      '(?P<params>.+?))?'
                                      '( :(?P<trail>.+))?$')

        # Remove blacklisted actions
        for action in self._actions:
            name = getattr(action, 'name', action.__name__)
            if name in self.config.BLACKLIST:
                if self.config.VERBOSE:
                    print("BOT: Removing blacklisted action {}.".format(name))

        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((self.host, self.port))

    def handle_connect(self):
        """Executes together with the first I/O operation on the socket."""
        self._outbuf = 'NICK {}\r\n'.format(self.nick)
        self._outbuf += 'USER {} 0 * :{}\r\n'.format(self.nick, self.realname)
        for channel in self.channels:
            self._outbuf += 'JOIN {}\r\n'.format(channel)

    def handle_close(self):
        """Close the socket on connection close."""
        self.close()

    def handle_read(self):
        """Execute when there is data on the socket
        ready for a read operation."""
        try:
            self._inbuf += self.recv(512).decode('utf-8')
        except UnicodeDecodeError:
            self._inbuf += self.recv(512).decode('latin2')
        except:
            pass

        # Process the data
        self.process_data()

    def handle_error(self):
        """Reconnect on error."""

        asyncore.dispatcher.handle_error(self)

        if self.config.VERBOSE:
            print('Connection lost, reconnecting...')

        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((self.host, self.port))

    def _send(self, data):
        """Add the data to the output buffer."""
        self._outbuf += data + '\r\n'

    def process_data(self):
        """Process the incoming data and perform operations."""
        while True:
            # Find the end of a line of text
            end = self._inbuf.find('\r\n')

            if end == -1:
                break

            # Get the line and remove it from the input buffer
            line = self._inbuf[:end]
            self._inbuf = self._inbuf[end + 2:]

            if self.config.VERBOSE:
                print(line)

            # Process the line
            groups = self.irc_message.match(line).groupdict()
            prefix = groups.get('prefix')
            command = groups.get('command')
            parameters = groups.get('params')
            trailing = groups.get('trail')

            # If it's a PING then respond with a PONG and continue
            if command == 'PING':
                self._send('PONG {}'.format(trailing))
                continue

            for action in self._actions:
                match = None
                if trailing and action.rule:
                    pattern = action.rule.replace('$botnick', self.nick)
                    match = re.search(pattern, trailing,
                                      re.LOCALE | re.UNICODE)

                if match or command in action.events:
                    action(self, Message(prefix, command, parameters,
                                         trailing), match)

    def writable(self):
        """Return True if there is data to be sent by the socket
        else return False."""
        return (len(self._outbuf) > 0)

    def handle_write(self):
        """Executes when there is data to be sent through the socket
        and sends it."""
        sent = self.send(self._outbuf.encode('utf-8'))
        self._outbuf = self._outbuf[sent:]

    def register(self, action):
        """Register a new bot action."""

        name = getattr(action, 'name', action.__name__)

        # If the action is invalid mention it
        if not isclass(action) and not hasattr(action, 'events') and\
           not hasattr(action, 'rule'):
            raise AttributeError("""Action {} doesn\'t have any means """
                                 """to begin. Define a rule or events"""
                                 """on which the action should """
                                 """be called.""".format(name))
        # Register the action
        if isclass(action):
            print("BOT: Registered action {}.".format(action.__name__))
            for a in action(self)._actions:
                self._actions.append(a)
                print('BOT: \_Registerd subaction {}.'.format(a.__name__))
        elif isfunction(action):
            self._actions.append(action)
            print("BOT: Registered action {}.".format(name))

    def say(self, message, *args, **kwargs):
        """Say the message to the given recipient.
        All channels if no recipient specified."""

        action = kwargs.get('action', False)

        for msg in message.split('\n'):
            # If the message is an action to perform
            if action:
                msg = '\001ACTION {}\001'.format(msg)

            try:
                recpt = args[0]
            except IndexError:
                recpt = None

            if not recpt:
                for channel in self.channels:
                    self._send('PRIVMSG {} :{}\r\n'.format(channel, msg))
            else:
                self._send('PRIVMSG {} :{}\r\n'.format(recpt, msg))

    def command(self, *args):
        """Perform the given command on the channel."""
        self._send('{}\r\n'.format(' '.join(args)))
