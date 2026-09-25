from nicegui import ui,app
from views.login import login
from  views.chats import chats

#vista login
@ui.page('/')
def page_login():
    login()

#vista chats
@ui.page('/chats')
def page_chats():
    if not app.storage.user.get('authenticated',False):
        ui.navigate.to('/')
        return
    
    chats(app.storage.user['user_id'])



ui.run(storage_secret='a34c56sd78v9df0bdfbs4v5s6d7')