import os
from flask import Blueprint, render_template, request, current_app

from database.operations import select
from database.sql_provider import SQLProvider

blueprint_query = Blueprint(
    'blueprint_query',
    __name__,
    template_folder='templates',
    static_folder='static'
)
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_query.route('/')
def query_index():
    return render_template('query/query_menu.html')


@blueprint_query.route('/query_light_1', methods=['GET', 'POST'])
def query_light_1():
    if request.method == 'GET':
        return render_template('query/query_light_1.html', wrong=False)
    else:
        flight_id_name = request.form.get('flight_id_name')

        sql = provider.get('query_light_1.sql', start_flight_id=flight_id_name)
        flights = select(current_app.config['db_config'], sql)

        if flights:
            return render_template('query/dynamic.html', table_items=flights, back_site='blueprint_query.query_light_1')
        else:
            return render_template('query/query_light_1.html', wrong=True)


@blueprint_query.route('/query_light_2', methods=['GET', 'POST'])
def query_light_2():
    if request.method == 'GET':
        return render_template('query/query_light_2.html', wrong=False)
    else:
        date = request.form.get('date')

        sql = provider.get('query_light_2.sql', year=date[:4], month=date[5:7])
        flights = select(current_app.config['db_config'], sql)

        if flights:
            return render_template('query/dynamic.html', table_items=flights, back_site='blueprint_query.query_light_2')
        else:
            return render_template('query/query_light_2.html', wrong=True)


@blueprint_query.route('/query_light_3', methods=['GET', 'POST'])
def query_light_3():
    if request.method == 'GET':
        return render_template('query/query_light_3.html', wrong=False)
    else:
        days = request.form.get('days')

        sql = provider.get('query_light_3.sql', days=days)
        flights = select(current_app.config['db_config'], sql)

        if flights:
            return render_template('query/dynamic.html', table_items=flights, back_site='blueprint_query.query_light_3')
        else:
            return render_template('query/query_light_3.html', wrong=True)


@blueprint_query.route('/query_hard_1', methods=['GET', 'POST'])
def query_hard_1():
    if request.method == 'GET':
        return render_template('query/query_hard_1.html', wrong=False)
    else:
        date = request.form.get('date')

        sql = provider.get('query_hard_1.sql', year=date[:4], month=date[5:7])
        flights = select(current_app.config['db_config'], sql)

        if flights:
            return render_template('query/dynamic.html', table_items=flights, back_site='blueprint_query.query_hard_1')
        else:
            return render_template('query/query_hard_1.html', wrong=True)


@blueprint_query.route('/query_hard_2', methods=['GET', 'POST'])
def query_hard_2():
    if request.method == 'GET':
        return render_template('query/query_hard_2.html', wrong=False)
    else:
        year = request.form.get('year')

        sql = provider.get('query_hard_2.sql', year=year)
        flights = select(current_app.config['db_config'], sql)

        if flights:
            return render_template('query/dynamic.html', table_items=flights, back_site='blueprint_query.query_hard_2')
        else:
            return render_template('query/query_hard_2.html', wrong=True)


@blueprint_query.route('/query_hard_3', methods=['GET', 'POST'])
def query_hard_3():
    if request.method == 'GET':
        return render_template('query/query_hard_3.html', wrong=False)
    else:
        flight_id_name = request.form.get('flight_id_name')
        date = request.form.get('date')

        sql = provider.get('query_hard_3.sql', flight_id_name=flight_id_name, year=date[:4], month=date[5:7])
        flights = select(current_app.config['db_config'], sql)

        if flights:
            return render_template('query/dynamic.html', table_items=flights, back_site='blueprint_query.query_hard_3')
        else:
            return render_template('query/query_hard_3.html', wrong=True)
