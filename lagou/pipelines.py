# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time
from scrapy.conf import settings
import pymysql


class JobPipeline(object):
    def process_item(self, item, spider):
        db_settings = settings.get('DB_SETTINGS')
        connect = pymysql.connect(**db_settings)
        cursor = connect.cursor()
        query_sql = 'SELECT * FROM job WHERE url=%s'
        cursor.execute(query_sql, (item['url'],))
        result = cursor.fetchall()
        if result:
            return item
        sql = 'insert into job(name, company, salary, city, experience, education, nature, duty, address, url) ' \
              'values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        datas = (
            item['name'],
            item['company'],
            item['salary'],
            item['city'],
            item['experience'],
            item['education'],
            item['nature'],
            item['duty'],
            item['address'],
            item['url'],
        )
        cursor.execute(sql, datas)
        cursor.close()
        connect.commit()
        connect.close()

        return item
