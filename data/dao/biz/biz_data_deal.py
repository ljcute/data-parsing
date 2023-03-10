#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author  : yanpan
# @Time    : 2022/7/28 15:13
# @Site    : 
# @File    : biz_data_deal.py
# @Software: PyCharm
import datetime
import time
from configparser import ConfigParser
import pandas as pd
from utils.snowflake_utils import get_id
import os

from db_connection import Mysqldb

base_dir = os.path.dirname(os.path.abspath(__file__))
full_path = os.path.join(base_dir, '../../../config/config.ini')

cf = ConfigParser()
cf.read(full_path, encoding='utf-8')

config = {
    "host": cf.get('mysql-biz', 'host'),
    "port": cf.getint('mysql-biz', 'port'),
    "database": cf.get('mysql-biz', 'schema'),
    "charset": cf.get('mysql-biz', 'charset'),
    "user": cf.get('mysql-biz', 'username'),
    "passwd": cf.get('mysql-biz', 'password')
}

# 实例化
db = Mysqldb(config)

def update_business_security_useless(biz_date, secu_id, broker_id, biz_type):
    sql = f'update t_broker_mt_business_security set data_status = 0 ,biz_status = 2, end_dt= {biz_date},update_dt = now() ' \
          f'where secu_id = {secu_id} and broker_id = {broker_id} and biz_type = {biz_type} and start_dt <= {biz_date} and {biz_date} < end_dt and data_status=1 and biz_status=1'
    db.commit_data(sql)

def update_business_security_useless_jys(biz_date, secu_id, broker_id, biz_type, data_desc):
    sql = f'update t_broker_mt_business_security set data_status = 0 ,biz_status = 2, end_dt= {biz_date},update_dt = now() ' \
          f'where secu_id = {secu_id} and broker_id = {broker_id} and biz_type = {biz_type} and start_dt <= {biz_date} and {biz_date} < end_dt and data_status=1 and biz_status=1 and data_desc = {data_desc}'
    db.commit_data(sql)

def update_business_security(biz_date, secu_id, broker_id, biz_type):
    sql = f'update t_broker_mt_business_security set end_dt= {biz_date},update_dt = now() ' \
          f'where secu_id = {secu_id} and broker_id = {broker_id} and biz_type = {biz_type} and start_dt <= {biz_date} and {biz_date} < end_dt and data_status=1 and biz_status=1'
    db.commit_data(sql)


def update_business_security_one(biz_date, secu_id, broker_id, biz_type):
    sql = f'update t_broker_mt_business_security set end_dt= {biz_date},update_dt = now() ' \
          f'where secu_id = {secu_id} and broker_id = {broker_id} and biz_type = {biz_type} and start_dt <= {biz_date} and {biz_date} < end_dt and data_status=1 and biz_status=1'
    db.commit_data(sql)

def update_business_security_one_jys(biz_date, secu_id, broker_id, biz_type,data_desc):
    sql = f'update t_broker_mt_business_security set end_dt= {biz_date},update_dt = now() ' \
          f'where secu_id = {secu_id} and broker_id = {broker_id} and biz_type = {biz_type} and start_dt <= {biz_date} and {biz_date} < end_dt and data_status=1 and biz_status=1 and data_desc = {data_desc}'
    db.commit_data(sql)

def update_business_expalin(biz_date, secu_id, broker_id, biz_type, forever_end_dt):
    sql = f'update t_broker_mt_business_security set end_dt = "{forever_end_dt}",update_dt = now() ' \
          f'where secu_id = {secu_id} and broker_id = {broker_id} and biz_type = {biz_type} and start_dt != {biz_date} and end_dt = {biz_date} and data_status=1 and biz_status=1'
    print(f'sql:{sql}')
    db.commit_data(sql)

def update_business_expalin_other(biz_date, secu_id, broker_id, biz_type, forever_end_dt):
    sql = f'update t_broker_mt_business_security set data_status = 0 ,biz_status = 2,update_dt = now() ' \
          f'where secu_id = {secu_id} and broker_id = {broker_id} and biz_type = {biz_type} and start_dt = {biz_date} and end_dt = "{forever_end_dt}" and data_status=1 and biz_status=1'
    print(f'sql:{sql}')
    db.commit_data(sql)

