# Import libraries required for connecting to mysql
import mysql.connector

# Import libraries required for connecting to DB2
import ibm_db
# Connect to MySQL
connection = mysql.connector.connect(user='root', password='NDM5NC1yYWNoZW1l',host='127.0.0.1',database='sales')

# create cursor

cursor = connection.cursor()
# Connect to DB2
dsn_hostname = "" # e.g.: "dashdb-txn-sbox-yp-dal09-04.services.dal.bluemix.net"
dsn_uid = ""        # e.g. "abc12345"
dsn_pwd = ""      # e.g. "7dBZ3wWt9XN6$o0J"
dsn_port = "32459"                # e.g. "50000" 
dsn_database = "bludb"            # i.e. "BLUDB"
dsn_driver = "{IBM DB2 ODBC DRIVER}" # i.e. "{IBM DB2 ODBC DRIVER}"           
dsn_protocol = "TCPIP"            # i.e. "TCPIP"
dsn_security = "SSL"              # i.e. "SSL"

#Create the dsn connection string
dsn = (
    "DRIVER={0};"
    "DATABASE={1};"
    "HOSTNAME={2};"
    "PORT={3};"
    "PROTOCOL={4};"
    "UID={5};"
    "PWD={6};"
    "SECURITY={7};").format(dsn_driver, dsn_database, dsn_hostname, dsn_port, dsn_protocol, dsn_uid, dsn_pwd, dsn_security)

# create connection
conn = ibm_db.connect(dsn, "", "")
print ("Connected to database: ", dsn_database, "as user: ", dsn_uid, "on host: ", dsn_hostname)

# Find out the last rowid from DB2 data warehouse
# The function get_last_rowid must return the last rowid of the table sales_data on the IBM DB2 database.

def get_last_rowid():
    SQL="SELECT MAX(ROWID) FROM sales_data;"
    stmt = ibm_db.exec_immediate(conn, SQL)
    tuple_rowid = ibm_db.fetch_tuple(stmt)
    return tuple_rowid


last_row_id = get_last_rowid()
print("Last row id on production datawarehouse =", last_row_id[0])

# List out all records in MySQL database with rowid greater than the one on the Data warehouse
# The function get_latest_records must return a list of all records that have a rowid greater than the last_row_id in the sales_data table in the sales database on the MySQL staging data warehouse.

def get_latest_records(rowid):
    SQL= f"SELECT * FROM sales_data where ROWID > '{rowid[0]}';"
    cursor.execute(SQL)
    records = cursor.fetchall()
    # print(records)
    return records	

new_records = get_latest_records(last_row_id)

print("New rows on staging datawarehouse = ", len(new_records))

# Insert the additional records from MySQL into DB2 data warehouse.
# The function insert_records must insert all the records passed to it into the sales_data table in IBM DB2 database.

def insert_records(records):
    for row in records:
        print(row)
        insert_row_query = "INSERT INTO SALES_DATA (ROWID, PRODUCT_ID, CUSTOMER_ID, QUANTITY) VALUES (?, ?, ?, ?);"
        stmt = ibm_db.prepare(conn, insert_row_query)
        ibm_db.execute(stmt, row)
	

insert_records(new_records)
print("New rows inserted into production datawarehouse = ", len(new_records))

# disconnect from mysql warehouse
connection.close()

# disconnect from DB2 data warehouse
ibm_db.close(conn)
# End of program
