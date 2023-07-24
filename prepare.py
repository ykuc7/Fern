#!/usr/bin/python
# -*- coding: utf-8 -*-
import pprint
import sys
import re
import json


def skip_excess(file_path):
    with open(file_path, 'r', encoding='shift-jis') as file:
        lines = file.readlines()

    ret = ''
    # 最後に出現する「---」のインデックスを取得
    last_dash_index = len(lines) - 1
    for i, line in enumerate(reversed(lines)):
        if line.startswith('---'):
            last_dash_index = len(lines) - 1 - i
            break

    newline_count = 0
    # スキップする行以外の行を処理
    for line in lines[last_dash_index + 1:]:
        line = line.strip()
        if line:
            newline_count = 0
            # ここからスキップされない行に対する処理
            ret += line + '\n'
        else:
            newline_count += 1
            if newline_count >= 2:
                break

    return ret


def extract_ruby_pairs(text):
    ruby_pattern = r'《(.*?)》'  # ルビを抽出する正規表現パターン
    matches = re.split(ruby_pattern, text)
    kanji_list = extract_kanji(text)

    ruby_dict = {}
    sentences = matches[0::2]
    rubies = matches[1::2]

    for i, sentence in enumerate(sentences):
        kanji = ''
        for char in reversed(sentence):
            if char not in kanji_list:
                break
            kanji = char + kanji
        if kanji:
            ruby_dict[kanji] = rubies[i]

    pprint.pprint(ruby_dict)

    return ruby_dict


def extract_kanji(text):
    kanji_pattern = r'[\u4E00-\u9FFF]+'  # Unicodeで漢字の範囲を指定
    kanji_list = re.findall(kanji_pattern, text)
    return kanji_list


def remove_enclosed_text(text):
    pattern = r'《[^》]+》|\[[^\]]+\]|［[^］]+］'
    result = re.sub(pattern, '', text)
    return result


def insert_line_breaks(text):
    result = ''
    line_length = 0
    i = 0
    while i < len(text):
        char = text[i]
        result += char
        line_length += 1

        if line_length >= 30 and (char in {'.', '。', '、', '」'}):
            if i + 1 < len(text) and text[i + 1] == '」':
                i += 1
                result += text[i + 1]
                result += '\n'
                line_length = 0
            else:
                result += '\n'
                line_length = 0

        i += 1

    return result


def remove_leading_spaces(text):
    lines = text.split('\n')
    cleaned_lines = []

    for line in lines:
        cleaned_line = line.lstrip(' 　')  # 半角スペースと全角スペースを除去
        cleaned_lines.append(cleaned_line)

    result = '\n'.join(cleaned_lines)
    return result


def export_ruby_json(pairs):
    word_sets = []
    for k, v in pairs.items():
        word_sets.append({
            'IsEnabled': True,
            'From': k,
            'To': v,
            'IsRegex': False,
            'IgnoreCase': False,
            'Description': ''
        })

    data = {
        'WordSets': word_sets,
        'PronouncingSets': [],
    }
    dst_path_main = './YukkuriMovieMaker.KanjiToYomi.UserDictionary.json'
    dst_path_bak = './YukkuriMovieMaker.KanjiToYomi.UserDictionary.json.bak'
    with open(dst_path_main, mode="wt", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    with open(dst_path_bak, mode="wt", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def process_text(text):
    pairs = extract_ruby_pairs(text)
    export_ruby_json(pairs)
    cleaned_text = remove_enclosed_text(text)
    cleaned_text = remove_leading_spaces(cleaned_text)
    processed_text = insert_line_breaks(cleaned_text)

    return processed_text


def write_to_file(file_path, text):
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(text)
        print(f"処理結果をファイル '{file_path}' に保存しました。")
    except:
        print(f"エラー: ファイル '{file_path}' への書き込み中に問題が発生しました。")


def main():
    if len(sys.argv) < 2:
        print("引数エラー: ファイルパスを指定してください。")
        return

    file_path = sys.argv[1]
    text = skip_excess(file_path)
    processed_text = process_text(text)

    if processed_text:
        print("処理後の文字列:", processed_text)

        output_file_path = "prepared.txt"
        write_to_file(output_file_path, processed_text)


if __name__ == "__main__":
    main()
