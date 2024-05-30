import datetime,sqlite3,flet as fl,os
from flet_route import Params,Basket
def Home(page:fl.Page,params:Params,basket:Basket):
    dialog=fl.AlertDialog()
    page.dialog=dialog
    def tables(e):
        d_tables.disabled=False
        db=sqlite3.connect('db.db')
        d_tables.options=[fl.dropdown.Option(str(table)) for table in range(1,db.execute('select TABLES from ROOMS where ROOM=?',(d_rooms.value,)).fetchone()[0]+1)]
        db.close()
        page.update()
    def populate(e):
        def info(e):
            dialog.title = fl.Text(e)
            dialog.open=True
            page.update()
        def remove(e):
            c_bill.controls.remove(e.control)
            t_bill.value = float(t_bill.value) - float(e[2])
            page.update()
        def add(e):
            if d_rooms.value==None or d_tables.value==None:
                dialog.title=fl.Text('ROOM A/O TABLE MISSING')
                dialog.open=True
                page.update()
            else:
                c_bill.controls.append(fl.TextButton(e[1]+' - '+e[2],on_click=remove))
                t_bill.value=float(t_bill.value)+float(e[2])
                page.update()
                db=sqlite3.connect('db.db')
                if db.execute('select DISH from OPEN where ROOM=? and N_TABLE=? and DISH=?',(d_rooms.value,d_tables.value,e[1],)).fetchone()==None:
                    db.execute('insert into OPEN values(?,?,?,?,?,?,?)',(t_user.value,d_rooms.value,d_tables.value,t_time.value,e[1],1,e[2],))
                else:db.execute('update OPEN set Q=Q+1,PRICE=PRICE+? where ROOM=? and N_TABLE=? and DISH=?',(e[2],d_rooms.value,d_tables.value,e[1],))
                db.commit()
                db.close()
        c_selected.controls.clear()
        db = sqlite3.connect('db.db')
        for dish in os.listdir('dishes/'+rg_meals.value):
            if dish!='.DS_Store':
                data=db.execute('select * from DISHES where DISH=?',(dish[:-4],)).fetchone()
                c_selected.controls.append(fl.Container(bgcolor=fl.colors.AMBER_50,on_click=lambda x,e=data:add(e),content=fl.Row(controls=[
                                                            fl.Text(data[1],width=200,size=30),
                                                            fl.Image(src='/'+data[0]+'/'+dish,width=100,height=100),
                                                            fl.Text('$. '+data[2],size=30),
                                                            fl.ElevatedButton('INFO',on_click=lambda x,e=data[3]:info(e))])))
        db.close()
        page.update()
    def bill(e):
        if d_rooms.value == None or d_tables.value == None:
            dialog.title = fl.Text('ROOM A/O TABLE MISSING')
            dialog.open = True
            page.update()
        else:
            db=sqlite3.connect('db.db')
            tot=db.execute('select sum(PRICE) from OPEN where ROOM=? and N_TABLE=?',(d_rooms.value,d_tables.value,)).fetchone()
            db.execute('insert into BILLS values(?,?,?,?,?)',(t_user.value,d_rooms.value,d_tables.value,t_time.value,tot[0]))
            db.commit()
            db.execute('delete from OPEN where ROOM=? and N_TABLE=?',(d_rooms.value,d_tables.value,))
            db.commit()
            db.close()
    r_intro=fl.Row(controls=[fl.Image(src='/Users/tommylatorre/Applications/lab/daRestaurant-Python,Flet,Sqlite3/images/banner.png',width=300,height=100),
                              fl.Image(src='/Users/tommylatorre/Applications/lab/daRestaurant-Python,Flet,Sqlite3/images/logo.png',width=50,height=50)],
                   alignment=fl.MainAxisAlignment.CENTER)
    r_buttons=fl.Row(controls=[fl.ElevatedButton('EDIT DISH',on_click=lambda _:page.go('/meal')),
                               fl.ElevatedButton('EDIT ROOM',on_click=lambda _:page.go('/room'))],alignment=fl.MainAxisAlignment.CENTER)
    db=sqlite3.connect('db.db')
    d_rooms=fl.Dropdown(label='ROOM',options=[fl.dropdown.Option(room[0]) for room in db.execute('select ROOM from ROOMS').fetchall()],on_change=tables)
    d_tables=fl.Dropdown(label='TABLE',disabled=True)
    t_user=fl.Text(db.execute('select USER from USERS where PW="CURRENT"').fetchone()[0])
    db.close()
    t_time=fl.Text(datetime.datetime.now().strftime('%m/%d,%Y - %H:%M'))
    r_header=fl.Row(controls=[d_rooms,d_tables,t_user,t_time],alignment=fl.MainAxisAlignment.CENTER)
    r_titles=fl.Row(controls=[fl.Text('MEALS',size=30,width=500),fl.Text('DISHES',size=30,width=600),fl.Text('BILL',size=30)])
    rg_meals=fl.RadioGroup(content=fl.Column([fl.Radio(value=meal,label=meal) for meal in next(os.walk('dishes'))[1]]),on_change=populate)
    c_meals=fl.Column(controls=[rg_meals],width=400,height=450)
    c_selected=fl.Column(scroll=fl.ScrollMode.ALWAYS,width=600,height=450)
    c_bill=fl.Column(height=450,width=400)
    r_body=fl.Row(controls=[c_meals,c_selected,c_bill])
    t_bill=fl.Text('0.00',size=50)
    return fl.View('/',controls=[r_intro,
                                 fl.Row(controls=[fl.IconButton(icon=fl.icons.EXIT_TO_APP_OUTLINED,icon_color='red',icon_size=50,on_click=lambda _:page.go('/'))],alignment=fl.MainAxisAlignment.END),
                                 r_buttons,r_header,r_titles,r_body,
                                 fl.Row(controls=[fl.Text('TOTAL: $. ',size=50),t_bill,fl.ElevatedButton('BILL',on_click=bill)],alignment=fl.MainAxisAlignment.END)])