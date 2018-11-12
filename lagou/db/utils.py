
from scrapy.conf import settings
import pymysql
import logging
import requests


proxy_pool = []

db_settings = settings.get('PROXY_DB_SETTINGS')
connect = pymysql.connect(**db_settings)
cursor = connect.cursor()
query_sql = 'SELECT http_type, ip, port FROM proxy WHERE http_type="http" ORDER BY verify_time DESC LIMIT 20'
cursor.execute(query_sql)
rows = cursor.fetchall()

for row in rows:
    proxy_pool.append(row[0].lower() + '://' + row[1] + ':' + row[2])


def verify(ip):
    r = requests.get('https://www.baidu.com', proxies={"http": ip})
    return r.status_code == 200
