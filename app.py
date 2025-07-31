# Arquivo: app.py
# (O início do arquivo continua o mesmo)
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

API_KEY = "ttMZrBTp4mD0xMkYAVxKMzyu7B9KL1nfCS6T1fMR"

# --- NOVA ROTA ADICIONADA ---
@app.route('/')
def serve_index():
    """Esta rota serve o arquivo 'monitor.html'"""
    # O arquivo 'monitor.html' deve estar na mesma pasta que o 'app.py'
    return send_from_directory('.', 'monitor.html')


# A sua rota de API continua igual
@app.route('/api/metar', methods=['GET'])
def get_metar():
    # ... (todo o código da função get_metar permanece o mesmo)
    localidade = request.args.get('local')
    if not localidade:
        return jsonify({"error": "O parâmetro 'local' (código ICAO) é obrigatório."}), 400
    api_url = f"https://api-redemet.decea.mil.br/mensagens/metar/{localidade}?api_key={API_KEY}"
    print(f"Recebido pedido para {localidade}. Consultando API REDEMET...")
    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        data = response.json()
        metar_message = data.get("data", {}).get("data", [{}])[0].get("mens")
        if metar_message:
            print(f"METAR encontrado para {localidade}: {metar_message}")
            return jsonify({"metar": metar_message})
        else:
            print(f"Nenhum METAR encontrado para {localidade}.")
            return jsonify({"error": f"METAR não encontrado para a localidade {localidade}"}), 404
    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão com a API REDEMET: {e}")
        return jsonify({"error": f"Não foi possível conectar à API REDEMET: {e}"}), 502
    except (KeyError, IndexError):
        print("Erro ao processar a resposta da API REDEMET. Formato inesperado.")
        return jsonify({"error": "Formato de resposta inesperado da API REDEMET"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)