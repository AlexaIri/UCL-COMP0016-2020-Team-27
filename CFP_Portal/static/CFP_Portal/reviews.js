$(document).ready(function() {
    $("#btnFetch").click(function() {
    // disable button
    $(this).prop("disabled", true);
    // add spinner to button
    $(this).html(
    '<i class="fa fa-circle-o-notch fa-spin"></i> loading...'
    );
    });
    });

autocollapse(); // when document first loads
/************************/

/* loading button */
$('#loadingBtn').click(function () {
    var btn = $(this);
    btn.button('loading');
    
    // perform ajax processing here is reset button when complete
    setTimeout(function() {
    btn.button('reset');
    }, 2000);
    
});
/************************/
