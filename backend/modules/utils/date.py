# ~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~
#      /\_/\
#     ( o.o )
#      > ^ <
#
# Author: Johan Hanekom
# Date: April 2025
#
# ~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~

# =============== // STANDARD IMPORT // ===============

import datetime

# =============== // LIBRARY IMPORT // ===============

import arrow

# =============== // CONSTANTS // ===============

import constants as c


def get_today(format_: str = c.DFORMAT_DATE_FOR_FILE) -> str:
    return arrow.now(c.TZ).format(format_)


def from_timestamp(timestamp: int) -> datetime:
    return arrow.get(timestamp).to(c.TZ).datetime


def humanize(date: datetime) -> str:
    return arrow.get(date).humanize(locale=c.LANGUAGE)  # type: ignore
