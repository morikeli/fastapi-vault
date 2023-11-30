from fastapi import FastAPI, Response, Depends
from sqlmodel import Session, select
from db.models import TrackModel
from db.database import engine
from typing import List, Union
from pathlib import Path
import json


app = FastAPI()

BASE_DIR = Path()

data = []

# create fastAPI dependency
def get_session():
    with Session(engine) as session: yield session


# startup event
@app.on_event('startup')
async def startup_event():
    DATA_FILE = BASE_DIR/'data/tracks.json'

    session = Session(engine)

    # check if db is already populated -> this is done to avoid duplicates
    stmt = select(TrackModel)
    result = session.exec(stmt).first() # get the first row

    # load data from json file
    if result is None:
        with open(DATA_FILE, 'r') as f:
            tracks = json.load(f)

            for track in tracks:
                session.add(TrackModel(**track))
        
        session.commit()    # commit changes

    session.close()


# GET endpoint
@app.get('/tracks/', response_model=List[TrackModel])
def tracks(session: Session = Depends(get_session)):
    # use context manager to create session - check startup_event() to see the difference
    stmt = select(TrackModel)
    result = session.exec(stmt).all()
    
    return result

@app.get('/tracks/{track_id}', response_model=Union[TrackModel, str])
def query_track(track_id: int, response: Response, session: Session = Depends(get_session)):
    # find track with the given ID or None if it does not exist
    
    track = session.get(TrackModel, track_id)
    
    if track is None:
        response.status_code = 404
        return "Track not found"
        
    return track

# POST endpoint
@app.post('/tracks/', response_model=TrackModel, status_code=201)
def create_track(track: TrackModel, session: Session = Depends(get_session)):
    session.add(track)
    session.commit()
    session.refresh(track)

    return track

# PUT endpoint
@app.put('/tracks/{track_id}', response_model=Union[TrackModel, str])
def query_track(track_id: int, response: Response, update_track: TrackModel, session: Session = Depends(get_session)):
    # find track with the given ID or None if it does not exist
    track = session.get(TrackModel, track_id)

    if track is None:
        response.status_code = 404
        return "Track not found"
    
    # update track data
    track_dict = update_track.dict(exclude_unset=True)  # "exclude_unset=True" excludes id when updating track
    for key, val in track_dict.items():
        setattr(track, key, val)

    session.add(track)
    session.commit()
    session.refresh(track)
    return track

# DELETE endpoint
@app.delete('/tracks/{track_id}')
def query_track(track_id: int, response: Response, session: Session = Depends(get_session)):
    # find track with the given ID or None if it does not exist
    track = session.get(TrackModel, track_id)
    
    if track is None:
        response.status_code = 404
        return "Track not found"

    session.delete(track)
    session.commit()
    return Response(status_code=204)
