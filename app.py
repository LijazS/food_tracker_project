from fastapi import FastAPI,Form, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Annotated
from database import get_db
import sqlite3
from datetime import date

class Food(BaseModel):
    name: str
    calories: int
    catagory: str
    date1: date
    


app = FastAPI()
templates = Jinja2Templates(directory="templates")



@app.get('/',response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request=request,
                                      name='home.html',
                                      context={"name":"Liijazz"})


@app.post('/add_food',response_class=HTMLResponse)
async def add_food(request: Request,data: Annotated[Food, Form()], db = Depends(get_db)):
    try:
        print(data.name,data.calories,data.catagory,data.date1)
        rows = db.execute("""
        INSERT INTO food_tab (name,calories,catagory,date1) VALUES (?,?,?,?)
                        """, (data.name,data.calories,data.catagory,data.date1))
        db.commit()
    except Exception:
        print(Exception)
        return "couldnt add data " 
    
    return templates.TemplateResponse(request=request,
                                      name='home.html',
                                      context={"name":"Liijazz","data":"Added your food successfully"})


@app.get('/food_page',response_class=HTMLResponse)
def get_food(request:Request, db = Depends(get_db)):
    
    
    return templates.TemplateResponse(request=request,
                                      name='foods.html',
                                      context={"name":"Liijazz"})


@app.post('/get_food',response_class=HTMLResponse)
def get_food(request:Request, d: date = Form(...),db = Depends(get_db)):
    try:
        rows = db.execute("""
        SELECT * FROM food_tab WHERE date1 = ?
                        """,(d.isoformat(),)).fetchall()
        foods = [dict(r) for r in rows]
        sums = sum(f["calories"] for f in foods)
    except Exception as e:
        print("DB error:", repr(e))
        return {"error": str(e)}
    
    return templates.TemplateResponse(request=request,
                                      name='foodsPage.html',
                                      context={"name":"Liijazz","foods":foods,"total":sums,"date":d.isoformat()})
    

