$('#report-submit').click(function() {
    response_ = $('#report-response');
    button = $(this);

    link = $('input[name="short_url"]').val();
    if (!link) {
        response_.html('لطفا فیلد لینک را کامل کنید !');
        return
    }

    button.html('<i class="fa fa-spinner fa-spin"></i>');

    axios.get(`/api/v1/report?short_url=${link}`)
    .then(response => {
        response_.css('color', '#06b841');
        response_.html(response.data.response);
        button.html('گزارش');
    })
    .catch(error => {
        response_.css('color', 'red');
        response_.html(error.response.data.error);
        button.html('گزارش');
    });     
});
