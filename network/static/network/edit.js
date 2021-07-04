document.addEventListener('DOMContentLoaded', function() { 
    document.querySelectorAll('.postEdit').forEach(icon => {
        icon.addEventListener('click', function() {
            post_id = parseInt(this.dataset.editid);

            postContentP = document.querySelector(`[data-content="${post_id}"]`);

            postContent = postContentP.innerHTML;

            ta = document.createElement('textarea');

            ta.setAttribute("class", "form-control edit-post");
            ta.setAttribute("rows", "3");
            ta.setAttribute("maxlength", "200")

            ta.innerHTML = postContent;
            postContentP.style.display = 'none';
            iconGroup = document.querySelector(`.iconGroup-${post_id}`);
            iconGroup.style.display = "none";

            ta.appendAfter(document.querySelector(`.cardHeading-${post_id}`));

            saveBtn = document.createElement('button');
            saveBtn.setAttribute("class", "btn btn-sm btn-success mt-2 mr-2");
            saveBtn.setAttribute("style", "float:right; ");
            saveBtn.setAttribute('data-updatedid', `${post_id}`);
            saveBtn.innerHTML = "Save";
            saveBtn.appendAfter(ta);

            cancelBtn = document.createElement('button');
            cancelBtn.setAttribute("class", "btn btn-sm btn-danger mt-2 mr-1");
            cancelBtn.setAttribute("style", "float:right; ");
            cancelBtn.innerHTML = "Cancel";
            cancelBtn.appendAfter(ta);

            saveBtn.addEventListener('click', async function() {
                await fetch(`/editPost/${post_id}`, {
                    method: 'PUT',
                    body: JSON.stringify({
                        content: ta.value,
                    })
                  })
                  .then(response => response.json())
                  .then(result => { 
                    if(result.result == true) {
                        newContent = ta.value;

                        ta.remove();
                        saveBtn.remove();
                        cancelBtn.remove();
                        
                        postContentP.innerHTML = newContent;
                        postContentP.style.display = 'block';
                        iconGroup.style.display = 'block';

                        alert(result.message);

                    } else {
                        alert(result.message);
                    }
                  })
            });

            cancelBtn.addEventListener('click', function() {
                ta.remove();
                saveBtn.remove();
                cancelBtn.remove();

                postContentP.style.display = 'block';
                iconGroup.style.display = 'block';
            });


        });
    });


//appendAfter
Element.prototype.appendAfter = function (element) {
  element.parentNode.insertBefore(this, element.nextSibling);
},false;
    
//appendBefore
Element.prototype.appendBefore = function (element) {
    element.parentNode.insertBefore(this, element);
  },false;




});