def update_business_expalin_jys(biz_date, secu_id, broker_id, biz_type, forever_end_dt, data_desc):
    sql = f'update t_broker_mt_business_security set end_dt = "{forever_end_dt}",update_dt = now() ' \
          f'where secu_id = {secu_id} and broker_id = {broker_id} and biz_type = {biz_type} and start_dt != {biz_date} and data_status=1 and biz_status=1 and data_desc = {data_desc}'
    print(f'sql:{sql}')
    db.commit_data(sql)

def update_business_expalin_other_jys(biz_date, secu_id, broker_id, biz_type, forever_end_dt, data_desc):
    sql = f'update t_broker_mt_business_security set data_status = 0 ,biz_status = 2,update_dt = now() ' \
          f'where secu_id = {secu_id} and broker_id = {broker_id} and biz_type = {biz_type} and start_dt = {biz_date} and end_dt = "{forever_end_dt}" and data_status=1 and biz_status=1 and data_desc = {data_desc}'
    print(f'sql:{sql}')
    db.commit_data(sql)

def update_business_security_jys(biz_date, secu_id, broker_id, biz_type, data_desc):
    sql = f'update t_broker_mt_business_security set end_dt= {biz_date},update_dt = now() ' \
          f'where secu_id = {secu_id} and broker_id = {broker_id} and data_desc = {data_desc} and biz_type = {biz_type} and start_dt <= {biz_date} and {biz_date} < end_dt and data_status=1 and biz_status=1'
    db.commit_data(sql, )


def query_business_security_item(biz_dt, biz_type, broker_id):
    sql = f'select row_id,broker_id,secu_id,secu_type,biz_type,adjust_type,pre_value,cur_value from t_broker_mt_business_security ' \
          f'where start_dt <= {biz_dt} and {biz_dt} < end_dt and biz_type ={biz_type} and broker_id = {broker_id} and data_status=1 and biz_status=1'
    rs = db.select_all(sql)
    columns = []
    for i in rs:
        columns.append(str(i[2]))
    df = pd.DataFrame(list(rs), index=columns,
                      columns=['row_id', 'broker_id', 'secu_id', 'secu_type', 'biz_type', 'adjust_type', 'pre_value',
                               'cur_value'])
    return df

def query_business_security_item_today(biz_dt, biz_type, broker_id):
    sql = f'select row_id,broker_id,secu_id,secu_type,biz_type,adjust_type,pre_value,cur_value from t_broker_mt_business_security ' \
          f'where start_dt = {biz_dt} and biz_type ={biz_type} and broker_id = {broker_id} and data_status=1 and biz_status=1'
    rs = db.select_all(sql)
    columns = []
    for i in rs:
        columns.append(str(i[2]))
    df = pd.DataFrame(list(rs), index=columns,
                      columns=['row_id', 'broker_id', 'secu_id', 'secu_type', 'biz_type', 'adjust_type', 'pre_value',
                               'cur_value'])
    return df

def query_business_security_item_today_jys(biz_dt, biz_type, broker_id,data_desc):
    sql = f'select row_id,broker_id,secu_id,secu_type,biz_type,adjust_type,pre_value,cur_value from t_broker_mt_business_security ' \
          f'where start_dt = {biz_dt} and biz_type ={biz_type} and broker_id = {broker_id} and data_status=1 and biz_status=1 and data_desc = {data_desc}'
    rs = db.select_all(sql)
    columns = []
    for i in rs:
        columns.append(str(i[2]))
    df = pd.DataFrame(list(rs), index=columns,
                      columns=['row_id', 'broker_id', 'secu_id', 'secu_type', 'biz_type', 'adjust_type', 'pre_value',
                               'cur_value'])
    return df

def query_business_secu_id_item(biz_dt, biz_type, broker_id, secu_id):
    sql = f'select row_id,broker_id,secu_id,secu_type,biz_type,adjust_type,pre_value,cur_value from t_broker_mt_business_security ' \
          f'where start_dt = {biz_dt} and secu_id = {secu_id} and biz_type ={biz_type} and broker_id = {broker_id} and data_status=1 and biz_status=1'
    rs = db.select_all(sql)
    columns = []
    for i in rs:
        columns.append(str(i[2]))
    df = pd.DataFrame(list(rs), index=columns,
                      columns=['row_id', 'broker_id', 'secu_id', 'secu_type', 'biz_type', 'adjust_type', 'pre_value',
                               'cur_value'])
    return df

