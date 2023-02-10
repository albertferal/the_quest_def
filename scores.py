import sqlite3 as sql

def createDB():
    conn = sql.connect("Scoring.db")
    conn.commit()
    conn.close()

def createTable():
    conn = sql.connect("Scoring.db")
    cursor = conn.cursor()
    cursor.execute(
    """CREATE TABLE Scoring (
        name text,
        score integer
        )"""
    )
    conn.commit()
    conn.close()

def insertRow(name, puntaje):
    conn = sql.connect("Scoring.db")
    cursor = conn.cursor()
    instruccion = f"INSERT INTO Scoring VALUES ('{name}', {puntaje})"
    cursor.execute(instruccion)
    conn.commit()
    conn.close()

def deleteRow():
    conn = sql.connect("Scoring.db")
    cursor = conn.cursor()
    instruccion = f"DELETE FROM Scoring WHERE name like 'LOL'"
    cursor.execute(instruccion)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    #createDB()
    #createTable()
    #insertRow("AFA", 100000)
    deleteRow()