document.addEventListener('DOMContentLoaded', function() {
    const chefAiFab = document.getElementById('chefAiFab');
    const chefAiModal = document.getElementById('chefAiModal');
    const chefAiClose = document.getElementById('chefAiClose');
    const chefAiChatbox = document.getElementById('chefAiChatbox');
    const chefAiInput = document.getElementById('chefAiInput');
    const chefAiSendBtn = document.getElementById('chefAiSendBtn');
    
    const recipeId = window.recipeData?.id;

    if (chefAiFab) {
        chefAiFab.onclick = function() {
            chefAiModal.style.display = "block";
        }
    }

    if (chefAiClose) {
        chefAiClose.onclick = function() {
            chefAiModal.style.display = "none";
        }
    }

    window.onclick = function(event) {
        if (event.target == chefAiModal) {
            chefAiModal.style.display = "none";
        }
    }

    function addMessageToChatbox(message, sender) {
        const p = document.createElement('p');
        p.classList.add(sender === 'user' ? 'user-msg' : 'ai-msg');
        p.innerHTML = `<strong>${sender === 'user' ? 'Você' : 'Chef AI'}:</strong> ${message}`;
        chefAiChatbox.appendChild(p);
        chefAiChatbox.scrollTop = chefAiChatbox.scrollHeight;
    }

    async function sendQueryToAI() {
        const query = chefAiInput.value.trim();
        if (!query) return;

        addMessageToChatbox(query, 'user');
        chefAiInput.value = '';

        try {
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            const response = await fetch(`/recipe/${recipeId}/chef_ai/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({ query: query })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            addMessageToChatbox(data.answer, 'ai');

        } catch (error) {
            console.error('Chef AI Error:', error);
            addMessageToChatbox(`Desculpe, ocorreu um erro ao contatar o Chef AI: ${error.message}`, 'ai');
        }
    }

    if (chefAiSendBtn) {
        chefAiSendBtn.onclick = sendQueryToAI;
    }
    
    if (chefAiInput) {
        chefAiInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendQueryToAI();
            }
        });
    }
});
