import os
import re
import sys
import tabulate
import requests
from termcolor import colored
from dotenv import load_dotenv
from pymongo import MongoClient
from password_generator import PasswordGenerator

load_dotenv()
ConnectionString = os.environ["CONNECTION"] 
mClient = MongoClient(ConnectionString)
db = mClient['DB_NAME']
userCollection = db['finalUserSchema']
passCollection = db['pasSchema']

def main():
    username = login()
    commands = [["1", "View", "View saved password"], ["2", "Save", "Save new password"], ["3", "Rate", "Check how strong your password is"], 
                ["4", "Suggest", "Suggest changes to developer"], ["5", "Generate", "Generate a strong pasword"], ["6", "Delete", "Delete Saved Password"]]
    allowed = ["1", "2", "3", "4", "5", "6", "one", "two", "three", "four", "five", "six"]
    headers = {"Command", "Function", "Description"}
    print("+-----------+-----------------+\nPlease type the command to be executed:", end="\n\n")
    print(tabulate.tabulate(commands, headers, tablefmt="grid"))
    cmd = input(">> ").strip().lower()
    if cmd in allowed:
        if cmd == "5" or cmd == "five":
            print(f"Suggested password: {suggest()}")
            yn2 = input("would you like the program to suggest you another strong password? (y/n)").strip().lower()
            if yn2 == 'y' or yn2 == 'yes':
                print(f"Suggested password: {suggest()}")
            elif yn2 == 'n' or yn2 == "no":
                sys.exit("Stopping the program")
            else:
                print(colored("Please provide a valid argument (y, n, yes, no)", "red"))
        elif cmd == "3" or cmd == "three":
            toRate = input(colored("Enter your password: ", "yellow")).strip()
            security = rate(toRate)
            print(f"Your accounts password is {security}")
            if "weak" in security:
                yn = input("would you like the program to suggest you a strong password? (y/n)").strip().lower()
                if yn == 'y' or yn == 'yes':
                    print(f"Suggested password: {suggest()}")
                elif yn == 'n' or yn== "no":
                    sys.exit("Stopping the program")
        elif cmd == '1' or cmd == "one":
            app = input("password for? (App/website name): ").upper().strip()
            table = view(username, app)
            print(table)
        elif cmd == '2' or cmd == "two":
            app = input("App/website Name: ").strip()
            passw = input("App Password: ").strip()
            print(set(username,app, passw))
        elif cmd == '6'  or cmd == "six":
            print(delete(username))
        elif cmd == '4' or cmd == "four":
            suggestion = input("Enter suggestion: ").strip()
            print(suggestDEV(suggestion))
        else:
            print(colored("Please provide a valid argument (y, n, yes, no)", "red"))
    else:
        sys.exit(colored("Please provide a valid input (command number from the table)", "red"))

def view(name, app):
    if found := passCollection.find_one({"username": name, "name": app}):
        info = [[app.capitalize(), found["password"]]]
        theaders = ["App", "Password"]
        return tabulate.tabulate(info, theaders, tablefmt="grid")
    else:
        sys.exit(colored("The data was not found, use [2] save command to save it.", "red"))

def set(username, app, passw):
    passCollection.insert_one({
        "username":username,
        "name":app.upper(),
        "password":passw
    })
    return colored("Data saved", "green")

def delete(name):
    app = input("App/website Name: ").strip().upper()
    if found := passCollection.find_one({"username": name, "name": app}):
        passCollection.find_one_and_delete({
            "username":name,
            "name":app.upper(),
        })
        return colored("Data removed", "green")
    else:
        return colored(f"Password for {app.capitalize()} does not exist", "red")
def suggest():
    pwo = PasswordGenerator()
    password = pwo.generate()
    return password

def rate(toRate):
    if strong := re.search("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,10}$", toRate):
        return colored("strong", "green")
    else:
        return colored("[!] weak: combine symbols, numbers and letters in different case.", "red")
    
def login():
    print("+-----------+-----------------+\nEnter username & password")
    pUser = input("USERNAME: ").strip()
    pWord = input("PASSWORD: ").strip()
    if check := userCollection.find_one({'username':pUser, 'password': pWord}):
         print(colored(f"Logged in as {pUser}", "green"))
         return pUser
    else:
        print("We couldn't find your data:")
        setup()

def setup():
    print("+-----------+-----------------+\nSetup username & password")
    pUser = input("USERNAME: ").strip()
    pWord = input("PASSWORD: ").strip()
    if check := userCollection.find_one({'username':pUser}):
        sys.exit(f"Please try again with another username as {pUser} is taken.")
    else:
        strong = re.search("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,10}$", pWord)
        userCollection.insert_one({
            "username":pUser,
            "password":pWord
        })
        print(colored("Your data is saved, you can now login!", "green"))
    if not strong:
        print("Your password can be improved, you can change it (using change command) to secured", end=" ")
        print(colored(f"suggested password: {suggest()}", "yellow"))
    login()

def suggestDEV(sug):
    DISCORD_WEBHOOK_URL = os.environ['DISCORD_WEBHOOK_URL']
    payload = {'content': f"New suggestion for CS50P project: {sug}"}
    response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
    return "your suggestion has been " + colored("sent!", "green")
if __name__ == "__main__":
    main()
