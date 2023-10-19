from fastapi import FastAPI

app=FastAPI()

@app.get("/")
def home():
    return {"Data": "Test"}

@app.get("/about")
def about():
    return {"Data": "This page shows general information about the webservice"}