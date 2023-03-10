#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author  : yanpan
# @Time    : 2022/8/19 15:01
# @Site    : 
# @File    : dfcf_securities_parsing.py
# @Software: PyCharm
from data.ms.genralhandler import *


def dfcf_parsing_data(rs, data_):
    bzj_data = []
    rz_data = []
    rq_data = []
    rzrq_data = []
    stockgroup_data = []
    if rs[2] == '2':
        logger.info(f'东方财富证券可充抵保证金证券解析开始...')
        for data in data_:
            market = data[3]
            sec_code = data[0]
            sec_name = data[1]
            # rate = round(float(str(data[2]).strip('%')), 3)
            rate = rate_is_normal_two(data[2])
            bzj_data.append([market, sec_code, sec_name, rate])
        securities_bzj_parsing_data(rs, 3, bzj_data)
        logger.info(f'东方财富证券可充抵保证金证券解析结束...')
        time.sleep(5)
        logger.info(f'东方财富证券集中度分组数据解析开始...')
        # 集中度分组数据解析
        for _data in data_:
            market =_data[3]
            sec_code = _data[0]
            sec_name = _data[1]
            stockgroup_name = None
            stock_group = _data[4]
            if stock_group == 'A组':
                stockgroup_name = 1
            elif stock_group == 'B组':
                stockgroup_name = 2
            elif stock_group == 'C组':
                stockgroup_name = 3
            elif stock_group == 'D组':
                stockgroup_name = 4
            elif stock_group == 'E组':
                stockgroup_name = 5
            elif stock_group == 'F组':
                stockgroup_name = 6
            else:
                stockgroup_name = 0
            stockgroup_data.append([market, sec_code, sec_name, stockgroup_name])

        securities_stockgroup_parsing_data(rs, 4, stockgroup_data)
        logger.info(f'东方财富证券集中度分组数据解析结束...')

    elif rs[2] == '3':
        logger.info(f'东方财富证券融资融券标的证券解析开始...')
        for data in data_:
            sec_code = data[0]
            sec_name = data[1]
            # rz_rate = round(float(str(data[2]).strip('%')), 3)
            # rq_rate = round(float(str(data[3]).strip('%')), 3)
            rz_rate = rate_is_normal_two(data[2])
            rq_rate = rate_is_normal_two(data[3])
            rzrq_data.append([sec_code, sec_name, rz_rate, rq_rate])

        temp_data = securities_normal_parsing_data(rzrq_data)
        for temp in temp_data:
            if len(temp) == 6:
                rz_data.append([temp[0], temp[1], temp[2], temp[4], temp[5]])
                rq_data.append([temp[0], temp[1], temp[3], temp[4], temp[5]])
            else:
                logger.error(f'该条记录无证券id{temp},需人工修复!')

        logger.info(f'东方财富证券融资标的证券解析开始...')
        securities_rzrq_parsing_data(rs, 1, rz_data)
        logger.info(f'东方财富证券融资标的证券解析结束...')

        time.sleep(5)
        logger.info(f'东方财富证券融券标的证券解析开始...')
        securities_rzrq_parsing_data(rs, 2, rq_data)
        logger.info(f'东方财富证券融券标的证券解析结束...')

        logger.info(f'东方财富证券融资融券标的证券解析结束...')

