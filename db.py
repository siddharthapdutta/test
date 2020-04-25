import psycopg2

def find(lat, long):
    try:
        connection = psycopg2.connect("dbname='postgres' user='postgres' host='localhost' password='1234' port='5432'")
        cursor = connection.cursor()
        find_table_query = "SELECT * FROM pincode WHERE lat='{}' AND long='{}'".format(lat, long)
        cursor.execute(find_table_query)
        record = cursor.fetchone()
        if record is not None:
            result = {'Pin Code': record[0],
                      'Address': record[1],
                      'City': record[2]}
        else:
            result = {}
        return result
    except:
        return {'Error': 'Database Error'}
    finally:
        cursor.close()
        connection.close()

MAX_DIST = 100
def insert(key, place, admin, lat, lon):
    try:
        connection = psycopg2.connect("dbname='postgres' user='postgres' host='localhost' password='1234' port='5432'")
        cursor = connection.cursor()
        check_dist_query = "SELECT key, place, earth_distance(ll_to_earth(p.lat, p.long),ll_to_earth(%f,%f))/1000 AS distance FROM pincode p;"%(lat, lon)
        cursor.execute(check_dist_query)
        records = cursor.fetchall()
        for k, p, distance in records:
            if (distance != None):
                if (distance < MAX_DIST):
                    return {'Error': 'Inserted {} is close to {}'.format(place, p)}
            if (k == key):
                return {'Error': 'Key Already Exists'}
        insert_table_query = "INSERT INTO pincode(key, place, admin, lat, long, acc) VALUES('%s','%s','%s',%s,%s,%s);"%(key,place,admin,lat,lon,'NULL')
        cursor.execute(insert_table_query)
        connection.commit()
        return {'Inserted':'True'}
    except:
        print(p, distance)
        return {'Inserted':'False'}
    finally:
        cursor.close()
        connection.close()