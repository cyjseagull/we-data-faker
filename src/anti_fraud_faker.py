#!/usr/bin/python
# -*-coding:utf-8-*-
import sys
import argparse
import os
from utils import faker
from utils import faker_utils
from utils import common


def parse_cmd():
    parser = argparse.ArgumentParser(description='fake anti fraud table')
    # fake entity
    parser.add_argument('--user_faker', '-u', default=None,
                        help="The user table name")
    parser.add_argument('--user_faker_num', default=None,
                        help="The number of records in the user table")
    parser.add_argument('--joined_user_table_path', default=None,
                        help="The user table used to generate joined users")
    parser.add_argument('--joined_user_num', default=0,
                        help="The joined user num")

    parser.add_argument('--tx_faker', '-t', default=None,
                        help="The tx-apply table name")
    parser.add_argument('--tx_faker_num', default=None,
                        help="The number of records in the tx-apply table")
    parser.add_argument("--user_table", default=None,
                        help="User table name used to generate tx-apply table")

    parser.add_argument('--ip_faker', '-i', default=None,
                        help="The ip-address table name")
    parser.add_argument('--ip_faker_num', default=None,
                        help="The number of records in the ip-address table")

    parser.add_argument("--wx_faker", '-w', default=None,
                        help="The wx table name")
    parser.add_argument("--wx_faker_num", default=None,
                        help="The number of records in the wx table")

    parser.add_argument('--gps_faker', '-g', default=None,
                        help="The gps table name")
    parser.add_argument('--gps_faker_percent', default=None,
                        help="The proportion of faked gps relative to gps in all regions of the country")
    # the afs faker
    parser.add_argument('--afs_faker', '-a', default=None,
                        help="The afs table name")
    parser.add_argument('--product_cd', '-p', default=None,
                        help="The product cd")

    # fake relationship
    parser.add_argument('--user_to_tx', default=False,
                        help="fake user to tx_apply relationship")
    parser.add_argument('--tx_to_gps', default=False,
                        help="fake tx_apply to gps relationship")
    parser.add_argument('--tx_to_ip', default=False,
                        help="fake tx_apply to ip relationship")
    parser.add_argument('--tx_to_wx', default=False,
                        help="fake tx_to wx relationship")

    parser.add_argument('--src', default=None,
                        help="The source of the relationship")
    parser.add_argument('--dst', default=None,
                        help="The dst of the relationship")
    parser.add_argument('--count', default=None,
                        help="The size of the relationship")
    return parser.parse_args()


def fake_user_table(args, faker):
    if args.user_faker is None:
        return
    if args.user_faker_num is None:
        raise RuntimeError("Must specify the record-num of faked user table")
    faker.fake_user_table(args.user_faker, int(
        args.user_faker_num), args.joined_user_table_path, int(args.joined_user_num))


def fake_tx_apply_table(args, faker):
    if args.tx_faker is None:
        return
    if args.tx_faker_num is None:
        raise RuntimeError(
            "Must specify the record-num of faked tx-apply table")
    if args.user_table is None:
        raise RuntimeError(
            "Must specify the user_table used to fake tx-apply table")
    faker.fake_tx_apply(args.tx_faker, int(args.tx_faker_num), args.user_table)


def fake_ip_table(args, faker):
    if args.ip_faker is None:
        return
    if args.ip_faker_num is None:
        raise RuntimeError("Must specify the record-num of faked ip table")
    faker.fake_ip_table(args.ip_faker, int(args.ip_faker_num))


def fake_wx_table(args, faker):
    if args.wx_faker is None:
        return
    if args.wx_faker_num is None:
        raise RuntimeError("Must specify the record num of faked wx-table")
    faker.fake_wx_information(args.wx_faker, int(args.wx_faker_num))


def fake_gps_table(args, faker):
    if args.gps_faker is None:
        return
    if args.gps_faker_percent is None:
        raise RuntimeError(
            "Must specify the proportion of faked gps relative to gps in all regions of the country")
    faker.fake_gps_information(args.gps_faker, int(args.gps_faker_percent))


def __check_param__(args):
    if args.src is None:
        raise RuntimeError(
            "Must specify the source of the relationship table with --src!")
    if args.dst is None:
        raise RuntimeError(
            "Must specify the dst of the relationship table with --dst!")
    if args.count is None:
        raise RuntimeError(
            "Must specify the count of the relationship table with --count!")
    if os.path.exists(args.src) is False:
        raise RuntimeError(
            "the specified source table %s is not exists!" % args.src)
    if os.path.exists(args.dst) is False:
        raise RuntimeError(
            "the specified dst table %s is not exists!" % args.dst)


def fake_user_to_tx_relationship(args, faker):
    if args.user_to_tx is False:
        return
    __check_param__(args)
    faker.fake_user_to_tx_apply_relationship(
        args.src, args.dst, int(args.count))


def fake_tx_to_gps_relationship(args, faker):
    if args.tx_to_gps is False:
        return
    __check_param__(args)
    faker.fake_tx_apply_to_gps_city_relationship(
        args.src, args.dst, int(args.count))


def fake_tx_to_wx_relationship(args, faker):
    if args.tx_to_wx is False:
        return
    __check_param__(args)
    faker.fake_tx_apply_to_wx_relationship(args.src, args.dst, int(args.count))


def fake_tx_to_ip_relationship(args, faker):
    if args.tx_to_ip is False:
        return
    __check_param__(args)
    faker.fake_tx_apply_to_ip_relationship(args.src, args.dst, int(args.count))


def fake_afs_table(args, faker):
    if args.afs_faker is None:
        return
    if args.product_cd is None:
        raise RuntimeError("Must specify the product cd")
    if args.count is None:
        raise RuntimeError("Must specify the fake count")
    faker.fake_afs_table(args.afs_faker, args.product_cd,
                         int(args.count), args.user_table)


if __name__ == '__main__':
    try:
        args = parse_cmd()
        faker_utils_impl = faker_utils.FakerUtils()
        faker = faker.FakerImpl(faker_utils_impl)
        fake_user_table(args, faker)
        fake_tx_apply_table(args, faker)
        fake_ip_table(args, faker)
        fake_wx_table(args, faker)
        fake_gps_table(args, faker)
        fake_user_to_tx_relationship(args, faker)
        fake_tx_to_gps_relationship(args, faker)
        fake_tx_to_wx_relationship(args, faker)
        fake_tx_to_ip_relationship(args, faker)
        fake_afs_table(args, faker)
    except RuntimeError as e:
        common.log_error("error: %s" % str(e))
