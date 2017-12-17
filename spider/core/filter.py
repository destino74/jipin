import pymysql

import settings


class DummyFilter(object):
    def __init__(self, source_id):
        self.conn = pymysql.connect(settings.DB_HOST, user=settings.DB_USER, passwd=settings.DB_PASSWORD,
                                    db='recruitment', connect_timeout=5, charset='utf8',
                                    cursorclass=pymysql.cursors.DictCursor)
        self.cur = self.conn.cursor()
        self.cur.execute("""select detail_id from recruitment_detail where source_id = %s""", [source_id])
        result = self.cur.fetchall()
        self.info_set = set([x['detail_id'] for x in result])
        self.cur.close()
        self.conn.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.info_set.clear()

    def exist(self, did):
        return did in self.info_set
