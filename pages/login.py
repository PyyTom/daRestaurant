import sqlite3,flet as fl
from flet_route import Params,Basket
def Login(page:fl.Page,params:Params,basket:Basket):
    def check(e):
        db=sqlite3.connect('db.db')
        if db.execute('select * from USERS where USER=? and PW=?',(d_user.value,pw.value,)).fetchall()!=[]:
            db.execute('insert into USERS values(?,?)',(d_user.value,'CURRENT'))
            db.commit()
            page.go('/home')
        else:
            dlg = fl.AlertDialog(title=fl.Text('USERNAME A/O PASSWORD WRONG/S'))
            page.dialog = dlg
            dlg.open=True
            page.update()
        db.close()
    db=sqlite3.connect('db.db')
    db.execute('delete from USERS where PW="CURRENT"')
    db.commit()
    d_user=fl.Dropdown(label='USER',options=[fl.dropdown.Option(u[0]) for u in db.execute('select USER from USERS').fetchall()])
    db.close()
    pw=fl.TextField(label='PASSWORD',password=True,can_reveal_password=True)
    r_buttons=fl.Row(controls=[fl.ElevatedButton('LOGIN', on_click=check),
                               fl.ElevatedButton('EDIT USERS', on_click=lambda _: page.go('/user'))])
    column=fl.Column(controls=[fl.Text('LOGIN',size=50),d_user,pw,r_buttons])
    return fl.View('/',controls=[fl.Row(controls=[fl.IconButton(icon=fl.icons.EXIT_TO_APP_SHARP,icon_size=50,icon_color='red', on_click=lambda _:page.window_destroy())],alignment=fl.MainAxisAlignment.END),
                                 fl.Row(controls=[column],alignment=fl.MainAxisAlignment.CENTER)])