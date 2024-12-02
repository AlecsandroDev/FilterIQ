function carregarHistorico() {
    axios
        .get("https://filteriq.onrender.com/chat")
        .then(function (response) {
            const mensagens = response.data;
            mensagens.forEach(function (interacao) {
                document.getElementById("messages").innerHTML += `
                    <div class="user-message">
                        <strong>Você:</strong> ${interacao.mensagem}
                    </div>
                    <div class="bot-message">
                        <strong>FilterIQ:</strong> ${interacao.resposta}
                    </div>
                `;
            });
            const messagesContainer = document.getElementById("messages");
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        })
        .catch(function (error) {
            console.error("Erro ao carregar o histórico:", error);
        });
}

document.getElementById("chatForm").addEventListener("submit", function (event) {
    event.preventDefault();

    const userMessage = document.getElementById("userMessage").value;
    document.getElementById("userMessage").value = "";

    document.getElementById("messages").innerHTML += `
        <div class="user-message">
            <strong>Você:</strong> ${userMessage}
        </div>
    `;

    const loaderContainer = document.createElement("div");
    loaderContainer.className = "bot-message";

    const loadingElement = document.createElement("div");
    loadingElement.className = "loader";
    loaderContainer.appendChild(loadingElement);
    document.getElementById("messages").appendChild(loaderContainer);
    loadingElement.style.display = "block";

    const messagesContainer = document.getElementById("messages");
    messagesContainer.scrollTop = messagesContainer.scrollHeight;

    axios
        .post("https://filteriq.onrender.com/talk/openai", {
            user: userMessage,
        }, {
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(function (response) {
            loadingElement.remove();

            const botMessageElement = document.createElement("div");
            botMessageElement.innerHTML = `
                <strong>FilterIQ:</strong> ${response.data.resposta}
            `;
            loaderContainer.appendChild(botMessageElement);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        })
        .catch(function (error) {
            loadingElement.remove();
            document.getElementById("messages").innerHTML += `
                <div class="bot-message">
                    <strong>Erro:</strong> ${error.message}
                </div>
            `;
        });
});

function alternarTema() {
    document.body.classList.toggle("dark-mode");
    document.body.classList.toggle("light-mode");
}

carregarHistorico();
alternarTema();
