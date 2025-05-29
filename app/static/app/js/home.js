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

function toggleFilters() {
    const filtersSection = document.getElementById('filters-section');
    if (filtersSection.style.display === 'none') {
        filtersSection.style.display = 'block';
    } else {
        filtersSection.style.display = 'none';
    }
}

function clearFilters() {
    document.querySelector('[name="search"]').value = '';
    document.querySelector('[name="category"]').value = '';
    document.querySelector('[name="prep_time"]').value = '';
    document.querySelector('[name="servings"]').value = '';
    if (document.querySelector('[name="favorites"]')) {
        document.querySelector('[name="favorites"]').value = '';
    }

    document.querySelector('[name="search"]').dispatchEvent(new Event('input', { bubbles: true }));
    document.querySelector('[name="category"]').dispatchEvent(new Event('change', { bubbles: true }));
    document.querySelector('[name="prep_time"]').dispatchEvent(new Event('change', { bubbles: true }));
    document.querySelector('[name="servings"]').dispatchEvent(new Event('change', { bubbles: true }));
    if (document.querySelector('[name="favorites"]')) {
        document.querySelector('[name="favorites"]').dispatchEvent(new Event('change', { bubbles: true }));
    }
}