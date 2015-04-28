__author__ = 'omriariav'
from LiveRailClass import *


if __name__ == "__main__":
    worker = LiveRailClass()
    worker.login("USERNAME","PASSWORD")
    worker.setEntity(worker._entity)
    res = worker.revenueReport({
        "start": '2011-03-01 00:00',
        "end": '2011-03-01 01:00',
        "dimensions": "order_id",
        "metrics": "revenue"
    })

    pprint(res)
