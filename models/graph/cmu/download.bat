@echo off

echo [download] model graph : cmu
SET "DIR=%~dp0"

:: 関数の代わりにバッチファイルのサブルーチンを使用します
call :extract_download_url "http://www.mediafire.com/file/qlzzr20mpocnpa3/graph_opt.pb"
SET "DOWNLOAD_URL=%URL%"

:: PowerShellを使用してファイルをダウンロードします
PowerShell -Command "& {Invoke-WebRequest -Uri '%DOWNLOAD_URL%' -OutFile '%DIR%graph_opt.pb'}"

echo [download] end
goto :eof

:extract_download_url
:: PowerShellを使用してURLを抽出します
SET "mediafire_url=%~1"
FOR /F "delims=" %%I IN ('PowerShell -Command "& { (Invoke-WebRequest -Uri '%mediafire_url%').Links | Where-Object { $_.href -like 'http*://download*' } | Select-Object -Last 1 -ExpandProperty href }"') DO SET "URL=%%I"
goto :eof
