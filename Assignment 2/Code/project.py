import psycopg2
import Interface
import sys


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

    app = Interface.QApplication(sys.argv)
    widget = Interface.MyWidget(password)
    widget.show()
    sys.exit(app.exec())
