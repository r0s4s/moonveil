/* 
*****************************************************************
*  global.js                                                    *
*****************************************************************
*                                                               *
*                      This file is part of:                    *
*                        MOONVEIL PROJECT                       *
*                                                               *
*****************************************************************
*/

/* Nav Burger */

document.addEventListener('DOMContentLoaded', () => {
    // Get all "navbar-burger" elements
    const $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);

    // Add a click event on each of them
    $navbarBurgers.forEach( el => {
        el.addEventListener('click', () => {
            // Get the target from the "data-target" attribute
            const target = el.dataset.target;
            const $target = document.getElementById(target);

            // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
            el.classList.toggle('is-active');
            $target.classList.toggle('is-active');
        });
    });
});

/* Inactive Links */
/*
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.sidebar-nav a.inactive').forEach(link => {
        link.addEventListener('click', event => event.preventDefault());
    });
});
*/

/* Tabs Navigation */

/*
document.addEventListener('DOMContentLoaded', () => {
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const targetId = button.dataset.target;
            const targetContent = document.getElementById(targetId);
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            button.classList.add('active');
            targetContent.classList.add('active');
        });
    });
});
*/

document.addEventListener('DOMContentLoaded', () => {
    const tabButtons = document.querySelectorAll('.menu-list a.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const targetId = button.dataset.target;
            const targetContent = document.getElementById(targetId);
            tabButtons.forEach(btn => {
                btn.classList.remove('active');
            });
            tabContents.forEach(content => {
                content.classList.add('is-hidden');
            });
            button.classList.add('active');
            targetContent.classList.remove('is-hidden');
        });
    });
});

/* Tab Navigation URI Fragments */

/*
document.addEventListener('DOMContentLoaded', function () {
    function switchTab(tabId) {
        document.querySelectorAll(
            '.tab-button').forEach(function (button) {
            button.classList.remove('active');
        });

        const targetButton = document.querySelector(
            `.tab-button[data-target="${tabId}"]`);
        if (targetButton) {
            targetButton.classList.add('active');
        }

        document.querySelectorAll(
            '.tab-content').forEach(function (content) {
            content.style.display = 'none';
        });

        const targetContent = document.getElementById(tabId);
        if (targetContent) {
            targetContent.style.display = 'block';
        }
    }

    const initialTab = window.location.hash.substring(1);
    if (initialTab) {
        switchTab(initialTab);
    }

    document.querySelectorAll('.tab-button').forEach(function (button) {
        button.addEventListener('click', function () {
            const targetTab = button.getAttribute('data-target');
            switchTab(targetTab);
            window.location.hash = targetTab;
        });
    });
});
*/

/* Loading Spinner */

document.addEventListener('DOMContentLoaded', function () {
    const asmForms = document.querySelectorAll('.asm-form');
    asmForms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            const loadingSpinnerContainer = document.getElementById(
                'loading-spinner-container'
            );
            
            loadingSpinnerContainer.style.display = 'flex';
            fetch(form.action, {
                method: form.method,
                body: new FormData(form)
            }).then(function(response) {
                loadingSpinnerContainer.style.display = 'none';
                window.location.reload();
            }).catch(function(error) {
                loadingSpinnerContainer.style.display = 'none';
                console.error('Error during command execution:', error);
            });
        });
    });
});
