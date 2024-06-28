let searchResults = [];
// Function to perform the search
function searchBooks() {
    const searchBar = document.getElementById('search_bar');
    const query = searchBar.value;

    if (query) {
        console.log('Searching for:', query);
        const apiUrl = `http://127.0.0.1:5000/search?query=${encodeURIComponent(query)}`;
        fetch(apiUrl)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok ' + response.statusText);
                }
                return response.json();
            })
            .then(data => {
                searchResults = data.data;
                console.log('Search results:', searchResults);
                displayResults(searchResults);
            })
            .catch(error => {
                console.error('There has been a problem with your fetch operation:', error);
            });
    } else {
        console.log('Please enter a search term.');
    }
}

function displayResults(books) {
    const resultsContainer = document.getElementById('results');
    resultsContainer.innerHTML = '';  // Clear previous results

    books.forEach(book => {
        const bookCard = document.createElement('div');
        bookCard.className = 'book-card';

        const bookCover = document.createElement('img');
        bookCover.className = 'book-cover';
        bookCover.src = book.cover_url || 'default-cover.jpg';  // Replace with actual cover URL field
        bookCover.alt = 'Book Cover';

        const bookTitle = document.createElement('div');
        bookTitle.className = 'book-title';
        bookTitle.textContent = book.title;

        const bookAuthor = document.createElement('div');
        bookAuthor.className = 'book-author';
        bookAuthor.textContent = book.author;

        const bookRating = document.createElement('div');
        bookRating.className = 'book-rating';
        bookRating.textContent = book.rating || '★★★★☆';  // Replace with actual rating field

        const detailsButton = document.createElement('button');
        detailsButton.className = 'details-button';
        detailsButton.textContent = 'Details';
        detailsButton.addEventListener('click', () => {
            // Handle details button click (e.g., show more information)
            alert(`More details about: ${book.title}`);
        });

        bookCard.appendChild(bookCover);
        bookCard.appendChild(bookTitle);
        bookCard.appendChild(bookAuthor);
        bookCard.appendChild(bookRating);
        bookCard.appendChild(bookDescription);
        bookCard.appendChild(detailsButton);

        resultsContainer.appendChild(bookCard);
    });
}

document.getElementById('search_button').addEventListener('click', searchBooks);