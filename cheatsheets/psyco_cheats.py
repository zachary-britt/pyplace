import psycopg2
from datetime import datetime

conn = psycopg2.connect(dbname='socialmedia', user='zack', host='/var/run/postgresql')
c = conn.cursor()

today = '2014-08-14'

# This is not strictly necessary but demonstrates how you can convert a date
# to another format
ts = datetime.strptime(today, '%Y-%m-%d').strftime("%Y%m%d")

c.execute(
    '''CREATE TABLE logins_7d AS
    SELECT userid, COUNT(*) AS cnt, timestamp %(ts)s AS date_7d
    FROM logins
    WHERE logins.tmstmp > timestamp %(ts)s - interval '7 days'
    GROUP BY userid;''', {'ts': ts}
)

print('All done, committing table')

conn.commit()
conn.close()
