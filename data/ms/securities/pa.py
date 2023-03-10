#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author  : yanpan
# @Time    : 2022/12/21 9:21
# @Site    : 
# @File    : pa.py
# @Software: PyCharm
import pandas as pd
from data.ms.base_tools import get_df_from_cdata, match_sid_by_code_and_name


def _get_format_df(cdata):
    df = get_df_from_cdata(cdata)
    df['sec_code'] = df['证券代码'].apply(lambda x: ('000000'+str(x))[-max(6, len(str(x))):])
    df['sec_name'] = df['证券简称']
    df['sec_name'] = df['sec_name'].str.replace(' ', '')
    _df = match_sid_by_code_and_name(df)
    df = df.merge(_df, on=['sec_code', 'sec_name'])
    df['sec_code'] = df['scd']
    df['start_dt'] = None
    df.sort_values(by=["sec_code", "sec_name"], ascending=[True, True])
    dep_data = df.duplicated(["sec_code", "sec_name"]).sum()
    dep_line = df[df.duplicated(["sec_code", "sec_name"], keep='last')]  # 查看删除重复的行
    dep_list = dep_line.values.tolist()
    df.drop_duplicates(subset=["sec_code", "sec_name"], keep='first', inplace=True, ignore_index=False)
    biz_dt = cdata['biz_dt'].values[0]
    print(biz_dt)
    return biz_dt, df


def _format_dbq(cdata, market):
    biz_dt, df = _get_format_df(cdata)
    df['rate'] = df['折算率'].apply(lambda x: int(x*100))
    dbq = df[['sec_type', 'sec_id', 'sec_code', 'rate']].copy()
    return biz_dt, dbq, pd.DataFrame()


def _format_rz_rq_bdq(cdata, market):
    biz_dt, df = _get_format_df(cdata)
    df['rz_rate'] = df['融资比例'].apply(lambda x: int(x*100))
    df['rq_rate'] = df['融券比例'].apply(lambda x: int(x*100))
    rz = df[['sec_type', 'sec_id', 'sec_code', 'rz_rate']].copy()
    rz.rename(columns={'rz_rate': 'rate'}, inplace=True)
    rq = df[['sec_type', 'sec_id', 'sec_code', 'rq_rate']].copy()
    rq.rename(columns={'rq_rate': 'rate'}, inplace=True)
    rz = rz[rz['rate'] >= 100]
    rq = rq[rq['rate'] >= 50]
    return biz_dt, rz, rq
