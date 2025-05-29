function toggleFavorite(recipeId, button, isAuthenticated) {
    if (!isAuthenticated) {
        alert('You need to be logged in to favorite recipes.');
        return;
    }

    fetch(`/recipe/${recipeId}/toggle-favorite/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        const heartIcon = button.querySelector('i');
        if (data.is_favorited) {
            heartIcon.classList.remove('fa-regular');
            heartIcon.classList.add('fa-solid');
            button.classList.add('liked');
        } else {
            heartIcon.classList.remove('fa-solid');
            heartIcon.classList.add('fa-regular');
            button.classList.remove('liked');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}