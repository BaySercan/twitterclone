document.addEventListener('DOMContentLoaded', function() {
    console.log("Index page loaded");
    document.querySelector('textarea').value = "";

    document.querySelectorAll('.like').forEach(button => {
        button.addEventListener('click', function() {
            post_id = this.dataset.postid
            like(post_id);
        })
    });

    document.querySelector('form').onsubmit = function (event) {
        event.preventDefault();

        fetch('/newPost', {
            method: 'POST',
            body: JSON.stringify({
                content: document.querySelector('textarea').value,
            })
          })
          .then(response => response.json())
          .then(result => {
              // Print 
              document.querySelector('textarea').value = "";

              newPostDiv = document.createElement('div');
              newPostDiv.setAttribute("class", "card mb-1 newPost");

              newPostDiv.innerHTML = `<div class="card-body">
                  <div style="display: flex; justify-content: space-between; vertical-align: middle;">
                      <a href="#" style="text-decoration: none; color: black; margin: 0px; vertical-align: middle;">
                          <h5 class="card-title" style="font-weight: 600; margin: 0px;">${result.userName}</h5>
                      </a>
                      <h6 class="card-subtitle mb-2 text-muted" style="margin: 0px !important;">${result.created}</h6>
                  </div>
                  <p class="card-text ml-3 mt-2">${result.content}</p>
                  <a href="javascript:void(0)" class="card-link ml-3" onclick="like(${result.post_id})">
                      <i class="fa fa-heart-o" style="font-size:24px; color:red" data-postid="${result.post_id}"></i>
                      </a><p style="font-weight: 500; display: inline;" id="${result.post_id}">0</p>
                  <a href="#" class="card-link ml-3"><i class="fa fa-edit" style="font-size: 24px;"></i></a>
              </div>`;

              document.querySelector("#latestPostsSection").insertAdjacentElement('afterbegin', newPostDiv);
              
              console.log(result);
                
          });
      
          return false;
    };

});


