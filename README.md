# A budget application

## This is my first coding/dev project in the last 12 years

This is a simple app that lets you track your budget comparing Planned amounts vs Actual amounts for expenses, revenue and savings.

The user enters the new Budget and Actuals details in forms generated with the Python Flask module, which are rendered in HTML. The data is then saved in a SQALchemy database.

The Budget and Actual details can be seen/updated/deleted in 2 tables. Also, they are visualized on the front page through SVG graphs generated with the PYGAL Python module, which pulls the data directly from the database.

![alt text](https://i.imgur.com/WJDmvf8.jpg)
![alt text](https://i.imgur.com/zeegh0I.jpg)
![alt text](https://i.imgur.com/DrAoKVN.jpg)
![alt text](https://i.imgur.com/ZAmTAuZ.jpg)

The application also supports user registering, reseting user password, updating user account. 

The back-end is built in Python 3.6.5, with Flask 1.0.2 module, Pygal module, SQLAlchemy module and a few other smaller modules.

**Note:** to run the application you will need to set up environment variables. See config.py for more details