def query_business_secu_id_item_jys(biz_dt, biz_type, broker_id, secu_id, data_desc):
    sql = f'select row_id,broker_id,secu_id,secu_type,biz_type,adjust_type,pre_value,cur_value from t_broker_mt_business_security ' \
          f'where start_dt = {biz_dt} and secu_id = {secu_id} and biz_type ={biz_type} and broker_id = {broker_id} and data_status=1 and biz_status=1 and data_desc = {data_desc}'
    rs = db.select_all(sql)
    columns = []
    for i in rs:
        columns.append(str(i[2]))
    df = pd.DataFrame(list(rs), index=columns,
                      columns=['row_id', 'broker_id', 'secu_id', 'secu_type', 'biz_type', 'adjust_type', 'pre_value',
                               'cur_value'])
    return df

def query_business_security_item_jys(biz_dt, biz_type, broker_id, data_desc):
    sql = f'select row_id,broker_id,secu_id,secu_type,biz_type,adjust_type,pre_value,cur_value from t_broker_mt_business_security ' \
          f'where start_dt <= {biz_dt} and {biz_dt} < end_dt and biz_type ={biz_type} and broker_id = {broker_id} and data_status=1 and biz_status=1 and data_desc = {data_desc}'
    rs = db.select_all(sql)
    columns = []
    for i in rs:
        columns.append(str(i[2]))
    df = pd.DataFrame(list(rs), index=columns,
                      columns=['row_id', 'broker_id', 'secu_id', 'secu_type', 'biz_type', 'adjust_type', 'pre_value',
                               'cur_value'])
    return df


def query_is_have_secu_id(biz_dt, biz_type, broker_id, secu_id):
    sql = f'select row_id,broker_id,secu_id,secu_type,biz_type,adjust_type,pre_value,cur_value from t_broker_mt_business_security ' \
          f'where start_dt <= {biz_dt} and {biz_dt} < end_dt and biz_type ={biz_type} and broker_id = {broker_id} and secu_id = {secu_id} and data_status=1 and biz_status=1'
    rs = db.select_all(sql)
    return rs

def query_is_have_secu_id_out(biz_dt, biz_type, broker_id, secu_id, adjust_type):
    sql = f'select row_id,broker_id,secu_id,secu_type,biz_type,adjust_type,pre_value,cur_value from t_broker_mt_business_security ' \
          f'where start_dt <= {biz_dt} and {biz_dt} < end_dt and biz_type ={biz_type} and broker_id = {broker_id} and secu_id = {secu_id} and data_status=1 and biz_status=1 and adjust_type = {adjust_type}'
    rs = db.select_all(sql)
    return rs


def query_is_have_secu_id_jys(biz_dt, biz_type, broker_id, secu_id, data_desc):
    sql = f'select row_id,broker_id,secu_id,secu_type,biz_type,adjust_type,pre_value,cur_value from t_broker_mt_business_security ' \
          f'where start_dt <= {biz_dt} and {biz_dt} < end_dt and biz_type ={biz_type} and broker_id = {broker_id} and secu_id = {secu_id} and data_status=1 and biz_status=1 and data_desc = {data_desc}'
    rs = db.select_all(sql)
    return rs

def query_is_have_secu_id_jys_out(biz_dt, biz_type, broker_id, secu_id, data_desc, adjust_type):
    sql = f'select row_id,broker_id,secu_id,secu_type,biz_type,adjust_type,pre_value,cur_value from t_broker_mt_business_security ' \
          f'where start_dt <= {biz_dt} and {biz_dt} < end_dt and biz_type ={biz_type} and broker_id = {broker_id} and secu_id = {secu_id} and data_status=1 and biz_status=1 and data_desc = {data_desc} and adjust_type = {adjust_type}'
    rs = db.select_all(sql)
    return rs


