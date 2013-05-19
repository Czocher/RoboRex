class action:
    """Decorate the given function to use with the bot.
    Keyword arguments:
    rule -- the regular expression to match in the chat messages.
    events -- a list of events to react to.
    name -- functionality user-friendly name.
    help -- docstring shown to the user as function help, if ommited
            the function docstring is taken instead."""

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __call__(self, obj):
        obj.name = self.kwargs.get('name', obj.__name__)

        obj.help = self.kwargs.get('help', obj.__doc__)
        if obj.help is None:
            raise AttributeError('{} has no documentation'.format(obj.name, ))
        else:
            obj.help = '\n'.join([h.strip() for h in obj.help.split('\n')])

        if not hasattr(obj, 'rule') and not hasattr(obj, 'events') and \
           not self.kwargs.get('rule') and not self.kwargs.get('events'):
            raise AttributeError('Action {} doesn\'t have any means'
                                 'to begin. Define a rule or events'
                                 'on which the action'
                                 'should be called.'.format(obj.name))

        if not hasattr(obj, 'rule'):
            obj.rule = self.kwargs.get('rule', '')

        if not hasattr(obj, 'events'):
            obj.events = self.kwargs.get('events', ())

        return obj


class MultiAction:
    """Class representing a combination of a few bot actions."""

    def __init__(self, bot, *args, **kwargs):
        self._actions = []

        for func_string in dir(self):

            if func_string == '__class__':
                continue
            func = getattr(self, func_string)

            if hasattr(func, 'rule') or hasattr(func, 'events'):
                self._actions.append(func)
