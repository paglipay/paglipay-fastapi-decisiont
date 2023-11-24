from fastapi import FastAPI
from fastapi.params import Body
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings

from .utils import DecisionTree
import json
import uuid
import threading

# models.Base.metadata.create_all(bind=engine)

flask_process_data = {"OLD_TEXT": ""}
flask_process = {}
import_obj_instance_hash = {}

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return {"message": "Hello World pushing out to ubuntu"}

@app.get('/show/{hash}')
def show(hash):
    return flask_process_data[hash]


@app.post('/start/{hash}')
def start(hash, data: dict = Body(...)):
    d = {}
    name = hash
    # data = request.get_json()
    print('data: ', data)
    if 'jobs' in data:
        name = data.pop('jobs')
    d = data
    if hash in flask_process_data:
        flask_process_data[hash].update(d)
        import_obj_instance = import_obj_instance_hash[hash]

    else:
        print('NEW HASH: ', hash)
        flask_process_data[hash] = d
        import_obj_instance_hash[hash] = {}
        import_obj_instance = import_obj_instance_hash[hash]

    d = flask_process_data[hash]

    # name = 'start.json'

    thread = threading.Thread(
        target=do_process, args=(d, name, import_obj_instance,))
    flask_process[hash] = thread
    thread.daemon = False
    thread.start()
    thread.join()
    
    if not 'uuid' in hash:
        d['uuid'] = hash
    
    # return {"message": f"HI {hash}", "data": flask_process_data[hash]}
    return d


def do_process(flask_data, json_file, module_instances):
    if ".json" in json_file:
        c = DecisionTree.DecisionTree(
            json.load(open(json_file)),
            tree_name=json_file,
            module_instances=module_instances,
            data=flask_data,
        )
    else:
        c = DecisionTree.DecisionTree(
            json_file,
            tree_name=uuid.uuid1(),
            module_instances=module_instances,
            data=flask_data,
        )
        
def thread_process(data):
    pass
