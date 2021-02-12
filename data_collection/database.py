import os
import sqlite3

class Column:
    def __init__(self, name, item_type, value=None):
        self.name = name
        self.type = item_type
        self.value = f'"{value}"' if item_type == 'TEXT' else value

class Database:
    PATH = os.path.join(os.path.dirname(__file__), 'database.sqlite3')
    def __init__(self):
        self.connection = sqlite3.connect(self.PATH)
        self.cursor = self.connection.cursor()
    
    def create_new_table(self, table_name, columns):
        command = f"CREATE TABLE {table_name} ("
        command += ', '.join([f'{column.name} {column.type}' for column in columns]) + ')'
        self.cursor.execute(command)
        self.connection.commit()
    
    def add_to_table(self, table_name, columns):
        command = f'INSERT INTO {table_name} ('
        command += ', '.join([f'{column.name}' for column in columns]) + ') VALUES ('
        command += ', '.join([f'{column.value}' for column in columns]) + ')'
        print(command)
        self.cursor.execute(command)
        self.connection.commit()

    def sanitize_value(self, type, value):
        return f'"{value}"' if type == 'TEXT' else value

    def update_value(self, table_name, column, new_value):
        command = f"UPDATE {table_name} SET {column.name} = {self.sanitize_value(column.type, new_value)} " + \
            f"WHERE {column.name} = {column.value}"
        self.cursor.execute(command)

    def get_value_from_table(self, table_name, column_name, expected_value=None):
        command = f"SELECT {column_name} FROM {table_name}" 
        if expected_value: 
            command += "WHERE {column_name} = {expected_value}"
        return self.cursor.execute(command).fetchall()

    def close_connection(self):
        self.connection.close()


# Test - the code below currently works
db = Database()
db.create_new_table('Forecasts', [Column('Description','TEXT')])
db.add_to_table('Forecasts', [Column('Description','TEXT','72F Sunny')])
val = db.get_value_from_table('Forecasts', 'Description')[0][0]
print(val)
db.update_value('Forecasts',Column('Description','TEXT',val),'70F Cloudy')
new_val = db.get_value_from_table('Forecasts', 'Description')[0][0]
print(new_val)
db.close_connection()
