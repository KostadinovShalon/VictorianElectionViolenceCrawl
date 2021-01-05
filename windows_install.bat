@ECHO OFF
call conda activate base
call conda remove --name vevcrawler --all -y
call conda create -n vevcrawler -y
call conda activate vevcrawler
call conda install -y Twisted
call pip install vev_crawler-2.1.5-py3-none-any.whl
call conda install -y numpy
call set FLASK_APP=application
call flask init-db