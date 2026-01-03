/* 
*****************************************************************
*  target.js                                                    *
*****************************************************************
*                                                               *
*                      This file is part of:                    *
*                        MOONVEIL PROJECT                       *
*                                                               *
*****************************************************************
*/

/* Deletion Prompt */
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.delete-form button').forEach(button => {
    button.addEventListener('click', event => {
        const confirmed = confirm(
            'Are you sure you want to delete this target project ?'
        );

        if (!confirmed) {
            event.preventDefault();
        }
    });
    });
});
