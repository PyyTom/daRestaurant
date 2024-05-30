import sqlite3,flet as fl
from flet_route import Params,Basket
def User(page:fl.Page,params:Params,basket:Basket):
    dialog=fl.AlertDialog()
    page.dialog=dialog
    def clear():
        t_new_user.value=''
        t_new_user.disabled=True
        t_pw.value=''
        t_pw.disabled=True
        t_re_pw.value=''
        t_re_pw.disabled=True
        b_save.disabled=True
        b_delete.disabled=True
    def add(e):
        if t_new_user.value=='' or t_pw.value=='' or t_re_pw.value=='':
            dialog.title=fl.Text('FIELDS REQUIRED')
            dialog.open=True
        else:
            if t_pw.value==t_re_pw.value:
                db=sqlite3.connect('db.db')
                db.execute('insert into USERS values(?,?)',((t_new_user.value).upper(),t_pw.value,))
                db.commit()
                db.close()
                dialog.title=fl.Text('USER CORRECTLY ADDED')
                dialog.open=True
                clear()
            else:
                dialog.title=fl.Text('PASSWORDS NOT MATCHING')
                dialog.open=True
        page.update()
    def delete(e):
        if d_users.value=='NEW':
            dialog.title=fl.Text('USER NOT EXISTING')
            dialog.open=True
        else:
            db=sqlite3.connect('db.db')
            db.execute('delete from USERS where USER=?',(d_users.value,))
            db.commit()
            db.close()
            dialog.title=fl.Text('USER CORRECTLY DELETED')
            dialog.open=True
            clear()
        page.update()
    def check_user(e):
        if d_users.value=='NEW':
            t_new_user.disabled=False
            t_pw.disabled=False
            t_re_pw.disabled=False
            b_save.disabled=False
            t_new_user.focus=True
        else:
            t_new_user.disabled=True
            b_save.disabled=True
            b_delete.disabled=False
        page.update()
    t_new_user=fl.TextField(disabled=True)
    d_users=fl.Dropdown(label='USER',options=[fl.dropdown.Option('NEW')],on_change=check_user)
    db=sqlite3.connect('db.db')
    if db.execute('select count(*) from USERS').fetchone()[0]!=0:
        for user in db.execute('select USER from USERS where PW!="CURRENT"').fetchall():d_users.options.append(fl.dropdown.Option(user[0]))
    db.close()
    c_user=fl.Column(controls=[d_users,t_new_user])
    t_pw=fl.TextField(label='PASSWORD',password=True,can_reveal_password=True,disabled=True)
    t_re_pw=fl.TextField(label='CONFIRM PASSWORD',password=True,can_reveal_password=True,disabled=True)
    c_pw=fl.Column(controls=[t_pw,t_re_pw])
    r_data=fl.Row(controls=[c_user,c_pw],alignment=fl.MainAxisAlignment.CENTER)
    b_save=fl.ElevatedButton('SAVE',on_click=add,disabled=True)
    b_delete=fl.ElevatedButton('DELETE',on_click=delete,disabled=True)
    r_buttons=fl.Row(controls=[b_save,b_delete],alignment=fl.MainAxisAlignment.CENTER)
    return fl.View('/',controls=[fl.Row(controls=[fl.IconButton(on_click=lambda _:page.go('/'),icon=fl.icons.EXIT_TO_APP_OUTLINED,icon_size=50,icon_color='red')],alignment=fl.MainAxisAlignment.END),
                                 fl.Row(controls=[fl.Text('ADD/DELETE USER',size=50)],alignment=fl.MainAxisAlignment.CENTER),
                                 r_data,r_buttons])