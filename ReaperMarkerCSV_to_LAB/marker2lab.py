#!/usr/bin/env python3
# Copyright (c) 2022 oatsu
"""
REAPERから出力したマーカーCSVファイルをLABファイルに変換する。
"""
import utaupy


def convert_marker_csv_to_label(path_marker_csv, path_label):
    """REAPERのマーカー用CSVをラベルファイルに変換する。
    """
    with open(path_marker_csv, 'r', encoding='utf-8') as f:
        lines = f.readlines()[1:]

    _, name, start, _, _ = lines[1].split(',')

    # 時刻データをもとにラベルオブジェクトにする
    label = utaupy.label.Label()
    for line in lines:
        _, name, start, _, _ = line.split(',')
        # 一応形式を確認
        if start.count('.') > 1:
            raise ValueError('時刻は小節番号ではなく小数で表記してください。')
        ph = utaupy.label.Phoneme()
        ph.symbol = name
        ph.start = round(float(start) * 10000000)
        label.append(ph)

    # 発声終了時刻を補完
    label.reload()
    # ENDの行を削除する
    label = label[: -1]
    # ファイル出力
    label.write(path_label)


def main():
    path_marker_csv = input().strip('\"')
    path_label = path_marker_csv.replace('.csv', '.lab')
    convert_marker_csv_to_label(path_marker_csv, path_label)


if __name__ == "__main__":
    main()
