import os
from flask import Blueprint, render_template, request, current_app, session
from db_utilities.work_with_db import select_dict, insert_table
from db_utilities.sql_provider import SQLProvider


blueprint_schedule = Blueprint('bp_schedule', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_schedule.route('/')
def get_schedule():
    _sql = provider.get('get_session_list.sql')
    sessions = select_dict(current_app.config['db_config'], _sql)
    print(sessions)
    return render_template('schedule_dynamic.html', sessions=sessions)
