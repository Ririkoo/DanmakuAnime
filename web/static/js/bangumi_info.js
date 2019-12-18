function draw_danmaku_count(sid, grain) {
    var myChart = echarts.init(document.getElementById('danmaku_count'), 'light', {
        renderer: 'svg'
    });
    myChart.clear()
    myChart.showLoading();
    let url = 'http://127.0.0.1:5000/data/danmaku_count/' + grain + '/' + String(sid) 
    $.get(url).done(function (data) {
        // console.log(data)
        myChart.hideLoading();
        myChart.setOption({
            "animation": true,
            "animationThreshold": 2000,
            "animationDuration": 3000,
            "animationEasing": "cubicOut",
            "animationDelay": 0,
            "animationDurationUpdate": 300,
            "animationEasingUpdate": "cubicOut",
            "animationDelayUpdate": 0,
            title: {
                text: grain + ' - Level'
            },
            tooltip: {
                trigger: 'axis',
                position: function (pt) {
                    return [pt[0], '10%'];
                }
            },
            dataZoom: { 
            },
            toolbox: {
                "show": true,
                "feature": {
                    "saveAsImage": {
                        "show": true,
                        "title": "save as image",
                        "type": "png"
                    },
                    "restore": {
                        "show": true,
                        "title": "restore"
                    },
                    "dataView": {
                        "show": true,
                        "title": "data view",
                        "readOnly": false
                    },
                    "dataZoom": {
                        "show": true,
                        "title": {
                            "zoom": "data zoom",
                            "back": "data zoom restore"
                        }
                    }
                }
            },
            xAxis: {
                data: data['time_sequence']
            },
            yAxis: {},
            series: [{
                name: 'Danmaku Count',
                type: 'line',
                smooth: true,
                symbol: 'none',
                itemStyle: {
                    color: 'rgb(255, 70, 131)'
                },
                areaStyle: {
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                        offset: 0,
                        color: 'rgb(255, 158, 68)'
                    }, {
                        offset: 1,
                        color: 'rgb(255, 70, 131)'
                    }])
                },
                data: data['danmaku_count']
            }]
        });
    });
}

function draw_danmaku_number(sid) {
    var myChart = echarts.init(document.getElementById('danmaku_number'), 'light', {
        renderer: 'svg'
    });
    myChart.clear()
    myChart.showLoading();
    let url = 'http://127.0.0.1:5000/data/danmaku_number/'+ String(sid) + '/all'
    $.get(url).done(function (data) {
        // console.log(data)
        myChart.hideLoading();
        myChart.setOption({
            "animation": true,
            "animationThreshold": 2000,
            "animationDuration": 3000,
            "animationEasing": "cubicOut",
            "animationDelay": 0,
            "animationDurationUpdate": 300,
            "animationEasingUpdate": "cubicOut",
            "animationDelayUpdate": 0,
            tooltip: {},
            toolbox: {
                "show": true,
                "feature": {
                    "saveAsImage": {
                        "show": true,
                        "title": "save as image",
                        "type": "png"
                    },
                    "restore": {
                        "show": true,
                        "title": "restore"
                    },
                    "dataView": {
                        "show": true,
                        "title": "data view",
                        "readOnly": false
                    },
                    "dataZoom": {
                        "show": true,
                        "title": {
                            "zoom": "data zoom",
                            "back": "data zoom restore"
                        }
                    }
                }
            },
            xAxis: {
                data: data['index']
            },
            yAxis: {},
            series: [{
                name: 'Danmaku Count',
                type: 'line',
                data: data['danmaku_count']
            }]
        });
    });
}

