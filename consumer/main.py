# coding=utf-8
import json
import sys
import time
import traceback
import pymysql
import redis
import settings

redis_db = redis.StrictRedis(host='localhost', port=6379, db=0)


def deserialize():
    ret = []

    def time_limit_task():
        spent_time = 0
        while redis_db.llen("detail") != 0:
            beg = time.time()
            info_byte = redis_db.lpop("detail")
            info_dt = json.loads(info_byte)
            ret.append(info_dt)
            end = time.time()
            spent_time += end - beg
            if spent_time >= 3:
                break

    try:
        time_limit_task()
    except Exception:
        traceback.print_exc()

    return ret


if __name__ == '__main__':
    try:
        conn = pymysql.connect(settings.DB_HOST, user=settings.DB_USER, passwd=settings.DB_PASSWORD, db='recruitment',
                               connect_timeout=5, charset='utf8')

        sql = """
        Insert ignore into recruitment_detail 
        (title, salary, province, experience, education, content, address, url, company, icon,  source_id, detail_id) 
        values 
        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        with conn.cursor() as cur:
            while True:
                    details = deserialize()
                    if details:
                        params = [(d['title'], d['salary'], d['province'], d['experience'], d['education'],
                                   d['content'], d['address'], d['url'], d['company'],
                                   d['icon'], d['source_id'], d['detail_id']) for d in details]
                        cur.executemany(sql, params)
                        conn.commit()
                        print "入库%s条数据" % len(details)
                    time.sleep(5)
    except KeyboardInterrupt:
        print 'User KeyboardInterrupt'
    except Exception:
        traceback.print_exc()
        sys.exit(0)




