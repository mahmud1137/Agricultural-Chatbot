async function askBot() {
    const questionInput = document.getElementById("question");
    const question = questionInput.value.trim();
    const messagesDiv = document.getElementById("messages");

    if (!question) return;

    messagesDiv.innerHTML += `<div class="user"><strong>You:</strong> ${question}</div>`;
    questionInput.value = "";

    const typingEl = document.createElement("div");
    typingEl.className = "bot";
    typingEl.innerHTML = "<em>Thinking...</em>";
    messagesDiv.appendChild(typingEl);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;

    try {
        const res = await fetch("http://127.0.0.1:5000/ask", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question })
        });
        const data = await res.json();

        let formattedAnswer = data.answer
            .replace(/\n/g, '<br>') 
            .replace(/- (.*?)(<br>|$)/g, '<li>$1</li>'); 
        if (formattedAnswer.includes('<li>')) {
            formattedAnswer = formattedAnswer.replace(/(<li>.*<\/li>)/gs, '<ul>$1</ul>');
        }

        typingEl.innerHTML = `<strong>Bot:</strong> ${formattedAnswer}`;

    } catch (err) {
        typingEl.innerHTML = `<strong>Bot:</strong> Error connecting to server.`;
    }

    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

document.getElementById("question").addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        askBot();
    }
});

document.getElementById("sendBtn").addEventListener("click", askBot);
