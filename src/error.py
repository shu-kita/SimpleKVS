# -*- coding: utf-8 -*-

class InvalidFileExtensionError(ValueError):
    """
    ファイルの拡張子が不正の時のエラー
    """
    pass

class SettingFileNotFoundError(FileNotFoundError):
    """
    設定ファイルが見つからない時のエラー
    """
    pass