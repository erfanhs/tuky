if (Cookies.get('UserToken')) {
    window.location.href = '/';
}

$('.register-submit').click(function() {

    registration_error = $('.registration-error');
    button = $(this);
    last_inner = button.html();
    button.html('<i class="fa fa-spinner fa-spin"></i>');

    email = $('input[name="email"]').val();
    password = $('input[name="password"]').val();

    if (!email || !password) {
        registration_error.html('لطفا تمامی فیلد ها را پر کنید.');
        button.html(last_inner);
        return
    }

    if (!(/.*@.*\..{2,}/gm.test(email))) {
        registration_error.html('فرمت ایمیل وارد شده اشتباه می باشد !');
        button.html(last_inner);
        return
    }
    
    method = button.attr('id');
    URL = (method=='login') ? "/api/v1/login/" : "/api/v1/signup/";
    grecaptcha.ready(function() {
        grecaptcha.execute('6Lc_ndYUAAAAALHYgOdnhtSMXbpMJ71Ha574PT4p', {action: 'homepage'}).then(function(token) {

            let data = {
                password: password,
                email: email,
                recaptchaToken: token
            };


            let config = {
                headers: {
                    'X-CSRFToken': Cookies.get('csrftoken')
                }
            };

            axios.post(URL, data, config)
            .then(response => {
                if (method == 'signup') {
                    body_block = $('#body-block');
                    body_block.empty();
                    email_sent = `<h3 style="color: white; text-align: center; margin-top: 30px;">${response.data.response}</h3>`
                    body_block.append($(email_sent));
                }
                else if (method == 'login') {
                    token = response.data.token;
                    Cookies.set('UserToken', token);
                    localStorage['UserEmail'] = response.data.email;
                    window.location.href = "/";
                }
            })
            .catch(error => {
                registration_error.html(error.response.data.error);
                button.html(last_inner);
            });


        });
    });
});
