
'use strict';

$(document).ready(function() {
    $('.content').hide();
    $('#taulak').show();
    $('#lda_menu').hide();
    window.location = $('#taulak_switch').attr("href");
    $('#taulak_switch').addClass('active');
});

$('.switch').click(function() {
    $('.switch').removeClass('active');
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
    $(this).addClass('active');
});

$('#number_btn').click(function() { 
    if ($('#form_kopurua').val()=="1") { 
        $('#menu').css('width', '16%'); 
        $('#display').css('width','84%');
        $('#display').css('left','16%');
        $('#nav').css('width','84%');
        $('#form1').css('width','50%');
        $('#not_form').css('width','50%');
        $('#form2').show();
        $('#form_kopurua').val("2"); 
        $('#number_btn').html("Itxi");

    } else{
        $('#menu').css('width', '8%'); 
        $('#display').css('width','92%');
        $('#display').css('left','8%');
        $('#nav').css('width','92%');
        $('#form1').css('width','100%');
        $('#not_form').css('width','100%');
        $('#form2').hide();
        $('#form_kopurua').val("1"); 
        $('#number_btn').html("Alderatu");
    }

}); 









$('#forms').on('submit', function(){
    var url = window.location.href; 
    var post_url;
    var form_data;       
    if (url.endsWith('#taulak')){
        post_url = $('#forms').data("taulak");
        console.log(post_url);
        form_data = new FormData(this);
        $.ajax({
                type:"POST",
                url : post_url,
                data: form_data,
                headers: {'X-CSRFToken': csrftoken},
                processData: false,
                contentType: false,
                success:function(response){
                    $("#taula1").empty();
                    $("#taula2").empty();
                    if (response.warn) {
                        alert(response.warn);
                    }
                    if (response.taula_err1.length > 0){
                        $("#taula1").append('<caption style="font-weight: bold">'+ response.titulua1 + '</caption>');
                        $("#taula1").append('<tr><th>Entitatea</th><th>M</th><th>Stopwords</th><th>M(stopwords)</th><th>Tf_idf</th><th>M(tf_idf)</th></tr>');
                        $.each(response.taula_err1, function(index,row){
                            var NewRow = '<tr>'; 
                            $.each(row,function(index,e){
                                NewRow += '<td>'+ e +'</td>';
                            });
                            NewRow += '</tr>';
                            $("#taula1").append(NewRow);
                        });    
                    }
                    
                    if(response.taula_err2.length > 0) {
                        $("#taula2").append('<caption style="font-weight: bold">'+ response.titulua2 + '</caption>');
                        $("#taula2").append('<tr><th>Entitatea</th><th>M</th><th>Stopwords</th><th>M(stopwords</th><th>Tf_idf</th><th>M(tf_idf)</th></tr>');
                        $.each(response.taula_err2, function(index,row){
                            var NewRow = '<tr>';
                            $.each(row,function(index,e){
                                NewRow += '<td>'+ e +'</td>';
                            });
                            NewRow += '</tr>';
                            $("#taula2").append(NewRow);
                        });
                    }
                },              
            });

    }else if (url.endsWith('#parteHartzeak')){
        post_url = $('#forms').data("parte-hartzeak");
        var form_data = new FormData(this);
        $.ajax({
            url: post_url,
            type:"POST",
            headers: {'X-CSRFToken': csrftoken},
            data: form_data,
            processData: false,
            contentType: false,
            success:function(response){
                $("#parteHartzeak1").empty();
                $("#parteHartzeak2").empty();

                if (response.warn) {
                    alert(response.warn);
                }

                if (response.parteHartze_err1.length > 0){
                    $("#parteHartzeak1").append('<h1>' + response.titulua1 + '</h1>');
                    var NewRow;
                    $.each(response.parteHartze_err1, function(index,r){
                        NewRow = '<p>' + r + '</p>'; 
                        $("#parteHartzeak1").append(NewRow);
                        if (index>20){
                            return false;
                        }
                    });
                }

                if (response.parteHartze_err2.length > 0){
                    $("#parteHartzeak2").append('<h1>' + response.titulua2 + '</h1>');
                    var NewRow;
                    $.each(response.parteHartze_err2, function(index,r){
                        NewRow = '<p>' + r + '</p>'; 
                        $("#parteHartzeak2").append(NewRow);
                        if (index>20){
                            return false;
                        }
                    });
                }          
            },
        });
        
    }else if (url.endsWith('#scatter')){
        post_url = $('#forms').data("scatter");
        form_data = new FormData(this);
        $.ajax({
            url: post_url,
            type:"POST",
            headers: {'X-CSRFToken': csrftoken},
            data: form_data,
            processData: false,
            contentType: false,
            success:function(response){
                if (response.warn) {
                    alert(response.warn);
                }
            },
        });
        console.log($('#scatter_iframe').data("scatter"));
        $('#scatter_iframe').attr("src", $('#scatter_iframe').data("scatter"));
    }

    return false;
});


$('#form_lda').on('submit', function(){
    var filter = $('input[name="filtroa"]:checked').val();
    var html = "";
    if (filter=="gizon"){
        html = "/static/bis/ldavis_gizon.html";

    }else if (filter=="emakume"){
        html = "/static/bis/ldavis_emakume.html";

    }else if (filter=="euskara"){
        html = "/static/bis/ldavis_euskara.html";

    }else if (filter=="gaztelera"){
        html = "/static/bis/ldavis_gaztelera.html";

    }else{
        html = "/static/bis/ldavis.html";
    }
    console.log(html)
    
    if (html!=$('#lda_iframe').attr("src")){
        $('#lda_iframe').attr("src", html);
    }

    return false;
});  


var get_hilabetea = function() {
    var get_url = $('.urtea').data("hilabete_handler");
    var select;

    switch (this.id) { 
        case 'urtea_h1': 
            select = $('#hilabetea_h1'); 
            break;
        case 'urtea_b1': 
            select = $('#hilabetea_b1'); 
            break;
        case 'urtea_h2': 
            select = $('#hilabetea_h2'); 
            break;		
        case 'urtea_b2': 
            select = $('#hilabetea_b2'); 
            break;
        default:
            alert('Nola aukeratu duzu urte hau?');
    }
    
    $.ajax({
        type:"GET",
        url : get_url,
        data : "urtea="+$(this).val(),
        success : function(response) {
            if (response.hilabeteak){
                select.empty();
                select.append('<option selected value=""></option>');
                $.each(response.hilabeteak, function(index, hilabetea) {         
                    select.append(
                            $('<option></option>').val(hilabetea).html(hilabetea)
                        );
                });
                select.prop('disabled', false);
            }else{
                select.empty();
                select.prop('disabled', 'disabled');
            }
        },
    });

    return false;
};

$('.urtea').change(get_hilabetea);

    // var sentiment_form = function(){
    //     console.log("Sentiment handler")
    //     var post_url = $('#forms').data("sentiments");
    //     var form_data = new FormData(this);
    //     $.ajax({
    //         url: post_url,
    //         type:"POST",
    //         data: form_data,
    //         processData: false,
    //         contentType: false,
    //         success:function(response){
    //             $("#sentiments").empty();

    //             if (response.warn) {
    //                 alert(response.warn);
    //             }else{
    //                 $("#sentiments").append(response.html);
    //             }
    //         },
    //     });
    // };


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');


