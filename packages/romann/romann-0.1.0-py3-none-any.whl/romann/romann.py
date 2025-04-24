"""
romann.py - Japanese to natural romaji/English conversion library.
"""

import os
import re
import json
import jaconv
from pykakasi import kakasi
from sudachipy import tokenizer, dictionary

class RomanConverter:
    """
    RomanConverter class for converting Japanese text to natural romaji/English.
    Uses SudachiPy for morphological analysis and customizable dictionaries.
    """
    # ヘボン式ローマ字の外来語英語の辞書
    hira_dict_path = os.path.join(os.path.dirname(__file__), "hiragana_english.json")
    with open(hira_dict_path, encoding="utf-8") as f:
        HIRAGANA_ENGLISH = json.load(f)

    def __init__(self):
        """
        Initialize the RomanConverter with kakasi and SudachiPy.
        """
        self.converter = kakasi()
        # SudachiPyの初期化
        self.tokenizer_obj = dictionary.Dictionary().create()
        self.mode = tokenizer.Tokenizer.SplitMode.C  # 最も細かい分割モード

    def convert_hiragana_english(self, word: str) -> str:
        """
        Convert romanized hiragana to English if it exists in the dictionary.
        """
        return self.HIRAGANA_ENGLISH.get(word.lower(), word).capitalize()

    def to_roman(self, text: str) -> str:
        """
        Convert Japanese text (kanji, hiragana, katakana) to romaji.
        Preserves non-Japanese characters as they are.
        Uses SudachiPy for morphological analysis to better handle loan words.

        Args:
            text (str): Input text containing Japanese characters

        Returns:
            str: Romanized text with natural capitalization and formatting
        """
        if not text:
            return ""

        # 中点（・）を空白に置換して処理
        text_processed = text.replace("・", " ")

        # 形態素解析で単語に分割
        tokens = self.tokenizer_obj.tokenize(text_processed, self.mode)

        result = []
        for token in tokens:
            # 表層形を取得
            surface = token.surface()

            # 英数字のみの場合はそのまま追加
            if re.match(r'^[a-zA-Z0-9]+$', surface):
                result.append(surface)
                continue

            # 読みを取得
            reading = token.reading_form()
            # 読みをひらがなに変換
            hiragana = jaconv.kata2hira(reading)

            # 外来語辞書に存在するか確認
            if hiragana in self.HIRAGANA_ENGLISH:
                # 辞書に存在する場合は英語表記を使用
                result.append(self.HIRAGANA_ENGLISH[hiragana])
            else:
                # 助詞「の」の特別処理
                if surface == "の" or hiragana == "の":
                    result.append("no")
                # 空白の場合はスキップ
                elif surface.strip() == "":
                    continue
                # 辞書に存在しない場合はkakasiでローマ字化
                else:
                    romaji = self.converter.convert(surface)
                    # collect hepburn
                    romaji_parts = [item['hepburn'] for item in romaji]
                    # Join without spaces for single token
                    romaji_text = ''.join(romaji_parts)
                    result.append(romaji_text)

        # 結果を結合して整形
        result_text = ' '.join(result)

        # 単語の先頭を大文字に
        words = result_text.split()
        capitalized_words = [word.capitalize() for word in words]
        result_text = ' '.join(capitalized_words)

        # 連続する空白を削除
        result_text = re.sub(r'\s+', ' ', result_text)

        return result_text.strip()

    def _kata_to_hira(self, text: str) -> str:
        """
        カタカナをひらがなに変換する
        """
        return jaconv.kata2hira(text)
