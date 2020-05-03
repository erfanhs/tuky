(function(){

    removeResponse = function() {
        setTimeout(function() {
            $('.settings-response').html('');
            $('.settings-response').css('color', 'red');
        }, 2000);
    }

    
    $('#reset-password').click(function() {
        opassword = $('input[name="opassword"]').val();
        npassword = $('input[name="npassword"]').val();
        if (!opassword || !npassword) {
            $('#reset-password-response').html('لطفا تمامی فیلد ها را پر کنید !');
            removeResponse();
            return
        }
        $(this).html('<i class="fa fa-spinner fa-spin"></i>');
        let data = {
            opassword: opassword,
            npassword: npassword
        }
        let config = {
            headers: {
                'X-CSRFToken': Cookies.get('csrftoken'),
                'Authorization': Cookies.get('UserToken')
            }
        }
        axios.post('/api/v1/change-password/', data, config)
        .then(response => {
            $('#reset-password-response').html(response.data.response);
            $('#reset-password-response').css('color', 'green');
            $(this).html('تغییر');
            removeResponse();
        })
        .catch(error => {
            $('#reset-password-response').html(error.response.data.error);
            $(this).html('تغییر');
            removeResponse();
        });
    });


    $('#del-acc').click(function() {
        password = $('input[name="password"]').val();
        
        if (!password) {
            $('#del-acc-response').html('لطفا تمامی فیلد ها را پر کنید !');
            removeResponse();
            return
        }

        $(this).html('<i class="fa fa-spinner fa-spin"></i>');
        let data = {
            password: password,
        }
        let config = {
            headers: {
                'X-CSRFToken': Cookies.get('csrftoken'),
                'Authorization': Cookies.get('UserToken')
            }
        }
        axios.post('/api/v1/delete-account/', data, config)
        .then(response => {
            $('#del-acc-response').html(response.data.response);
            $('#del-acc-response').css('color', 'green');
            $(this).html('حذف');
            Cookies.remove('UserToken');
            location.replace('/');
        })
        .catch(error => {
            $('#del-acc-response').html(error.response.data.error);
            $(this).html('حذف');
            removeResponse();
        });


    });


})();