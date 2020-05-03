(function() {
    advanced_form =
    `
    <div id="optional-inputs" style="display: none">
        <label for="url_id">${location.host}/</label>
        <input type="text" name="url_id" id="url_id" placeholder="آدرس دلخواه"/>
        <input type="password" name="password" placeholder="رمز عبور"/>
        <input type="text" name="expiration_date" id="expiration_date" placeholder="تاریخ انقضا لینک"/>
    </div>
    `;
    advanced_form = $(advanced_form);
    $('#shortner-form').append(advanced_form);
    today = new Date();
    tomorrow = new Date(today);
    tomorrow.setDate(tomorrow.getDate() + 1);
    flatpickr($('#expiration_date').get(0), {
        'disableMobile': true,
        'minDate': tomorrow,
        'dateFormat': 'Y/m/d'
    });
    checkbox_icon = $('#checkbox-icon');
    $('#checkbox').click(function() {
        if (checkbox_icon.hasClass('fa-plus')) {
            advanced_form.css('display', 'block');
            checkbox_icon.addClass('fa-minus');
            checkbox_icon.removeClass('fa-plus');
        }
        else {
            advanced_form.css('display', 'none');
            checkbox_icon.addClass('fa-plus');
            checkbox_icon.removeClass('fa-minus');
        }
    });
})();