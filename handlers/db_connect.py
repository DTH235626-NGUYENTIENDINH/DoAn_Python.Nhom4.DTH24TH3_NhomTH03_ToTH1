import pyodbc

def connect_to_db():
    try:
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=localhost;'
            'DATABASE=QuanLySach;'
            'Trusted_Connection=yes;'
        )
        return conn
    except Exception as e:
        print("Lỗi kết nối SQL Server:", e)
        return None