from importlib.metadata import version
import logging
import random

from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from functools import wraps
from lib.dnd import DndCommand
from lib.query_pass import QueryPassCommand


LOG_FILENAME = '/data/jack_bunny.log'
logging.basicConfig(
        filename=LOG_FILENAME,
        format="%(asctime)s\t%(name)s:%(levelname)s:call:%(message)s",
        level=logging.DEBUG,
)


app = Flask(__name__)
dnd = DndCommand()
google = QueryPassCommand('g', 'https://www.google.com/search')
ddgo = QueryPassCommand('d', 'https://duckduckgo.com/')

app.add_url_rule(google.flask_routes()[0], view_func=google.gen_response, endpoint="google")
app.add_url_rule(ddgo.flask_routes()[0], view_func=ddgo.gen_response, endpoint="ddgo")


for r in dnd.flask_routes():
    app.add_url_rule(r, view_func=dnd.gen_response)



def log_calls(f):
        @wraps(f)
        def decorated(*args, **kwargs):
                logging.info(f.__name__)
                return f(*args, **kwargs)
        return decorated


class Commands(object):


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
                new_url = request.host_url + f"/{search_command}?q={str(request.args.get('query', ''))}"
                logging.info(new_url)
                return redirect(new_url)
        except Exception as e:
                print(e)
                return f"{e} :: {request}"

if __name__ == '__main__':
        app.run()
