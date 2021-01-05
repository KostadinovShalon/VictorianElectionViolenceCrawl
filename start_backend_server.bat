@ECHO OFF
call conda activate vevcrawler
call waitress-serve --call --port 5000 "application:create_app"
