document.getElementById('fileInput').addEventListener('change', function(event) {
    const file = event.target.files[0];
    const previewImg = document.getElementById('previewImg');
    
    if (file) {
        const reader = new FileReader();
        
        reader.onload = function(e) {
            previewImg.src = e.target.result;
            // Mostra a imagem
            previewImg.style.display = 'block';  
        };

        // Lê a imagem como URL para exibição
        reader.readAsDataURL(file);  
    } else {
        // Esconde a imagem se nenhum arquivo for selecionado
        previewImg.style.display = 'none';  
    }
});

document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const formData = new FormData();
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];

    if (!file) {
        alert('Por favor, selecione uma imagem.');
        return;
    }

    formData.append('file', file);

    fetch('/archive', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('result').innerText = `Diagnóstico: ${data.diagnosis}`;
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('Ocorreu um erro no envio da imagem.');
    });
});
