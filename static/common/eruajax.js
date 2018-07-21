// 对jquery的ajax封装

'use strict';
var eruajax = {
    'get':function (args) {
        args['method'] = 'get';
        this.ajax(args);
    },
    'post':function (args) {
        args['method'] = 'post';
        this.ajax(args);
    },
    'ajax':function (args) {
        // 设置csrf_token
        this._ajaxSetup();
        $.ajax(args);
    },
    '_ajaxSetup': function () {
        $.ajaxSetup({
            'beforeSend':function (xhr, settings) {
                if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain){
                    var csrftoken = $('meta[name=csrf-token]').attr('content');
                    xhr.setRequestHeader("X-CSRFToken", csrftoken)
                }
            }
        });
    }
};