import psycopg2
import Interface
import sys

# This file is for running the whole application
# TODO
# Split db connection function away from main function


if __name__ == '__main__':
    # Ask them for password?

    conSuccessful = False

    while (not conSuccessful):
        print("Whats your password???(Key in EXIT (ALL CAPS to exit application))")
        password = (input())

        if (password == "EXIT"):
            print("Exiting application")
            exit()

        try:
            # Connecting to the database and initializing the cursor as class variables
            Interface.MyWidget.connection = psycopg2.connect(
                database="TPC-H", user='postgres', password=password, host='127.0.0.1', port='5432')
            Interface.MyWidget.connection.autocommit = True
            cursor = Interface.MyWidget.connection.cursor()
            print("Connected to PostgreSQL successfully!")
            conSuccessful = True
        except (Exception, psycopg2.Error) as error:
            # Error handling
            print("Error while connecting to PostgreSQL: ", error)
            # exit()

    # conn.autocommit = True
    # cursor = conn.cursor()

    # TODO This one need throw inside interface to run this so need set as local variable or something so they can run
    cursor.execute(
        f"EXPLAIN (FORMAT JSON) {'''SELECT * from Region, customer,nation Where region.r_regionkey = 0'''}")
    # f"EXPLAIN (FORMAT JSON) {'''SELECT * from Region'''}")
    # Example queries
    # cursor.execute('''SELECT * from Region''')
    result = cursor.fetchall()

    # TOREMOVE these are testing to see how the json file look like
    # print(result)
    # for x in result[0][0][0]["Plan"]:
    #     if(x != "Plans"):
    #         print("Key: ", x, " = ", result[0][0][0]["Plan"][x])
    # for y in result[0][0][0]["Plan"]["Plans"]:
    #     print("-------------")
    #     for z in y:
    #         print("Key: ",z, " = ", y[z])
    # print(result[0][0][0])

    # TODO This need to shift to interface, no nid do here, either that or init function take in the queries files
    fd = open('../Queries/2.sql', 'r')
    sqlFile = fd.read()
    fd.close()

    app = Interface.QApplication(sys.argv)
    widget = Interface.MyWidget(password)
    widget.setTestingMessage(sqlFile)
    widget.show()
    # widget.treeDisplay(result[0][0][0]["Plan"])
    sys.exit(app.exec())
