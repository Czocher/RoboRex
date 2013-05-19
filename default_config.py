# Basic bot information
BOT = {
    'nick': 'RoboRex',
    'realname': 'RoboRex',
    'channels': ('#Channel', )
}

# What server to join
SERVER = {
    'host': 'server.com',
    'port': 6667
}

# List of bot admins with passwords
ADMINS = {
    'Nick': 'password',
}

# What modules to load on start
MODULES = (
    'modules/admin.py',
    'modules/ignore.py',
    'modules/utils.py',
    'modules/randquote.py',
)

# Should the bot be verbose?
VERBOSE = True

# List of blacklisted function names
BLACKLIST = (
)

# List of usernames to ignore commands from
IGNORES = (
)

# Utils autogreet function configuration
GREETINGS = {
    'welcome': True, # Welcom joining users
    'bot-react': False, # React when someone says "bot"
    'name-react': False, # React when someone mentions the bots nick

    # List of greetings to use while greeting users
    'greetings': (
        'Well well well, who do we have here? Greetings {}!',
        'Hello {}!',
        'I\'m not one to gossip but {0} is... O hello {0}! Didn\'t see you there... heh',
        '\me hugs {}',
    )
}

# Randquote module configuration
RANDQUOTE = {
    'name-react': True, # Should the bot react to its name
    'bot-react': True, # Should the bot react if someone says "bot"
    'throw': 00, # The throw probability (0-100)
    'gather': 30, # the gather probability (0-100)
    'database': 'quote.db', # Database file, :memory: for RAM db
}
