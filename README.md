# Diagnóstico Automatizado

Este é um software de diagnóstico automatizado de pneumonia, que utiliza uma Rede Neural Convolucional (CNN) treinada para classificar imagens de raio-x do tórax. O sistema permite que o usuário envie uma imagem de raio-x e receba um diagnóstico indicando se há ou não pneumonia.

## Tecnologias Utilizadas

- **Backend**: Flask
- **Machine Learning**: PyTorch 
- **Frontend**: HTML, CSS e JavaScript
- **Bibliotecas**: `torch`, `torchvision`, `werkzeug`, `flask`, `FileReader`

## Funcionalidades

- **Envio de Imagens**: O usuário pode enviar uma imagem de raio-x do tórax.
- **Diagnóstico**: O software utiliza um modelo CNN treinado para classificar a imagem como "Com pneumonia" ou "Sem pneumonia".
- **Visualização**: A imagem enviada é pré-visualizada na página antes de ser enviada para o backend.
- **Resultado**: O diagnóstico é exibido na interface do usuário após a análise da imagem.

## Configuração do Projeto

- **Clonar o Projeto**: git clone https://github.com/matheus-almeida01/diagnostico_automatizado.git
- **Instalar dependências**: 
```bash
pip install -r requirements.txt
```
- **Executar o Projeto**: python app\main.py

## Uso

- **Acessar Rota**: http://127.0.0.1:5000
- **Selecionar Imagem**: Selecione uma imagem de raio-x através do campo de upload.
- **Enviar Imagem**: Clique no botão "Enviar Imagem" para enviar a imagem.
- **Resultado**: O diagnóstico aparecerá na tela, indicando "Com pneumonia" ou "Sem pneumonia".