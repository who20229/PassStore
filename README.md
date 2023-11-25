# [📍] About this project : PassStore
This project is a program that can be helpful for people who often forget their password! The user can: Save or delete a password of a specific app which is saved in a mongodb database, validate that their password is strong,
get the program to suggest a strong password.However, as no form of encryption is used, I do not suggest connection to database that another person owns.  
I made this project as my final project of CS50, if you have any questions, please send me a request in `late.np` on Discord.
## [⌨️] USAGE: How do i use this?
`requirements.txt` holds all the required libraries, it can be installed with `pip install -r requirements.txt`  

create .env and in .env file  
```
DISCORD_WEBHOOK_URL=Your_discord_webhook_url
CONNECTION=MONGO_CONNECTION_URL
```
replace `MONGO_CONNECTION_URL` with your connection string ([How to get mongo connection URL](https://www.mongodb.com/basics/mongodb-connection-string#:~:text=The%20MongoDB%20connection%20string%20for,port%20number%20you%20are%20using.))  
replace `DISCORD_WEBHOOK-URL` with your webhook URL
  
in `main.py` go to line 13 
```py
db = mClient['DB_NAME']
```
replace `DB_NAME` with the name of your database  
  
after installation:  
run: `python main.py` and enter a username and password
```
+-----------+-----------------+
Enter username & password
USERNAME: Your_username
PASSWORD: Your_password
```
if you are using this for the first time, you will be asked to register!
```
Enter username & password
USERNAME: Your_username
PASSWORD: Your_password
We couldn't find your data:
+-----------+-----------------+
Setup username & password
USERNAME: new_username
PASSWORD: new_password
```
after your login with your newly created username, you will be presented with a table of cmds select any one of them and follow the instructions
```
+-----------+-----------------+
Please type the command to be executed:

+------------+---------------+-----------------------------------+
|   Function | Description   | Command                           |
+============+===============+===================================+
|          1 | View          | View saved password               |
+------------+---------------+-----------------------------------+
|          2 | Save          | Save new password                 |
+------------+---------------+-----------------------------------+
|          3 | Rate          | Check how strong your password is |
+------------+---------------+-----------------------------------+
|          4 | Suggest       | Suggest changes to developer      |
+------------+---------------+-----------------------------------+
|          5 | Generate      | Generate a strong pasword         |
+------------+---------------+-----------------------------------+
|          6 | Delete        | Delete Saved Password             |
+------------+---------------+-----------------------------------+
>>
```
## [❓] Requirements and its functions
os: to access .env   
re : to check the strength of function  
sys : to access command line arguments  
tabulate : to showcase the command options and retrieved password when requested  
requests : send suggestions to dev
termcolor : aesthetics  
dotenv :access .env  
pymongo: database  
password_generator: generate random passwords

## [😲] What can be expected in the future
I plan on encrypting the password and usernames of user and store it in the database, this will only be decrypted when the user requests to view it so it can be more secure. The password right now is not encrypted before being saved to [mongodb](https://www.mongodb.com). So i suggest to use this in your **own** db only


## To know more refer to ths [Video Tutorial](https://youtu.be/ZFkeogXgRf4)
