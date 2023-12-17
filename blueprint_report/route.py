import os
import datetime
from flask import render_template, Blueprint, request, current_app, session, url_for, redirect
from db_utilities.sql_provider import SQLProvider
from db_utilities.work_with_db import select_dict, insert_table
from access import group_req


blueprint_report = Blueprint('bp_report', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_report.route('/menu')
@group_req
def report_menu():
    return render_template('reports_menu.html', reports=current_app.config['reports_config'])


@blueprint_report.route('/sells')
@group_req
def sells_report():
    return render_template('sells_report.html')


@blueprint_report.route('/create', methods=['GET', 'POST'])
@group_req
def create_report():
    if request.method == 'GET':
        return render_template('create_report.html')
    year = int(request.form.get('start'))
    month = int(request.form.get('end'))
    if year and month:
        start = datetime.datetime(int(year), int(month), 1)
        if month == 12:
            year += 1
            month = 0
        end = datetime.datetime(year, month + 1, 1)
        _sql = provider.get('create_report.sql', start=start, end=end)
        insert_table(current_app.config['db_config'], _sql)
        return "Отчёт успешно создан"
    return "Даты введены некорректно"


@blueprint_report.route('/view', methods=['GET', 'POST'])
@group_req
def view_report():
    if request.method == 'GET':
        return render_template('view_report.html')
    year = int(request.form.get('start'))
    month = int(request.form.get('end'))
    if year and month:
        start = datetime.datetime(int(year), int(month), 1)
        if month == 12:
            year += 1
            month = 0
        end = datetime.datetime(year, month + 1, 1)
        print(start, end)
        _sql = provider.get('view_report.sql', start=start, end=end)
        reports = select_dict(current_app.config['db_config'], _sql)
        print(reports)
        return render_template('dynamic_report.html', start=start, end=end, reports=reports)
    return "Даты введены некорректно"
