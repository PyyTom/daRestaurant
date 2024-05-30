import flet as fl,sqlite3
from flet_route import Params,Basket
def Room(page:fl.Page,params:Params,basket:Basket):
    dialog=fl.AlertDialog()
    page.dialog=dialog
    def save(e):
        if t_room.value=='':dialog.title=fl.Text('ROOM NAME NEEDED')
        else:
            db = sqlite3.connect('db.db')
            if d_rooms.value=='NEW':
                db.execute('insert into ROOMS values(?,?)',((t_room.value).upper(),t_tables.value,))
                dialog.title=fl.Text('ROOM CORRECTLY ADDED')
            else:
                db.execute('update ROOMS set TABLES=? where ROOM=?',(t_tables.value,t_room.value,))
                dialog.title=fl.Text('ROOM CORRECTLY UPDATED')
            db.commit()
            db.close()
            refresh()
        dialog.open=True
        page.update()
    def delete(e):
        if t_room.value=='':dialog.title=fl.Text('ROOM NAME NEEDED')
        else:
            db=sqlite3.connect('db.db')
            db.execute('delete from ROOMS where ROOM=?',(t_room.value,))
            db.commit()
            db.close()
            dialog.title=fl.Text('ROOM CORRECTLY DELETED')
            refresh()
        dialog.open=True
        t_room.disabled=True
        page.update()
    def check(e):
        if d_rooms.value=='NEW':t_room.disabled=False
        else:
            t_room.value=d_rooms.value
            db=sqlite3.connect('db.db')
            t_tables.value=db.execute('select TABLES from ROOMS where ROOM=?',(t_room.value,)).fetchone()
            db.close()
            b_delete.disabled=False
        page.update()
    def refresh():
        d_rooms.options=[fl.dropdown.Option('NEW')]
        db=sqlite3.connect('db.db')
        for room in db.execute('select ROOM from ROOMS').fetchall():d_rooms.options.append(fl.dropdown.Option(room[0]))
        db.close()
        t_room.value, t_tables.value = '', 0
        t_room.disabled = True
        b_delete.disabled=True
        page.update()
    d_rooms=fl.Dropdown(label='ROOMS',on_change=check)
    t_room=fl.TextField(disabled=True)
    r_room=fl.Row(controls=[d_rooms,t_room],alignment=fl.MainAxisAlignment.CENTER)
    def minus(e):
        t_tables.value=str(int(t_tables.value)-1)
        page.update()
    def plus(e):
        t_tables.value=str(int(t_tables.value)+1)
        page.update()
    b_minus=fl.IconButton(fl.icons.REMOVE,on_click=minus)
    t_tables=fl.TextField(label='TABLES',read_only=True)
    b_plus=fl.IconButton(fl.icons.ADD,on_click=plus)
    r_table=fl.Row(controls=[b_minus,t_tables,b_plus],alignment=fl.MainAxisAlignment.CENTER)
    b_save=fl.ElevatedButton('SAVE',on_click=save)
    b_delete=fl.ElevatedButton('DELETE',on_click=delete)
    r_buttons=fl.Row(controls=[b_save,b_delete],alignment=fl.MainAxisAlignment.CENTER)
    refresh()
    return fl.View('/',controls=[fl.Row(controls=[fl.IconButton(fl.icons.EXIT_TO_APP_OUTLINED,icon_color='red',icon_size=50,on_click=lambda _:page.go('/home'))],alignment=fl.MainAxisAlignment.END),
                                 fl.Row(controls=[fl.Text('EDIT ROOM',size=50)],alignment=fl.MainAxisAlignment.CENTER),
                                 r_room,r_table,r_buttons])