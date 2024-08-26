import os
import json
from db.mongodb import MongoDB
from dotenv import load_dotenv
from bson.objectid import ObjectId
from fastapi import FastAPI, Request ,HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

load_dotenv()

cluster= os.getenv("APP_NAME")
host = os.getenv("HOST")
user = os.getenv("MONGO_USERNAME")
password = os.getenv("MONGO_PASSWORD")
db_name = os.getenv("DB")
uri = os.getenv("URI")

uri = uri.format(
    user=user,
    password=password,
    host=host,
    cluster=cluster
)

collection_name = 'my_todolist'
mongo = MongoDB(uri, db_name)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def root(request: Request):
    data = list(mongo.find(collection_name,) )
    return templates.TemplateResponse("todolist.html",{"request":request,"tododict":data})


@app.get("/migrate")
async def migrate(request: Request):

    db_name = 'todo_list_db'
    collection_name = 'my_todolist'
    mongo = MongoDB(uri, db_name)

    try:
        with open('database.json') as f:
            data = json.load(f)
            for id, todo in data.items():
                document = {"id":int(id),"todo":todo}                
                mongo.insert(collection_name, document )
                print(f'document {document} LOADED')

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return RedirectResponse("/", 303)

@app.post("/add")
async def add_todo(request: Request):
    formdata = await request.form()
    
    maxid = mongo.db[collection_name].aggregate( [{"$group": {"_id": None, "maxId": { "$max": "$id" } } }])

    maxid_list = list(maxid) 
    if maxid_list:
        new_id = maxid_list[0]['maxId'] + 1
    else:
        new_id = 0

    document = {"id":int(new_id),"todo":formdata["newtodo"]}
    mongo.insert(collection_name,document)

    return RedirectResponse("/", 303)

@app.get("/api/hello")
def hello_world():
    return {'hello':'world'}



@app.get("/delete/{id}")
async def delete_todo(request: Request, id: str):
    mongo.delete(collection_name,{"_id":ObjectId(id)})
    return RedirectResponse("/", 303)