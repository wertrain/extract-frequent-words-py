:: 
:: MeCab 環境作成 bat
::
:: venv は仮想環境を作ったフォルダ名に適宜変更する
:: この bat を実行後に MECABRC を環境変数に追加する
:: もしくは下記のようにコピーされた etc\mecabrc へのパスを通すことで
::
:: import os
:: os.environ['MECABRC'] = r'.\venv\Scripts\etc\mecabrc'
::
::
cd /d %~dp0
TinyUnzipper.exe ".\mecab.zip" "."
copy /y ".\mecab\libmecab.dll" "..\venv\Scripts\libmecab.dll"
copy /y ".\mecab\mecab.exe" "..\venv\Scripts\mecab.exe"
echo D | xcopy /Y /E ".\mecab\dic" "..\venv\Scripts\dic"
echo D | xcopy /Y /E ".\mecab\etc" "..\venv\Scripts\etc"
rmdir /s /q ".\mecab"
