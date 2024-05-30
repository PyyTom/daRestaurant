import flet as fl,sqlite3,os
from flet_route import Params,Basket
def Meal(page:fl.Page,params:Params,basket:Basket):
    dialog=fl.AlertDialog()
    page.dialog=dialog
    def delete(e):
        if t_image.value=='' or d_meals.value=='' or t_dish.value=='' or t_price.value=='' or t_info.value=='':dialog.title=fl.Text('FIELDS MISSING')
        else:
            db=sqlite3.connect('db.db')
            db.execute('delete from DISHES where DISH=?',(t_dish.value,))
            db.commit()
            db.close()
            dialog.title = fl.Text('DISH CORRECTLY SAVED')
            t_image.value, d_meals.value, d_dishes.value, t_dish.value, t_price.value, t_info.value,b_delete.disabled = '', '', '', '', 0.00, '',True
        dialog.open = True
        page.update()
    def save(e):
        if t_image.value=='' or d_meals.value=='' or t_dish.value=='' or t_price.value=='' or t_info.value=='':dialog.title=fl.Text('FIELDS MISSING')
        else:
            os.rename('dishes/'+d_meals.value+'/'+t_image.value,'dishes/'+d_meals.value+'/'+(t_dish.value).upper()+t_image.value[-4:])
            db=sqlite3.connect('db.db')
            if db.execute('select * from DISHES where DISH=?',(t_dish.value,)).fetchall()==[]:
                db.execute('insert into DISHES values(?,?,?,?)',((d_meals.value).upper(),(t_dish.value).upper(),t_price.value,(t_info.value).upper(),))
            else:db.execute('update DISHES set PRICE=?,INFO=?,DISH=? where DISH=?',(t_price.value,(t_info.value).upper(),d_meals.value,t_dish.value,))
            db.commit()
            db.close()
            dialog.title = fl.Text('DISH CORRECTLY SAVED')
            t_image.value,d_meals.value,d_dishes.value,t_dish.value,t_price.value,t_info.value='','','','',0.00,''
        dialog.open=True
        page.update()
    def pick(e:fl.FilePickerResultEvent):
        t_image.value=e.files[0].name
        page.update()
    def check_dish(e):
        if d_dishes.value=='NEW':t_dish.disabled=False
        else:
            t_dish.value=d_dishes.value
            db=sqlite3.connect('db.db')
            data=db.execute('select * from DISHES where DISH=?',(d_dishes.value,)).fetchone()
            db.close()
            d_meals.value=data[0]
            t_dish.value=data[1]
            t_price.value=data[2]
            t_info.value=data[3]
            b_delete.disabled=False
        page.update()
    def check_meal(e):
        d_dishes.options=[fl.dropdown.Option('NEW')]
        db=sqlite3.connect('db.db')
        for dish in db.execute('select DISH from DISHES where MEAL=?',(d_meals.value,)).fetchall():d_dishes.options.append(fl.dropdown.Option(dish[0]))
        db.close()
        page.update()
    image=fl.FilePicker(on_result=pick)
    b_image=fl.ElevatedButton('CHOOSE IMAGE',on_click=lambda _:image.pick_files(allow_multiple=False))
    t_image=fl.TextField(read_only=True)
    r_image=fl.Row(controls=[image,b_image,t_image])
    d_meals=fl.Dropdown(label='MEALS',options=[fl.dropdown.Option(meal) for meal in next(os.walk('dishes'))[1]],on_change=check_meal)
    r_meal=fl.Row(controls=[d_meals],alignment=fl.MainAxisAlignment.CENTER)
    d_dishes=fl.Dropdown(label='DISHES',options=[fl.dropdown.Option('NEW')],on_change=check_dish)
    t_dish=fl.TextField(label='DISH',disabled=True)
    r_dish=fl.Row(controls=[d_dishes,t_dish])
    def minus(e):
        t_price.value=str(float(t_price.value)-0.50)
        page.update()
    def plus(e):
        t_price.value=str(float(t_price.value)+0.50)
        page.update()
    b_minus=fl.IconButton(fl.icons.REMOVE,on_click=minus)
    t_price=fl.TextField(label='PRICE $',value='0.00')
    b_plus=fl.IconButton(fl.icons.ADD,on_click=plus)
    r_price=fl.Row(controls=[b_minus,t_price,b_plus],alignment=fl.MainAxisAlignment.CENTER)
    t_info=fl.TextField(label='INFO',width=600)
    b_delete=fl.ElevatedButton('DELETE',on_click=delete,disabled=True)
    column=fl.Column(controls=[fl.Row(controls=[fl.Text('EDIT MEAL',size=50)],alignment=fl.MainAxisAlignment.CENTER),
                               r_image,r_meal,r_dish,r_price,t_info,
                               fl.Row(controls=[fl.ElevatedButton('SAVE',on_click=save),b_delete],alignment=fl.MainAxisAlignment.CENTER)])
    return fl.View('/',controls=[fl.Row(controls=[fl.IconButton(icon=fl.icons.EXIT_TO_APP_OUTLINED,icon_size=50,icon_color='red',on_click=lambda _:page.go('/home'))],alignment=fl.MainAxisAlignment.END),
                                 fl.Row(controls=[column],alignment=fl.MainAxisAlignment.CENTER)])