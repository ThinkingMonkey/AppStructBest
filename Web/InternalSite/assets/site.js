// vim:encoding=utf-8:ts=2:sw=2:expandtab

$(document).ready(function(){
    $('.attribute-detail-table tbody tr').mouseover(function(){
      $(this).find('td span').removeClass('display-none').addClass('display-block');
    });
    $('.attribute-detail-table tbody tr').mouseout(function(){
      $(this).find('td span').removeClass('display-block').addClass('display-none');  
    });
});


