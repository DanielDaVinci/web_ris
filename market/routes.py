import os

from flask import (
    Blueprint, render_template,
    request, current_app,
    session, redirect, url_for
)

from datetime import datetime
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
        basket = session.get('basket', None)

        print('all flights:', flights)
        print('basket:', session.get('basket', None))

        return render_template('market/search.html',
                               is_logged=session.get('user_group', None),
                               search_parameters=session['search'],
                               flights=flights,
                               basket=list(basket.values()) if basket else None,
                               min_date=datetime.now().date())
    else:
        session['search'] = {
            'departure_city': request.form.get('departure_city', None),
            'arrival_city': request.form.get('arrival_city', None),
            'flight_time': request.form.get('flight_time', None)
        }

        if request.form.get('schedule_id', None):
            schedule_id = request.form['schedule_id'].split('.')

            if schedule_id[0] == 'add':
                add_ticket(db_config, schedule_id[1])
            else:
                remove_ticket(db_config, schedule_id[1])

        return redirect(url_for('blueprint_market.market_search'))


def add_ticket(db_config, schedule_id):
    current_basket = session.get('basket', {})

    if schedule_id in current_basket:
        count = current_basket[schedule_id]['count']
        price = float(current_basket[schedule_id]['price']) / count

        current_basket[schedule_id]['count'] = count + 1
        current_basket[schedule_id]['price'] = price * (count + 1)
    else:
        sql = provider.get('find_flight_by_schedule_id.sql', schedule_id=schedule_id)
        flight = select(db_config, sql)[0]
        flight.update(count=1)
        current_basket[schedule_id] = flight

    session['basket'] = current_basket
    session.permanent = True


def remove_ticket(db_config, schedule_id):
    current_basket = session.get('basket', {})

    if schedule_id in current_basket:
        count = current_basket[schedule_id]['count']
        price = float(current_basket[schedule_id]['price']) / count

        if count == 1:
            current_basket.pop(schedule_id)
        else:
            current_basket[schedule_id]['count'] = count - 1
            current_basket[schedule_id]['price'] = price * (count - 1)

    session['basket'] = current_basket
    session.permanent = True


@blueprint_market.route('/registration', methods=['GET', 'POST'])
def registration_ticket():
    db_config = current_app.config['db_config']
    basket = session.get('basket', None)

    if request.method == 'GET':

        if not basket:
            return redirect(url_for('blueprint_market.market_search'))

        total_price = 0
        for schedule_id in basket.keys():
            total_price += float(basket[schedule_id]['price'])

        session['parameters'] = {schedule_id: {
            count: {
                'name': session.get('parameters', {}).get(schedule_id, {}).get(count, {}).get('name', ''),
                'surname': session.get('parameters', {}).get(schedule_id, {}).get(count, {}).get('surname', ''),
                'passport_info': session.get('parameters', {}).get(schedule_id, {}).get(count, {}).get('passport_info', '')
            } for count in range(basket[schedule_id]['count'])
        } for schedule_id in basket.keys()
        }
        print(session['parameters'])

        return render_template('market/registration_ticket.html',
                               is_logged=session.get('user_group', None),
                               basket=list(basket.values()),
                               total_price=total_price,
                               parameters=session.get('parameters', None))
    else:
        session['parameters'] = {schedule_id: {
            count: {
                'name': request.form.get(f'name.{schedule_id}.{count}', ''),
                'surname': request.form.get(f'surname.{schedule_id}.{count}', ''),
                'passport_info': request.form.get(f'passport_info.{schedule_id}.{count}', '')
            } for count in range(basket[schedule_id]['count'])
        } for schedule_id in basket.keys()
        }

        parameters = session['parameters']
        for schedule_id in parameters.keys():
            for count in parameters[schedule_id].keys():
                value = parameters[schedule_id][count]

                if not value['name'].isalpha() or not value['surname'].isalpha() or not value['passport_info'].isdigit():
                    return redirect(url_for('blueprint_market.registration_ticket'))

        return redirect(url_for('blueprint_market.buy_ticket'))


@blueprint_market.route('/buy')
def buy_ticket():
    db_config = current_app.config['db_config']

    parameters = session['parameters']
    if not parameters:
        return redirect(url_for('blueprint_market.registration_ticket'))

    sum_price = 0
    for schedule_id in parameters.keys():
        for count in parameters[schedule_id].keys():
            sql = provider.get('get_price_by_schedule_id.sql', schedule_id=schedule_id)
            price = select(db_config, sql)[0]['price']

            sql = provider.get('insert_ticket.sql',
                               buyer_name=parameters[schedule_id][count]['name'],
                               buyer_surname=parameters[schedule_id][count]['surname'],
                               passport_info=parameters[schedule_id][count]['passport_info'],
                               price=price,
                               schedule_id=schedule_id,
                               user_id='NULL')
            insert(db_config, sql)

            sum_price += price

    session.pop('basket')
    session.pop('parameters')

    return render_template('market/success.html',
                           is_logged=session.get('user_group', None))
