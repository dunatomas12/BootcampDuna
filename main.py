from fastapi import Body, FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

error404 = str("The kid is not registered in Santa's list :(")

class Kid(BaseModel):
    name: str
    age: float
    description: str | None = Field(
        default=None, title="Brief description of the child", max_length=300
    )
    behaviour: int | None = Field( description="The behaviour must be an integer in the scale of 0 to 10")

    class Config:
        schema_extra = {
            "example": {
                "name": "Luigi",
                "age": 8,
                "description": "Its a me, Mariooo",
                "behaviour": 7,
            }
        }

SantaList = {
    "Joanet" : {"name" : "Joanet", "age": 6, "description" : "He sticks his chewing gum under the tables in class", "behaviour" : 3},
    "Laura" : {"name" : "Laura", "age": 11, "description" : "She helps with house duties, but she doesn't pay attention sometimes", "behaviour" : 7},
    "Tina" : {"name" : "Tina", "age": 8, "description" : "She is very nice with her grandma", "behaviour" : 10},
}

@app.get("/")
async def read_main():
    return {"message": "Welcome to Santa's List! Add your kids' name, and let Santa know if they should recieve any presents"}

@app.get("/kids/")
async def read_kids():
    return SantaList #returns all kids in Santa's List

@app.get("/kids/{name}")
async def read_kid(name: str):
    if name not in SantaList:
        raise HTTPException(status_code=404, detail=error404)
    return SantaList.get(name) # returns a specific kid in  Santa's List

@app.post("/kids/")
async def create_kid(kid: Kid):
    SantaList[len(SantaList) + 1] = kid #adds a new kid to Santa's list
    return kid

@app.put("/kids/{name}")
async def update_kid(name: str, kid: Kid):
    if name not in SantaList:
        raise HTTPException(status_code=404, detail=error404)
    SantaList[name] = kid #updates an existing kid in Santa's List
    return kid

@app.delete("/kids/{name}")
async def delete_kid(name: str):
    if name not in SantaList:
        raise HTTPException(status_code=404, detail=error404)
    return SantaList.pop(name) #deletes an existing kid in Santa's List
