import json
import os

from flask import Flask, render_template, session

from blueprint_auto.route import blueprint_auto
from blueprint_film.route import blueprint_film
from blueprint_session.route import blueprint_session
from blueprint_schedule.route import blueprint_schedule
from blueprint_updates.route import blueprint_update
from blueprint_report.route import blueprint_report
from blueprint_query.route import blueprint_query

from db_utilities.sql_provider import SQLProvider
from db_utilities.work_with_db import select_dict


app = Flask(__name__)
with open('data_files/db_config.json') as file:
    app.config['db_config'] = json.load(file)
with open('data_files/access.json') as file:
    app.config['access_config'] = json.load(file)
with open('data_files/reports.json') as file:
    app.config['reports_config'] = json.load(file)
with open('data_files/query.json', encoding='utf-8') as file:
    app.config['query_config'] = json.load(file)
app.register_blueprint(blueprint_auto, url_prefix='/auto')
app.register_blueprint(blueprint_film, url_prefix='/film')
app.register_blueprint(blueprint_session, url_prefix='/session')
app.register_blueprint(blueprint_schedule, url_prefix='/schedule')
app.register_blueprint(blueprint_update, url_prefix='/update')
app.register_blueprint(blueprint_report, url_prefix='/report')
app.register_blueprint(blueprint_query, url_prefix='/query')
app.secret_key = 'key'

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))
print(app.config['reports_config'])
print(app.config['query_config'])


@app.route('/', methods=['GET'])
def main_menu():
    _sql = provider.get('get_film_list.sql')
    films = select_dict(app.config['db_config'], _sql)
    print(films)
    return render_template('main_menu.html', films=films)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)
