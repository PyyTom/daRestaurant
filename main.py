import sqlite3,flet as fl
db=sqlite3.connect('db.db')
db.execute('create table if not exists USERS(USER,PW)')
db.execute('create table if not exists ROOMS(ROOM,TABLES integer)')
db.execute('create table if not exists DISHES(MEAL,DISH,PRICE,INFO)')
db.execute('create table if not exists OPEN(USER,ROOM,N_TABLE integer,TIME,DISH,Q integer,PRICE float)')
db.execute('create table if not exists BILLS(USER,ROOM,N_TABLE integer,TIME,BILL)')
db.close()
from flet_route import Routing,path
from pages.login import Login
from pages.home import Home
from pages.user import User
from pages.meal import Meal
from pages.room import Room
def main(page:fl.Page):
    page.window_full_screen=True
    page.theme_mode='light'
    app_routes=[path(url='/',view=Login,clear=True),
                path(url='/home',view=Home,clear=True),
                path(url='/user', view=User, clear=True),
                path(url='/meal',view=Meal,clear=True),
                path(url='/room',view=Room,clear=True)]
    Routing(page=page,app_routes=app_routes)
    page.go(page.route)
fl.app(target=main,assets_dir='dishes')