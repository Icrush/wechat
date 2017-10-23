#!/usr/bin/env python
import sys
import MySQLdb as mdb

class db:
    DB_HOST = 'localhost'
    DB_USER = 'root'
    DB_PASSWORD = 'root'
    DB_NAME = 'wechat'

    def __init__(self):
        try:
            self.con = mdb.connect(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)      
            cur = con.cursor()
            cur.execute("SELECT VERSION()")
            data = cur.fetchone()
            print "Database version: %s" % data 
        except mdb.Error as e:
            print "Error:" + str(e)
            sys.exit(1)        
        finally:
            if self.con:
                self.con.close()


    def retrieve_data(self):
        """
        Retrieve the data from the table.
        """ 
        with self.con:
            cur = self.con.cursor()
            sql = "SELECT * FROM wx_user"
            cur.execute(sql)

            results = cur.fetchall()

            for r in results:
                print r


    def dict_cursor(self):
        """
        Retrieving data using a dict cursor instead of the default tuple cursor
        """
        
        with self.con:
            cur = self.con.cursor(mdb.cursors.DictCursor)
            cur.execute("SELECT * FROM wx_user")

            results = cur.fetchall()

            for row in results:
                print "%d %s" % (row['id'], row['openID'])


    def insert(self,name):
        """
        Retrieving the data and showing along with the column headers
        """

        with self.con:
            cur = self.con.cursor()
            cur.execute("insert into wx_user(openID) values ('" + name + "')")
            print "Number of rows insert: %d" % cur.rowcount


    def update_prep_stmt(self):
        """
        Using prepared statements to update the entries
        """

        with self.con:
            cur = self.con.cursor()
            cur.execute("UPDATE writers SET name = %s WHERE id = %s",
                        ('Guy de Muapasant', 4))

            print "Number of rows updated: %d" % cur.rowcount


if __name__ == "__main__" :
    print help (db)