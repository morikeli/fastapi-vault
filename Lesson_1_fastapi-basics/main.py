from fastapi import FastAPI, Response
from typing import List, Union
from db.models import Track
from pathlib import Path
import json


app = FastAPI()

BASE_DIR = Path()

data = []

# startup event
@app.on_event('startup')
async def startup_event():
    datapath = BASE_DIR/'data/tracks.json'

    with open(datapath, 'r') as f:
        tracks = json.load(f)

        for track in tracks:
            data.append(Track(**track).dict())


# GET endpoint
@app.get('/tracks/', response_model=List[Track])
def tracks():
    return data

@app.get('/tracks/{track_id}', response_model=Union[Track, str])
def query_track(track_id: int, response: Response):
    # find track with the given ID or None if it does not exist
    track = None
    for track_record in data:
        if track_record['id'] == track_id:
            track = track_record
            break
    
    if track is None:
        response.status_code = 404
        return "Track not found"
    
    return track

# POST endpoint
@app.post('/tracks/', response_model=Track, status_code=201)
def create_track(track: Track):
    track_dict = track.dict()
    track_dict['id'] = max(data, key=lambda x: x['id']).get('id') + 1
    data.append(track_dict)
    
    return track_dict

# PUT endpoint
@app.put('/tracks/{track_id}', response_model=Union[Track, str])
def query_track(track_id: int, response: Response, update_track: Track):
    # find track with the given ID or None if it does not exist
    track = None
    for track_record in data:
        if track_record['id'] == track_id:
            track = track_record
            break
    
    if track is None:
        response.status_code = 404
        return "Track not found"
    
    for key, val in update_track.dict().items():
        if key != 'id':
            track[key] = val

    return track

# DELETE endpoint
@app.delete('/tracks/{track_id}')
def query_track(track_id: int, response: Response):
    # find track with the given ID or None if it does not exist
    track_index = None
    for idx, track_record in enumerate(data):
        if track_record['id'] == track_id:
            track_index = idx
            break
    
    if track_index is None:
        response.status_code = 404
        return "Track not found"

    del data[track_index]
    return Response(status_code=204)
