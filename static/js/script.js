// Função para carregar o histórico de mensagens
function carregarHistorico() {
    axios
        .get("https://filteriq.onrender.com/chat")
        .then(function (response) {
            const mensagens = response.data;
            const messagesContainer = document.getElementById("messages");
            mensagens.forEach(function (interacao) {
                // Adicionando as mensagens no container
                messagesContainer.innerHTML += `
                    <div class="user-message">
                        <strong>Você:</strong> ${interacao.mensagem}
                    </div>
                    <div class="bot-message">
                        <strong>FilterIQ:</strong> ${interacao.resposta}
                    </div>
                `;
            });
            // Rolando a área de mensagens para o final
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        })
        .catch(function (error) {
            console.error("Erro ao carregar o histórico:", error);
        });
}

// Função para enviar a mensagem do usuário e receber a resposta
document.getElementById("chatForm").addEventListener("submit", function (event) {
    event.preventDefault();

    const userMessage = document.getElementById("userMessage").value;
    document.getElementById("userMessage").value = ""; // Limpando o campo de input

    const messagesContainer = document.getElementById("messages");

    // Exibindo a mensagem do usuário na tela
    messagesContainer.innerHTML += `
        <div class="user-message">
            <strong>Você:</strong> ${userMessage}
        </div>
    `;

    // Criando o elemento de loader (aguardando a resposta do bot)
    const loaderContainer = document.createElement("div");
    loaderContainer.className = "bot-message";
    const loadingElement = document.createElement("div");
    loadingElement.className = "loader";
    loaderContainer.appendChild(loadingElement);
    messagesContainer.appendChild(loaderContainer);
    loadingElement.style.display = "block";

    // Rolando a área de mensagens para o final
    messagesContainer.scrollTop = messagesContainer.scrollHeight;

    // Enviando a mensagem para o servidor (API)
    axios
        .post("https://filteriq.onrender.com/openai", {
            user: userMessage,
        }, {
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(function (response) {
            // Removendo o loader
            loadingElement.remove();

            // Exibindo a resposta do bot
            const botMessageElement = document.createElement("div");
            botMessageElement.innerHTML = `
                <strong>FilterIQ:</strong> ${response.data.resposta}
            `;
            loaderContainer.appendChild(botMessageElement);

            // Rolando a área de mensagens para o final
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        })
        .catch(function (error) {
            // Removendo o loader em caso de erro
            loadingElement.remove();
            messagesContainer.innerHTML += `
                <div class="bot-message">
                    <strong>Erro:</strong> ${error.message}
                </div>
            `;
        });
});

// Função para alternar entre o tema claro e escuro
function alternarTema() {
    document.body.classList.toggle("dark-mode");
    document.body.classList.toggle("light-mode");
}

// Carregando o histórico e aplicando o tema
carregarHistorico();
alternarTema();
