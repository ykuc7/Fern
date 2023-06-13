#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import re

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

def remove_enclosed_text(text):
    pattern = r'《[^》]+》|\[[^\]]+\]|［[^］]+］'
    result = re.sub(pattern, '', text)
    return result

def insert_punctuation(text):
    if len(text) <= 30:
        return text

    for i in range(30, 0, -1):
        if text[i] in {',', '.', '!', '?', '。', '、'}:
            return text[:i+1] + '\n' + insert_punctuation(text[i+1:])

    return text[:30] + '\n' + insert_punctuation(text[30:])

def remove_leading_spaces(text):
    lines = text.split('\n')
    cleaned_lines = []

    for line in lines:
        cleaned_line = line.lstrip(' 　')  # 半角スペースと全角スペースを除去
        cleaned_lines.append(cleaned_line)

    result = '\n'.join(cleaned_lines)
    return result

def process_text(text):
    cleaned_text = remove_enclosed_text(text)
    cleaned_text = remove_leading_spaces(cleaned_text)
    processed_text = insert_punctuation(cleaned_text)

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
