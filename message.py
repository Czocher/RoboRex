import re


class Message:
    """Represents a single message."""
    irc_prefix = re.compile('^((?P<nick>\S+)\!(?P<user>\S+)\@(?P<host>\S+))?'
                            '(?P<servername>\S+)?$')

    def __init__(self, prefix, command, parameters, trailing):
        self._prefix = prefix
        self._command = command
        self._parameters = parameters
        self._trailing = trailing

        groups = self.irc_prefix.match(prefix).groupdict()
        self.servername = groups['servername']
        self.nick = groups.get('nick')
        self.user = groups.get('user')
        self.host = groups.get('host')

        if command == 'PRIVMSG':
            if parameters.startswith('#'):
                self.channel = parameters
            else:
                self.channel = self.nick
            self.content = trailing
        elif command == 'JOIN':
            self.channel = trailing
        elif command == 'PART':
            self.channel = parameters
            self.content = trailing
        elif command == 'QUIT':
            self.content = trailing
        elif command == 'MODE':
            if '@' in prefix:
                self.channel, self.mode, self.whom = parameters.split()
            else:
                self.who = prefix
                self.whom = parameters
                self.what = trailing

    def __getitem__(self, index):
        return getattr(self, index, None)
