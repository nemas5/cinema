import os
from flask import Blueprint, render_template, request, current_app, session
from db_utilities.work_with_db import select_dict, insert_table
from db_utilities.sql_provider import SQLProvider


blueprint_film = Blueprint('bp_film', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_film.route('/<f_id>', methods=['GET'])
def get_film(f_id: int):
    _sql = provider.get('get_film.sql', f_id=f_id)
    film = select_dict(current_app.config['db_config'], _sql)[0]
    _sql = provider.get('get_sessions_list.sql', f_id=f_id)
    sessions = select_dict(current_app.config['db_config'], _sql)
    print(film, sessions)
    if sessions is None:
        sessions = []
    return render_template('film_dynamic.html', sessions=sessions, film=film)
