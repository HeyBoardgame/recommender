from fastapi import FastAPI

app = FastAPI()


@app.get('/recommends')
async def recommend_to_single():
    return {'message': 'recommend to single user'}


@app.get('/recommends/group')
async def recommend_to_group():
    return {'message': 'recommend to group'}
