#!/usr/bin/python
#-*-coding:utf-8-*-
import random
from utils.common import AREA_INFO
from utils import common
import requests
import json
import datetime
import pandas as pd
import s2cell
import math
import ipaddress
import os
import re
import numpy
import uuid

class IpInformation:
    """
    the ip information
    """
    def __init__(self, ip):
        self.__ip = ip
    
    @property
    def ip(self):
        return self.__ip
    
    @ip.setter
    def ip(self, ip):
        self.__ip = ip
    
    @property
    def province(self):
        return self.__province
    
    @province.setter
    def province(self, province):
        self.__province = province
    
    @property
    def city(self):
        return self.__city

    @city.setter
    def city(self, city):
        self.__city = city
    
    @property
    def city_code(self):
        return self.__city_code

    @city_code.setter
    def city_code(self, city_code):
        self.__city_code = city_code
    
    @property
    def operator(self):
        return self.__operator

    @operator.setter
    def operator(self, operator):
        self.__operator = operator

class FakerUtils:
    """
    the faker
    """
    def __init__(self):
        self.__generate_gps_city_csv__()
        # load the city gps information
        self.gps_df = pd.read_csv(common.CITY_GPS_INFO_CSV, sep = ',', usecols=[common.CITY_province, common.CITY_CODE, common.CITY_NAME, common.CITY_longitude, common.CITY_latitude, common.CITY_IS_BLACK], index_col = False)
        # city_code to city_name
        self.city_code_to_name = {}
        self.city_name_to_code = {}
        for row in self.gps_df.itertuples():
            city_code = row[2]
            city_name = row[1] + row[3]
            if city_code == "city_code":
                continue
            self.city_code_to_name[city_code] = city_name
            self.city_name_to_code[city_name] = city_code
        # load the ip information
        self.ip_df = pd.read_csv(common.IP_INFORMATION_DATABASE, sep = ',', usecols=['ip', 'province', 'operator'], index_col = False)
        self.ip_seg_list = self.ip_df.iloc[:, 0].values
        self.city_list = self.ip_df.iloc[:, 1].values
        self.operator = self.ip_df.iloc[:, 2].values

    # generate phone number
    def generate_phone_number(self):
        # 随机生成电话号码的前缀
        prefix = random.choice(['130', '131', '132', '133', '134', '135', '136', '137', '138', '139',
                            '150', '151', '152', '153', '155', '156', '157', '158', '159',
                            '180', '181', '182', '183', '184', '185', '186', '187', '188', '189'])
        # 随机生成电话号的后缀
        suffix = ''.join(random.choice(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']) for _ in range(8))
        # 将前缀和后缀组合起来，生成电话号
        return prefix + suffix
    
    # generate ipv4
    def generate_random_ipv4(self):
        """从列表seeds中随机生成一个ipv4地址并返回，要求如下：
        1. seeds列表中的值可以为ip地址、ip区间(A.B.C.D-A.B.C.D)、ip+掩码格式(A.B.C.D/M)。
        2. 生成的随机ip地址必须满足seeds中表示的ip范围内选择。
        """
        selected_record = random.randint(0, len(self.ip_seg_list) - 1)
        selected_ip = self.ip_seg_list[selected_record]
        # ip
        ipinfo = IpInformation(selected_ip)
        # city
        ipinfo.city = self.city_list[selected_record]
        # operator
        ipinfo.operator = self.operator[selected_record]
        # province
        ipinfo.province = ipinfo.city
        for code in common.AREA_INFO.keys():
            recorded_province = common.AREA_INFO.get(code)
            if ipinfo.city.startswith(recorded_province):
                ipinfo.city_code = code
        if "-" in selected_ip:
            # IP区间  A.B.C.D-A.B.C.D
            ip_start, ip_end = selected_ip.split("-")
            # ip区间最小值
            ip_min = int(ipaddress.ip_address(ip_start))
            # ip区间最大值
            ip_max = int(ipaddress.ip_address(ip_end))
            ipinfo.ip = str(ipaddress.ip_address(random.randint(ip_min, ip_max)))
        elif "/" in selected_ip:
            # IP掩码 A.B.C.D/M
            ipinfo.ip = str(random.choice(list(ipaddress.ip_network(selected_ip))))
        return ipinfo

    def __get_check_digit__(self, id_number):
        """通过身份证号获取校验码"""
        check_sum = 0
        for i in range(0, 17):
            check_sum += ((1 << (17 - i)) % 11) * int(id_number[i])
        check_digit = (12 - (check_sum % 11)) % 11
        return check_digit if check_digit < 10 else 'X'
    
    # generate id
    def generate_id(self, sex=0):
        """
        随机生成身份证号，sex = 0表示女性，sex = 1表示男性
        """
        # 随机生成一个区域码(6位数)
        id_number = str(random.choice(list(self.city_code_to_name.keys())))
        address = self.city_code_to_name.get(id_number)
        # 限定出生日期范围(8位数)
        start, end = "1960-01-01", "2000-12-30"
        days = (datetime.datetime.strptime(end, "%Y-%m-%d") - datetime.datetime.strptime(start, "%Y-%m-%d")).days + 1
        birth_days = datetime.datetime.strftime(
            datetime.datetime.strptime(start, "%Y-%m-%d") + datetime.timedelta(random.randint(0, days)), "%Y%m%d"
        )
        id_number += str(birth_days)
        # 顺序码(2位数)
        id_number += str(random.randint(10, 99))
        # 性别码(1位数)
        id_number += str(random.randrange(sex, 10, step=2))
        # 校验码(1位数)
        return (id_number + str(self.__get_check_digit__(id_number)), address, birth_days)

    def generate_randomtimes(self, start, end, frmt="%Y-%m-%d %H:%M:%S"):
        stime = datetime.datetime.strptime(start, frmt)
        etime = datetime.datetime.strptime(end, frmt)
        time = random.random() * (etime - stime) + stime
        return time.strftime(frmt)

    def generate_random_gps(self, base_log=None, base_lat=None, radius=None):
        radius_in_degrees = radius / 111300
        u = float(random.uniform(0.0, 1.0))
        v = float(random.uniform(0.0, 1.0))
        w = radius_in_degrees * math.sqrt(u)
        t = 2 * math.pi * v
        x = w * math.cos(t)
        y = w * math.sin(t)
        longitude = y + base_log
        latitude = x + base_lat
        # 这里是想保留14位小数
        loga = '%.14f' % longitude
        lata = '%.14f' % latitude
        return loga, lata

    def __generate_score_information__(self, weight):
        level = random.choices(population = [common.BAD, common.MIDDLE, common.GOOD], weights = weight)[0]
        score = 0
        if level == common.BAD:
            score = random.randint(10, 60)
        if level == common.MIDDLE:
            score = random.randint(60, 80)
        else:
            score = random.randint(80, 100)
        black = False
        if score < common.BLACK_SCORE:
            black = True
        return (score, level, black)

    def generate_person_score_information(self, degree): 
        """
        generate (score, level, black) according to degree
        """
        # bad: 35%, middle: 60%, good: 5%
        if degree == common.High_School:
            (score, level, black) = self.__generate_score_information__([35, 60, 5])
        # bad: 15%, middle: 70%, good: 15%
        if degree == common.Bachelor:
            (score, level, black) = self.__generate_score_information__([15, 70, 15])
        # bad: 5%, middle: 60%, good: 35%
        if degree == common.Master:
            (score, level, black) = self.__generate_score_information__([5, 60, 35])
        # bad: 0%, middle: 50%, good: 50%
        if degree == common.Phd:
            (score, level, black) = self.__generate_score_information__([0, 50, 50])
        return (score, level, black)

    def generate_wx_information(self):
        """
        generate the wx information
        """
        # union_id
        union_id = uuid.uuid1()
        # level
        level = random.choices(population = [common.BAD, common.MIDDLE, common.GOOD], weights = [5, 60, 35])[0]
        # register time
        time = self.generate_randomtimes(common.Register_START_TIME, common.END_TIME)
        # login days
        login_days = random.randint(0, common.MAX_WX_LOGIN_DAYS)
        # black
        black = False
        if level == common.BAD:
            black = True
        return (union_id, level, time, login_days, black)

    def __get_data__(self, city_data, province_code): 
        df = []
        for city in city_data:
            province_name = common.AREA_INFO.get(province_code)
            city_code = city['properties']['adcode']
            city_name = city['properties']['name']
            lon,lat = city['properties']['center']
            is_black = random.choices(population = [True, False], weights = [1, 99])[0]
            df.append([province_name, city_code,city_name,lon,lat, is_black])
        df = pd.DataFrame(df,columns=[common.CITY_province, common.CITY_CODE, common.CITY_NAME, common.CITY_longitude, common.CITY_latitude, common.CITY_IS_BLACK])
        return df

    def __get_gps_feature_list__(self, url):
        response = requests.get(url)
        common.log_info("* url: %s, status code: %d" % (url, response.status_code))
        if response.status_code == 200:
            data = json.loads(response.text)
            return (True, data['features'])
        return (False, None)
        
    def __generate_gps_city_csv__(self):
        if os.path.exists(common.CITY_GPS_INFO_CSV):
            return
        for code in common.AREA_INFO.keys():
            url = "%s%s_full" % (common.CITY_GPS_URL_PREFIX, code)
            (ret, data) = self.__get_gps_feature_list__(url)
            if ret is False:
                common.log_error("* generate gps information for (%s, %s) failed" % (code, common.AREA_INFO.get(code)))
                continue
            county = pd.DataFrame()
            pattern = '\d+'
            for city in data:
                city_code = city['properties']['adcode']
                url = re.sub(pattern,str(city_code),url)
                (ret, feature_data) = self.__get_gps_feature_list__(url)
                if ret is False:
                    common.log_error("* generate gps information for (%s, %s) failed" % (city_code, city['properties']['name']))
                    continue
                county_data = self.__get_data__(feature_data, code)
                county = pd.concat([county,county_data])
                common.log_info("* generate gps information for (%s, %s) success" % (city_code, city['properties']['name']))
            county.to_csv(common.CITY_GPS_INFO_CSV,encoding='utf-8', mode = 'a', index=False) 

    # generate gps information
    def generate_gps_information(self, fp, weight_list):
        """
        cell_id, city, province, city_code, if_black
        """
        for row in self.gps_df.itertuples():
            select = random.choices([True, False], weight_list)[0]
            if select is False:
                continue
            longitude = row[4]
            if longitude == 'longitude':
                continue
            latitude = row[5]
            cell_id = s2cell.lat_lon_to_cell_id(float(longitude), float(latitude))
            # object_key
            fp.write(str(cell_id) + ",")
            # cell_id
            fp.write(str(cell_id) + ",")
            # city
            city = row[3]
            fp.write(city + ",")
            # province
            province = row[1]
            fp.write(province + ",")
            # city_code
            city_code = row[2]
            fp.write(city_code + ",")
            # if_black
            is_black = row[6]
            fp.write(is_black + "\n")
