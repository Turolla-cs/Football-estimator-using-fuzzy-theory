from fastapi import FastAPI

back = FastAPI()

@back.get("/")
async def team_data(name: str):
    return 
