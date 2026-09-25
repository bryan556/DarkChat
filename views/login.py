from nicegui import ui,app
import sqlite3

##########
# Designer
##########

#vista login
def login():
    with ui.row().style('height: 100vh').classes('items-center justify-center'):   
        with ui.card().classes('bg- text-white').style('background-color: #141C33 ;'):
            with ui.row().style('justify-content: flex-start; align-items: center;'):
                ui.image('./static/img/logo.png').classes('w-50 items-start')
                with ui.column():
                    user= ui.input(placeholder='UserName').classes('bg-gray-800 rounded-lg [&_.q-field__native]:text-white')
                    paswword=ui.input('Password',password=True).classes('bg-gray-800 rounded-lg [&_.q-field__native]:text-white')
                    ui.button('Login',on_click=lambda:login_user(user.value, paswword.value))

"""
Logica de login

"""
#funcion para comprobar el inicio de sesion de un usuario
def login_user(user,password):
    conection = sqlite3.Connection('db.sqlite3')
    cursor = conection.cursor()

    cursor.execute('SELECT * FROM users WHERE user= ? AND password= ?',(user,password))

    usuario = cursor.fetchone()
    conection.close()

    if usuario :
        app.storage.user['authenticated'] = True
        app.storage.user['user_id'] = usuario[0]
        ui.notify('Login Correcto')
        ui.navigate.to('/chats')

    else:
        ui.notify('Error al inicio de sesion')        
