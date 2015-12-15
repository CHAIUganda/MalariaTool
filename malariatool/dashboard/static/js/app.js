$('#id_start_date, #id_end_date').datepicker({
    format: "yyyy-mm-dd",
    autoclose: true,
    todayHighlight: true
});

$('#id_affected_districts').select2();


$('#id_estimated_end_date').datepicker({
    format: "yyyy-mm-dd",
    autoclose: true,
    todayHighlight: true
});


$('.district-hover').popover();
$('.district-hover').popover({trigger: "hover"});