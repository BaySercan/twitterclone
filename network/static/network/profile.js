document.addEventListener('DOMContentLoaded', function() {
    console.log("Profile page loaded");

    document.querySelector('.follow').addEventListener('click', function() {
            profile_user_id = parseInt(this.dataset.profiluserid);
            follow(profile_user_id);
    });

    document.querySelectorAll('.like').forEach(button => {
        button.addEventListener('click', function() {
            post_id = this.dataset.postid
            like(post_id);
        })
    });
    
});

async function follow(profile_user_id) {
    button = document.querySelector(`[data-profiluserid="${profile_user_id}"]`)
    followersCount = parseInt(document.getElementById('followers').innerHTML);
    await fetch(`/follow/${profile_user_id}`, {
        method:'PUT',
        }).then(response => response.json()).then(data => {
            console.log(data.is_following)
             if (data.is_following == true) {
                 button.classList.remove("btn-primary");
                 button.classList.add("btn-outline-primary");
                 button.innerHTML = "Unfollow";
                 followersCount += 1;
              } else {
                 button.classList.remove("btn-outline-primary");
                 button.classList.add("btn-primary");
                 button.innerHTML = "Follow";
                 followersCount -= 1;
              }
               
              document.getElementById('followers').innerHTML = followersCount;
       });
 };

 