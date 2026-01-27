// Dark mode toggle functionality
document.addEventListener('DOMContentLoaded', function() {
    // Get the theme toggle button
    const themeToggle = document.getElementById('theme-toggle');

    if (themeToggle) {
        // Check for saved theme preference or default to light mode
        const currentTheme = localStorage.getItem('theme') || 'light';

        // Apply the current theme
        if (currentTheme === 'dark') {
            document.documentElement.classList.add('dark');
            updateToggleIcon(true);
        } else {
            document.documentElement.classList.remove('dark');
            updateToggleIcon(false);
        }

        // Toggle theme on button click
        themeToggle.addEventListener('click', function() {
            const isDark = document.documentElement.classList.toggle('dark');
            localStorage.setItem('theme', isDark ? 'dark' : 'light');
            updateToggleIcon(isDark);
        });
    }

    function updateToggleIcon(isDark) {
        const icon = themeToggle.querySelector('i');
        if (icon) {
            if (isDark) {
                icon.className = 'fas fa-sun text-xl'; // Sun icon for light mode toggle
            } else {
                icon.className = 'fas fa-moon text-xl'; // Moon icon for dark mode toggle
            }
        }
    }
});
