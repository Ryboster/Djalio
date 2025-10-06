let addEditorInstance = null;
let editEditorInstance = null;

function initializeAddCKEditor() {
    console.log("Attempting to initialize Add CKEditor");
    if (typeof CKEDITOR === 'undefined') {
        console.error("CKEditor not loaded!");
        return;
    }
    if (!addEditorInstance) {
        try {
            addEditorInstance = CKEDITOR.replace('add-content-input', {
                height: 300,
                width: '100%',
                filebrowserUploadUrl: '/upload-media/',
                filebrowserUploadMethod: 'form',
                uploadUrl: '/upload-media/',
                toolbar: [
                    { name: 'basicstyles', items: ['Bold', 'Italic', 'Underline'] },
                    { name: 'paragraph', items: ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent'] },
                    { name: 'links', items: ['Link', 'Unlink'] },
                    { name: 'insert', items: ['Image', 'Table'] },
                    { name: 'styles', items: ['Format'] },
                    { name: 'tools', items: ['Maximize'] }
                ],
                disallowedContent: 'img[src^="data:"]'
            });
            console.log("Add CKEditor initialized successfully");
        } catch (error) {
            console.error("Error initializing Add CKEditor:", error);
        }
    }
}

function initializeEditCKEditor() {
    console.log("Attempting to initialize Edit CKEditor");
    if (typeof CKEDITOR === 'undefined') {
        console.error("CKEditor not loaded!");
        return;
    }
    if (!editEditorInstance) {
        try {
            editEditorInstance = CKEDITOR.replace('edit-content-input', {
                height: 300,
                width: '100%',
                filebrowserUploadUrl: '/upload-media/',
                filebrowserUploadMethod: 'form',
                uploadUrl: '/upload-media/',
                toolbar: [
                    { name: 'basicstyles', items: ['Bold', 'Italic', 'Underline'] },
                    { name: 'paragraph', items: ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent'] },
                    { name: 'links', items: ['Link', 'Unlink'] },
                    { name: 'insert', items: ['Image', 'Table'] },
                    { name: 'styles', items: ['Format'] },
                    { name: 'tools', items: ['Maximize'] }
                ],
                disallowedContent: 'img[src^="data:"]'
            });
            console.log("Edit CKEditor initialized successfully");
        } catch (error) {
            console.error("Error initializing Edit CKEditor:", error);
        }
    }
}

function showAddEntryForm() {
    console.log("showAddEntryForm called");
    const overlay = document.getElementById('addEntryFormOverlay');
    overlay.style.display = 'flex';
    if (typeof CKEDITOR !== 'undefined') {
        setTimeout(initializeAddCKEditor, 300);
    } else {
        console.error("CKEditor not available");
    }
}

function showEditEntryForm() {
    console.log("showEditEntryForm called");
    const overlay = document.getElementById('editEntryFormOverlay');
    overlay.style.display = 'flex';
    if (typeof CKEDITOR !== 'undefined') {
        setTimeout(initializeEditCKEditor, 300);
    } else {
        console.error("CKEditor not available");
    }
}

function hideAddEntryForm() {
    const overlay = document.getElementById('addEntryFormOverlay');
    overlay.style.display = 'none';
    if (addEditorInstance) {
        addEditorInstance.destroy();
        addEditorInstance = null;
    }
}

function hideEditEntryForm() {
    const overlay = document.getElementById('editEntryFormOverlay');
    overlay.style.display = 'none';
    if (editEditorInstance) {
        editEditorInstance.destroy();
        editEditorInstance = null;
    }
}

// Form submission handlers
document.addEventListener('DOMContentLoaded', function() {
    // Add form submission handler
    document.getElementById('addEntryForm').addEventListener('submit', function(e) {
        if (addEditorInstance) {
            addEditorInstance.updateElement();
        }
    });

    // Edit form submission handler
    document.getElementById('editEntryForm').addEventListener('submit', function(e) {
        if (editEditorInstance) {
            editEditorInstance.updateElement();
        }
    });
});