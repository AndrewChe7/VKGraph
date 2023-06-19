
import vk_api
import json
from flask import Flask, Response
from tqdm import tqdm

app = Flask(__name__)

TOKEN = ''
session = vk_api.VkApi(token=TOKEN)

vkses = session.get_api()
how_deep = 1
user_ids = set()
friends_checked = set()
users = []
links = []

def get_user (user_id):
    try:
        return vkses.users.get(user_ids=user_id)[0]
    except Exception:
        return None

def get_friends (user_id):
    try:
        return vkses.friends.get(user_id=user_id)['items']
    except Exception:
        return []

def add_user (user):
    users.append({'id' : user['id'], 'name' : (user['first_name'] + ' ' + user['last_name'])})

def make_links ():
    for i in tqdm(range(len(users))):
        friends = get_friends(users[i]['id'])
        for j in range(i):
            if users[j]['id'] in friends:
                links.append({
                    'source' : users[i]['id'], 
                    'target' : users[j]['id'], 
                    'value' : 1
                    })

def export (): 
    with open('../Viewer/users.json', 'w') as f:
        f.write(json.dumps({
            'nodes' : users,
            'links' : links
            }))

@app.route('/')
@app.route('/Viewer.html')
def index():
    with open('../Viewer/Viewer.html') as f:
        return Response(f.read(), mimetype='text/html')

@app.route('/controls.js')
def controls():
    with open('../Viewer/controls.js') as f:
        return Response(f.read(), mimetype='text/javascript')
    
@app.route('/render.js')
def render():
    with open('../Viewer/render.js') as f:
        return Response(f.read(), mimetype='text/javascript')

@app.route('/render.css')
def css():
    with open('../Viewer/render.css') as f:
        return Response(f.read(), mimetype='text/css')

@app.route('/users.json')
def users_json():
    with open('../Viewer/users.json') as f:
        return Response(f.read(), mimetype='application/json')


def main ():
    ids = input('ID: ').split(',')
    how_deep = int(input('How deep? '))
    users = [get_user(id) for id in ids]
    ids = [user['id'] for user in users]
    for id in ids:
        user_ids.add(id)
    print('Getting users ids...')
    for i in range(how_deep):
        print(f'Step {i+1}')
        user_ids_copy = user_ids.copy()
        for user_id in tqdm(user_ids_copy):
            if user_id in friends_checked:
                continue
            friends = get_friends(user_id)
            friends_checked.add(user_id)
            for friend_id in friends:
                user_ids.add(friend_id)        
    print(f'Added {len(user_ids)} user ids')
    print('Getting users info...')
    for user_id in tqdm(user_ids):
        add_user(get_user(user_id))
    print('Creating links between users')
    make_links()
    export()
    app.run(debug = True, use_reloader=False)

if __name__ == '__main__':
    main()