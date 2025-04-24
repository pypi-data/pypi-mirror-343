#!/usr/bin/env python
import datetime

def from_date(date=datetime.datetime.now(), format="%Y-%m-%d"):
    return date.strftime(format)


def to_date(date_string,format="%Y-%m-%d" ):
    return datetime.datetime.strptime(date_string, format)

