=============
RoboRex
=============
:Info: See `github <http://github.com/czocher/roborex>` for the latest source.
:Author: Paweł Jan Czochański <czochanski@gmail.com>

About
=====

RoboRex is a very simple irc bot written in Python without any external dependencies. It's very small (200 lines of code) and easy to expand with modules.

Usage
-----

Copy the `default_config.py` file and set all needed parameters.

Run the bot with the `python3 bot.py config_file.py` command.

Run `python3 bot.py` for usage info.

Writing modules
===============

Bot functionalities can be expanded with simple functions matched using IRC events or regular expressions. Some simple, well-commented examples can be found in the `example_module.py` file.

In the `action.py` file a `action` decorator and a `MultiAction` class are defined which simplify module writing. More information regarding module writing can be found in the example_module file.

At least one event or rule must be given for each bot action, if a rule and an event is given at the same time, rules have priority over events.

Simple function example::

  @action(events=('PRIVMSG',))
  def repeat(bot, message, *args, **kwargs):
      """Repeat every message on the chat."""
      bot.say(message.content, message.channel)

The bot actions recieve the following named parameters on input:

-  bot - the main bot object.
-  message - a object containing the full information about the recived IRC message. For more information see the message definition in the `message.py` file.
-  match - the regexp match object returned after a successful re.match python operation.

If you need your own configuration options (eg. for your own module) you can access them from the bot.config class field.

Useful bot class methods:

-  command(args) - perform the given command on the server
-  say(message, to_whom, action=False) - sends the given string as PRIVMSG to the given nick or channel. If no recipient specified the PRIVMSG is sent to all channels, if action == True, then message is sent as an action.
