

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
/* ============================================
   AUTH JS — add these to the bottom of script.js
   ============================================ */

// Toggle password visibility
function togglePassword(fieldId) {
    const input = document.getElementById(fieldId);
    if (input) {
        input.type = input.type === 'password' ? 'text' : 'password';
    }
}

// Live password match check on register page
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
