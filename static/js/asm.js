/* 
*****************************************************************
*  asm.js                                                       *
*****************************************************************
*                                                               *
*                      This file is part of:                    *
*                        MOONVEIL PROJECT                       *
*                                                               *
*****************************************************************
*/

/* Load More */
document.addEventListener('DOMContentLoaded', function () {
    function loadMoreContent(buttonId, listId, hiddenListId) {
        const loadMoreButton = document.getElementById(buttonId);
        if (!loadMoreButton) return;

        const list = document.getElementById(listId);
        const hiddenList = document.getElementById(hiddenListId);

        function toggleLoadMoreButton() {
            if (hiddenList.children.length > 0) {
                loadMoreButton.style.display = 'block';
            } else {
                loadMoreButton.style.display = 'none';
            }
        }

        toggleLoadMoreButton();
        loadMoreButton.addEventListener('click', function () {
            const items = hiddenList.querySelectorAll('li');
            let loadedCount = 0;

            items.forEach(function (item, index) {
                if (loadedCount < 10) {
                    list.appendChild(item.cloneNode(true));
                    item.remove();
                    loadedCount++;
                }
            });
            toggleLoadMoreButton();
        });
    }

    loadMoreContent(
        'load-more-subdomains-button',
        'subdomains-list',
        'hidden-subdomains'
    );

    loadMoreContent(
        'load-more-archives-button',
        'archives-list',
        'hidden-archives'
    );

    loadMoreContent(
        'load-more-permutations-button',
        'permutations-list',
        'hidden-permutations'
    );

    loadMoreContent(
        'load-more-bruteforced-button',
        'bruteforced-list',
        'hidden-bruteforced'
    );
});
