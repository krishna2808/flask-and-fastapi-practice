from fastapi import Depends, FastAPI, HTTPException, status, Response,  Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from fastapi.responses import HTMLResponse

from forms import Registraion, Login


app = FastAPI()



@app.get('/')
def first_page():
    return {'name : ' 'krishna'}

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse("items.html", {"request": request, "id": id})


@app.get('/login' , response_class=HTMLResponse)
async def login(request: Request):
    message = None 
    form = Login()
    print('form ****************** ', form)
    # if request.method == 'POST':
    #     print(form.user_name.data, form.password.data)
    #     if form.validate_on_submit():
    #         return {'name':  'krishna'}

    return templates.TemplateResponse("login.html", {"request": request, "name": 'krishna', 'form': form})        
    # return render_template('login.html', form=form, message=message )  
            


