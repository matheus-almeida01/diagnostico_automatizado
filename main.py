from flask import Flask, request
from werkzeug.utils import secure_filename
from io import BytesIO

app = Flask(__name__)

# Extensões permitidas
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Verifica se o request contém o campo 'file'
        if 'file' not in request.files:
            return 'Nenhum arquivo foi enviado.'
        
        file = request.files['file']
        
        # Se nenhum arquivo for selecionado
        if file.filename == '':
            return 'Nenhum arquivo foi selecionado.'
        
        # Verifica se o arquivo é permitido
        if file and allowed_file(file.filename):
            # Aqui o arquivo é carregado na memória, mas não salvo no disco
            img_bytes = BytesIO(file.read())
            filename = secure_filename(file.filename)
            return f'Imagem {filename} recebida com sucesso, mas não foi salva.'

if __name__ == '__main__':
    app.run(debug=True)