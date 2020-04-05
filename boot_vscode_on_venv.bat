@echo off
:: 現在のディレクトリに移動
cd /d %~dp0
:: virtualenv を起動
call "venv\Scripts\activate"
:: Visual Studio Code を起動
code
