

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

$(document).on('click','#add-relation', function(){
    $('#add-relation-form'.show(500));
})

$(document).on('click', '#delete-relation',function(){
    $.ajax({
        type : "post",
        url : "/user/delete_relation",
        data : $(this).val()
    })
})


