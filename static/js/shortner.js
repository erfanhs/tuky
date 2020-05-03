function addToTable(link) {
    tbody = $('tbody');
    if (tbody.children().length == 15) {
        $('#next').prop('disabled', false);
        tbody.children().last().remove();
    }

    tr = addRow(link, tbody, true);
    tr.insertBefore(tbody.children().first());

    tr.find('.fa-copy').attr('data-original-title', 'Copy').hover(function(){
        $(this).tooltip('show');
    });

    if (tbody.children().last().html() == '<td colspan="5" style="width: 100 !importante; text-align: center;">! هیچ لینکی برای نمایش موجود نیست</td>')
        tbody.children().last().remove();
}


function showLink(link) {
    short_url = $('.site-title');
    short_url.css('direction', 'ltr');
    copy_b = 
    `
    <i class="fa fa-copy" onclick="copy('${link.short_url}', this)" data-original-title="Copy"></i>
    `;
    copy_b = $(copy_b);
    short_url.html(sliceText(link.short_url, 25));
    short_url.append(copy_b);
    copy_b.hover(function() {
        $(this).tooltip('show');
    });
    if ($('#checkbox-icon').hasClass('fa-minus')) $('#checkbox').trigger('click');
    $('#shortner-main :input').val('');
}



$('#shortner-submit').click(function() {

    link = $('input[name="long_url"]').val();
    if (!link) {
        alert('لطفا فیلد لینک را پر کنید !')
        return
    }
    url_id = $('input[name="url_id"]').val();
    password = $('input[name="password"]').val();
    expiration_date = $('input[name="expiration_date"]').val();

    $(this).html('<i class="fa fa-spinner fa-spin"></i>');

    let data = {
        long_url: link
    };

    let config = {
        headers: {
            'X-CSRFToken': Cookies.get('csrftoken'),
        }
    };

    UserToken = Cookies.get('UserToken');

    if (UserToken) {
        data['url_id'] = url_id;
        data['password'] = password;
        data['expiration_date'] = expiration_date;
        config.headers['Authorization'] = UserToken;
    } else {
        grecaptcha.ready(function() {
            grecaptcha.execute('6Lc_ndYUAAAAALHYgOdnhtSMXbpMJ71Ha574PT4p', {action: 'homepage'}).then(function(token) {
                data['recaptchaToken'] = token;
                axios.post("/api/v1/links/", data, config)
                .then(response => {
                    showLink(response.data);
                    $('#shortner-submit').html('کوتاه کن');
                })
                .catch(error => {
                    alert(error.response.data.error);
                    $('#shortner-submit').html('کوتاه کن');
                });
                
            });
        });
        return
    }

    axios.post("/api/v1/links/", data, config)
    .then(response => {
        showLink(response.data);
        addToTable(response.data);
        $(this).html('کوتاه کن');
    })
    .catch(error => {
        alert(error.response.data.error);
        $(this).html('کوتاه کن');
    });


});