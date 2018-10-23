#!/usr/bin/python3.5
# coding: utf-8

import pymysql

class ConnectionMariaDB():

    def __init__(self):
        # Variable que determina si estamos conectados a MariaDB...
        self.connected = False
        self.error = ""

    def connect(self, host, user, password, database, port=3306):

        try:
            self.db = pymysql.connect(host=host,
                                      user=user,
                                      password=password,
                                      db=database,
                                      charset='utf8mb4',
                                      cursorclass=pymysql.cursors.DictCursor,
                                      port=port)
            self.cursor = self.db.cursor()
            self.connected = True
            return True
        except pymysql.Error as e:
            self.error = "Error: %s" % (e)
        except:
            self.error = "Error unknown"
        return False

    def query(self, query, params=None, execute=True):
        """
        Funcion que ejecuta una instruccion mysql
        Tiene que recibir:
            - query
        Puede recibir:
            - params => tupla con las variables
            - execute => devuelve los registros
        Devuelve False en caso de error
        """
        if self.connected:
            self.error = ""
            try:
                self.cursor.execute(query, params)
                self.db.commit()
                return self.cursor if execute else True

            except pymysql.Error as e:
                self.error = "Error: %s" % (e)
        return False

    def close(self):

        self.connected = False
        try:
            self.cursor.close()
        except:
            print('no se pudo cerrar la SESION')


