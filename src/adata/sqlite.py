# adata.sqlite

''' 
Local SQLite3 databases on file

Do not use this, please.

'''
import sqlite3, os, sys

#----------------------------------------------------------------------------
#--- DB

def sql_get_table(sql):
    l=sql.split(" ")
    return l[l.index("FROM")+1]

#------------------------------------------------------------------------------
class DataBase(object):
    '''Open a SQLite3 path
       Types: TEXT, INTEGER, FLOAT, BLOB, NULL

    '''

    def __init__(self, path=':memory:'):
        
        self.path = path
        self.log = None
        self.datatype = {}

        try:
            self.connection = sqlite3.connect(path)
            #python2 self.connection.text_factory = lambda x: unicode(x, "utf-8", "ignore")
            self.cursor = self.connection.cursor()

        except sqlite3.Error as e:
            print("SQLite3 version %s" % sqlite3.version)
            print(e)

        
        #self.connection.text_factory = str

        
        
        
    def info(self):    
        txt= "DB "+self.path+"', "+str(len(self.tables()))
        txt+=" tables ("+str(self.size())+"Kb)"
        #repr(self.scheme())
        return txt
        
    def __del__(self):
        self.cursor.close()
        #log("Disconnected from database")
    
    def size(self):
        """Cuantos Kb ocupa la base de datos
        """
        return os.path.getsize(self.path)/1024

    def scheme(self):
        lines=[]
        sql="SELECT * FROM sqlite_master ORDER BY name;"
        self.cursor.execute(sql)
        for cosa in self.cursor:
            print(str(cosa))
            lines.append(str(cosa))
        return lines
    
    def tables(self):
        tables=[]
        sql="SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;"
        self.cursor.execute(sql)
        for table in self.cursor:
            if table[0][0:7]!="sqlite_": tables.append(table[0])
        return tables

    def fields(self, table):
        fields=[]
        sql="SELECT * FROM "+str(table)+" WHERE 0;"
        self.cursor.execute(sql)
        for field in self.cursor.description:
            #print "CAMPO "+str(campo)
            fields.append(field[0])
        return fields

    def types(self, table):
        fields=[]
        sql="SELECT sql FROM sqlite_master WHERE tbl_name='"+str(table)+"';"
        self.cursor.execute(sql)
        #if not self.datatype.has_key(table): 
        self.datatype[table]={}
        for cosa in self.cursor:
            s=cosa[0]
            if s is None: continue
            if "CREATE" in s:
                tmp = s[s.find("(")+1:s.rfind(")")]
                for c in tmp.replace("\n","").replace("\r","").split(","):
                    name = c[c.find("[")+1:c.rfind("]")]
                    try:
                        size = int(c[c.find("(")+1:c.rfind(")")])
                    except:
                        size = None
                    self.datatype[table][name]={"KEY": "UNIQUE" in c,
                                                "NULL": not ("NOT NULL" in c),
                                                "SIZE": size}
                    fp = c.find("(")
                    if fp!=-1: c = c[:fp]
                    self.datatype[table][name]["TYPE"] = c.split(" ")[1]
        #print repr(self.datatype[table])
        return self.datatype[table]

    def result(self,sql):
        result=[]
        self.cursor.execute(sql)
        for record in self.cursor:
            #if self.debug: print "    - "+str(record)
            result.append(record)
        if self.log is not None: 
            self.log.write(" SQL: "+sql+" -> "+str(len(result))+"\n")
        return result
                    
    def query(self,command):
        if self.log is not None: 
            self.log.write(" SQL: "+command+"\n")
        try:
            self.cursor.execute(command)
        except:
            error=str(sys.exc_info()[1])
            print(" SQL: "+command)
            print(" SQL: "+error)
            
        if command[0:6]=="SELECT":
            result=[]
            print("Registros:")
            for record in self.cursor:
                print(repr(record))
                result.append(record)
            return result
        else:
            self.connection.commit()

