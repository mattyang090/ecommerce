$(document).ready(function(){
    $('.login-info-box').fadeOut();
    $('.login-show').addClass('show-log-panel');
});


$('.login-reg-panel input[type="radio"]').on('change', function() {
    if($('#log-login-show').is(':checked')) {
        $('.register-info-box').fadeOut(); 
        $('.login-info-box').fadeIn();
        
        $('.white-panel').addClass('right-log');
        $('.register-show').addClass('show-log-panel');
        $('.login-show').removeClass('show-log-panel');
        
    }
    else if($('#log-reg-show').is(':checked')) {
        $('.register-info-box').fadeIn();
        $('.login-info-box').fadeOut();
        
        $('.white-panel').removeClass('right-log');
        
        $('.login-show').addClass('show-log-panel');
        $('.register-show').removeClass('show-log-panel');
    }
});
    // $.ajax({
    //   url: '/weight',
    //   method: 'get',
    //   data: "nah",
    //   success: function(duhdata){
    //     console.log("Received this from server: ", duhdata)
    //     console.log("I should probably put that in the DOM...")
    //   }
    // })
$(document).on('click','.category_button',function($e){
    $e.preventDefault()
    var text = $(this).text();
    $.get(`/categorize/${text}`,function(data,status){
        console.log(data)
        console.log(status)
        $('#target').html(data)
    });
});

$(document).on('click','.club_button',function($e){
    $e.preventDefault()
    var text = $(this).text();
    $.get(`/categorize/Clubs/${text}`,function(data,status){
        console.log(data)
        console.log(status)
        $('#target').html(data)
    });
});

$(document).on('click','.ball_button',function($e){
    $e.preventDefault()
    var text = $(this).text();
    $.get(`/categorize/Balls/${text}`,function(data,status){
        console.log(data)
        console.log(status)
        $('#target').html(data)
    });
});

$(document).on('click','.apparel_button',function($e){
    $e.preventDefault()
    var text = $(this).text();
    $.get(`/categorize/Apparel/${text}`,function(data,status){
        console.log(data)
        console.log(status)
        $('#target').html(data)
    });
});

$(document).on('click','.brand_button',function($e){
    $e.preventDefault()
    var text = $(this).text();
    $.get(`/categorizebrand/${text}`,function(data,status){
        console.log(data)
        console.log(status)
        $('#target').html(data)
    });
});

