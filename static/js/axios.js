axios.interceptors.response.use(function (response) {
    return response;
}, function (error) {
    status_code = error.response.status
    // handle unauthorized error
    if (status_code == 401) {
        $('#body-block').empty();
        $('#body-block').append('<div style="color:white; width: 80%; margin-top:50px; margin-right: 10%; text-align: center;"><h2>خطا در احراز هویت !</h2></div>');
    }
    // handle server errors
    else if (status_code.toString()[0] == '5') {
        $('#body-block').empty();
        $('#body-block').append('<div style="color:white; width: 80%; margin-top:50px; margin-right: 10%; text-align: center;"><h2>سایت فعلا در دسترس نیست ! خطای سرور</h2></div>');
    }
    return Promise.reject(error);
});