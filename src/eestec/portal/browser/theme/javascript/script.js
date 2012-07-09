(function ($) {
    $(function () {
        $('#mobile-globalnav').bind('click', function() {
            $('#portal-globalnav').toggleClass('visible');
            $('#portal-searchbox').removeClass('visible');
        });
    
        $('#mobile-search').bind('click', function() {
            $('#portal-searchbox').toggleClass('visible');
            $('#portal-globalnav').removeClass('visible');
        });
    
        $('#mobile-page-settings').bind('click', function() {
            $('#edit-bar').toggleClass('visible');
            $(this).toggleClass('selected');
        });
    });
    
}(jQuery));