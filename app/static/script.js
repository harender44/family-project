

$(document).on('click',".letknow",function(e){
    d =  $(this).val()
    $.ajax({
        url: '/user/letknow',
        type : 'post',
        data : {'id':d},
        beforeSend : function(){
            $(this).css('background','black'),
            $(this).attr("disabled",true)
        }
    })
    .done(function(){
        $(this).hide()
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
                    alert(response.results)
                    response.results.forEach(r => {
                        $("#results").append("<li><p>"+r[1]+"</p><button value="+r[0]+">Add Friend</button><li>")
                    });
                }
            })
        }
    })
})