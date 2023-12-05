#!/usr/bin/python
#-*-coding:utf-8-*-
import logging
logging.basicConfig(format='%(message)s',
                    level=logging.DEBUG)

# gender information
Gender_Man = 0
Gender_Woman = 1

# degree_information
High_School = 0
Bachelor = 1
Master = 2
Phd = 3
# level
BAD = 0
MIDDLE = 1 
GOOD = 2
# black threshold
BLACK_SCORE = 60
# person type
APPLY_PERSON  = 0
INDICATOR_PERSON = 1
CO_LOAN_PERSON = 2
PERSON_TYPE_WEIGHT = [60, 10, 30]

MAX_WX_LOGIN_DAYS = 90

# the ip info file
IP_INFORMATION_DATABASE = "db/ipinfo.csv"

STAT_START_TIME = '2023-10-1 00:00:00'
Register_START_TIME = '2003-10-1 00:00:00'
END_TIME = '2023-12-3 00:00:00'

CITY_GPS_URL_PREFIX = "https://geo.datav.aliyun.com/areas/bound/geojson?code="
CITY_GPS_INFO_CSV = "db/city_gps.csv"
CITY_province = "province"
CITY_CODE = "city_code"
CITY_NAME = "city_name"
CITY_longitude = "longitude"
CITY_latitude = "latitude"
CITY_IS_BLACK = "black"

# product_cd
PRODUCT_ZH = 0
PRODUCT_XJ = 1
PRODUCT_QJ = 2
# bzip type
BZIP_TYPE_list = ["APPLY", "LOAN"]
BZIP_TYPE_weight = [60, 40]

# 区域信息
AREA_INFO = {
    110000: u'北京市',
    120000: u'天津市',
    130000: u'河北省',
    140000: u'山西省',
    150000: u'内蒙古',
    210000: u'辽宁省',
    220000: u'吉林省',
    230000: u'黑龙江省',
    310000: u'上海',
    320000: u'江苏省',
    330000: u'浙江省',
    340000: u'安徽省',
    350000: u'福建省',
    360000: u'江西省',
    370000: u'山东省',
    410000: u'河南省',
    420000: u'湖北省',
    430000: u'湖南省',
    440000: u'广东省',
    450000: u'广西',
    460000: u'海南省',
    500000: u'重庆市',
    510000: u'四川省',
    520000: u'贵州省',
    530000: u'云南省',
    540000: u'西藏',
    610000: u'陕西省',
    620000: u'甘肃省',
    630000: u'青海省',
    640000: u'宁夏',
    650000: u'新疆维吾尔',
}

def log_error(error_msg):
    logging.error("\033[31m%s \033[0m" % error_msg)


def log_info(msg):
    logging.info("\033[32m%s \033[0m" % msg)

def log_debug(msg):
    logging.debug("%s" % msg)