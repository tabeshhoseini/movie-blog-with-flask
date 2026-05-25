

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