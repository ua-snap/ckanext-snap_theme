$('#additional_info_toggler').on('click', function() {
    if ($('#additional_info_wrapper').hasClass('in')) {
        $('#additional_info_toggler').html('Show additional information about this dataset&hellip;');
    } else {
        $('#additional_info_toggler').text('Hide additional information');
    }
});
