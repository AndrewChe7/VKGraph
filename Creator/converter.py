import json
from tqdm import tqdm

with open('../Viewer/users.json', encoding='utf-8') as f:
    data = json.load(f)
    result = 'nodedef>name VARCHAR,label VARCHAR\n'
    print('Converting users...')
    for node in tqdm(data['nodes']):
        result+='{},{}\n'.format(node['id'], node['name'])
    result += 'edgedef>node1 VARCHAR,node2 VARCHAR\n'
    print('Converting edges...')
    for edge in tqdm(data['links']):
        result += '{},{}\n'.format(edge['source'], edge['target'])
    with open('users.gdf', 'w', encoding='utf-8') as o:
        o.write(result)