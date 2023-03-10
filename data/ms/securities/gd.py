#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author  : yanpan
# @Time    : 2022/12/08 15:38
# @Site    :
# @File    : ax_securities_parsing.py
# @Software: PyCharm

import pandas as pd
from data.ms.base_tools import get_df_from_cdata, code_ref_id


def _get_format_df(cdata, market):
    df = get_df_from_cdata(cdata)
    df['market'] = df['证券市场'].map(lambda x: 'SZ' if str(x) == '深A' else 'SH' if str(x) == '沪A' else 'BJ' if str(x) == '北A' else str(x))
    df['sec_code'] = df['证券代码'].apply(lambda x: ('000000'+str(x))[-max(6, len(str(x))):])
    df['sec_code'] = df['sec_code'] + '.' + df['market']
    df['sec_name'] = df['证券简称']
    df['start_dt'] = None
    dt = str(df['日期'].values[0])
    if '-' in dt:
        biz_dt = dt
    else:
        biz_dt = str(dt)[:4] + '-' + str(dt)[4:6] + '-' + str(dt)[-2:]
    return biz_dt, code_ref_id(df)

def _format_dbq(cdata, market):
    biz_dt, df = _get_format_df(cdata, 'dbq')
    df['rate'] = df['调整后折算率'].apply(lambda x: int(str(x).replace('%', '')))
    dbq = df[['sec_type', 'sec_id', 'sec_code', 'rate']].copy()
    return biz_dt, dbq, pd.DataFrame()


def _format_rz_rq_bdq(cdata, market):
    biz_dt, df = _get_format_df(cdata, market)
    df['rz_rate'] = 100
    df['rq_rate'] = 50
    rz = df.loc[df['融资标的'] == '是'][['sec_type', 'sec_id', 'sec_code', 'rz_rate']].copy()
    rz.rename(columns={'rz_rate': 'rate'}, inplace=True)
    rq = df.loc[df['融券标的'] == '是'][['sec_type', 'sec_id', 'sec_code', 'rq_rate']].copy()
    rq.rename(columns={'rq_rate': 'rate'}, inplace=True)
    return biz_dt, rz, rq


def _format_rz_bdq(cdata, market):
    biz_dt, df = _get_format_df(cdata, market)
    df['rate'] = 100
    rz = df[['sec_type', 'sec_id', 'sec_code', 'rate']].copy()
    return biz_dt, rz


def _format_rq_bdq(cdata, market):
    biz_dt, df = _get_format_df(cdata, market)
    df['rate'] = 50
    rq = df[['sec_type', 'sec_id', 'sec_code', 'rate']].copy()
    return biz_dt, rq
