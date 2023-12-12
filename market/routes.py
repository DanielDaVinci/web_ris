import os

from flask import (
    Blueprint, render_template,
    request, current_app,
    session, redirect, url_for
)

from access import login_required, group_required, external_required
from cache.wrapper import fetch_from_cache
from database.operations import select, insert
from database.sql_provider import SQLProvider

blueprint_market = Blueprint(
    'blueprint_market',
    __name__,
    template_folder='templates',
    static_folder='static'
)
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_market.route('/', methods=['GET', 'POST'])
def market_index():
    if request.method == 'GET':
        return render_template('market/index.html',
                               is_logged=session.get('user_group', None),
                               search_parameters=session.get('search', None))
    else:
        session['search'] = {
            'departure_city': request.form.get('departure_city', None),
            'arrival_city': request.form.get('arrival_city', None),
            'flight_time': request.form.get('flight_time', None)
        }
        print(session['search'])

        values = [session['search'][key] for key in session['search'].keys()]
        if None in values or '' in values:
            return render_template('market/index.html',
                                   is_logged=session.get('user_group', None),
                                   search_parameters=session['search'])

        return redirect(url_for('blueprint_market.market_search'))


@blueprint_market.route('/search', methods=['GET', 'POST'])
def market_search():
    db_config = current_app.config['db_config']
    cache_config = current_app.config['cache_config']

    if request.method == 'GET':

        if not session.get('search', None):
            session['search'] = {
                'departure_city': '',
                'arrival_city': '',
                'flight_time': ''
            }

        sql = provider.get('find_flights_by_parameters.sql',
                           departure_city=session['search']['departure_city'],
                           arrival_city=session['search']['arrival_city'],
                           flight_time=session['search']['flight_time'])

        flights = select(db_config, sql)
        print(flights)

        return render_template('market/search.html',
                               is_logged=session.get('user_group', None),
                               search_parameters=session['search'],
                               flights=flights)
    else:
        session['search'] = {
            'departure_city': request.form.get('departure_city', None),
            'arrival_city': request.form.get('arrival_city', None),
            'flight_time': request.form.get('flight_time', None)
        }

        values = [session['search'][k] for k in session['search'].keys()]

        if None in values or '' in values:
            return render_template('market/search.html',
                                   is_logged=session.get('user_group', None),
                                   search_parameters=session['search'])

        return redirect(url_for('blueprint_market.market_search'))


@blueprint_market.route('/registration/<int:schedule_id>', methods=['GET', 'POST'])
def registration_ticket(schedule_id):
    db_config = current_app.config['db_config']

    if request.method == 'GET':
        sql = provider.get('find_flight_by_schedule_id.sql', schedule_id=schedule_id)
        result = select(db_config, sql)

        if not result:
            return redirect(url_for('blueprint_market.market_search'))

        flight = result[0]

        return render_template('market/registration_ticket.html',
                               is_logged=session.get('user_group', None),
                               flight=flight,
                               buy_parameters=session.get('buy', None))
    else:
        session['buy'] = {
            'schedule_id': schedule_id,
            'name': request.form.get('name', None),
            'surname': request.form.get('surname', None),
            'passport_info': request.form.get('passport_info', None),
        }

        values = [session['buy'][k] for k in session['buy'].keys()]

        if None in values or '' in values:
            return redirect(url_for('blueprint_market.registration_ticket',
                                    is_logged=session.get('user_group', None),
                                    schedule_id=schedule_id))

        return redirect(url_for('blueprint_market.buy_ticket'))


@blueprint_market.route('/buy')
@external_required
def buy_ticket():
    db_config = current_app.config['db_config']

    if not session.get('buy', None):
        return redirect(url_for('blueprint_market.market_index'))

    sql = provider.get('get_price_by_schedule_id.sql', schedule_id=session['buy']['schedule_id'])
    price = select(db_config, sql)[0]['price']

    sql = provider.get('insert_ticket.sql',
                       buyer_name=session['buy']['name'],
                       buyer_surname=session['buy']['surname'],
                       passport_info=session['buy']['passport_info'],
                       price=price,
                       schedule_id=session['buy']['schedule_id'],
                       user_id=session['user_id'])
    insert(db_config, sql)

    sql = provider.get('find_flight_by_schedule_id.sql', schedule_id=session['buy']['schedule_id'])
    flight = select(db_config, sql)[0]

    session.pop('buy')

    return render_template('market/success.html',
                           is_logged=session.get('user_group', None),
                           flight=flight)
