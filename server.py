

ServersDict = {
    'Althena': {
        'hostname': '10.0.0.19',
        'username': 'peter',
        'password': '123456',
        'num_gpus': 2,
    },

    'RTX': {
        'hostname': '10.0.0.17',
        'username': 'batman',
        'password': '123456',
        'num_gpus': 1,
    },

    'RTX2': {
        'hostname': '10.0.0.13',
        'username': 'ghost',
        'password': '123456',
        'num_gpus': 1,
    },

    'TiTan X': {
        'hostname': '10.0.0.174',
        'username': 'jason',
        'password': '123456',
        'num_gpus': 2,
    },

    'TiTan2': {
        'hostname': '10.0.0.11',
        'username': 'hulk',
        'password': '123456',
        'num_gpus': 2,
    }
}

def dump():
    import json
    with open('server.json', 'w') as file:
        json.dump(ServersDict, file)

def load():
    import json
    with open('server.json', 'r') as file:
        sd = json.load(file)
        for name in sd:
            print(name)
            for k in sd[name]:
                print('\t{}:{}'.format(k, sd[name][k]))
        return sd



if __name__ == '__main__':
    load()