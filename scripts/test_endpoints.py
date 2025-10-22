import urllib.request

urls = [
    'http://127.0.0.1:8000/api/pacientes/',
    'http://127.0.0.1:8000/api/enderecos/',
    'http://127.0.0.1:8000/api/contatos/',
    'http://127.0.0.1:8000/api/anamneses/',
    'http://127.0.0.1:8000/api/agendamentos/',
]

for u in urls:
    req = urllib.request.Request(u, headers={'Accept': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            body = r.read().decode('utf-8')
            print(u)
            print('STATUS:', r.status)
            print('BODY:', body[:1000])
            print('-' * 60)
    except Exception as e:
        print(u)
        print('ERROR:', repr(e))
        print('-' * 60)