function draw_danmaku_length(sid) {
    var myChart = echarts.init(document.getElementById('danmaku_length'), 'light', {
        renderer: 'svg'
    });
    myChart.clear()
    myChart.showLoading();
    let url = 'http://127.0.0.1:5000/data/danmaku/'+ String(sid) + '/length'
    $.get(url).done(function (data) {
        // console.log(data)
        myChart.hideLoading();
        myChart.setOption({
            "animation": true,
            "animationThreshold": 2000,
            "animationDuration": 1000,
            "animationEasing": "cubicOut",
            "animationDelay": 0,
            "animationDurationUpdate": 300,
            "animationEasingUpdate": "cubicOut",
            "animationDelayUpdate": 0,
            tooltip : {
                trigger: 'item',
                // formatter: "{a} <br/>{b} : {c} ({d}%)"
            },
            legend: {
                type: 'scroll',
                orient: 'vertical',
                right: 10,
                top: 20,
                bottom: 20,
                data: data.legend,
            },
            series : [
                {
                    name: 'Characters count:',
                    type: 'pie',
                    radius : '55%',
                    center: ['40%', '50%'],
                    data: data.series_data,
                    itemStyle: {
                        emphasis: {
                            shadowBlur: 10,
                            shadowOffsetX: 0,
                            shadowColor: 'rgba(0, 0, 0, 0.5)'
                        }
                    }
                }
            ]
        
        });
    });
}

function draw_hotwords(sid) {
    let url = 'http://127.0.0.1:5000/data/danmaku/'+ String(sid) + '/hotwords'
    $.get(url).done(function (data) {
        // console.log(data)
        WordCloud(document.getElementById('wordcloud'), { list:data, weightFactor: 0.35})
        html = ''
        for (i=0; i<data.length; i++){
            html += '<tr>'
            html += '<td>' +data[i][0] +'</td>'
            html += '<td>' +data[i][1] +'</td>'
            html += '</tr>'
        }
        $('#hotwords_content').html(html);
    });

}

function draw_topbar(num) {
    var myChart = echarts.init(document.getElementById('top_played'),'light',{
        renderer: 'svg'
    });
    myChart.clear()
    myChart.showLoading();
    num = String(num)
    let url = 'http://127.0.0.1:5000/top/popularity/' + num
    $.get(url).done(function (data) {
        // console.log(data)
        myChart.hideLoading();
        myChart.setOption({
            "animation": true,
            "animationThreshold": 2000,
            "animationDuration": 1000,
            "animationEasing": "cubicOut",
            "animationDelay": 0,
            "animationDurationUpdate": 300,
            "animationEasingUpdate": "cubicOut",
            "animationDelayUpdate": 0,
            title: {
                text: 'Top ' + num + ': Played Animation',
                subtext: 'Data Source: Bilibili, Bangumi.tv , Niconico, MyAnimelist',
                x: 'center'
            },
            toolbox: {
                "show": true,
                "feature": {
                    "saveAsImage": {
                        "show": true,
                        "title": "save as image",
                        "type": "png"
                    },
                    "restore": { 
                        "show": true,
                        "title": "restore"
                    },
                    "dataView": {
                        "show": true,
                        "title": "data view",
                        "readOnly": false
                    },
                    "dataZoom": {
                        "show": true,
                        "title": {
                            "zoom": "data zoom",
                            "back": "data zoom restore"
                        }
                    }
                }
            },
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    type: 'shadow'
                }
            },
            // legend: {
            //     data: ['Play Count', 'Danmaku']
            // },
            grid: {
                left: '3%',
                right: '4%',
                bottom: '3%',
                containLabel: true
            },
            xAxis: {
                type: 'value',
                boundaryGap: [0, 0.01]
            },
            yAxis: {
                type: 'category',
                inverse: true,
                data: data.title
            },
            series: [
                {
                    name: 'Playing Count',
                    type: 'bar',
                    data: data.cmp_value['Play Count']
                },
                {
                    name: 'Danmaku',
                    type: 'bar',
                    data: data.cmp_value['Danmaku']
                }
            ]       
        });
    });
}

