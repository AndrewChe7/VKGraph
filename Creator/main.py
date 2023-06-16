
import vk_api
import json


TOKEN = ''
session = vk_api.VkApi(token=TOKEN)

vkses = session.get_api()
users = []
links = []


def get_user (user_id):
	return vkses.users.get(user_ids=user_id)[0]


def get_friends (user_id):
	return vkses.friends.get(user_id=user_id)['items']


def add_user (user):
	users.append({'id' : user['id'], 'name' : (user['first_name'] + ' ' + user['last_name'])})
	print('add user ' + str(user['id']))


def make_links ():
	for i in range(len(users)):
		for j in range(i):
			try:
				if users[j]['id'] in get_friends(users[i]['id']):
					links.append({
						'source' : users[i]['id'], 
						'target' : users[j]['id'], 
						'value' : 1 #len(api.friends.get_mutual(users[i]['id'], users[j]['id'])['response'])
						})
					print('add link ' + str(users[i]['id']) + ' and ' + str(users[j]['id'])) #TODO: names
			except: #TODO: Exceptions
				print ('something is wrong')


def export (): 
	with open('users.json', 'w') as f:
		f.write(json.dumps({
			'nodes' : users,
			'links' : links
			}))




def main ():
	id = int(input('ID: '))
	add_user(get_user(id))
	for friend_id in get_friends(id):
		add_user(get_user(friend_id))
	make_links()
	export()



if __name__ == '__main__':
	main()