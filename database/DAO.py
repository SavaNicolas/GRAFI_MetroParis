from database.DB_connect import DBConnect
from model.connessione import Connessione
from model.fermata import Fermata


class DAO():

    @staticmethod
    def getAllFermate():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM fermata"
        cursor.execute(query)

        for row in cursor:
            result.append(Fermata(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def hasConnessione(u:Fermata,v:Fermata):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM connessione WHERE c.id_stazP=%s and c.id_stazA=%s"
        cursor.execute(query,(u.id_fermata,v.id_fermata))


        cursor.close()
        conn.close()
        return len(result)>0 #se è <0 restituisce false, true se è >0

    @staticmethod
    def getVicini(u: Fermata):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM connessione WHERE c.id_stazP=%s" #non abbiamo più l'arrivo
        cursor.execute(query, (u.id_fermata, ))

        for row in cursor:
            result.append(Connessione(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def allEdges():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM connessione"
        cursor.execute(query)

        for row in cursor:
            result.append(Connessione(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def allEdgesVel():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT c.id_stazP, c.id_stazA, MAX(l.velocita) as v
FROM connessione c, linea l
WHERE c.id_linea = l.id_linea
GROUP BY c.id_stazP, c.id_stazA
ORDER BY c.id_stazP ASC, c.id_stazA ASC"""
        cursor.execute(query)

        for row in cursor:
            result.append((row["c.id_stazP"],row["c.id_stazA"],row["v"]))

        cursor.close()
        conn.close()
        return result