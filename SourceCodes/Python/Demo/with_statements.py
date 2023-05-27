# New implementation:
def with_statement():
    sql_connector = ConnectorFactory().get_sql_connector()
    with sql_connector as cursor:
        cursor.execute('SELECT * FROM users', )
        print(cursor.fetchall())
    with HelloContextManager() as hello:
        print(hello)
    with open("input.txt") as in_file, open("output.txt", "w") as out_file:
        for line in in_file:
            out_file.write(line)