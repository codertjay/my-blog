 document.getElementById('like').addEventListener('click',loadUnlike_and_like);
 document.getElementById('unlike').addEventListener('click',loadUnlike_and_like);



function loadUnlike_and_like(){
    // Create Xhr object
    const xhr = new XMLHttpRequest()
    // Open - type, url/file, async
    const url = 'like_action/'
    xhr.open('GET',url)
    xhr.onload = function(){
        if (this.status == 200){
            var output = JSON.parse(this.response)
            console.log (this.response)

           var like = output.unlike
           var unlike = output.like
            console.log (like)
            console.log (unlike)

            document.getElementById('unlike').innerHTML = unlike + '<small>'+"unlike" + '</small>'
            document.getElementById('like').innerHTML = like + '<small>'+"Like" + '</small>'
        }
    }
    xhr.onerror = function(){
        alert('An error occurred. Please try again later ')
    }

    xhr.send()
    console.log (xhr.response)
    console.log ('post unliked ')
}

$(".comment-reply-btn").click(function (event) {
    event.preventDefault();
    $(".comment-reply").fadeToggle()

    // $(this).next(".comment-reply").fadeToggle()
})


