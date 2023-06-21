import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def insert_emailaddress(conn, email):
    """Create a new email in the EMAILADDRESS table."""
    sql_select = "SELECT ID FROM EMAILADDRESS WHERE EMAIL = ?"
    cur = conn.cursor()
    cur.execute(sql_select, (email,))
    row = cur.fetchone()
    if row:
        email_id = row[0]
    else:
        sql_insert = "INSERT INTO EMAILADDRESS(EMAIL) VALUES (?)"
        cur.execute(sql_insert, (email,))
        email_id = cur.lastrowid
        conn.commit()
    return email_id


def insert_domain(conn, domain, email_id):
    """Create a new domain in the DOMAIN table."""
    sql_select = "SELECT ID FROM DOMAIN WHERE DOMAIN = ?"
    cur = conn.cursor()
    cur.execute(sql_select, (domain,))
    row = cur.fetchone()
    if row:
        domain_id = row[0]
    else:
        sql_insert = "INSERT INTO DOMAIN(DOMAIN, EMAILID) VALUES (?, ?)"
        cur.execute(sql_insert, (domain, email_id))
        conn.commit()
        domain_id = cur.lastrowid
    return domain_id


def insert_day(conn, day, email_id):
    """Create a new day in the DAY table."""
    sql_select = "SELECT ID FROM DAY WHERE DAY = ?"
    cur = conn.cursor()
    cur.execute(sql_select, (day,))
    row = cur.fetchone()
    if row:
        day_id = row[0]
    else:
        sql_insert = "INSERT INTO DAY(DAY, EMAILID) VALUES (?, ?)"
        cur.execute(sql_insert, (day, email_id))
        conn.commit()
        day_id = cur.lastrowid
    return day_id


def insert_spamconf(conn, spam_conf, email_id):
    """Create a new spam_conf in the SPAMCONF table."""
    sql_insert = "INSERT INTO SPAMCONF(SPAMCONF, EMAILID) VALUES (?, ?)"
    cur = conn.cursor()
    cur.execute(sql_insert, (spam_conf, email_id))
    conn.commit()
    return cur.lastrowid


def main():
    database = "mbox.db"

    sql_create_emailaddress_table = """CREATE TABLE IF NOT EXISTS EMAILADDRESS (
                                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                        EMAIL TEXT NOT NULL
                                    );"""

    sql_create_domain_table = """CREATE TABLE IF NOT EXISTS DOMAIN (
                                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                    DOMAIN TEXT UNIQUE NOT NULL,
                                    EMAILID INTEGER NOT NULL,
                                    FOREIGN KEY (EMAILID) REFERENCES EMAILADDRESS (ID)
                                );"""

    sql_create_day_table = """CREATE TABLE IF NOT EXISTS DAY (
                                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                    DAY TEXT NOT NULL,
                                    EMAILID INTEGER NOT NULL,
                                    FOREIGN KEY (EMAILID) REFERENCES EMAILADDRESS (ID)
                                );"""

    sql_create_spamconf_table = """CREATE TABLE IF NOT EXISTS SPAMCONF (
                                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                    SPAMCONF TEXT NOT NULL,
                                    EMAILID INTEGER NOT NULL,
                                    FOREIGN KEY (EMAILID) REFERENCES EMAILADDRESS (ID)
                                );"""

    # Create a database connection
    conn = create_connection(database)

    # Create tables
    if conn is not None:
        # Create EMAILADDRESS table
        create_table(conn, sql_create_emailaddress_table)

        # Create DOMAIN table
        create_table(conn, sql_create_domain_table)

        # Create DAY table
        create_table(conn, sql_create_day_table)

        # Create SPAMCONF table
        create_table(conn, sql_create_spamconf_table)
    else:
        print("Error! Cannot create the database connection.")
        return

    file_name = "mbox.txt"
    with open(f'Data/{file_name}', "r") as file:
        lines = file.readlines()

        for line in lines:
            if line.startswith("From "):
                components = line.split()

                email = components[1]
                domain = email.split('@')[1]
                day = components[2]

                email_id = insert_emailaddress(conn, email)
                insert_domain(conn, domain, email_id)
                insert_day(conn, day, email_id)
                insert_emailaddress(conn, email)

                if line.startswith("X-DSPAM-Confidence: "):
                    takes = line.split()
                    spam_conf = takes[1]
                    insert_spamconf(conn, spam_conf, email_id)

    # Display only domains in the table
    cursor = conn.execute(
        "SELECT DOMAIN FROM DOMAIN")
    domains = cursor.fetchall()
    print("\nDomains:")
    for domain in domains:
        print(domain[0])

    # ask user for domain
    domain = input("\nEnter a domain: ")
    cursor = conn.execute(
        "SELECT EMAIL FROM EMAILADDRESS WHERE ID IN (SELECT EMAILID FROM DOMAIN WHERE DOMAIN = ?)", (domain,))
    emails = cursor.fetchall()
    print("\nEmails:")
    for email in emails:
        print(email[0])

    conn.close()


if __name__ == '__main__':
    main()
