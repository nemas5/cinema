import os
from flask import Blueprint, render_template, request, current_app, session
from db_utilities.work_with_db import select_dict, insert_table
from db_utilities.sql_provider import SQLProvider

from access import group_req


blueprint_update = Blueprint('bp_update', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_update.route('/admin')
@group_req
def admin_menu():
    return render_template('admin_panel.html')


@blueprint_update.route('/film', methods=['GET', 'POST'])
@group_req
def add_film():
    if request.method == 'GET':
        return render_template('add_film.html')
    name = request.form.get('name')
    director = request.form.get('director')
    country = request.form.get('country')
    year = request.form.get('year')
    duration = request.form.get('duration')
    _sql = provider.get('add_film.sql', nm=name, director=director,
                        duration=duration, country=country, year=year,
                        u_id=session['user_id'])
    insert_table(current_app.config['db_config'], _sql)
    return 'Фильм добавлен'


@blueprint_update.route('/ses', methods=['GET', 'POST'])
@group_req
def add_ses():
    if request.method == 'GET':
        return render_template('add_ses.html')
    f_id = request.form.get('f_id')
    h_id = request.form.get('h_id')
    coef = request.form.get('coef')
    dt = request.form.get('dt')
    _sql = provider.get('add_film.sql', f_id=f_id, director=h_id,
                        duration=coef, country=dt, u_id=session['user_id'])
    insert_table(current_app.config['db_config'], _sql)
    return 'Сеанс добавлен'