def insert_broker_mt_business_security(insert_data_list):
    insert_data_list_ = []
    for i in range(0, len(insert_data_list)):
        row_id = get_id()
        insert_data_list[i].insert(0, row_id + 1)
        insert_data_list[i].append(str(datetime.datetime.now()))
        insert_data_list[i].append(str(datetime.datetime.now()))
        insert_data_list_.append(insert_data_list[i])
        time.sleep(0.001)

    sql = "insert into t_broker_mt_business_security(row_id,broker_id,secu_id,secu_type,biz_type,adjust_type,pre_value,cur_value," \
          "data_status,biz_status,start_dt,end_dt,data_desc,create_dt,update_dt) " \
          "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
    db.commit_data(sql, insert_data_list_)


def insert_data_process_controler(biz_id, data_processor, data_type, data_source, data_status, last_process_bizdt,
                                  last_process_status, last_process_result):
    ctl_id = get_id()
    value = (ctl_id, biz_id, data_processor, data_type, data_source, str(datetime.datetime.now()),
             str(datetime.datetime.now()), data_status, str(last_process_bizdt), last_process_status,
             last_process_result, str(datetime.datetime.now()), str(datetime.datetime.now()))

    sql = f'insert into t_data_process_controller values {value}'
    db.commit_data(sql)


def insert_data_process_log(biz_id, data_processor, data_type, data_source, start_dt, end_dt, cost_time, record_num,
                            data_status,
                            last_process_bizdt, last_process_status, last_process_result):
    ctl_id = get_id()
    value = (ctl_id, biz_id, data_processor, data_type, data_source, str(start_dt),
             str(end_dt), cost_time, record_num, data_status, str(last_process_bizdt), last_process_status,
             last_process_result, str(datetime.datetime.now()), str(datetime.datetime.now()))
    sql = f'insert into t_data_process_log values {value}'
    db.commit_data(sql)


def insert_exchange_mt_transactions_total(biz_dt, exchange_market, financing_balance, financing_purchase_amount,
                                          lending_securities_volume,
                                          lending_securities_amount, lending_securities_sales_volume,
                                          margin_trading_balance, data_status,
                                          creator_id, updater_id):
    row_id = get_id()
    value = (
        row_id, str(biz_dt), exchange_market, financing_balance, financing_purchase_amount, lending_securities_volume,
        lending_securities_amount, lending_securities_sales_volume, margin_trading_balance, data_status,
        creator_id, str(datetime.datetime.now()), updater_id, str(datetime.datetime.now()))
    sql = f'insert into t_exchange_mt_transactions_total values {value}'
    db.commit_data(sql)


def insert_exchange_mt_transactions_items(data_list):
    data_list_ = []
    for i in range(0, len(data_list)):
        row_id = get_id()
        data_list[i].insert(0, row_id + 1)
        data_list[i].insert(-1, str(datetime.datetime.now()))
        data_list[i].append(str(datetime.datetime.now()))
        data_list_.append(data_list[i])
        time.sleep(0.001)

    sql = "insert into t_exchange_mt_transactions_items(row_id,secu_id,secu_code,secu_name,biz_dt,financing_balance," \
          "financing_purchase_amount,lending_securities_volume,lending_securities_amount,lending_securities_sales_volume" \
          ",margin_trading_balance,data_status,creator_id,create_dt,updater_id,update_dt)" \
          " values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    db.commit_data(sql, data_list_)

# def insert_exchange_mt_transactions_items(secu_id, secu_code, secu_name, biz_dt, financing_balance,
#                                           financing_purchase_amount, lending_securities_volume,
#                                           lending_securities_amount, lending_securities_sales_volume,
#                                           margin_trading_balance, data_status, creator_id, updater_id):
#     row_id = get_id()
#     value = (row_id, secu_id, secu_code, secu_name, str(biz_dt), financing_balance, financing_purchase_amount,
#              lending_securities_volume, lending_securities_amount, lending_securities_sales_volume,
#              margin_trading_balance, data_status, creator_id, str(datetime.datetime.now())
#              , updater_id, str(datetime.datetime.now()))
#     sql = f'insert into t_exchange_mt_transactions_items values {value}'
#     db.commit_data(sql)
