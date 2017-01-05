# -*- coding:utf-8 -*-

import time, random
import heapq
from heapq import heappop, heappush, heappushpop
import pandas as pd


INTERVAL = 5

class HeapQueue:
    def __init__(self,capacity=10000):
        self._queue = []
        self._capacity = capacity

    def len(self):
        return len(self._queue)

    def push(self, priority,item):
        if len(self._queue) < self._capacity:
            heappush(self._queue, (priority, item))
        else:
            heappushpop(self._queue, (priority, item))

    def pop(self):
        if len(self._queue) > 0:
            return heappop(self._queue)

    def get_smallest(self, x):
        result = heapq.nsmallest(x, self._queue, key=lambda s: s[0])
        return [item[2] for item in result]

    def get_largest(self, x):
        result = heapq.nlargest(x, self._queue, key=lambda s: s[0])
        return result


class TSFrame(object):
    def __init__(self,capacity=500):
        self._queue = pd.DataFrame()
        self._capacity = capacity

    def push_X(self,line):
        if len(self._queue) < self._capacity:
            LineParser.parse2df_X(line, self._queue)
        else:
            min_index = self._queue.index.min()
            self._queue.drop(min_index, inplace=True)

    def push_Y(self,line):
        LineParser.parse2df_Y(line)

    def pop(self):
        tmp_df = self._queue.dropna(axis=0)
        min_index = tmp_df.min()
        return




class LineParser(object):

    @staticmethod
    def parse_X(line):
        tmp = line.decode().replace("\"","").split(' ')
        record = tmp[1]
        tms = tmp[-1]
        return(record,tms)

    @staticmethod
    def parse_Y(line):
        tmp = line.decode().replace("\"","").split(',')
        record = tmp[:-1]
        tms = tmp[-1]
        return(record,tms)

    @staticmethod
    def parse2df_X(line, df):
        tmp = line.decode().replace("\"", "").split(' ')
        record = tmp[1]
        tms = int(tmp[-1]) - int(tmp[-1]) % INTERVAL
        time_index = pd.to_datetime(int(tms),unit='s')
        df.loc[time_index, 'tms'] = time_index

        record_metrics = record.split(',')
        for metric in record_metrics:
            metric_pair = metric.split('=')
            metric_key = int(metric_pair[0])
            metric_val = float(metric_pair[1])
            df.loc[time_index, metric_key] = metric_val

    @staticmethod
    def parse2df_Y(line, df):
        tmp = line.decode().replace("\"", "").split(',')
        records= tmp[1:]
        tms = int(tmp[0]) - int(tmp[0])%INTERVAL
        print(tms)
        time_index = pd.to_datetime(tms,unit='s')

        df.loc[time_index, 'tms'] = time_index
        record_metrics = records
        for metric in record_metrics:
            metric_pair = metric.split('=')
            metric_key = metric_pair[0]
            metric_val = float(metric_pair[1])
            df.loc[time_index, metric_key] = metric_val


class TSMatrix(object):
    pass




if __name__ == '__main__':

    pq = HeapQueue()
    for i in range(5):
        tms = int(time.time())+random.random()*10
        pq.push(tms, i)
    print(pq.pop())
    print(pq.pop())
    print(pq.get_largest(2))  # this can get the latest msg order by timestamp
    print(pq.pop())

    print('*'*50)

    dff = pd.DataFrame()
    telegraf_str1 = b'ABT 2=20,3=30,1=10 1483570657'
    telegraf_str2 = b'ABT 2=21,3=31,1=11 1483570642'
    telegraf_str3 = b'ABT 2=21,3=31,1=11 1483570682'

    LineParser.parse2df_X(telegraf_str1, dff)
    LineParser.parse2df_X(telegraf_str2, dff)
    LineParser.parse2df_X(telegraf_str3, dff)

    print(dff.head(2))

    nginx_str1 = b'1483570656,latency=101,cost=202'
    nginx_str2 = b'1483570644,latency=111,cost=222'

    LineParser.parse2df_Y(nginx_str1, dff)
    LineParser.parse2df_Y(nginx_str2, dff)
    print(dff.head(5))

    drop_index = dff.index.min()
    latest_index = dff.index.max()

    dff.drop(drop_index,inplace=True)

    print(dff.head(2))

    dfn = dff.dropna(axis=0)
    print('no inplace',dfn.head())
    print(dff.head())

    dff.dropna(axis=0,inplace=True)
    print(dff.ix(latest_index))

    print('*'*50)
    #
    # one = pd.merge(dff,dfn,on = 'tms')
    # print(one.head(1))
