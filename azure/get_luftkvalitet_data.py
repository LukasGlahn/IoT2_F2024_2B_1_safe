import sqlite3


def get_dht_sgp_data(number_of_rows, rum=1):
    query = f'SELECT * FROM luftkvalitet WHERE rumid IS {rum} ORDER BY rowid DESC LIMIT 20;'
    datetimes = []
    temperatures = []
    humidites = []
    co2_levels = []
    voc_levels = []
    try:
        conn = sqlite3.connect("database/main_db.db")
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchmany(number_of_rows)
        for row in rows:
            datetimes.append(row[2])
            temperatures.append(row[3])
            humidites.append(row[4])
            co2_levels.append(row[5])
            voc_levels.append(row[6])
        return datetimes, temperatures, humidites, co2_levels, voc_levels

    except sqlite3.Error as sql_e:
        print(f'sqlite encounterd a error: {sql_e}')
        conn.rollback()

    except Exception as e:
        print(f'encounterd a error: {e}')


    finally:
        conn.close()

get_dht_sgp_data(10)
