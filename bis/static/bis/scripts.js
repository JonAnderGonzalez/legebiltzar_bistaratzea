$(function() {
    'use strict';

    $(document).ready(function() {
        $('.content').hide();
        $('#tables').show();
        $('#lda_menu').hide();
        $('#tables_switch').addClass('active')
    });
    
    $('.switch').click(function() {
        $('.switch').removeClass('active')
        var display = $(this).attr("href");
        $('.content').hide();
        if (display=="#lda"){
            $('#menu').hide();
            $('#lda_menu').show();
        }else{
            $('#menu').show();
            $('#lda_menu').hide();
        }
        $(display).show();
        $(this).addClass('active')
    });

    $('#number_btn').click(function() { 
        if ($('#form_number').val()=="1") { 
            $('#menu').css('width', '20%'); 
            $('#display').css('width','80%');
            $('#display').css('left','20%');
            $('#nav').css('width','80%');
            $('#form1').css('width','50%');
            $('#not_form').css('width','50%')
            $('#form2').show();
            $('#form_number').val("2"); 
            $('#number_btn').html("Itxi");
    
        } else{
            $('#menu').css('width', '10%'); 
            $('#display').css('width','90%');
            $('#display').css('left','10%');
            $('#nav').css('width','90%');
            $('#form1').css('width','100%');
            $('#not_form').css('width','100%')
            $('#form2').hide();
            $('#form_number').val("1"); 
            $('#number_btn').html("Alderatu");
        }
    
    }); 


    var participations_form = function(){
        var post_url = $('#forms').data("participations");
        var form_data = new FormData(this);
        $.ajax({
            url: post_url,
            type:"POST",
            data: form_data,
            processData: false,
            contentType: false,
            success:function(response){
                $("#participations1").empty();
                $("#participations2").empty();

                if (response.warn) {
                    alert(response.warn);
                }

                if (response.participation_rows1.length > 0){
                    $("#participations1").append('<h1>' + response.title1 + '</h1>');
                    var NewRow;
                    $.each(response.participation_rows1, function(index,r){
                        NewRow = '<p>' + r + '</p>'; 
                        $("#participations1").append(NewRow);
                        if (index>20){
                            return false;
                        }
                    });
                }

                if (response.participation_rows2.length > 0){
                    $("#participations2").append('<h1>' + response.title2 + '</h1>');
                    var NewRow;
                    $.each(response.participation_rows2, function(index,r){
                        NewRow = '<p>' + r + '</p>'; 
                        $("#participations2").append(NewRow);
                        if (index>20){
                            return false;
                        }
                    });
                }          
            },
        });
    };
    
    var scatter_form = function(){
        var post_url = $('#forms').data("scatter");
        var form_data = new FormData(this);
        $.ajax({
            url: post_url,
            type:"POST",
            data: form_data,
            processData: false,
            contentType: false,
            success:function(response){
                if (response.warn) {
                    alert(response.warn);
                }        
            },
        });
        $('#scatter_iframe').attr("src", $('#scatter_iframe').attr("src"));
    };

    var sentiment_form = function(){
        console.log("Sentiment handler")
        // var post_url = $('#forms').data("sentiments");
        // var form_data = new FormData(this);
        // $.ajax({
        //     url: post_url,
        //     type:"POST",
        //     data: form_data,
        //     processData: false,
        //     contentType: false,
        //     success:function(response){
        //         $("#sentiments").empty();

        //         if (response.warn) {
        //             alert(response.warn);
        //         }else{
        //             $("#sentiments").append(response.html);
        //         }
        //     },
        // });
    };

    if ($('#lda_id').hasClass('active')){
        setInterval(function(){   
            console.log($('#lda_iframe').attr("src"))
            var filter = $('input[name="filtroa"]:checked').val();
            var html = "";
            if (filter=="Gizon"){
                html = "/static/vis/ldavis_gizon.html";
    
            }else if (filter=="Emakume"){
                html = "/static/vis/ldavis_emakume.html";
    
            }else if (filter=="Euskara"){
                html = "/static/vis/ldavis_euskara.html";
    
            }else if (filter=="Gaztelera"){
                html = "/static/vis/ldavis_gaztelera.html";
    
            }else{
                html = "/static/vis/ldavis.html";
            }
            if (html!=$('#lda_iframe').attr("src")){
                $('#lda_iframe').attr("src", html);
            }
        }, 2000);
    }
});
