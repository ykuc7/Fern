#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import csv


def create_csv_file(text_file_path):
    output_csv_path = 'output.csv'  # 出力CSVファイルのパス
    column_a_text = 'ずんだもん'  # A列に入れる任意の文字列

    with open(text_file_path, 'r', encoding='utf-8') as text_file:
        lines = text_file.readlines()

    with open(output_csv_path, 'w', encoding='utf-8', newline='') as csv_file:
        writer = csv.writer(csv_file)
        for line in lines:
            line = line.strip()
            writer.writerow([column_a_text, line])


def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py input_file.txt")
        return

    text_file_path = sys.argv[1]  # 入力テキストファイルのパス

    create_csv_file(text_file_path)


if __name__ == '__main__':
    main()
