def add_users(id_num, cur):
    sql = f"INSERT INTO users(Telegram_ID) VALUES('{id_num}')"
    cur.execute(sql)

def add_user_alert(id_num, cur):
    sql = f"INSERT INTO alerts(Telegram_ID) VALUES('{id_num}')"
    cur.execute(sql)

def all_users(cur):
    cur.execute(f"SELECT Telegram_ID FROM users")
    rows = cur.fetchall()
    unique = [] 
    for i in rows:
        unique.append(i[0])
    return unique

def add_up(id_num, pair, price, cur):
    sql = f"UPDATE alerts SET {pair}_Up = '{price}' WHERE Telegram_ID = {id_num}"
    cur.execute(sql)

def add_down(id_num, pair, price, cur):
    sql = f"UPDATE alerts SET {pair}_Down = '{price}' WHERE Telegram_ID = {id_num}"
    cur.execute(sql)

def all_up(id_num, pair, cur):
    cur.execute(f"SELECT {pair}_Up FROM alerts WHERE Telegram_ID = {id_num}")
    rows = cur.fetchall()
    if rows[0][0] == None:
        rows = 'Nothing'
        return rows
    else:
        return rows[0][0]

def all_down(id_num, pair, cur):
    cur.execute(f"SELECT {pair}_Down FROM alerts WHERE Telegram_ID = {id_num}")
    rows = cur.fetchall()
    if rows[0][0] == None or rows[0][0] == '':
        rows = 'Nothing'
        return rows
    else:
        return rows[0][0]

def add_feedback(id_num, message, cur):
    sql = f"INSERT INTO feedback(Telegram_ID, Message) VALUES('{id_num}', '{message}')"
    cur.execute(sql)

def special(code, cur):
    cur.execute(f"SELECT Details FROM special where Code = '{code}'")
    rows = cur.fetchall()
    return rows[0][0]

def available_pairs(code, cur):
    cur.execute(f"SELECT Details FROM special where Code = '{code}'")
    rows = cur.fetchall()
    rows = rows[0][0].split(' ')
    return rows