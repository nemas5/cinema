import os
from flask import render_template, Blueprint, request, current_app, session, url_for, redirect
from db_utilities.sql_provider import SQLProvider
from db_utilities.work_with_db import select_dict


blueprint_order = Blueprint('bp_order', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_order.route('/', method=['GET', 'POST'])
def order_index():
    if request.method == 'GET':
        _sql = provider.get('all_products.sql')
        products = select_dict(current_app.config['db_config'], _sql)
        current_basket = session.get('basket', {})
        return render_template('basket_order_list.html', items=products, basket=current_basket)
    else:
        prod_id = request.form.get('prod_id')
        _sql = provider.get('get_prod.sql', prod_id=prod_id)
        item = select_dict(current_app.config['db_config'], _sql)
        add_to_basket(prod_id, item)
        return redirect(url_for('bp_order.order_index'))
    # Сделать редирект - создать новый хтпп запрос гет с указанием того урл, что в редиректе


def add_to_basket(prod_id, item):
    session.permanent = True
    pass
# Фласк отслеживает появление новых ключей в сессии, но не отслеживает изменения
# Оформление заказа - занесение информации в базу данных

@blueprint_order.route('/save_order')
def save_order():
    pass
    # одну в ордер
    # по количеству товаров в корзине к моменту нажатия ордер лист заполнить


# первая запись user order
# потом в order list