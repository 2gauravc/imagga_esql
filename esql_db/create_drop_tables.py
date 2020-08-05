import psycopg2
import config_esql
import sys, getopt

def connect_db():
    """ Connect to the PostgreSQL database server """
    
    con = None
    try:
        
        # connect to the PostgreSQL server
        
        con = psycopg2.connect(host=config_esql.server,
                                database=config_esql.database,
                                user=config_esql.database,
                                password=config_esql.password)	
        # create a cursor
        return (con)
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        print ('Could not connect to DB. Exiting..')
        sys.exit(2)

def parse_sql(sql_file):

    print('1. Parsing the SQL file')
    f = open(sql_file, "r")

    # Read the SQL file with the commands 
    cmd_text = f.read()
    # Parse and extract the SQL statements. Statements are separated by ';'
    cmds = cmd_text.split(";")
    cmds = cmds[:-1]
    print ('\t Found {} SQL statements'.format(len(cmds)))
    return(cmds)


def execute_sql(cmds):

    print('2. Starting execution of SQL Statements')

    try:
        # Connect to the database
        con = connect_db()
        cur = con.cursor()

        # Execute the commands one by one
        for command in cmds:
            cur.execute(command)

        # Close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        con.commit()
        print('\t Execution successful. Commited all changes')

    except (Exception, psycopg2.DatabaseError) as error:
                print(error)
    finally:
        if con is not None:
            con.close()

def report_db_status():
    print('3. Checking the DB status')
    try:
        # Connect to the database
        con = connect_db()
        cur = con.cursor()

        # Get the list of tables in the DB
        cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = %s", ('public',))
        recs = cur.fetchall()
        print('\tFound {} tables'.format(len(recs)))
        
        for rec in recs:
            print('\t\t {}'.format(str(rec)))

        # Close communication with the PostgreSQL database server
        cur.close()


    except (Exception, psycopg2.DatabaseError) as error:
                print(error)
    finally:
        if con is not None:
            con.close()

                    

def main(argv):

        try:
            opts, args = getopt.getopt(argv,"i:", ["sqlfile="]) 
	except getopt.GetoptError:
            print ('Usage: python create_drop_tables.py --sqlfile=<sql_file_path>')
            sys.exit(2)

        req_options = 0
	for opt, arg in opts:
            if opt == '--sqlfile':
                sql_file = arg
                req_options = 1

        if (req_options == 0):
            print ('Usage: python create_db.py --sqlfile=<sql_file_path>')
            sys.exit(2)


        # Parse the SQL statements from the file
        cmds = parse_sql(sql_file)

        #Execute the SQLs
        execute_sql(cmds)

        #Report DB Status
        report_db_status()

	
if __name__ == "__main__":
   main(sys.argv[1:])
