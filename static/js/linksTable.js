function updateLink(url_id_, long_url_, expiration_date_, el) {

    $(el).html('<i class="fa fa-spinner fa-spin"></i>');

    url_id = $('#url_id_').val();
    if (!url_id) url_id = url_id_;
    long_url = $('#long_url_').val();
    if (!long_url) long_url = long_url_;
    expiration_date = $('#expiration_date_').val();
    if (!expiration_date) expiration_date = expiration_date_;

    let data = {
        'url_id': url_id,
        'long_url': long_url,
    }
    let config = {
        'headers': {
            'Authorization': Cookies.get('UserToken'),
            'X-CSRFToken': Cookies.get('csrftoken')
        }
    }

    if (expiration_date != '---') data['expiration_date'] = expiration_date;

    axios.put('/api/v1/links/'+url_id_+'/', data, config)
    .then(response => {

        $(el).html('ویرایش');
        $('#modal').remove();
        $('body').removeClass('stop-scrolling');

        old_tr = $(`tr[name='${url_id_}']`);
        next_el = old_tr.next();
        old_tr.remove();
        new_tr = addRow(response.data, $('tbody'), return_row=true);
        if (next_el.length)
            new_tr.insertBefore(next_el);
        else
            $('tbody').append(new_tr);
        
    })
    .catch(error => {
        alert(error.response.data.error);
        el.innerHTML = 'ویرایش';
    });
}



function openQrModal(qr_img) {
    modal = 
    `
    <div id="modal">
        <div class="modal-content" id="qr-modal-content">
            <img src="${qr_img}" id="qr_img"/>
        </div>
    </div>
    `;
    modal = $(modal);
    $('body').append(modal);
    $('body').addClass('stop-scrolling');
    
    window.onclick = function(event) {
        if (event.target == modal.get(0)) {
            modal.remove();
            $('body').removeClass('stop-scrolling');
        }
    }
}


function openEditModal(url_id, long_url, expiration_date) {
    modal = 
    `
    <div id="modal">
        <div class="modal-content">
            <span class="close">&times;</span>
            <div id="update-form-container">
                <h4>ویرایش لینک</h4>
                <label for="long_url_">لینک بلند:</label>
                <input type="text" name="long_url" id="long_url_" value="${long_url}" placeholder="لینک بلند .."/>
                <br>
                <br>
                <label for="url_id_">لینک کوتاه:</label>
                <input type="text" name="url_id" id="url_id_" value="${url_id}" placeholder="آدرس دلخواه لینک کوتاه .."/>
                <br>
                <br>
                <label for="expiration_date_">تاریخ انقضا:</label>
                <input type="text" name="expiration_date" id="expiration_date_" value="${expiration_date == '---' ? '' : expiration_date}" placeholder="تاریخ انقضا .."/>
                <br><br>
                <button onclick="updateLink('${url_id}', '${long_url}', '${expiration_date}', this)">ویرایش</button>
            </div>
        </div>
    </div>
    `;
    modal = $(modal);
    $('body').append(modal);

    const today = new Date();
    const tomorrow = new Date(today);
    tomorrow.setDate(tomorrow.getDate() + 1);
    flatpickr(document.getElementById('expiration_date_'), {
        'disableMobile': true,
        'minDate': tomorrow,
        'dateFormat': 'Y/m/d'
    });


    $('body').addClass('stop-scrolling');

    window.onclick = function(event) {
        if (event.target == modal.get(0)) {
            modal.remove();
            $('body').removeClass('stop-scrolling');
        }
    }

    $('.close').click(function() {
        modal.remove();
        $('body').removeClass('stop-scrolling');
    });
    
}


function deleteUrl(url_id, el) {
    el = $(el);
    el.removeClass();
    el.addClass('fa fa-spinner fa-spin');
    el.css('color', 'red');

    skip = parseInt($('table').attr('skip'));

    let config = {
        'headers': {
            'Authorization': Cookies.get('UserToken'),
            'X-CSRFToken': Cookies.get('csrftoken')
        }
    }
    axios.delete('/api/v1/links/'+url_id, config)
    .then(response => {
        $(`tr[name='${url_id}']`).remove();
        search = $('input[name="search"]').val();
        url = `/api/v1/links?all=false&limit=16&skip=${skip}`
        if (search) url += `&search=${search}`
        axios.get(url, config)
        .then(response => {
            data = response.data;
            if (data.length < 15) {
                if (!data.length) {
                    if (!$('#back').prop('disabled')) $('#back').trigger('click');
                    $('tbody').html('<tr><td colspan="5" style="width: 100 !importante; text-align: center;">! هیچ لینکی برای نمایش موجود نیست</td></tr>');
                }
                $('#next').prop('disabled', true);
            } else {
                if (data.length == 15) {
                    link = data[data.length-1];
                    $('#next').prop('disabled', true);
                } else {
                    link = data[data.length-2];
                }
                tr = addRow(link, $('tbody'));
            }
        })
        .catch(error => {
        });
    })
    .catch(error => {
    });
}

