import os
from flask import Blueprint, render_template, request, current_app, session
from db_utilities.work_with_db import select_dict, insert_table
from db_utilities.sql_provider import SQLProvider
from access import login_req, group_req


blueprint_query = Blueprint('bp_query', __name__, template_folder='templates')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_query.route('/', methods=['GET'])
@group_req
def query_menu():
    if request.method == 'GET':
        config = current_app.config['query_config']
        return render_template('query_menu.html', config=config, keys=config.keys())


@blueprint_query.route('/<query_id>', methods=['GET', 'POST'])
@group_req
def query(query_id: str):
    config = current_app.config['query_config'][query_id]
    if request.method == 'GET':
        if query_id == "query_1" or query_id == "query_2":
            _sql = provider.get(config['query_file'])
            ans = select_dict(current_app.config['db_config'], _sql)
            print(ans)
            return render_template("output_dynamic.html", config=config, ans=ans)
        else:
            return render_template("input_dynamic.html", config=config)
    else:
        param = dict()
        for i in config['input_id']:
            param[i] = request.form.get(i)
        _sql = provider.get(config['query_file'], config=config, **param)
        ans = select_dict(current_app.config['db_config'], _sql)
        print(ans)
        return render_template("output_dynamic.html", config=config, ans=ans)