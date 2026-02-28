from flask import Flask, render_template, request
from trust_motor import executar_trust_web

app = Flask(__name__)

@app.route('/')
def index():
    # Carrega a página inicial do seu site
    return render_template('index.html')

@app.route('/executar', methods=['POST'])
def executar():
    # Captura o código enviado pelo formulário HTML
    codigo_trust = request.form.get('codigo', '')
    
    # Chama o motor da Trust que acabamos de completar
    saida_lista = executar_trust_web(codigo_trust)
    
    # Retorna para a página enviando os resultados processados
    return render_template('index.html', resultado=saida_lista, codigo_previo=codigo_trust)

if __name__ == '__main__':
    # Roda o servidor localmente
    print("Servidor Trust Online! Acesse: http://0.0.0.0:5000")
    # A linha abaixo deve ter exatamente 4 espaços de recuo
    app.run(host='0.0.0.0', port=5000, debug=True)
