function reveal() {
    var reveals = document.querySelectorAll(".reveal");
  
    for (var i = 0; i < reveals.length; i++) {
      var windowHeight = window.innerHeight;
      var elementTop = reveals[i].getBoundingClientRect().top;
      var elementVisible = 150;
  
      if (elementTop < windowHeight - elementVisible) {
        reveals[i].classList.add("active");
      } else {
        reveals[i].classList.remove("active");
      }
    }
  }
  
  window.addEventListener("scroll", reveal);

$(document).on('click',"#results button",function(e){
    d =  $(this).val()
    $.ajax({
        url: '/user/add_friend',
        type : 'post',
        data : {'id':d},
        beforeSend : function(){
            $(this).css('background','black'),
            $(this).attr("disabled",true)
        }
    })
    .done(function(response){
        if(response.success){
            $('#results').empty();
            $('#search').val("");
            $('#success_').text(response.success);
            $('#success_').show(1000)
            const timeo = setTimeout(function(){
                $('#success_').hide(500)
            }, 4000)
        }
    })
    e.preventDefault()
})

$(document).on('click','#accept-friend',function(){
    id = $(this).val()
    $.ajax({
        type : "post",
        url : "/user/accept_friend",
        data : {'id':id}
    })
})

$('.search_bar').ready(function(){
    $('#search').keyup(function(){
        var q = $(this).val();
        $("#results").empty()
        if (q.length >1){
            $.ajax({
                type : "post",
                url : "/user/search",
                cache : false,
                data : {'q':q},
            })
            .done(function(response){
                if(response.results){
                    response.results.forEach(r => {
                        $("#results").append("<li><p>"+r[1]+"</p><button value="+r[0]+">Add Friend</button><li>")
                    });
                }
            })
        }
    })
})

$(document).on('click','.add-relation-click',function(){
    id_ = $(this).attr('value');
    $('#add-relation-form form').attr({'name':id_});
    $('#add-relation-form').show(400);
})

$(document).on('submit','#add-relation-form form',function(){
    $.ajax({
        type : "post",
        url : "/user/add_relation",
        data : $(this).serialize()+"&id_="+$(this).attr('name')
    })
    .done(function(reponse){
        if (response.error){
            $('#error_').text(response.error);
            $('#error_').show(500);
            const timeo = setTimeout(function(){
                $('#error_').hide(500)
            }, 4000)
        }
    })
})

$(document).on('click', '.delete-relation-click',function(){
    alert($(this).attr('value'))
    $.ajax({
        type : "post",
        url : "/user/delete_relation",
        data : {"id_" : $(this).attr('value')}
    })
    .done(function(response){
        if (response.error){
            $('#error_').show(500);
            $('#error_').text(response.error);
            const timeo = setTimeout(function(){
                $('#error_').hide(500)
            }, 4000)
        }
        else{
            $('#success_').show(500);
            $('#success_').text(response.error);
            const timeo = setTimeout(function(){
                $('#success_').hide(500)
            }, 4000)
        }
    })
})


