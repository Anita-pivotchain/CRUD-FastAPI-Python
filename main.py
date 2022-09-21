

from http import client
from urllib import request
import uvicorn 
from pydantic import BaseModel
from fastapi import FastAPI , Request
from fastapi.responses import JSONResponse
from pymongo import MongoClient
from starlette.requests import Request


client=MongoClient("mongodb://localhost:27017/")
fapidb = client['Employee']
fcoll  = fapidb['Emplo_info']


class Info(BaseModel):
    Employee_id:str
    Employee_name: str
    age: int

app=FastAPI()

@app.post('/create')
def create_name(info:dict):
    print("Method Called:"+str(info))
    # print(data)
    id=fapidb.fcoll.insert_one(info).inserted_id
    print("Information Added"+str(id))
    return{"User created"}
    

    
@app.put('/info')
def read_info(response:JSONResponse,info:dict):
    try:
        # print("method call:"+str(p))
        res = fapidb.fcoll.find_one(info)
        print(res)
        if(res==None):
            response.status_code = 404
            return "Info not found"
        return str(res)
    except Exception as ex:
        print(ex)  
        response.status_code = 404 
        return "Info not found"

        

@app.get('/info/')
def read_all_info(response:JSONResponse):
    try:
        print("method call:"+str(id))
        res = fapidb.fcoll.find({})
        res_list=[]
        for r in res:
           res_list.append(str(r))
            
        if res==None:
            response.status_code=404
            return "Not Found"
    
        return str(res_list)

    except Exception as ex:
        print(ex)  
        response.status_code = 404 
        return "Error Occured"

@app.put('/update/{id}')
def update_info(info:dict,id:int):
    print("method call"+str(id))
    res1=fapidb.fcoll.update_one({"Emp_id":id},{'$set':info},upsert=True)
    # res = fapidb.fcoll.find_one({'Emp_id':id})
    print(res1)
    return "Update success"





@app.put('/update')
def update_info(info:dict):

    
    fapidb.fcoll.update_one(info["condition"],{"$set":info["update"]},upsert=False)
    # fapidb.fcoll.update_one(info[p],{"$set":info},upsert=False)

    # fapidb.fcoll.update_one(p,{"$set":info["update"]},upsert=False)
    # fapidb.fcoll.update_one({},{"$set":info},upsert=False)
    return "Update success"

@app.put('/delete/{id}')
def deleted_info(id:int):
    print("method call"+str(id))
    
    fapidb.fcoll.delete_one({"Emp_id":id})

    return "Deleted "

@app.put('/delete')
def deleted_info(info:dict):
    # print("method call"+str(id))
    
    fapidb.fcoll.delete_one(info)

    return "Deleted "    





if '__name__'=='__main__':
    uvicorn.run(app,port=8000)






















