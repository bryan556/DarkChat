from nicegui import ui
import sqlite3

###########
#Designer 
#############

#Vista de chats
def chats(user_actual):
    #quitar todos los espacios
    ui.query('.nicegui-content').classes('p-0') 
    #cabecera
    with ui.header():
        ui.label('DarkChat')
        ui.space()
        ui.label('Mario')
        ui.button(icon='menu')
    #contenedor entre ambos
    with ui.row().classes('w-full h-[calc(100vh-64px)] gap-0'):

        #Dialog Card Contacts
        with ui.dialog() as dialog:

            with ui.card():
                ui.label('Add Contact')
                contact_id=ui.input('User ID')
                with ui.row():
                    ui.button('ADD',on_click=lambda:add_contact(user_actual,contact_id.value))
                    ui.button('CANCEL',on_click=dialog.close)      

        #contenedor izquierdo
        with ui.column().classes('bg-blue text-black font-bold h-full w-50'):
            with ui.row().classes('w-full items-center'):
                ui.label('Contacts')
                ui.space()
                ui.button(icon='add',on_click=dialog.open).props('round')

            #Mostrar todos los contactos
            with ui.list():
                contactos = list_contacts(user_actual)
                for contact in contactos:
                    with ui.item():
                        ui.label(contact[1])

                        
        #contenedor derecho
        with ui.column().classes('bg-green text-black font-bold h-full flex-1'):
            ui.label('Chat')

            ui.space()

            #contenedor derecho abajo envio-mensaje
            with ui.row().classes('w-full h-28 items-center gap-2'):
                ui.input(placeholder='Escribe un mensaje...') \
                    .props('borderless') \
                    .classes('bg-white text-black rounded-xl h-12 flex-1')

                ui.button(icon='send').props('round')


"""
Logica para vista de chats
"""

#Funcion y vista para agregar un contacto
def add_contact(user_actual, contact_id):

    if not contact_id:
        ui.notify('Ingrese un ID')
        return
    #conexion a sqlite
    conection = sqlite3.connect('db.sqlite3')
    cursor = conection.cursor()

    cursor.execute(
        'SELECT id, user FROM users WHERE id = ?',
        (contact_id,)
    )

    contacto = cursor.fetchone()

    #verificar que existe
    if not contacto:
        ui.notify('El usuario no existe')
        conection.close()
        return
    #validacion para no agregarse asi mismo
    if contacto[0] == user_actual:
        ui.notify('No puedes agregarte a ti mismo')
        conection.close()
        return

    cursor.execute(
        'SELECT * FROM contacts WHERE user_id = ? AND contact_id = ?',
        (user_actual, contacto[0])
    )

    existe = cursor.fetchone()
    #verificar que si el contacto ya esta agregado
    if existe:
        ui.notify('El contacto ya existe')
        conection.close()
        return
    #Asociar el contacto nuevo con el usuario actual
    cursor.execute(
        'INSERT INTO contacts (user_id, contact_id) VALUES (?, ?)',
        (user_actual, contacto[0])
    )

    conection.commit()
    conection.close()
    ui.notify(f'{contacto[1]} agregado correctamente')
    ui.navigate.reload()

def list_contacts(user_actual):
    conection = sqlite3.connect('db.sqlite3')
    cursor = conection.cursor()

    contacts = cursor.execute("""SELECT users.id, users.user FROM contacts
                                JOIN users ON contacts.contact_id = users.id
                                WHERE contacts.user_id = ?""",(user_actual,)).fetchall()
    conection.close()
    return contacts
    