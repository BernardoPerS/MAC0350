async function enviarUsuario() {
    const dados = {
        nome: document.getElementById('nome').value,
        senha: document.getElementById('senha').value,
        bio: document.getElementById('bio').value
    };

    const resposta = await fetch('/usuarios', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(dados)
    });

    if (resposta.ok) {
        const resultado = await resposta.json();
        alert("Usuário " + resultado.usuario + " criado!");
    } else {
        alert("Erro ao enviar!");
    }
}


async function realizarLogin() {
    const dados = {
        nome: document.getElementById('nome').value,
        senha: document.getElementById('senha').value
    }
    
    const resposta = await fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(dados)
    });

    if (resposta.ok) {
        alert("Login realizado!");
        window.location.href = "/profile"; // Redireciona para o perfil após logar
    } else {
        alert("Usuário não encontrado!");
    }
}