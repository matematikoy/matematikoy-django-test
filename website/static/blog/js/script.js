document.addEventListener('DOMContentLoaded', function () {
    ativarFormComentarios(); // Ativa os comentários
    ativarFormLikes(); // Ativa os likes nos botões já existentes

    function ativarFormComentarios() {
        document.querySelectorAll('.form-comment').forEach(form => {
            form.addEventListener('submit', function (e) {
                e.preventDefault();
    
                console.log('📤 Enviando comentário...');
    
                const formData = new FormData(form);  // Usa FormData para permitir upload de imagens
                formData.append('post_id', form.getAttribute('data-post-id'));  // Adiciona o ID do post
    
                fetch('/api/comentarios/adicionar/', {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCsrfToken()  // CSRF separado, porque FormData cuida do tipo de conteúdo
                    },
                    body: formData  // 🔥 Agora os dados são enviados corretamente
                })
                .then(response => response.json())
                .then(data => {
                    console.log("📩 Resposta da API:", data);  
    
                    if (data.success) {
                        adicionarComentarioNaTela(data.comment, form.getAttribute('data-post-id'));
                        form.reset();  // Limpa o formulário após envio
                    } else {
                        alert(data.error);
                    }
                })
                .catch(error => console.error('❌ Erro ao enviar o comentário:', error));
            });
        });
    }
    
    function adicionarComentarioNaTela(comment, postId) {
        const commentList = document.getElementById('comment-list-' + postId);
    
        const li = document.createElement('li');
        li.classList.add('comment-item'); // Adiciona a classe correta
    
        // Criar a imagem do comentário
        let imgHtml = '';
        if (comment.picture_url) {
            imgHtml = `<img class="comment-picture" src="${comment.picture_url}" alt="Imagem do post">`;
        }
    
        li.innerHTML = `
            ${imgHtml}
            <div class="comment-text">
                <strong>${comment.user}</strong> : ${comment.comment}
                <small>(${comment.created_at})</small>
                <form class="form-like" action="/like/comment/${comment.id}/" method="POST">
                    <input type="hidden" name="csrfmiddlewaretoken" value="${getCsrfToken()}">
                    <div class="comment-react">
                        <button type="submit" class="like-button">
                            <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none">
                                <path d="M19.4626 3.99415C16.7809 2.34923 14.4404 3.01211 13.0344 4.06801C12.4578 4.50096 12.1696 4.71743 12 4.71743C11.8304 4.71743 11.5422 4.50096 10.9656 4.06801C9.55962 3.01211 7.21909 2.34923 4.53744 3.99415C1.01807 6.15294 0.221721 13.2749 8.33953 19.2834C9.88572 20.4278 10.6588 21 12 21C13.3412 21 14.1143 20.4278 15.6605 19.2834C23.7783 13.2749 22.9819 6.15294 19.4626 3.99415Z"
                                    stroke="#ffffff" stroke-width="2" stroke-linecap="round" fill="none"></path>
                            </svg>
                            <span>${comment.likes}</span>
                        </button>
                    </div>
                </form>
            </div>
            <hr>
        `;
    
        commentList.appendChild(li);
        ativarFormLikes(); // Reativa os eventos de like para novos comentários
    }

    ativarFormLikes(); // Ativa os botões de like

    function ativarFormLikes() {
        document.querySelectorAll('.form-like').forEach(form => {
            form.onsubmit = function (e) {
                e.preventDefault();

                const formElement = e.target;
                const likeButton = formElement.querySelector('.like-button'); 
                if (!likeButton) {
                    console.error('❌ Botão de like não encontrado no formulário:', formElement);
                    return;
                }

                const likeCount = likeButton.querySelector('span'); 
                if (!likeCount) {
                    console.error('❌ Contador de likes não encontrado dentro do botão:', likeButton);
                    return;
                }

                const actionUrl = formElement.getAttribute('action');

                fetch(actionUrl, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCsrfToken(),
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({})
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        likeCount.textContent = `${data.likes}`;
                        if (data.liked) {
                            likeButton.classList.add('liked');  
                            localStorage.setItem(`liked-${actionUrl}`, 'true'); 
                        } else {
                            likeButton.classList.remove('liked');  
                            localStorage.removeItem(`liked-${actionUrl}`);
                        }
                    } else {
                        console.error('Erro ao dar like:', data.error);
                    }
                })
                .catch(error => {
                    console.error('Erro ao enviar like:', error);
                });
            };
        });

        // 🔥 Mantém os likes mesmo após o refresh, usando localStorage
        document.querySelectorAll('.form-like').forEach(form => {
            const likeButton = form.querySelector('.like-button');
            const actionUrl = form.getAttribute('action');

            if (likeButton && localStorage.getItem(`liked-${actionUrl}`) === 'true') {
                likeButton.classList.add('liked');
            }
        });
    }

    function getCsrfToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }
});



//LIKE

