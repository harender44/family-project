

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