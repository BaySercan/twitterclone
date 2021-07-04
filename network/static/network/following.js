document.addEventListener('DOMContentLoaded', function() {
    console.log("Following page loaded");

    document.querySelectorAll('.like').forEach(button => {
        button.addEventListener('click', function() {
            post_id = this.dataset.postid
            like(post_id);
        })
    });

});
