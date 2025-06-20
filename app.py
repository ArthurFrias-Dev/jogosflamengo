from flask import Flask, jsonify, send_from_directory
import requests

app = Flask(__name__)

# key arthurfelipeloureiro API_KEY = 'b2b7ba44472c426b8e3d62f05c2cfbd5'
# key loureirofrias API_KEY = '85d171afad504cca9299342a6742c5db'
API_KEY = 'b2b7ba44472c426b8e3d62f05c2cfbd5'
FLAMENGO_ID = 1783
headers = {'X-Auth-Token': API_KEY}

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/jogos')
def jogos():
    url = "https://api.football-data.org/v4/competitions/BSA/matches?season=2025"
    res = requests.get(url, headers=headers)

    if res.status_code == 200:
        todos_os_jogos = res.json().get('matches', [])
        
        # Filtra jogos do Flamengo que ainda não estão finalizados
        jogos_nao_finalizados = [
            j for j in todos_os_jogos
            if (j['homeTeam']['id'] == FLAMENGO_ID or j['awayTeam']['id'] == FLAMENGO_ID)
            and j['status'] != 'FINISHED'
        ]

        return jsonify(jogos_nao_finalizados)
    else:
        print("❌ Erro API:", res.status_code, res.text)
        return jsonify({'erro': 'Erro ao buscar jogos'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
