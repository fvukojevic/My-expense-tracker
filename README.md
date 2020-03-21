# My Expense Tracker

Small App created using Python in the backoffice and Vue.js on the front side that helps you track your expenses. App stores new expenses with current date inside Mysql table. 

There is no login/register, it is using the the google api to automatically login user and use his token for his expenses.

You can sort your expenses by categories or add custom categories and use those. 

You also have a preview or an overview page where you can see all your expenses/expenses from a date..to a date.. and stuff like that. And you also always have an option to download/export expenses inside the xlsx file and that get's downloaded for you.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

## Prerequisites

- docker v17.03+ ([installation instructions](https://confluence.votum.info:9443/display/DEV/Docker#Docker-Installdocker))
- docker-compose v1.13+ ([installation instructions](https://confluence.votum.info:9443/display/DEV/Docker#Docker-Installdocker-compose))
- Python version >= 3.0
- Create an google client id and connect your app to it. My app is running on localhost:8080 and enabling that port makes app only accessible from it. Without your google client id and port setup the app will not work.

Good package and documentation on the last point: https://www.npmjs.com/package/vue-google-login

## Setup

In Docker Preferences/FileSharing put the directory you copied the project into as path. Once that is done inisde the terminal get inside the folder. Running `make clean && make setup` will start your application. Other make command you can easily see inside the Makefile, and exactly what they do.

Python part is still not dockerized, will probably get around it next week. As of now, once the frontend and mysql db are running on docker, just get inside main.py file and run it. Should get things started for you

## Authors

* **Ferdo Vukojević** - *Initial work* - [fvukojevic](https://github.com/fvukojevic)

## Images from the app

![Alt text](https://github.com/fvukojevic/My-expense-tracker/blob/master/images/sign_in.png "Sign in")

![Alt text](https://github.com/fvukojevic/My-expense-tracker/blob/master/images/main.png "Main panel")

![Alt text](https://github.com/fvukojevic/My-expense-tracker/blob/master/images/expenses.png "Expenses panel")

![Alt text](https://github.com/fvukojevic/My-expense-tracker/blob/master/images/excel.png "Excel")


