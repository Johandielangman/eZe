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

from datetime import datetime

# =============== // LIBRARY IMPORT // ===============

import arrow

# =============== // MODULE IMPORT // ===============

import modules.utils as utils
import constants as c


def test_get_today_default_format():
    today = utils.get_today()
    expected_format = arrow.now(c.TZ).format(c.DFORMAT_DATE_FOR_FILE)
    assert today == expected_format


def test_get_today_custom_format():
    custom_format = "YYYY-MM-DD"
    today = utils.get_today(format_=custom_format)
    expected_format = arrow.now(c.TZ).format(custom_format)
    assert today == expected_format


def test_from_timestamp():
    timestamp = 1672531200  # Example timestamp (Jan 1, 2023)
    result = utils.from_timestamp(timestamp)
    expected_datetime = arrow.get(timestamp).to(c.TZ).datetime
    assert result == expected_datetime


def test_humanize():
    date = datetime(2023, 1, 1)
    result = utils.humanize(date)
    expected_humanized = arrow.get(date).humanize(locale=c.LANGUAGE)
    assert result == expected_humanized
