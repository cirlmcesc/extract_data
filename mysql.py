#This Python file uses the following encoding: utf-8

import lib
import MySQLdb

class proMysql:
    def __init__(self, mysql_config):
        self.mysql = MySQLdb.connect(
            host = mysql_config['host'], 
            user = mysql_config['user'], 
            passwd = mysql_config['passwd'], 
            db = mysql_config['db'], 
            charset = mysql_config['charset'])

        self.db = self.mysql.cursor(cursorclass = MySQLdb.cursors.DictCursor)

    def select(self, table, join = '', field = '*', where = {}, other = []):
        self.db.execute(self.__selectString(
            table = table, join = join, field = field, 
            where = where, other = other))

        return self.db.fetchall()

    def get(self, table, join = '', field = '*', where = {}, other = []):
        self.db.execute(self.__selectString(
            table = table, join = join, field = field, 
            where = where, other = other))

        return self.db.fetchone()

    def has(self, table, where):
        res = self.get(table = table, field = '*', where = where)

        return not res is None

    def update(self, table, dictionary, where = {}):
        sql = "UPDATE " + table + ' set '

        sql += self.__spliceWhereString(dictionary = dictionary)

        sql += ' WHERE ' + self.__spliceWhereString(dictionary = where)

        self.db.execute(sql)

        return self.mysql.commit()

    def insert(self, table, dictionary):
        sql = "INSERT INTO " + table + " ("
        
        keylist =  dictionary[0].keys() if isinstance(dictionary, list) else dictionary.keys()

        sql += ', '.join(keylist) + ") VALUES "

        if isinstance(dictionary, list):
            values = []

            for instance in dictionary:
                temporary_list = []

                for key in keylist:
                    temporary_list.append("'" + instance.get(key) + "'")

                values.append("(" + ', '.join(temporary_list) + ")")

            sql += ', '.join(values)
            
        else:
            sql += "("

            temporary_list = []

            for key in keylist:
                temporary_list.append("'" + dictionary.get(key) + "'")

            sql += ', '.join(temporary_list) + ')'

        self.db.execute(sql)

        return self.mysql.commit()

    def delete(self, table, where = {}):
        sql = "DELETE FROM " + table

        if len(where) > 0:
            sql += ' WHERE ' + self.__spliceWhereString(dictionary = where)

        self.db.execute(sql)

        return self.mysql.commit()

    def __selectString(self, table, join = '', field = '*', where = {}, other = []):
        sql = "SELECT "

        if isinstance(field, str):
            sql += ' ' + field + ' '
        else:
            sql += ' ' + ', '.join(field)

        sql += ' FROM ' + table + ' ' + join

        if len(where) > 0:
            sql += 'WHERE ' + self.__spliceWhereString(where)

        if len(other) > 0:
            sql += ' '.join(other)

        return sql

    def __spliceWhereString(self, dictionary):
        temporary_list = []

        for key in dictionary:
            temporary_list.append(key + "='" + dictionary.get(key) + "'")

        return ' AND '.join(temporary_list)

    def close(self):
        return self.mysql.close()