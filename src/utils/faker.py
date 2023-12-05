#!/usr/bin/python
# -*-coding:utf-8-*-
from utils import common
import random
import pandas as pd
import uuid
import os
from datetime import datetime
from faker import Faker
import chardet


class FakerImpl:
    """
    the faker
    """

    def __init__(self, faker_utils):
        self.faker_utils = faker_utils
        self.name_faker = Faker("zh_CN")

    def fake_user_table(self, user_table_name, fake_count, joined_user_table_name, joined_num):
        """
        generate the user information, include:
        object_key: ecif_no
        ecif_no
        age
        gender
        degree
        addess
        score
        level
        black
        """
        fp = open(user_table_name, "w+")
        common.log_info("* fake_user_table: %s, fake_count: %d" %
                        (user_table_name, fake_count))
        # write the schema
        schema = "object_key,ecif_no,name,birthday,age,gender,degree,address,score,level,black"
        fp.write(schema.replace(' ', '') + "\n")
        id_set = []
        # read the joined_user_table
        joined_user_list = []
        joined_user_address_list = []
        if joined_user_table_name is not None and joined_num != 0:
            joined_user_df = pd.read_csv(joined_user_table_name, usecols=[
                                         "object_key", "name", "birthday", "age", "gender", "address"], index_col=False)
            joined_user_list = joined_user_df.iloc[:, 0].values
            joined_user_name_list = joined_user_df.iloc[:, 1].values
            joined_user_birthday_list = joined_user_df.iloc[:, 2].values
            joined_user_age_list = joined_user_df.iloc[:, 3].values
            joined_user_gender_list = joined_user_df.iloc[:, 4].values
            joined_user_address_list = joined_user_df.iloc[:, 5].values
        print("#### joined_user_list: %s" % str(joined_user_list))
        print("#### joined_user_name_list: %s" % str(joined_user_name_list))
        print("#### joined_user_birthday_list: %s" %
              str(joined_user_birthday_list))
        print("### joined_user_age_list: %s" % str(joined_user_age_list))
        print("### joined_user_gender_list: %s" % str(joined_user_gender_list))
        print("### joined_user_address_list: %s" %
              str(joined_user_address_list))
        for i in range(0, fake_count):
            if i < joined_num:
                selected_record = random.randint(0, len(joined_user_list) - 1)
                id_no = joined_user_list[selected_record]
                address = joined_user_address_list[selected_record]
                name = joined_user_name_list[selected_record]
                birthday = joined_user_birthday_list[selected_record]
                age = joined_user_age_list[selected_record]
                gender = joined_user_gender_list[selected_record]
            else:
                (id_no, address, birthday) = self.faker_utils.generate_id()
                age = str(random.randint(18, 70))
                name = self.name_faker.name()
                gender = str(random.randint(0, 1))
            if id_no in id_set:
                continue
            id_set.append(id_no)
            # object_key
            fp.write(id_no + ",")
            # ecif_no
            fp.write(id_no + ",")
            # name
            fp.write(name + ",")
            # birthday
            fp.write(str(birthday) + ",")
            # age
            fp.write(str(age) + ",")
            # gender
            fp.write(str(gender) + ",")
            # degree
            degree = random.choices(
                [common.High_School, common.Bachelor, common.Master, common.Phd], [10, 50, 30, 10])[0]
            fp.write(str(degree) + ",")
            # address
            fp.write(address + ",")
            # score
            (score, level, black) = self.faker_utils.generate_person_score_information(degree)
            fp.write(str(score) + ",")
            # level
            fp.write(str(level) + ",")
            # black
            fp.write(str(black) + "\n")
        fp.close()
        common.log_info("fake user_table: %s success" % user_table_name)

    def fake_tx_apply(self, tx_apply_table_name, fake_count, user_table_name):
        """
        generate the tx_apply information, include:
        object_key: app_no
        app_no
        person_type
        afs_biz_no
        ecif_no
        time
        score
        """
        df = pd.read_csv(user_table_name, encoding='ISO-8859-1',
                         usecols=['ecif_no', 'score'], sep=',', index_col=False)
        user_set = df.iloc[:, 0].values
        score_set = df.iloc[:, 1].values
        fp = open(tx_apply_table_name, "w+")
        # write schema
        schema = "object_key,app_no,person_type,afs_biz_no,ecif_no,time,score"
        fp.write(schema.replace(' ', '') + "\n")
        common.log_info("* fake_tx_apply: %s, fake count: %d" %
                        (tx_apply_table_name, fake_count))
        tx_apply_set = []
        print_count = int(0.1 * float(fake_count))
        for i in range(0, fake_count):
            # object_key
            object_key = str(uuid.uuid1())
            if object_key in tx_apply_set:
                continue
            tx_apply_set.append(object_key)
            fp.write(object_key + ",")
            # app_no
            fp.write(object_key + ",")
            # person_type
            person_type = random.choices(population=[
                                         common.APPLY_PERSON, common.INDICATOR_PERSON, common.CO_LOAN_PERSON], weights=common.PERSON_TYPE_WEIGHT)[0]
            fp.write(str(person_type) + ",")
            # afs_biz_no
            afs_biz_no = str(uuid.uuid1())
            fp.write(afs_biz_no + ",")
            # ecif_no(use id as ecif_no)
            ecif_no = random.choice(user_set)
            fp.write(ecif_no + ",")
            # time
            fp.write(self.faker_utils.generate_randomtimes(
                common.STAT_START_TIME, common.END_TIME) + ",")
            # score
            score = random.choice(score_set)
            fp.write(str(score) + "\n")
            if i % print_count == 0:
                common.log_info("* %s records generated" % i)
        fp.close()
        common.log_info("fake tx_apply table: %s success" %
                        tx_apply_table_name)

    def fake_ip_table(self, ip_table_name, fake_count):
        """
        fake the ip table, include:
        object_key: ip
        ip
        city
        province
        city_code
        operator
        """
        fp = open(ip_table_name, "w+")
        # write schema
        schema = "object_key, ip, city, province, city_code, operator"
        fp.write(schema.replace(' ', '') + "\n")

        common.log_info("fake ip table: %s, fake count: %d" %
                        (ip_table_name, fake_count))
        ip_set = []
        i = 0
        print_count = int(0.1 * float(fake_count))
        while i < fake_count:
            ip_info = self.faker_utils.generate_random_ipv4()
            if ip_info.ip in ip_set:
                continue
            ip_set.append(ip_info.ip)
            # object_key
            fp.write(ip_info.ip + ",")
            # ip
            fp.write(ip_info.ip + ",")
            # city
            fp.write(ip_info.city + ",")
            # province
            fp.write(ip_info.province + ",")
            # city_code
            if hasattr(ip_info, 'city_code'):
                fp.write(str(ip_info.city_code) + ",")
            else:
                common.log_debug("### not found city code: %s" % ip_info.city)
                fp.write('None ,')
            # operator
            fp.write(ip_info.operator + "\n")
            i += 1
            if i % print_count == 0:
                common.log_info("* %s records generated" % i)
        fp.close()
        common.log_info("fake ip table: %s success" % ip_table_name)

    def fake_wx_information(self, wx_table_name, fake_count):
        """
        object_key, union_id, level, time, login_days, black
        """
        fp = open(wx_table_name, "w+")
        schema = "object_key, union_id, level, time, login_days, black"
        fp.write(schema.replace(' ', '') + "\n")
        common.log_info("fake wx table: %s, fake count: %d" %
                        (wx_table_name, fake_count))
        wx_union_set = []
        print_count = int(0.1 * float(fake_count))
        for i in range(0, fake_count):
            (union_id, level, time, login_days,
             black) = self.faker_utils.generate_wx_information()
            if union_id in wx_union_set:
                continue
            wx_union_set.append(union_id)
            # object_key
            fp.write(str(union_id) + ",")
            # union_id
            fp.write(str(union_id) + ",")
            # level
            fp.write(str(level) + ",")
            # time
            fp.write(time + ",")
            # login_days
            fp.write(str(login_days) + ",")
            # black
            fp.write(str(black) + "\n")
            if i % print_count == 0:
                common.log_info("* %s records generated" % i)
        fp.close()
        common.log_info("fake wx table: %s success" % wx_table_name)

    def fake_gps_information(self, gps_table_name, generated_percent):
        """
        object_key, cell_id, city, province, city_code, if_black
        """
        fp = open(gps_table_name, "w+")
        schema = "object_key, cell_id, city, province, city_code, if_black"
        fp.write(schema.replace(' ', '') + "\n")
        common.log_info("fake gps table: %s, percent: %d" %
                        (gps_table_name, generated_percent))
        self.faker_utils.generate_gps_information(
            fp, [generated_percent, 100 - generated_percent])
        fp.close()
        common.log_info("fake gps table: %s success" % (gps_table_name))

    def __generate_relationship_table_name__(self, src, dst):
        _, src_name = os.path.split(src)
        _, dst_name = os.path.split(dst)
        return "%s_to_%s_relation.csv" % (src_name.split('.')[0], dst_name.split('.')[0])

    def fake_user_to_tx_apply_relationship(self, user_table, tx_apply_table, fake_count):
        """
        user->tx_apply
        """
        # Note: the object_key of user_table is also ecif_no
        user_df = pd.read_csv(user_table, sep=',', usecols=[
                              'ecif_no'], index_col=False)
        tx_apply_table_df = pd.read_csv(tx_apply_table, sep=',', usecols=[
                                        'object_key', 'ecif_no', 'time'], index_col=False)
        schema = "object_key,from_key,to_key,app_time"
        user_ecif_no_list = user_df.iloc[:, 0].values
        tx_apply_object_key_list = tx_apply_table_df.iloc[:, 0].values
        tx_apply_ecif_no_list = tx_apply_table_df.iloc[:, 1].values
        tx_apply_time_list = tx_apply_table_df.iloc[:, 2].values
        i = 0
        size = len(user_ecif_no_list) - 1
        relationship_table_name = self.__generate_relationship_table_name__(
            user_table, tx_apply_table)
        fp = open(relationship_table_name, "w+")
        fp.write(schema + "\n")
        print_count = int(0.1 * float(fake_count))
        while i < fake_count:
            selected_record = random.randint(0, size)
            selected_ecif = user_ecif_no_list[selected_record]
            # object_key
            fp.write(str(uuid.uuid1()) + ",")
            # from_key
            fp.write(selected_ecif + ",")
            # to_key
            selected_record = random.randint(
                0, len(tx_apply_object_key_list) - 1)
            fp.write(tx_apply_object_key_list[selected_record] + ",")
            # app_time
            fp.write(str(tx_apply_time_list[selected_record]) + "\n")
            i += 1
            if i % print_count == 0:
                common.log_info("* %s records generated" % i)
        fp.close()

    def __fake_relationship__(self, fp, from_key_df, to_key_df, fake_count):
        from_key_object_key_list = from_key_df.iloc[:, 0].values
        from_key_time_list = from_key_df.iloc[:, 1].values
        to_key_object_key_list = to_key_df.iloc[:, 0].values
        from_key_list = []
        print_count = int(0.1 * float(fake_count))
        i = 0
        while i < fake_count:
            selected_record = random.randint(
                0, len(from_key_object_key_list) - 1)
            from_key = from_key_object_key_list[selected_record]
            # object_key
            fp.write(str(uuid.uuid1()) + ",")
            # from_key
            fp.write(from_key + ",")
            # to_key
            selected_to_key_record = random.randint(
                0, len(to_key_object_key_list) - 1)
            fp.write(str(to_key_object_key_list[selected_to_key_record]) + ",")
            # app_time
            fp.write(str(from_key_time_list[selected_record]) + "\n")
            i += 1
            if i % print_count == 0:
                common.log_info("* %s records generated" % i)

    def fake_tx_apply_to_gps_city_relationship(self, tx_apply_table, gps_table, fake_count):
        """
        tx_apply->gps
        """
        tx_apply_df = pd.read_csv(tx_apply_table, sep=',', usecols=[
                                  'object_key', 'time'], index_col=False)
        gps_df = pd.read_csv(gps_table, sep=',', usecols=[
                             'object_key'], index_col=False)
        schema = "object_key, from_key, to_key, app_time"
        relationship_table_name = self.__generate_relationship_table_name__(
            tx_apply_table, gps_table)
        fp = open(relationship_table_name, "w+")
        fp.write(schema.replace(' ', '') + '\n')
        self.__fake_relationship__(fp, tx_apply_df, gps_df, fake_count)
        fp.close()

    def fake_tx_apply_to_wx_relationship(self, tx_apply_table, wx_table, fake_count):
        """
        tx_apply->wx
        """
        tx_apply_df = pd.read_csv(tx_apply_table, sep=',', usecols=[
                                  'object_key', 'time'], index_col=False)
        wx_df = pd.read_csv(wx_table, sep=',', usecols=[
                            'object_key'], index_col=False)
        relationship_table_name = self.__generate_relationship_table_name__(
            tx_apply_table, wx_table)
        fp = open(relationship_table_name, "w+")
        schema = "object_key, from_key, to_key, app_time"
        fp.write(schema.replace(' ', '') + '\n')
        self.__fake_relationship__(fp, tx_apply_df, wx_df, fake_count)
        fp.close()

    def fake_tx_apply_to_ip_relationship(self, tx_apply_table, ip_table, fake_count):
        """
        tx_apply->ip
        """
        tx_apply_df = pd.read_csv(tx_apply_table, sep=',', usecols=[
                                  'object_key', 'time'], index_col=False)
        ip_table_df = pd.read_csv(ip_table, sep=',', usecols=[
                                  'object_key'], index_col=False)
        relationship_table_name = self.__generate_relationship_table_name__(
            tx_apply_table, ip_table)
        fp = open(relationship_table_name, "w+")
        schema = "object_key, from_key, to_key, app_time"
        fp.write(schema.replace(' ', '') + '\n')
        self.__fake_relationship__(fp, tx_apply_df, ip_table_df, fake_count)
        fp.close()

    def fake_afs_table(self, afs_table_name, product_cd, fake_count, user_table_name):
        """
        generate the tx_apply information, include:
        afs_biz_no
        product_cd
        person_type
        application_name
        ecif_no
        id_no
        phone_no
        biz_type: apply, loan
        app_id
        open_id
        union_id
        card_no
        bank_home_no
        email
        birth_date
        gender
        trans_amt
        pbc_work_address
        pbc_home_address
        work_address
        household_address
        trans_home_address
        source_flag
        created_datetime
        last_modified_datetime
        """
        user_num = 0
        if user_table_name is not None:
            user_df = pd.read_csv(user_table_name, usecols=[
                                  "object_key", "name", "birthday", "age", "gender", "address"], index_col=False)
            user_list = user_df.iloc[:, 0].values
            user_name_list = user_df.iloc[:, 1].values
            user_birthday_list = user_df.iloc[:, 2].values
            user_age_list = user_df.iloc[:, 3].values
            user_gender_list = user_df.iloc[:, 4].values
            user_address_list = user_df.iloc[:, 5].values
            user_num = len(user_list)
        schema = "afs_biz_no, product_cd, person_type, application_name, ecif_no, id_no, phone_no, \
                biz_type, app_id, open_id, union_id, card_no, bank_home_no, email, birth_date, gender, trans_amt, pbc_work_address,\
                pbc_home_address, work_address, household_address, trans_home_address, source_flag, created_datetime, last_modified_datetime"
        fp = open(afs_table_name, "w+")
        fp.write(schema.replace(' ', '') + "\n")
        random_range = min(2*fake_count, user_num - 1)
        for i in range(0, fake_count):
            # select from the user
            if user_num > 0:
                random.seed(datetime.now())
                selected_index = random.randint(0, random_range)
                id_no = str(user_list[selected_index])
                address = str(user_address_list[selected_index])
                application_name = str(user_name_list[selected_index])
                birthday = user_birthday_list[selected_index]
                age = user_age_list[selected_index]
                gender = user_gender_list[selected_index]
            else:
                # ecif_no, id_no
                (id_no, address, birthday) = self.faker_utils.generate_id()
                application_name = self.name_faker.name()
            ecif_no = id_no
            # afs_biz_no
            afs_biz_no = str(uuid.uuid1())
            fp.write(afs_biz_no + ",")
            # product_cd
            fp.write(product_cd + ",")
            # person_type
            person_type = random.choices(population=[
                                         common.APPLY_PERSON, common.INDICATOR_PERSON, common.CO_LOAN_PERSON], weights=common.PERSON_TYPE_WEIGHT)[0]
            fp.write(str(person_type) + ",")
            # application_name
            fp.write(application_name + ",")
            # ecif_no
            fp.write(ecif_no + ",")
            # id_no
            fp.write(id_no + ",")
            # phone_no
            phone_no = self.faker_utils.generate_phone_number()
            fp.write(phone_no + ",")
            # biz_type
            biz_type = random.choices(
                population=common.BZIP_TYPE_list, weights=common.BZIP_TYPE_weight)[0]
            fp.write(biz_type + ",")
            # app_id
            fp.write(afs_biz_no + ",")
            # open_id, union_id
            (union_id, level, time, login_days,
             black) = self.faker_utils.generate_wx_information()
            fp.write(str(union_id) + ",")
            fp.write(str(union_id) + ",")
            # card_no
            fp.write(id_no + ",")
            # bank_home_no
            fp.write(id_no + ",")
            # email
            email = application_name + "@163.com"
            fp.write(email + ",")
            # birthday
            fp.write(str(birthday) + ",")
            # gender
            gender = random.choices(
                population=[common.Gender_Man, common.Gender_Woman], weights=[60, 40])[0]
            fp.write(str(gender) + ",")
            # trans_amt
            trans_amt = random.randint(10000, 5000000)
            fp.write(str(trans_amt) + ",")
            #  pbc_home_address
            fp.write(address + ",")
            # work_address
            fp.write(address + ",")
            # household_address
            fp.write(address + ",")
            # trans_home_address
            fp.write(address + ",")
            # source_flag
            fp.write(str(0) + ",")
            # created_datetime
            created_datetime = self.faker_utils.generate_randomtimes(
                common.STAT_START_TIME, common.END_TIME)
            fp.write(created_datetime + ",")
            # last_modified_datetime
            fp.write(created_datetime + "\n")
        fp.close()
