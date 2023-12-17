import os
import datetime
from flask import Blueprint, render_template, request, current_app, session, redirect, url_for
from db_utilities.work_with_db import select_dict, insert_table
from db_utilities.sql_provider import SQLProvider
from access import login_req


blueprint_session = Blueprint('bp_session', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_session.route('/add/<ses_id>/<t_id>')
def add_to_basket(ses_id: int, t_id: int):
    session.permanent = True
    if not('basket' in session):
        session['basket'] = []
    session['basket'].append(int(t_id))
    return redirect(url_for('bp_session.get_session', ses_id=ses_id))


@blueprint_session.route('/remove/<ses_id>/<t_id>')
def remove_from_basket(ses_id: int, t_id: int):
    session['basket'].remove(int(t_id))
    return redirect(url_for('bp_session.get_session', ses_id=ses_id))


@blueprint_session.route('/<ses_id>')
def get_session(ses_id: int):
    _sql = provider.get('get_session.sql', ses_id=ses_id)
    ses = select_dict(current_app.config['db_config'], _sql)[0]
    _sql = provider.get('get_tickets.sql', ses_id=ses_id)
    tickets = select_dict(current_app.config['db_config'], _sql)
    if 'basket' in session:
        basket = session['basket']
    else:
        basket = []
    print(basket, tickets)
    return render_template('session_dynamic.html', ses=ses, tickets=tickets,
                           basket=basket)


@blueprint_session.route('/order/<ses_id>')
@login_req
def order(ses_id: int):
    ses_id = int(ses_id)
    if 'basket' in session and len(session['basket']) != 0:
        for i in session['basket']:
            _sql = provider.get('buy_ticket.sql', ses_id=ses_id, t_id=i)
            insert_table(current_app.config['db_config'], _sql)
        _sql = provider.get('add_check.sql', u_id=session['user_id'], dt=datetime.datetime.now())
        insert_table(current_app.config['db_config'], _sql)
        session.pop('basket')
        return redirect(url_for('bp_session.get_session', ses_id=ses_id))
    return redirect(url_for('bp_session.get_session', ses_id=ses_id))