function addRow(link, tbody, return_row=false) {
    tr = 
    `
    <tr name="${link['url_id']}">
        <td></td>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
    </tr>
    `;
    tr = $(tr);

    result = link['dateTime'].match(/(\d*)-(\d*)-(\d*)T(\d*):(\d*):/i);
    dateTime = result[1] + '/' + result[2] + '/' + result[3] + ' ' + result[4] + ':' + result[5];
    if (!link['expiration_date']) {
        expiration_date = '---';
    } else {
        result = link['expiration_date'].match(/(\d*)-(\d*)-(\d*)T/i);
        expiration_date = result[1] + '/' + result[2] + '/' + result[3];
    }

    TDs = tr.children();
    TDs.eq(0).html(`<a href="${link['long_url']}" target="_blank">${sliceText(link['long_url'], 52)}</a>`);
    TDs.eq(1).html(dateTime);
    TDs.eq(2).html(expiration_date);
    TDs.eq(3).html(`<i class="fas fa-copy" style="float: left;" onclick='copy("${link['short_url']}", this)'></i><h6 style="float: left; margin-left: 5px">${sliceText(link['short_url'], 39)}</h6>`);
    statsButton = `<i class="fas fa-chart-bar" title="آمار کلیک" onclick="window.location.href='${link['stats']}'"></i>`;
    views_count_td_content = 
    `
    ${link['views_count']}
    <div id="link-controller">
        ${(link['expired']) ? "<i class='fa fa-warning' title='! این لینک منقضی شده است'></i>":''}
        ${(link['banned']) ? "<i class='fa fa-ban' title='! این لینک به دلیل محتوای نامناسب بن شده است'></i>":''}
        ${link['has_password'] ? "<i class='fas fa-lock' title='.این لینک دارای رمز عبور است'></i>":""}
        ${(link['views_count']>0) ? statsButton:''}
        <i class="fas fa-edit" title="ویرایش" onclick="openEditModal('${link['url_id']}', '${link['long_url']}', '${expiration_date}')"></i>
        <i class="fas fa-qrcode" title="QR کد" onclick="openQrModal('${link['qr_img']}')"></i>
        <i class="fas fa-trash-alt" title="حذف" onclick="deleteUrl('${link['url_id']}', this)"></i>
    </div>
    `;
    TDs.eq(4).html(views_count_td_content);

    if (return_row) return tr;
    tbody.append(tr);
}


function getUserLinks(skip, button=null, search=null) {

    if (button) $(button).html('<i class="fa fa-spinner fa-spin"></i>');

    table_container = 
    `
    <div id="table-container">
        <table skip="${skip}">
            <thead>
                <th>لینک اصلی</th>
                <th>تاریخ ایجاد</th>
                <th>تاریخ انقضا</th>
                <th>لینک کوتاه</th>
                <th>تعداد بازدید</th>
            </thead>
            <tbody>
            </tbody>
        </table>
    </div>
    `;
    table_container = $(table_container);

    let config = {
        'headers': {
            'Authorization': Cookies.get('UserToken'),
            'X-CSRFToken': Cookies.get('csrftoken')
        }
    }

    search = $('input[name="search"]').val();
    url = `/api/v1/links?all=false&limit=15&skip=${skip}`
    if (search) url += `&search=${search}`

    axios.get(url, config)
    .then(response => {

        links = response.data;

        if (!links.length) table_container.find('tbody').html('<tr><td colspan="5" style="width: 100 !importante; text-align: center;">! هیچ لینکی برای نمایش موجود نیست</td></tr>');

        for (var i=0; i<links.length; i++) addRow(links[i], table_container.find('tbody'));

        $('#loading-container').remove();
        $('#table-container').remove();
        $('#table-controller').remove();

        table_container.insertBefore('#container3');

        table_controller = 
        `
        <div id="table-controller">
            <button onclick="getUserLinks(${skip-15}, this)" id="back"><i class="fa fa-angle-left"></i></button>
            <button onclick="getUserLinks(${skip+15}, this)" id="next" style="margin-left: 4px;"><i class="fa fa-angle-right"></i></button>
        </div>
        `;
        $(table_controller).insertBefore('#container3');
 
        if (links.length < 15) $('#next').prop( "disabled", true);
        if (skip == 0) $('#back').prop("disabled", true);

        $('#search-loading').remove();
        if (!$('#search-container').length) {
            search = 
            `
            <div id="search-container">
                <input type="text" name="search" placeholder=".. جستجو در لینک ها" style="float: right"/>
            </div>
            `;
            search = $(search)
            search.insertBefore('#table-container');
            search.keypress(function(e) {
                var keycode = (event.keyCode ? event.keyCode : event.which);
                if (keycode == '13') {
                    search_input = $('input[name="search"]');
                    $('#search-container').append('<i class="fa fa-spinner fa-spin" id="search-loading"></i>');
                    getUserLinks(parseInt($('table').attr('skip')), null, search_input.val());
                }
            });
        }


        $('#container3').css('margin-top', '100px');

        setTimeout(function() {
            $('.fa-copy').attr('data-original-title', 'Copy')
            .hover(function () {
                $(this).tooltip('show');
            });
        }, 600);

    })
    .catch(error => {
    });

}


$('<div id="loading-container"><i class="fa fa-spinner fa-spin"></i></div>').insertAfter('#shortner-main');