function draw_topratebar(num) {
    var myChart = echarts.init(document.getElementById('top_rate'),'light',{
        renderer: 'svg'
    });
    myChart.clear()
    myChart.showLoading();
    num = String(num)
    let url = 'http://127.0.0.1:5000/top/rating/' + num
    $.get(url).done(function (data) {
        // console.log(data)
        myChart.hideLoading();
        myChart.setOption({
            "animation": true,
            "animationThreshold": 2000,
            "animationDuration": 1000,
            "animationEasing": "cubicOut",
            "animationDelay": 0,
            "animationDurationUpdate": 300,
            "animationEasingUpdate": "cubicOut",
            "animationDelayUpdate": 0,
            title: {
                text: 'Top ' + num + ': Rating Animation',
                subtext: 'Data Source: Bilibili, Bangumi.tv, MyAnimelist',
                x: 'left'
            },
            toolbox: {
                "show": true,
                "feature": {
                    "saveAsImage": {
                        "show": true,
                        "title": "save as image",
                        "type": "png"
                    },
                    "restore": {
                        "show": true,
                        "title": "restore"
                    },
                    "dataView": {
                        "show": true,
                        "title": "data view",
                        "readOnly": false
                    },
                    "dataZoom": {
                        "show": true,
                        "title": {
                            "zoom": "data zoom",
                            "back": "data zoom restore"
                        }
                    }
                }
            },
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    type: 'shadow'
                }
            },
            legend : {
                data : [ 'Bilibili', 'Bangumi.tv', 'MyAnimeList'],
                selected : {
                    'Bilibili' : false,
                    'Bangumi.tv' : true,
                    'MyAnimeList' : true
                },
                selectedMode : 'multiple'
            },
            grid: {
                left: '3%',
                right: '4%',
                bottom: '3%',
                containLabel: true
            },
            xAxis: {
                type: 'value',
                boundaryGap: [0, 0.01]
            },
            yAxis: {
                type: 'category',
                inverse: true,
                data: data.title
            },
            series: [
                {
                    name: 'Bilibili',
                    type: 'bar',
                    data: data.cmp_value['rating']
                },
                {
                    name: 'Bangumi.tv',
                    type: 'bar',
                    data: data.cmp_value['bgm_rating']
                },
                {
                    name: 'MyAnimeList',
                    type: 'bar',
                    data: data.cmp_value['mal_rating']
                }
            ]       
        });
    });
}

function draw_danmaku_time(sid) {
    var myChart = echarts.init(document.getElementById('danmaku_time'),'light',{
        renderer: 'svg'
    });
    myChart.clear()
    myChart.showLoading();
    let url = 'http://127.0.0.1:5000/data/danmaku_time/' + String(sid) + '/all'
    $.get(url).done(function (data) {
        // console.log(data)
        myChart.hideLoading();
        myChart.setOption({
            "animation": true,
            "animationThreshold": 2000,
            "animationDuration": 1000,
            "animationEasing": "cubicOut",
            "animationDelay": 0,
            "animationDurationUpdate": 300,
            "animationEasingUpdate": "cubicOut",
            "animationDelayUpdate": 0,
            tooltip: {
            },
            xAxis: {
                type: 'category',
                data: data.timelist,
            },
            yAxis: {
                type: 'value',
            },
            series: [
                {
                    type: 'bar',
                    data: data.sent_time_list
                }
            ]       
        });
    });
}

function draw_danmaku_emotion(sid) {
    var myChart = echarts.init(document.getElementById('danmaku_emotion'),'light',{
        renderer: 'svg'
    });
    myChart.clear()
    myChart.showLoading();
    let url = 'http://127.0.0.1:5000/data/danmaku_emotion/' + String(sid) + '/all'
    $.get(url).done(function (data) {
        // console.log(data)
        myChart.hideLoading();
        myChart.setOption({
            "animation": true,
            "animationThreshold": 2000,
            "animationDuration": 1000,
            "animationEasing": "cubicOut",
            "animationDelay": 0,
            "animationDurationUpdate": 300,
            "animationEasingUpdate": "cubicOut",
            "animationDelayUpdate": 0,
            tooltip: {
                trigger: 'axis',
                position: function (pt) {
                    return [pt[0], '10%'];
                }
            },
            dataZoom: { 
            },
            toolbox: {
                "show": true,
                "feature": {
                    "saveAsImage": {
                        "show": true,
                        "title": "save as image",
                        "type": "png"
                    },
                    "dataView": {
                        "show": true,
                        "title": "data view",
                        "readOnly": false
                    },
                    "dataZoom": {
                        "show": true,
                        "title": {
                            "zoom": "data zoom",
                            "back": "data zoom restore"
                        }
                    }
                }
            },
            xAxis: {
                data: data['time_sequence']
            },
            yAxis: {},
            visualMap: {
                top: 10,
                right: 10,
                pieces: [{
                    gt: 0,
                    lte: 0.5,
                    color: 'rgb(254,215,102)'
                }, {
                    gt: 0.5,
                    lte: 1.0,
                    color: 'rgb(62,163,216)'
                }],
                outOfRange: {
                    color: '#999'
                }
            },    
            series: [{
                symbolSize: 8,
                name: 'Emotion',
                type: 'scatter',
                data: data['danmaku_emotion'],
                markLine: {
                    silent: true,
                    data: [{
                        yAxis: 0.5
                    }, {
                        yAxis: 1.0
                    }]
                }
            }]
        });
    });

}

