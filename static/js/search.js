/* 
*****************************************************************
*  search.js                                                    *
*****************************************************************
*                                                               *
*                      This file is part of:                    *
*                        MOONVEIL PROJECT                       *
*                                                               *
*****************************************************************
*/

/* Validation */
function validateSearchForm() {
    var queryInput = document.getElementById('search-input');
    var query = queryInput.value.trim();
    var regexSubdomains = /^[a-zA-Z_-]+:[a-zA-Z0-9_\-\/.]+(\s+(and|or)\s+[a-zA-Z_-]+:[a-zA-Z0-9_\-\/.]+)*$/;
    // var regexArchives = /^[a-zA-Z0-9_.\-]+$/;
    // var regexArchives = /^[a-zA-Z0-9_.?\-\/]+$/;
    var regexArchives = /^[a-zA-Z0-9=_.?\-\/]+$/;
    var errorMessage = document.getElementById('query-error');
    var searchType = document.getElementById('search-type-select').value;

    if (searchType === 'subdomains' && !regexSubdomains.test(query)) {
        errorMessage.innerText = 'Invalid query syntax. Please use the \'attribute:value\' format.';
        errorMessage.style.opacity = 1;
        queryInput.classList.add('error-border');
        return false;
    } else if (searchType === 'archives' && !regexArchives.test(query)) {
        errorMessage.innerText = 'Invalid archive keyword. Please enter a valid keyword.';
        errorMessage.style.opacity = 1;
        queryInput.classList.add('error-border');
        return false;
    } else {
        errorMessage.innerText = '';
        errorMessage.style.opacity = 0;
        queryInput.classList.remove('error-border');
        return true;
    }
}

/* Card Image Zoom */
document.addEventListener('DOMContentLoaded', function () {
    const cardImages = document.querySelectorAll('.card-image');

    cardImages.forEach((image) => {
        image.addEventListener('click', function () {
            image.classList.toggle('zoomed');
        });
    });
});

/* Card Image Zoom */
document.addEventListener('DOMContentLoaded', function () {
    const cardImages = document.querySelectorAll('.card-image');
    let zoomedImage = null;

    cardImages.forEach((image) => {
        image.addEventListener('click', function () {
            if (zoomedImage !== this) {
                zoomImage(this);
            } else {
                closeZoomedImage();
            }
        });
    });

    function zoomImage(image) {
        if (zoomedImage) {
            closeZoomedImage();
        }
        zoomedImage = image;
        zoomedImage.classList.add('zoomed');
        document.body.classList.add('zoomed');
        zoomedImage.addEventListener('click', closeZoomedImage);
        document.body.addEventListener(
            'click', handleClickOutsideZoomedImage);
    }

    function closeZoomedImage() {
        if (zoomedImage) {
            zoomedImage.classList.remove('zoomed');
            document.body.classList.remove('zoomed');
            zoomedImage.removeEventListener('click', closeZoomedImage);
            document.body.removeEventListener(
                'click', handleClickOutsideZoomedImage);
            zoomedImage = null;
        }
    }

    function handleClickOutsideZoomedImage(event) {
        if (!zoomedImage.contains(event.target)) {
            closeZoomedImage();
        }
    }
});

/* Response Pop-up */
document.addEventListener('DOMContentLoaded', function () {
    const responseButtons = document.querySelectorAll('.response-button');

    responseButtons.forEach((button) => {
        button.addEventListener('click', function () {
            const responseContent = button.dataset.responseContent;
            const escapedResponse = escapeHtml(responseContent);
            openPopup(escapedResponse);
        });
    });

    function openPopup(content) {
        const popup = document.createElement('div');
        popup.className = 'response-popup';
        popup.innerHTML = `
            <div class="popup-content">
                <span>HTTP Response</span><br>
                <pre>${content}</pre><br>
                <button class="close-button">Close</button>
            </div>
        `;

        popup.querySelector(
            '.close-button').addEventListener('click', function () {
            popup.remove();
        });

        document.body.appendChild(popup);
    }

    function escapeHtml(html) {
        return html.replace(/[\u00A0-\u9999<>&]/gim, function (i) {
            return '&#' + i.charCodeAt(0) + ';';
        });
    }
});
