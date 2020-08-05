import psycopg2
import sys, getopt
import pandas as pd
import config_esql
def connect_db():
    """ Connect to the PostgreSQL database server """
    con = None
    try:
        
        # connect to the PostgreSQL server
        print('\t Connecting to the PostgreSQL database...')
        con = psycopg2.connect(host=config_esql.server,
                                database=config_esql.database,
                                user=config_esql.database,
                                password=config_esql.password)	
        # create a cursor
        print('\t Connection successful')
        return (con)
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        print ("\t Could not connect to DB. Exiting..")
        sys.exit(2)



def report_table_recs(tables):
    
    #Connect to the database
    con = connect_db()
    cur = con.cursor()

    try:
        for table in tables:
            qry = "SELECT COUNT(*) FROM %s" % table
            cur.execute(qry)
            cnt = cur.fetchall()
            cnt_rec = cnt[0][0]
            print ('\t Table {} has {} records'.format(table,cnt_rec))
            
        
        # Close communication with the PostgreSQL database server
        cur.close()
        
    except (Exception, psycopg2.DatabaseError) as error:
                print(error)
    finally:
        if con is not None:
            con.close()

    

def read_insert_data_into_tables(tables,datafiles):
    con = connect_db()
    cur = con.cursor()
                
    for table,datafile in zip(tables,datafiles):
        f = open(datafile, 'r')
        cur.copy_from(f, table, sep=',',null="")
        con.commit()
        print('\t Committed data into table: {}'.format(table))
        
    con.close()
