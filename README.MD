**Approach for running the python scripts:-**
-

First of all fill the required detail in the **.env** file as instructed. The packages used for running these scripts are mentioned in the **requirements.txt** file, install them in your environment before running running the scripts.
I have used **MySQL 8.0.17** as a relational database.

- First run the **create_database.py** file. The work of this script is to create a database. Command to run this script:- **python create_database.py**
 
- After this run the **users_etl.py** file. This script creates the **customer_details** table and **purchase_history** table. Command to run this script:- **python users_etl.py**

- After this run the **restaurants_etl.py** file. This script creates the **restaurant_detail** table, **rest_timingss** table and **menu_details** table. Command to run this script:- **python restaurants_etl.py**.

 

 
 
