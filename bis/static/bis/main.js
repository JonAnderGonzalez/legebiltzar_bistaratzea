$(function() {
    'use strict';

        

















    $('#forms').on('submit', function(){
        // var mode = $('.active').attr('id');
        // switch (mode) {
        //     case 'tables_switch':
        //         tables_form();
        //         break;
        //     case 'participations_switch':
        //         participations_form();
        //         break;
        //     case 'scatter_switch':
        //         scatter_form();
        //         break;
        //     case 'sentiments_switch':
        //         sentiment_form();
        //         break;
        //     default:
        //         text = alert("Zerbait gaizki atera egin da.");
        // }  
        var form = $('#forms')
        var post_url = form.data("taulak");
        var form_data = new FormData(this);
        console.log(form_data)
        $.ajax({
            type:"POST",
            headers: {'X-CSRFToken': csrftoken},
            url : post_url,
            data: form_data,
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
                    $("#taula1").append('<tr><th>Entitatea</th><th>Maiztasuna</th><th>Tf_idf</th><th>Maiztasuna(tf_idf)</th></tr>');
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
                    $("#taula2").append('<tr><th>Entitatea</th><th>Maiztasuna</th><th>Tf_idf</th><th>Maiztasuna(tf_idf)</th></tr>');
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
            }
        });

        return false;
    };

    $('.urtea').change(get_hilabetea);

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
});
