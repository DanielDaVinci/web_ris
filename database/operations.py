from typing import List

from .connection import DBContextManager
from .sql_provider import SQLProvider
from datetime import datetime


def select(db_config: dict, sql: str) -> List:
    result = []
    with DBContextManager(db_config) as cursor:
        if cursor is None:
            raise ValueError('Курсор не создан')

        cursor.execute(sql)
        schema = [column[0] for column in cursor.description]

        for row in cursor.fetchall():
            result.append(dict(zip(schema, row)))

    return result


def insert(db_config: dict, sql: str):
    with DBContextManager(db_config) as cursor:
        if cursor is None:
            raise ValueError('Курсор не создан')

        result = cursor.execute(sql)

        if not result:
            raise ValueError('Incorrect SQL Insert')


def call_procedure(db_config: dict, proc_name: str, *args):
    result = []
    with DBContextManager(db_config) as cursor:
        if cursor is None:
            raise ValueError('Курсор не создан')

        param_list = []
        for arg in args:
            param_list.append(arg)

        cursor.callproc(proc_name, param_list)

        schema = [column[0] for column in cursor.description]

        for row in cursor.fetchall():
            result.append(dict(zip(schema, row)))

    return result

# def save_order_with_list(db_config: dict, user_id: int, current_basket: dict, provider: SQLProvider):
#     with DBContextManager(db_config) as cursor:
#         if cursor is None:
#             raise ValueError('Курсор не создан')
#
#         current_date = str(datetime.now().date())
#         sql1 = provider.get('insert_order.sql', user_id=user_id, order_date=current_date)
#         result1 = cursor.execute(sql1)
#
#         if result1 != 1:
#             raise ValueError('Incorrect SQL Insert')
#
#         sql2 = provider.get('select_order_by_user_id.sql', user_id=user_id)
#         cursor.execute(sql2)
#         order_id = cursor.fetchall()[-1][0]
#
#         if order_id:
#             sum_price = 0
#             for key in current_basket:
#                 prod_amount = current_basket[key]['amount']
#                 prod_sum = current_basket[key]['amount'] * current_basket[key]['price']
#                 sum_price += prod_sum
#
#                 sql3 = provider.get('insert_order_list.sql', order_id=order_id, prod_id=key, prod_amount=prod_amount, prod_sum=prod_sum)
#                 cursor.execute(sql3)
#
#             return order_id, sum_price
#
#     return 0, 0
