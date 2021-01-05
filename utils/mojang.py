import requests
import json
import base64


def get_uuid(playername: str) -> (str, str):
    '''Get UUID with playername from Mojang API
    
    Returns:
    (str, str):UUID and playername
    '''
    payload = [playername]
    r = requests.post('https://api.mojang.com/profiles/minecraft', data=json.dumps(payload))
    r = r.json()
    if len(r) > 0:
        return (r[0]['id'], r[0]['name'])
    else:
        raise Exception(f'Cannnot find UUID for player {playername}')


def get_skin_url(uuid: str) -> (str, bool):
    '''Get skin URL and style from Mojang API
    
    Returns:
    (str, bool):Skin URL and if the player model has slim arms
    '''
    r = requests.get(f'https://sessionserver.mojang.com/session/minecraft/profile/{uuid}')
    r = r.json()
    value = json.loads(base64.b64decode(r['properties'][0]['value']))
    skin = value['textures']['SKIN']
    if 'metadata' in skin and skin['metadata']['model'] == 'slim':
        is_slim = True
    else:
        is_slim = False
    return skin['url'], is_slim
