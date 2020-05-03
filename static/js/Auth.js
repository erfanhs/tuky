(function(){

    logged = function() {
        $('.navbar-nav.ml-auto').html(
            '<a href="" onclick="Cookies.remove(`UserToken`)" class="nav-item nav-link">خروج</a>' + 
            `<a href="/settings" class="nav-item nav-link">تنظیمات</a>`
        );
        shortner_inputs_script = document.createElement('script');
        shortner_inputs_script.setAttribute('src', '/static/js/shortner_inputs.js');
        $('#shortner-form').get(0).appendChild(shortner_inputs_script);
        getUserLinks(0);
    }

    guest = function() {
        recaptcha_script = document.createElement('script');
        recaptcha_script.setAttribute('src', 'https://www.google.com/recaptcha/api.js?render=6Lc_ndYUAAAAALHYgOdnhtSMXbpMJ71Ha574PT4p');
        document.body.appendChild(recaptcha_script);
        $('.navbar-nav.ml-auto').html(`<a href="/registration" class="nav-item nav-link">ورود / ثبت نام</a>`);
        if (location.pathname == '/') {
            imageAndText =
            `
            <div id="container2">
                <div>
                    <h2>مدیریت لینک ها، استفاده از دامنه های دلخواه و مشاهده آمار لینک.</h2>
                    <button onclick="window.location.href = \`/registration\`;">ورود / ثبت نام</button>
                </div>
                <img src="./static/images/stats.jpg" alt="کوتاه کننده لینک">
            </div>
            `;
            $(imageAndText).insertBefore('#container3');
            $('#loading-container').remove();
        }
        $("#checkbox").click(function () {
            alert('برای استفاده از این گزینه نیاز به لاگین دارید !');
        });
    }

    $(document).ready(function() {
        token = Cookies.get('UserToken');
        if (token) logged();
        else guest();
    });
    
})();