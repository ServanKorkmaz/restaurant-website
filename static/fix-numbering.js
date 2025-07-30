// Fix for double numbering in menu items
document.addEventListener('DOMContentLoaded', function () {
    // Find all menu item titles that have double numbering
    const menuTitles = document.querySelectorAll('.menu-section h5.card-title');
    
    menuTitles.forEach(function(title) {
        // Check if title contains pattern like "1. 01." or "2. 02."
        const regex = /^\d+\.\s+(\d+\.\s*.+)$/;
        const match = title.textContent.match(regex);
        
        if (match) {
            // Replace with just the numbered part (e.g., "01. Kylling...")
            title.textContent = match[1];
        }
    });
});