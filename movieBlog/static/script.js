// ONLY keep modal interaction (UI stuff that needs instant response)

// Delete Modal functionality (just UI, no data logic)
const deleteModal = document.getElementById('deleteModal');
const deleteBlogTitle = document.getElementById('deleteBlogTitle');
let currentDeleteId = null;

// Open modal - pure UI, no data
function openDeleteModal(id, title) {
    currentDeleteId = id;
    deleteBlogTitle.textContent = `"${title}"`;
    deleteModal.classList.add('active');
}

// Close modal - pure UI
if (document.getElementById('closeDeleteModal')) {
    document.getElementById('closeDeleteModal').addEventListener('click', () => {
        deleteModal.classList.remove('active');
    });
}

// Close modal when clicking outside - pure UI
window.addEventListener('click', (e) => {
    if (deleteModal && e.target === deleteModal) {
        deleteModal.classList.remove('active');
    }
});

// That's it! Everything else goes to Flask



// // DOM Elements
// const blogList = document.getElementById('blogList');
// const emptyState = document.getElementById('emptyState');
// const deleteModal = document.getElementById('deleteModal');
// const deleteBlogTitle = document.getElementById('deleteBlogTitle');

// // Sample data (replace with your API calls later)
// let blogs = [
//     {
//         id: 1,
//         title: 'The Shawshank Redemption',
//         director: 'Frank Darabont',
//         year: 1994,
//         rating: 9.5,
//         content: 'An absolutely brilliant film about hope and friendship. The performances are outstanding and the storytelling is masterful. Every scene serves a purpose and the payoff is incredibly satisfying.'
//     },
//     {
//         id: 2,
//         title: 'Inception',
//         director: 'Christopher Nolan',
//         year: 2010,
//         rating: 9.0,
//         content: 'A mind-bending masterpiece that keeps you thinking long after the credits roll. The layers of dreams within dreams create a complex narrative that rewards multiple viewings. The visual effects are stunning.'
//     }
// ];

// let currentDeleteId = null;

// // Render blog posts
// function renderBlogs() {
//     if (!blogList) return; // Only run on index page

//     blogList.innerHTML = '';

//     if (blogs.length === 0) {
//         emptyState.style.display = 'block';
//         return;
//     }

//     emptyState.style.display = 'none';

//     blogs.forEach(blog => {
//         const card = document.createElement('div');
//         card.className = 'blog-card';
//         card.innerHTML = `
//             <h3>${blog.title} (${blog.year})</h3>
//             <div class="movie-info">Directed by ${blog.director}</div>
//             <span class="rating">★ ${blog.rating}/10</span>
//             <div class="content">${blog.content}</div>
//             <div class="card-actions">
//                 <a href="/edit/${blog.id}" class="btn-edit">Edit</a>
//                 <button class="btn-delete-card" onclick="openDeleteModal(${blog.id})">Delete</button>
//             </div>
//         `;
//         blogList.appendChild(card);
//     });
// }

// // Open Delete Modal
// function openDeleteModal(id) {
//     const blog = blogs.find(b => b.id === id);
//     if (!blog) return;

//     currentDeleteId = id;
//     deleteBlogTitle.textContent = `"${blog.title}"`;
//     deleteModal.classList.add('active');
// }

// // Close Delete Modal
// if (document.getElementById('closeDeleteModal')) {
//     document.getElementById('closeDeleteModal').addEventListener('click', () => {
//         deleteModal.classList.remove('active');
//     });
// }

// // Handle delete confirmation
// if (document.getElementById('confirmDelete')) {
//     document.getElementById('confirmDelete').addEventListener('click', () => {
//         if (currentDeleteId) {
//             blogs = blogs.filter(b => b.id !== currentDeleteId);
//             currentDeleteId = null;
//             deleteModal.classList.remove('active');
//             renderBlogs();
//             // Here you would also send DELETE request to your Flask backend
//         }
//     });
// }

// // Close modal when clicking outside
// window.addEventListener('click', (e) => {
//     if (deleteModal && e.target === deleteModal) {
//         deleteModal.classList.remove('active');
//     }
// });

// // Initial render
// renderBlogs();