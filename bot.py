#! /usr/bin/python3
"""
bot.py -- A simple IRC bot
Copyright 2013, Paweł Jan Czochański
Licensed under the GPL v3 license.
"""

import asyncore
import imp
import argparse
import os
from ircbot import IRCBot

parser = argparse.ArgumentParser(description='Python IRC bot.')
parser.add_argument('--verbose', action='store_true',
                    help='Become more verbose.')
parser.add_argument('config', type=str,
                    help='A py file with the bot\'s config.')
arguments = parser.parse_args()

# Load the config from the given file
if not os.path.exists(arguments.config):
    raise ValueError('Config file {}'
            'does not exist.'.format(arguments.config,))
config = imp.load_source('config', arguments.config)

# Set verbose mode if needed
VERBOSE = config.VERBOSE or arguments.verbose

# Create the bot
ircbot = IRCBot()
ircbot.setup(config)

# Load the actions from the specified modules
for path in config.MODULES:
    if not os.path.exists(path):
        raise ValueError('Module %s does not exist.' % (path, ))
    name = os.path.basename(path)[:-3]
    module = imp.load_source(name, path)

# Start the bot
asyncore.loop()
