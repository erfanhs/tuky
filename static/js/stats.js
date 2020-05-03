(function(){


    $(window).resize(function() {
        if (this.resizeTO) clearTimeout(this.resizeTO);
        this.resizeTO = setTimeout(function() {
            $(this).trigger('resizeEnd');
        }, 300);
    });

    var width = $(window).width();
    $(window).on('resizeEnd', function() {
        if ($(this).width() != width) {
            width = $(this).width();
            drawRegionsMap();
        }
    });

    google.charts.load('current', {'packages':['geochart'], 'mapsApiKey': 'AIzaSyD-9tSrke72PouQMnMX-a7eZSW0jkFMBWY'});

    function drawRegionsMap(countries_json) {

        map_chart = document.getElementById('map-chart');

        if (countries_json) {
            countries = Object.keys(countries_json);
            clicks = Object.values(countries_json);
            data = [['Country', 'Clicks']];
            for (var i=0; i<countries.length; i++) {
                data.push([ countries[i], clicks[i] ]);
            }
            window.map_data = data;
        }
        data = google.visualization.arrayToDataTable( window.map_data );
        var mapchart = new google.visualization.GeoChart(map_chart);
        options = {};
        mapchart.draw(data, options);
    }



    function randomRGB() {
        return `rgb(${Math.floor(Math.random() * 150)},${Math.floor(Math.random() * 150)},${Math.floor(Math.random() * 150)})`
    }



    function getNewCanvas(id) {
        canvas = $(`#${id}`);
        parent = canvas.parent();
        canvas.remove();
        if (id == 'timeLine') {
            parent.append(`<canvas id="${id}"></canvas>`);
            NewCanvas = $(`#${id}`);
            NewCanvas.attr('height', 100);
        }
        else {
            parent.append(`<canvas class="pie" id="${id}"></canvas>`);
            NewCanvas = $(`#${id}`);
            NewCanvas.attr({'width': 100, 'height': 70});
        }
        return NewCanvas;
    }


    time_line_labels = {};
    function setTimeLineLabels() {
        // lastDay
        now = moment();
        labels = [];
        labels.push(now.format('HH:00'));
        for (var i=1; i<24; i++) labels.push(now.subtract(1, 'hour').format('HH:00'));
        labels.reverse();
        time_line_labels['lastDay'] = labels;
        // lastWeek
        now = moment();
        labels = [];
        labels.push(now.format('MMM D'));
        for (var i=1; i<7; i++) labels.push(now.subtract(1, 'days').format('MMM D'));
        labels.reverse();
        time_line_labels['lastWeek'] = labels;
        // lastMonth
        now = moment();
        labels = [];
        labels.push(now.format('MMM D'));
        for (var i=1; i<30; i++) labels.push(now.subtract(1, 'days').format('MMM D'));
        labels.reverse();
        time_line_labels['lastMonth'] = labels;
        // allTime
        now = moment();
        labels = [];
        labels.push(now.format('MMM Y'));
        for (var i=1; i<18; i++) labels.push(now.subtract(1, 'months').format('MMM Y'));
        labels.reverse();
        time_line_labels['allTime'] = labels;
    }

    function showStats(data) {


        $('#total-clicks').html(data['totalClicks']);

        pie_charts_json = {
            os: 'تفکیک بر اساس سیستم عامل',
            browser: 'تفکیک بر اساس مرورگر',
            device: 'تفکیک بر اساس دستگاه'
        }

        Object.keys(pie_charts_json).forEach((item, index) => {
            ctx = getNewCanvas('pie-'+item);
            backgroundColors = [];
            for (var i=0; i<Object.keys(data[item]).length; i++) backgroundColors.push(randomRGB());
            
            var item_chart = new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: Object.keys(data[item]),
                    datasets: [{
                        data: Object.values(data[item]),
                        backgroundColor: backgroundColors
                    }]
                },
                options: {
                    title: {
                        display: true,
                        text: pie_charts_json[item],
                        fontFamily: "'Vazir', sans-serif",
                        fontStyle: "normal",
                        fontSize: 20
                    }
                }
            });
        
        });


        var ctx = getNewCanvas('timeLine');

        var timeLine = new Chart(ctx, {
            type: 'line',
            data: {
                labels: time_line_labels[data['time_interval']],
                datasets: [{
                    data: data['timeLine'],
                    borderWidth: 1,
                    pointRadius: 2,
                    pointHoverRadius: 2,
                    pointBackgroundColor: '#81a8db',
                    backgroundColor: 'rgba(149, 185, 245, 0.5)'
                }]
            },
            options: {
                title: {
                    display: true,
                    text: 'گزارش تعداد کلیک در بازه زمانی',
                    fontFamily: "'Vazir', sans-serif",
                    fontStyle: "normal",
                    fontSize: 20
                },
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                },
                legend: {
                    display: false
                }
            }
        });

        $('#map-chart').remove();
        map_chart = $('<div id="map-chart"></div>');
        map_chart.insertBefore('.timeLine');
        drawRegionsMap(data['country']);
        
    }

    window.onload = function() {

        url_id = window.location.pathname.split('/').slice(-1)[0]
        let config = {
            headers: {
                'X-CSRFToken': Cookies.get('csrftoken'),
                'Authorization': Cookies.get('UserToken')
            }	
        };
        axios.get(`/api/v1/links/${url_id}/stats`, config)
        .then(response => {
            stats_content =
            `
            <div class="stats-header">
                <h3 dir="ltr">${location.host + '/' + ((url_id.length <= 5) ? url_id : url_id.slice(0,5)+'...')}</h3>
                <h6>آخرین بروزرسانی: ${moment().format('H:m')}</h6>
                <button onclick="location.reload();" id="updateStats">بروزرسانی</button>
            </div>

            <div class="stats-container">
                <div class="stats-container-header">
                    <div class="times-menu">
                        <button id='lastDay' class='time-interval' disabled='true'>روز</button>
                        <button id='lastWeek' class='time-interval'>هفته</button>
                        <button id='lastMonth' class='time-interval'>ماه</button>
                        <button id='allTime' class='time-interval' style="width: auto !important;">همه زمان ها</button>
                    </div>
                    <h6>Clicks: <span id="total-clicks">20<span></h6>
                </div>
                <div style="background-color: white; text-align: center;">تفکیک بر اساس کشور</div>
                <div id="map-chart">
                </div>
                <div class="timeLine">
                    <canvas id="timeLine"></canvas>
                </div>
                <div class="pie-container">
                    <div>
                        <canvas class="pie" id="pie-os"></canvas>
                    </div>
                    <div>
                        <canvas class="pie" id="pie-browser"></canvas>
                    </div>
                    <div>
                        <canvas class="pie" id="pie-device"></canvas>
                    </div>
                </div>
            </div>
            <div style="width: 100%; text-align: center; padding-bottom: 50px;">
                <button class="returnToHome" onclick="window.location.href = '/'">بازگشت به خانه</button>
                <button class="updateStats" onclick="location.reload();">بروزرسانی آمار</button>
            </div>
            `;
            $('#body-block').append($(stats_content));

            $(function(){
                $('.time-interval').click(function(){
                    showStats( response.data[ $(this).attr('id') ] );
                    $('.time-interval').prop("disabled", false);
                    $(this).prop("disabled", true);
                });
            });
            setTimeLineLabels();
            showStats(response.data.lastDay);
        })
        .catch(error => {
            errors = {
                401: '<h2>برای مشاهده آمار ابتدا لاگین کنید !</h2>',
                403: '<h2>این لینک متعلق به شما نیست و اجازه مشاهده آمار آن را ندارید !</h2>',
                404: '<h2>این لینک یافت نشد !</h2>'
            }
            error_box = `<div class="stats-error">${errors[error.response.status]}</div>`;
            $('#body-block').append($(error_box));
        });

    }


})();
