// Delete Modal functionality
const deleteModal = document.getElementById('deleteModal');
const deleteBlogTitle = document.getElementById('deleteBlogTitle');
let currentDeleteId = null;

function openDeleteModal(id, title) {
    currentDeleteId = id;
    deleteBlogTitle.textContent = `"${title}"`;
    deleteModal.classList.add('active');
}

if (document.getElementById('closeDeleteModal')) {
    document.getElementById('closeDeleteModal').addEventListener('click', () => {
        deleteModal.classList.remove('active');
    });
}

window.addEventListener('click', (e) => {
    if (deleteModal && e.target === deleteModal) {
        deleteModal.classList.remove('active');
    }
});

// Toggle password visibility
function togglePassword(fieldId) {
    const input = document.getElementById(fieldId);
    if (input) {
        input.type = input.type === 'password' ? 'text' : 'password';
    }
}

// Live password match check
const confirmInput = document.getElementById('confirm_password');
const passwordInput = document.getElementById('password');
const hint = document.getElementById('passwordMatchHint');

if (confirmInput && passwordInput && hint) {
    confirmInput.addEventListener('input', checkPasswordMatch);
    passwordInput.addEventListener('input', checkPasswordMatch);
}

function checkPasswordMatch() {
    if (confirmInput.value === '') {
        hint.textContent = '';
        hint.className = 'field-hint';
        return;
    }
    if (passwordInput.value === confirmInput.value) {
        hint.textContent = '✓ Passwords match';
        hint.className = 'field-hint match';
    } else {
        hint.textContent = '✗ Passwords do not match';
        hint.className = 'field-hint no-match';
    }
}

// Like button toggle
function toggleLike(btn, movieId) {
    btn.disabled = true;

    fetch(`/like/${movieId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    })
        .then(res => res.json())
        .then(data => {
            const icon = btn.querySelector('.like-icon');
            const count = btn.querySelector('.like-count');

            if (data.liked) {
                icon.textContent = '❤️';
                btn.classList.add('liked');
            } else {
                icon.textContent = '🤍';
                btn.classList.remove('liked');
            }

            count.textContent = data.count;

            btn.classList.remove('like-pop');
            void btn.offsetWidth;
            btn.classList.add('like-pop');
        })
        .catch(err => console.error('Like error:', err))
        .finally(() => { btn.disabled = false; });
}

document.addEventListener('click', function (e) {
    const btn = e.target.closest('.btn-like');
    if (!btn) return;
    const movieId = btn.dataset.movieId;
    toggleLike(btn, movieId);
});