from flask import Flask, request, jsonify, render_template
from cnn import diagnosis

app = Flask(__name__)

# Extensões permitidas
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Função para validar arquivo 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Rotas
@app.route('/')
def index():
    # Renderiza o frontend do projeto
    return render_template('index.html')

@app.route('/archive', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        try:
            # Verifica se o request contém o campo 'file'
            if 'file' not in request.files:
                return jsonify({'error': 'Nenhum arquivo foi enviado.'}), 400
            
            file = request.files['file']
            
            # Se nenhum arquivo for selecionado
            if file.filename == '':
                return jsonify({'error': 'Nenhum arquivo foi selecionado.'}), 400
            
            # Verifica se o arquivo é permitido
            if file and allowed_file(file.filename):
                # Recebe o arquivo enviado pelo usuario e faz o diagnóstico
                img_bytes = file.read()
                img_diagnosis = diagnosis(img_bytes)
                # Retorna o diagnóstico
                return jsonify({'diagnosis': img_diagnosis}), 200
            
        except Exception as e:
            # Retorna a mensagem de erro
            return jsonify({'error': str(e)}), 500  

if __name__ == '__main__':
    app.run(debug=True)