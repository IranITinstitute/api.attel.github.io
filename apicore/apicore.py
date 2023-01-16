from typing import Union
from fastapi import FastAPI, Form
from apihandler import qr_login, qr_confirm, db_list, static_login, account_logout
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse

app = FastAPI()


# загружаем страницу логина в зависимости от способа входа

@app.get("/api/login/", response_class=HTMLResponse)
async def login_page(q: Union[str, None] = None):


# для обычного логин пароль

    if q == None or q == 'static':
        html_content = """
        <html>
            <head>
                <title>Login page</title>
            </head>
            <body>
                <h1>Enter ID</h1>
                <input>ID</input>
                <button href="">Send</button>
            </body>
        </html>
        """

# для входа по qr коду

    if q == 'qr':
        html_content = """
        <html>
            <head>
                <title>Login page</title>
            </head>
            <body>
            <form>
                <h1>Enter ID</h1>
                <input>ID</input>
                <button href="">SendQR</button>
            </form>
            </body>
        </html>
        """
    return HTMLResponse(content=html_content, status_code=200)

# если статик то обычный вход если qr то редирект на страницу с кодом

@app.get("/api/logon/{id}", response_class=RedirectResponse)
async def login(id: int, q: Union[str, None] = None):

    if q == None or q == 'static':
        static_login(id)
        ret = f"http://127.0.0.1:42069/api/account/{id}"

    if q == 'qr':
        
        qrhash = qr_login(id)
        ret = f"http://127.0.0.1:42069/api/logon/{id}/confirm?q={qrhash}"
        
    return RedirectResponse(ret)


# страница ожидания активации кода

@app.get("/api/logon/{id}/confirm", response_class=HTMLResponse)
async def confirm(id: int, q: Union[str, None] = None):

    q = qr_login(id)
    html_content = f"""
    <html>
        <head>
            <title>Login page</title>
        </head>
        <body>
            <h1>Waiting id {id} QR code confirmation</h1>
            <img src='data:image/jpeg;base64,{q}'>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


# ссылка и потдвертждение с телефона

@app.get("/api/logon/{id}/confirm/QR", response_class=RedirectResponse)   
async def confirmQRcode(id: int, q: Union[str, None] = None):
    if q == 'confirmation':
        
        status = qr_confirm(id, q)

        if status == 'confirmed':
        
            return RedirectResponse(f"http://127.0.0.1:42069/api/account/{id}")

    
# страница аккаунта после удачного входа

@app.get("/api/account/{id}")
async def account_page(id: int):
    html_content = f"""
        <html>
            <head>
                <title>Account</title>
            </head>
            <body>
                <h1>Hello, {id} id!<h1>
                <button href="http://127.0.0.1:42069/api/account/logout/6">logout</button>
            </body>
        </html>
        """
    return HTMLResponse(content=html_content, status_code=200)


# страница с данными логина пользователей

@app.get("/api/db")
async def get_db():
    return db_list()


# логаут функция

@app.get("/api/account/logout/{id}", response_class=RedirectResponse)
async def logout(id: int):
    account_logout(id)
    return RedirectResponse("http://127.0.0.1:42069/api/login/")

