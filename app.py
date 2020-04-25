from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
import db

app = FastAPI(debug=True)

class Location(BaseModel):
	key: str
	place: str
	admin: str
	lat: float
	lon: float

@app.post('/post_location/')
async def create_location(location: Location):
	res = db.insert(location.key, location. place, location.admin, location.lat, location.lon)
	return res
#{"key":"IN/000000","place":"test","admin": "adm","lat" : 38.889069444444,"lon": -77.034502777778}

@app.get('/get_location/')
async def get_location(lat: str, long: str):
	res = db.find(lat, long)
	return res

if __name__ == '__main__':
	uvicorn.run(app, host="127.0.0.1", port="8000")

