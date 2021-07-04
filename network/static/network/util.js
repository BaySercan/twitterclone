async function like(post_id) {
    button = document.querySelector(`[data-postid="${post_id}"]`)
    console.log(`Like button for post: (${post_id}) clicked`);
    likeCount = parseInt(document.getElementById(post_id).innerHTML);
    console.log(`İşlem öncesi like sayısı: ${likeCount}`)
     await fetch(`/likeUnlike/${post_id}`, {
       method: 'PUT',
       headers: {ignoreCache: false,},
       }).then(response => response.json()).then(data => {
            if (data.is_liked == true) {
                button.classList.remove("fa-heart-o");
                button.classList.add("fa-heart");
                likeCount += 1;
             } else {
                button.classList.remove("fa-heart");
                button.classList.add("fa-heart-o");
                likeCount -= 1;
             }
              console.log(`İşlem sonrası like sayısı: ${likeCount}`)
              document.getElementById(post_id).innerHTML = likeCount;
      });
 } 

 async function like(post_id) {
    button = document.querySelector(`[data-postid="${post_id}"]`)
    console.log(`Like button for post: (${post_id}) clicked`);
    likeCount = parseInt(document.getElementById(post_id).innerHTML);
    console.log(`İşlem öncesi like sayısı: ${likeCount}`)
     await fetch(`/likeUnlike/${post_id}`, {
       method: 'PUT',
       headers: {ignoreCache: false,},
       }).then(response => response.json()).then(data => {
            if (data.is_liked == true) {
                button.classList.remove("fa-heart-o");
                button.classList.add("fa-heart");
                likeCount += 1;
             } else {
                button.classList.remove("fa-heart");
                button.classList.add("fa-heart-o");
                likeCount -= 1;
             }
              console.log(`İşlem sonrası like sayısı: ${likeCount}`)
              document.getElementById(post_id).innerHTML = likeCount;
      });
 } 