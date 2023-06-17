
import vk_api
import json
from flask import Flask, Response

app = Flask(__name__)

TOKEN = ''
session = vk_api.VkApi(token=TOKEN)

vkses = session.get_api()
users = []
links = []

def get_user (user_id):
    try:
        return vkses.users.get(user_ids=user_id)[0]
    except Exception:
        print(f'Can\'t get user information for {user_id}')
        return None

def get_friends (user_id):
    try:
        return vkses.friends.get(user_id=user_id)['items']
    except Exception:
        print(f'Can\'t get friends for user {user_id}')
        return []

def add_user (user):
    users.append({'id' : user['id'], 'name' : (user['first_name'] + ' ' + user['last_name'])})

def make_links ():
    for i in range(len(users)):
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
def users():
    with open('../Viewer/users.json') as f:
    	return Response(f.read(), mimetype='application/json')


def main ():
    id = input('ID: ')
    user = get_user(id)
    id = user['id']
    add_user(user)
    for friend_id in get_friends(id):
        add_user(get_user(friend_id))
    print(f'Added {len(users)} users')
    make_links()
    export()
    app.run(debug = True)

if __name__ == '__main__':
    main()