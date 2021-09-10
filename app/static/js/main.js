
// Datetime
$(document).ready(function () {
    $('.date').dateDropper({

    });
});


// Timepicker
$(document).ready(function(){
    $('#time').timepicker({
        timeFormat: 'HH:mm',
        interval: 30,
        scrollbar: true,
        minTime: '08:00',
        maxTime: '20:00',
        size: "20px",
        use24hours: true
    });
});





//Nav
// Menu-toggle button

$(document).ready(function () {
    $(".menu-icon").on("click", function () {
      $("nav ul").toggleClass("showing");
    });
    
  
  });