#!/usr/bin/env python
import argparse

from lal_modules import core


def main():
    args = process_args()
    senders = args.senderName
    senders_addr = args.senderAddr
    receivers = args.receiverName
    receivers_addr = args.receiverAddr
    ccs = args.ccName
    cc_addr = args.ccAddr
    text = core.read_main_article(args.article_file)
    if not text:
        return
    output_filename = args.outputFileName

    text_path, letter_path = core.generate_text_and_letter(senders, senders_addr,
                                                           receivers, receivers_addr,
                                                           ccs, cc_addr,
                                                           text)
    core.merge_text_and_letter(text_path, letter_path, output_filename)
    core.clean_temp_files(text_path, letter_path)
    return


def process_args():
    arg_parser = argparse.ArgumentParser(
        description='台灣郵局存證信函產生器', add_help=False)

    arg_parser.add_argument('--help',
                            action='help',
                            help='顯示使用說明')
    arg_parser.add_argument('article_file',
                            action='store',
                            help='存證信函全文之純文字檔路徑')
    arg_parser.add_argument('--senderName',
                            action='append',
                            nargs='+',
                            metavar='寄件人姓名',
                            default=[])
    arg_parser.add_argument('--senderAddr',
                            action='append',
                            metavar='寄件人詳細地址',
                            default=[])
    arg_parser.add_argument('--receiverName',
                            action='append',
                            nargs='+',
                            metavar='收件人姓名',
                            default=[])
    arg_parser.add_argument('--receiverAddr',
                            action='append',
                            metavar='收件人詳細地址',
                            default=[])
    arg_parser.add_argument('--ccName',
                            action='append',
                            nargs='+',
                            metavar='副本收件人姓名',
                            default=[])
    arg_parser.add_argument('--ccAddr',
                            action='append',
                            metavar='副本收件人詳細地址',
                            default=[])
    arg_parser.add_argument('--outputFileName',
                            action='store',
                            metavar='輸出之檔案名稱',
                            default='output.pdf')

    return arg_parser.parse_args()


# Main program goes here
##############################
# Main program goes here
# Main program goes here
if __name__ == '__main__':
    main()
