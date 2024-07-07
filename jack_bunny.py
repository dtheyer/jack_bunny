from importlib.metadata import version
import logging
import random

from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from functools import wraps


app = Flask(__name__)

LOG_FILENAME = '/data/jack_bunny.log'
logging.basicConfig(
        filename=LOG_FILENAME,
        format="%(asctime)s\t%(name)s:%(levelname)s:call:%(message)s",
        level=logging.DEBUG,
)


def log_calls(f):
        @wraps(f)
        def decorated(*args, **kwargs):
                logging.info(f.__name__)
                return f(*args, **kwargs)
        return decorated


class Commands(object):

        @log_calls
        def g(self, arg=None):
                """'g [search_query]' search Google"""
                if arg:
                        return 'http://www.google.com/search?q={0}'.format(arg)
                else:
                        return 'https://www.google.com'

        @log_calls
        def d20(self, arg=None):
                roll = random.randint(1, 20)
                return f'You got a {roll}!'

        @log_calls
        def d(self, arg=None):
                """'d [search_query]' search DuckDuckGo"""
                if arg:
                        return 'https://duckduckgo.com/?q={0}'.format(arg)
                else:
                        return 'https://duckduckgo.com/'

        @log_calls
        def help(self, arg=None):
                """'help' returns a list of usable commands """
                help_list = []
                for values in Commands.__dict__.values():
                        if callable(values):
                                help_list.append(values.__doc__)
                return help_list

        # [CUSTOM SHORTCUTS] Add your company shortcuts here.
        # [END CUSTOM SHORTCUTS]


@app.route('/')
def index():
        return render_template('home.html')


@app.route('/q/')
def route():
        # Process the query.
        try:
                query = str(request.args.get('query', ''))
                tokenized_query = query.split(' ', 1)
                search_command = tokenized_query[0].lower()
                option_args = None
                if len(tokenized_query) == 2:
                        option_args = tokenized_query[1]
        except Exception as e:
                print(e)
                search_command = query
                option_args = None

        try:
                command = getattr(Commands(), search_command)
                if search_command == 'help':
                        return render_template(
                                'help.html',
                                command_list=command(None)
                        )
                url = command(option_args)
                if not "http" in url:
                    return url
                return redirect(url)
        except Exception as e:
                # Fallback option is to google search.
                logging.error(str(e) + ' %s' % str(request))
                return redirect(Commands().g(query))


if __name__ == '__main__':
        app.run()