function draw_danmaku_emotion_pie(sid) {
    var myChart = echarts.init(document.getElementById('danmaku_emotion_pie'), 'light', {
        renderer: 'svg'
    });
    myChart.clear()
    myChart.showLoading();
    let url = 'http://127.0.0.1:5000/data/danmaku_emotion/'+ String(sid) + '/all_pie'
    $.get(url).done(function (data) {
        // console.log(data)
        myChart.hideLoading();
        myChart.setOption({
            "animation": true,
            "animationThreshold": 2000,
            "animationDuration": 1000,
            "animationEasing": "cubicOut",
            "animationDelay": 0,
            "animationDurationUpdate": 300,
            "animationEasingUpdate": "cubicOut",
            "animationDelayUpdate": 0,
            tooltip : {
                trigger: 'item',
                formatter: "{a} <br/>{b} : {c} ({d}%)"
            },
            legend: {
                type: 'scroll',
                orient: 'vertical',
                right: 10,
                top: 20,
                bottom: 20,
                data: data.legend,
            },
            series : [
                {
                    name: 'Emotion:',
                    type: 'pie',
                    radius: ['50%', '70%'],
                    avoidLabelOverlap: false,
                    label: {
                        normal: {
                            show: false,
                            position: 'center'
                        },
                        emphasis: {
                            show: true,
                            textStyle: {
                                fontSize: '30',
                                fontWeight: 'bold'
                            }
                        }
                    },
                    labelLine: {
                        normal: {
                            show: false
                        }
                    },
                    // radius : '55%',
                    // center: ['40%', '50%'],
                    // roseType : 'radius',
                    data: data.series_data,
                    // itemStyle: {
                    //     emphasis: {
                    //         shadowBlur: 10,
                    //         shadowOffsetX: 0,
                    //         shadowColor: 'rgba(0, 0, 0, 0.5)'
                    //     }
                    // }
                }
            ]
        
        });
    });
}

function draw_topic_pie(sid) {
    var myChart = echarts.init(document.getElementById('kyoani_topic'), 'light', {
        renderer: 'svg'
    });
    myChart.clear()
    myChart.showLoading();
    let url = 'http://127.0.0.1:5000/data/tag_distribution'
    $.get(url).done(function (data) {
        // console.log(data)
        myChart.hideLoading();
        myChart.setOption({
            "animation": true,
            "animationThreshold": 2000,
            "animationDuration": 1000,
            "animationEasing": "cubicOut",
            "animationDelay": 0,
            "animationDurationUpdate": 300,
            "animationEasingUpdate": "cubicOut",
            "animationDelayUpdate": 0,
            tooltip : {
                trigger: 'item',
                formatter: "{a} <br/>{b} : {c} ({d}%)"
            },
            legend: {
                type: 'scroll',
                orient: 'vertical',
                right: 10,
                top: 30,
                // bottom: 30,
                data: data.legend,
            },
            series : [
                {
                    name: 'Topic:',
                    type: 'pie',
                    radius : '70%',
                    center: ['50%', '50%'],
                    roseType : 'radius',
                    data: data.series_data,
                    itemStyle: {
                        emphasis: {
                            shadowBlur: 10,
                            shadowOffsetX: 0,
                            shadowColor: 'rgba(0, 0, 0, 0.5)'
                        }
                    }
                }
            ]
        
        });
    });
}