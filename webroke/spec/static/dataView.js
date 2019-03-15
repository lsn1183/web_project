var translation2 = {
    'version': '版本',
    'spec_file_name': '文件名',
    'language': '语言',
    'summary': '概要',
    'premise': '前提',
    'call_condition': '呼出',
};

var searchResultHeader = {
    "req_spec": "req_spec",
    "req_spec_no": "req_spec_no",
    "version": "版本",
    "req_spec_name": "式样名",
    "req_spec_file_name": "文件名",
    "spec_chapter_num": "章节号",
    "spec_chapter_title": "章节名",
};

var req = {
    "author_name": "担当",
    "hu_def_id": "H/U要件定義ID",
    "requirement_id": "TAGL要件定義ID",
    "spec_chapter_num": "spec_chapter_num",
    "unique_id": "ユニークID",
    "major_category": "H/U要件定義書から転記-大分類",
    "medium_catetory": "H/U要件定義書から転記-中分類",
    "small_category": "H/U要件定義書から転記-小分類",
    "detail": "H/U要件定義書から転記-詳細",
    "base": "H/U要件定義書から転記-基本要件",
    "rel_requiremant": "H/U要件定義書から転記-関連基本要件",
    "exception": "除外",
    "dcu_status": "H/U要件定義書から転記-DCU-状態",
    "dcu_trigger": "H/U要件定義書から転記-DCU-トリガー",
    "dcu_action": "H/U要件定義書から転記-DCU-動作",
    "meu_status": "H/U要件定義書から転記-MEU-状態",
    "meu_trigger": "H/U要件定義書から転記-MEU-トリガー",
    "meu_action": "H/U要件定義書から転記-MEU-動作",
    "hu_req_remark": "H/U要件定義書から転記-備考(HU要件定義)",
    "dcu_meu": "DCU/MEUどちらの想定か",
    "pf_status": "責務分担-TAGL-PF-状態",
    "pf_trigger": "責務分担-TAGL-PF-トリガー",
    "pf_action": "責務分担-TAGL-PF-動作",
    "remark": "備考",
    "notice": "責務分担の特記事項",
    "rel_hal_design": "参考文献-参考ウォークスルー図",
    "rel_flow_diagram": "参考文献-参考HAL設計書",
    "other_spec": "参考文献-その他仕様（リファハード仕様等）",
    "implementation": "リファレンスハード上での実現可否",
    "analysis": "詳細分析可否",
    "unrequire": "未要件分析",
    "file_name": "文件名",
    "id": "id",
};

var spec_analysis = {
    "author_name": "担当者",
    "requirement_id": "TAGL要件定義ID",
    "spec_chapter_num": "spec_chapter_num",
    "id": "id",
    "unique_id": "ユニークID",
    "major_category": "大分類",
    "medium_catetory": "中分類",
    "small_category": "小分類",
    "detail": "詳細",
    "base": "基本要件",
    "rel_requiremant": "関連基本要件",
    "exception": "除外",
    "dcu_meu": "TAGL-PF-DCU/MEUどちらの要件か",
    "pf_status": "TAGL-PF-状態",
    "fp_trigger": "TAGL-PF-トリガー",
    "pf_action": "TAGL-PF-動作",
    "seq_diagram": "シーケンス図",
    "application": "責務分担-アプリケーション",
    "kernel": "責務分担-kernel",
    "systemd": "責務分担-systemd",
    "supple_spec": "補足参照仕様書",
    "uncheck": "未検証",
    "remark": "備考",
    "file_name": "文件名",
};

var spec_req = {
    "req_spec": "req_spec",
    "req_spec_name": "req_spec_name",
    "req_spec_file_name": "req_spec_file_name",
    "no": "no",
    "req_chapter_num": "req_chapter_num",
    "req_chapter_title": "req_chapter_title",
    "req_page": "req_page",
    "update_date": "update_date",
    "category": "category",
    "spec_num": "spec_num",
    "spec_file_name": "spec_file_name",
    "version": "version",
    "spec_chapter_num": "spec_chapter_num",
    "spec_chapter_title": "spec_chapter_title",
    "need": "need",
    "reason": "reason",
    "department": "department",
    "group_name": "group_name",
    "name": "name",
    "date": "date",
    "remark": "remark",
};

var viewModel;
var selectId;

(function ($, undefined) {
    "use strict";
    $.jstree.plugins.noclose = function () {
        this.close_node = $.noop;
    };
})(jQuery);

function GetQueryString(name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
    var r = window.location.search.substr(1).match(reg);
    if (r != null) return unescape(r[2]); return null;
}

function saveEditor(model, data) {
    console.log('save model = ' + model);
    console.log('save data = ' + JSON.stringify(data));
    var _request = "/doctree/relateDef.html";
    if (model === 'definition') {
        _request = "/doctree/relateDef.html";
    } else if (model === 'analysis') {
        _request = "/doctree/relateAnalysis.html";
    } else {

    }
    // if (Array.isArray(data) && data.length > 0) {

    $.ajax({
        type: "post",
        url: _request,
        dataType: "json",
        data: JSON.stringify(data),
        // headers: { 'Content-Type': 'application/json' },
        beforeSend: function (xhr) {
            xhr.setRequestHeader("Content-Type", "application/json");
        },
        success: function (data) { console.log('post success' + data); },
        error: function (data) { console.log('post error'); },
    });

    // }
}

function getData(model) {
    var data = [];
    var itemList = {};
    var normalData = {};
    var vals = [];

    if (!Array.isArray(viewData)) {
        return data;
    }
    data = viewData;
    itemList = data[selectId];

    for (key in itemList) {
        if (key === 'vals') {
            continue;
        }
        let valueDom = document.querySelector('.' + model + '-view [data-key="' + key + '"]');
        if (valueDom) {
            normalData[key] = valueDom.innerText;
        }
    }

    let valsDoms = document.querySelectorAll('.' + model + '-view [data-key="vals"]');
    if (valsDoms.length > 0) {
        valsDoms.forEach(function (valueDom, index) {
            vals.push(valueDom.innerText);
        });
    }
    normalData.vals = vals;
    Object.assign(itemList, normalData);

    return itemList;
}

function click_editor(evt) {
    var _target = evt.target;
    // var _model = _target.dataset.model;
    if (_target.dataset.status === 'save') {
        _target.dataset.status = 'editor';
        _target.innerText = 'Editor';
        var _container = _target.parentElement;
        _container.classList.remove('editor');
        $(_container).find('.var-value').attr('contenteditable', 'false');
        // do save
        saveEditor(viewModel, getData(viewModel));
    } else if (_target.dataset.status === 'editor') {
        _target.dataset.status = 'save';
        _target.innerText = 'Save';
        var _container = _target.parentElement;
        _container.classList.add('editor');
        $(_container).find('.var-value').attr('contenteditable', 'true');
    } else {
        console.log('editor button status error');
    }
}

function showContent(e, data) {
    var translation;
    var itemId = data.node.id.split('_')[1];
    var itemText = data.node.text;

    selectId = itemId;

    var editBtn = document.querySelector('.editor-btn');

    editBtn.dataset.id = itemId;

    if (viewModel === 'definition') {
        document.querySelector('.definition-view .view-name').innerText = data.node.text;
        // 数据填充
        var dbValues = viewData[itemId];

        // set normal data
        Object.keys(req).forEach(function (key, index) {
            var _td_value = document.querySelector('.definition-view [data-key=' + key + ']');
            if (_td_value) {
                _td_value.innerText = dbValues[key];
            }
        });
        // set device_types data

        var device_types_dom = document.querySelectorAll('.definition-view [data-key="vals"]');

        for (var i = 0; i < device_types_dom.length; i++) {
            device_types_dom[i].innerText = dbValues.vals[i];
        }
    } else if (viewModel === 'analysis') {
        document.querySelector('.analysis-view .view-name').innerText = data.node.text;
        // 数据填充
        var dbValues = viewData[itemId];

        // set normal data
        Object.keys(spec_analysis).forEach(function (key, index) {
            var _td_value = document.querySelector('.analysis-view [data-key=' + key + ']');
            if (_td_value) {
                _td_value.innerText = dbValues[key];
            }
        });
        // set vals
        var device_types_dom = document.querySelectorAll('.analysis-view [data-key="vals"]');

        for (var i = 0; i < device_types_dom.length; i++) {
            device_types_dom[i].innerText = dbValues.vals[i];
        }
    }
    // 显示table
    document.querySelector('.' + viewModel + '-view').style.display = 'block';
}

/**
 * definition table 0
 */
function getDefTable_0() {

}

/**
 * definition table 1
 * H/U要件定義書から転記
 */
function getDefTable_1() {

}

/**
 * definition table 2
 * 責務分担
 */
function getDefTable_2() {

}

/**
 * definition table 3
 * 参考文献
 */
function getDefTable_3() {

}

/**
 * definition table 4
 */
function getDefTable_4() {

}

function renderView(model, _id) {
    var url;
    var cataLogData = [];
    if (model === 'definition') {
        url = '/doctree/relateDef.html';
        $.get(url,
            {
                "func_id": _id
            },
            function (jsonDT, textStatus) {
                viewData = jsonDT;
                // viewData = [{"author_name": "", "hu_def_id": "4.2.5.14.4.2", "requirement_id": "4.2.5.14.4.3", "unique_id": 0, "major_category": "\u30c0\u30a4\u30a2\u30b0", "medium_catetory": "\u30c0\u30a4\u30a2\u30b0CAN", "small_category": "DTV\u6e2c\u5b9a ", "detail": "DTV\u53d7\u4fe1\u30ec\u30d9\u30eb\u6e2c\u5b9a\u5b9f\u65bd", "base": "", "rel_requiremant": "", "dcu_status": "\u975eService\uff0cDevelop Diag\u753b\u9762", "dcu_trigger": "CAN\u547d\u4ee4\u53d7\u4fe1(DTV\u53d7\u4fe1\u30ec\u30d9\u30eb\u6e2c\u5b9a\u5b9f\u65bd)\n1.CANID\u662f0x70\n2.MODE\u662f0x30\n3.\u547d\u4ee4\u5185\u5bb90x23\n4.DTV\u53d7\u4fe1\u30ec\u30d9\u30eb\u6e2c\u5b9a\u5b9f\u65bd\u6307\u793a\u306e\u5024\u304c1\u3067\u3042\u308b\u5834\u5408\u306e\u307f", "dcu_action": "\u30c7\u30b8\u30bf\u30ebTV\u30c1\u30e5\u30fc\u30ca\u30fc\u691c\u67fb\u53d7\u4fe1\u30c1\u30e3\u30f3\u30cd\u30eb\u6307\u793a\u306e\u5024\u306b\u8a72\u5f53\u3059\u308b\u30c1\u30e3\u30f3\u30cd\u30eb\u306e\u53d7\u4fe1\u30ec\u30d9\u30eb\u3092\u6e2c\u5b9a\u3059\u308b\u3002", "meu_status": "-", "meu_trigger": "-", "meu_action": "-", "hu_req_remark": "", "dcu_meu": "DCU", "pf_status": "", "pf_trigger": "", "pf_action": "", "device_types": ["\u96fb\u6e90\u7ba1\u7406\u30c7\u30d0\u30a4\u30b9", "AVCLAN\u5236\u5fa1\u30c7\u30d0\u30a4\u30b9", "MOST\u5236\u5fa1\u30c7\u30d0\u30a4\u30b9", "CAN\u5236\u5fa1\u30c7\u30d0\u30a4\u30b9", "\u30b8\u30ab\u7dda\u5165\u529b\u30c7\u30d0\u30a4\u30b9", "\u63ee\u767a\u30e1\u30e2\u30ea\u30c7\u30d0\u30a4\u30b9", "\u4e0d\u63ee\u767a\u30e1\u30e2\u30ea\u30c7\u30d0\u30a4\u30b9", "\u97f3\u58f0\u51fa\u529b\u30c7\u30d0\u30a4\u30b9", "\u97f3\u58f0\u5165\u529b\u30bb\u30ec\u30af\u30bf\u30c7\u30d0\u30a4\u30b9", "BT\u30c7\u30d0\u30a4\u30b9", "WIFI\u30c7\u30d0\u30a4\u30b9", "\u30bf\u30c3\u30c1\u30d1\u30cd\u30eb\u5236\u5fa1\u30c7\u30d0\u30a4\u30b9", "\u30bf\u30c3\u30c1\u30d1\u30c3\u30c9\u5236\u5fa1\u30c7\u30d0\u30a4\u30b9", "\u30ed\u30fc\u30bf\u30ea\u30fc\u30b9\u30a4\u30c3\u30c1\u3001\u30ad\u30fc\u30b9\u30a4\u30c3\u30c1\u691c\u51fa\u30c7\u30d0\u30a4\u30b9", "GPS\u30c7\u30d0\u30a4\u30b9", "Radio\u30c1\u30e5\u30fc\u30ca\u30fc\u30c7\u30d0\u30a4\u30b9\uff08XM\u3001DAB\u542b\u3080\uff09", "\u5730\u30c7\u30b8\u30c1\u30e5\u30fc\u30ca\u30fc\u30c7\u30d0\u30a4\u30b9", "\u30bb\u30ad\u30e5\u30ea\u30c6\u30a3\u30c1\u30c3\u30d7\u30c7\u30d0\u30a4\u30b9", "\u30de\u30a4\u30af\u7528ADC\u30c7\u30d0\u30a4\u30b9", "DVD\u6620\u50cf\u30c7\u30b3\u30fc\u30c0\u30c7\u30d0\u30a4\u30b9", "\u6620\u50cf\u4fe1\u53f7\u5165\u529b\u30bb\u30ec\u30af\u30bf\u30c7\u30d0\u30a4\u30b9", "\u6620\u50cf\u4fe1\u53f7\u51fa\u529b\u30c7\u30d0\u30a4\u30b9(DCU\u2192\u5404\u30c7\u30a3\u30b9\u30d7\u30ec\u30a4/ MEU\u2192DCU)", "CD/DVD/BD\u5236\u5fa1\u30c7\u30d0\u30a4\u30b9", "ECNC\u30c7\u30d0\u30a4\u30b9", "USB2.0-Host/Function\u30c7\u30d0\u30a4\u30b9", "APPLE\u8a8d\u8a3c\u30c7\u30d0\u30a4\u30b9"], "vals": ["-", "-", "-", "- \u203b", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "- \u203b", "-", "-", "-", "-", "-", "-", "-", "-", "-"], "remark": "", "notice": "", "rel_flow_diagram": "", "rel_hal_design": "", "other_spec": "", "implementation": "", "analysis": "", "unrequire": "\u25cb"}];
                viewData.forEach(function (item, index) {
                    cataLogData.push({
                        "id": 'list_' + index,
                        "text": item.requirement_id + " 要件定義 - ユニークID: " + item.unique_id
                    });
                });
                $('#catalogTree').jstree({
                    'core': {
                        'check_callback': true,
                        'data': cataLogData
                    },
                    "plugins": ["search"],
                    "search": { "show_only_matches": true },
                }).on('ready.jstree', function () {
                    var t = $('#catalogTree').jstree(true);

                    t.deselect_all(true);
                    var to = false;
                    $('#searchCatalogTree').keyup(function () {
                        if (to) {
                            clearTimeout(to);
                        }
                        to = setTimeout(function () {
                            var v = $('#searchCatalogTree').val();
                            $('#catalogTree').jstree(true).search(v);
                        }, 1000);
                    });

                    $('#catalogTree').on('changed.jstree', function (e, data) {
                        showContent(e, data);
                    });
                });
            }, "json");

    } else if (model === 'analysis') {
        url = '/doctree/relateAnalysis.html';
        $.get(url,
            {
                "func_id": _id
            },
            function (jsonDT, textStatus) {
                viewData = jsonDT;
                // viewData = [{"author_name": "", "requirement_id": "4.2.5.14.4.3", "unique_id": 0, "major_category": "\u30c0\u30a4\u30a2\u30b0", "medium_catetory": "\u30c0\u30a4\u30a2\u30b0CAN", "small_category": "DTV\u6e2c\u5b9a ", "detail": "DTV\u53d7\u4fe1\u30ec\u30d9\u30eb\u6e2c\u5b9a\u5b9f\u65bd", "base": "", "rel_requiremant": "", "exception": "", "dcu_meu": "DCU", "pf_status": "\u975eService\uff0cDevelop Diag\u753b\u9762", "fp_trigger": "CAN\u547d\u4ee4\u53d7\u4fe1(DTV\u53d7\u4fe1\u30ec\u30d9\u30eb\u6e2c\u5b9a\u5b9f\u65bd)\n1.CANID\u662f0x70\n2.MODE\u662f0x30\n3.\u547d\u4ee4\u5185\u5bb90x23\n4.DTV\u53d7\u4fe1\u30ec\u30d9\u30eb\u6e2c\u5b9a\u5b9f\u65bd\u6307\u793a\u306e\u5024\u304c1\u3067\u3042\u308b\u5834\u5408\u306e\u307f", "pf_action": "\u30c7\u30b8\u30bf\u30ebTV\u30c1\u30e5\u30fc\u30ca\u30fc\u691c\u67fb\u53d7\u4fe1\u30c1\u30e3\u30f3\u30cd\u30eb\u6307\u793a\u306e\u5024\u306b\u8a72\u5f53\u3059\u308b\u30c1\u30e3\u30f3\u30cd\u30eb\u306e\u53d7\u4fe1\u30ec\u30d9\u30eb\u3092\u6e2c\u5b9a\u3059\u308b\u3002", "seq_diagram": "1.0", "supple_spec": "", "uncheck": "", "remark": "", "application": "-", "kernel": "-", "systemd": "-", "models": ["BaseSystem-System Service-System Manager", "BaseSystem-System Service-Device Detection Service\n", "BaseSystem-System Service-Window System", "BaseSystem-System Service-Logger Service", "BaseSystem-System Service-Resouce Manager", "BaseSystem-System Service-Task Manager", "BaseSystem-System Service-Update Service", "BaseSystem-System Service-Font", "BaseSystem-System Service-Mounter", "BaseSystem-System Service-Power Service", "BaseSystem-System Service-Graphics", "BaseSystem-Native Service-NPP Service", "BaseSystem-Native Service-Image Storage", "BaseSystem-Native Service-Framework Unified", "BaseSystem-Native Service-Shared Mem", "BaseSystem-Native Service-Lock Manager", "BaseSystem-Native Service-Backup Manager", "BaseSystem-Native Service-libextention", "BaseSystem-Native Service-libcommon", "BaseSystem-Peripheral Services-communication", "BaseSystem-Peripheral Services-CommSH4", "BaseSystem-Peripheral Services-CommUSB", "BaseSystem-Peripheral Services-sysupdate", "BaseSystem-Peripheral Services-PSMShadow", "BaseSystem-Peripheral Services-Lanserver", "BaseSystem-Peripheral Services-Switch Handler", "BaseSystem-Peripheral Services-CANGW_M", "BaseSystem-Peripheral Services-CANGW_S", "BaseSystem-Peripheral Services-amigovup", "BaseSystem-Peripheral Services-CDR", "BaseSystem-Peripheral Services-ExtUnitAuth", "BaseSystem-Peripheral Services-Logger Shadow", "BaseSystem-Peripheral Services-Proxy Service", "BaseSystem-Peripheral Services-Positioning", "BaseSystem-Peripheral Services-IPC", "BaseSystem-Peripheral Services-IPC_MP Shadow", "BaseSystem-Peripheral Services-MOSTShadow", "BaseSystem-Vehicle Services-clock", "BaseSystem-Vehicle Services-Diag Service", "BaseSystem-Vehicle Services-vehicle", "BaseSystem-Audio Service-Mic Service", "BaseSystem-Audio Service-Sound Service", "BaseSystem-Audio Service-ALSA", "BaseSystem-OtherServices-libev", "BaseSystem-OtherServices-librpc", "BaseSystem-OtherServices-libPosixBasedOS001legacy\n", "Applicatio Management-Applicatio Management-Mode Manager", "Applicatio Management-Applicatio Management-Arbitration Manager", "Applicatio Management-Applicatio Management-Display Service", "Applicatio Management-Applicatio Management-Audio Manager", "Applicatio Management-Applicatio Management-System App (Startup)", "Applicatio Management-Applicatio Management-Window Manager", "Application Service-Multimedia-media-Media Service", "Application Service-Multimedia-Radio-Radio Service", "Application Service-Multimedia-dtv-DTV Service", "Application Service-Multimedia-dtv-DTV Server", "Application Service-Multimedia-dtv-DTV vupservice", "Application Service-Connectivity-ConnBT-BT connection Service", "Application Service-Connectivity-ConnBT-BT Messaging Service", "Application Service-Connectivity-ConnBT-BT PhoneBook Service", "Application Service-Connectivity-ConnBT-BT TelBLL Service", "Application Service-Connectivity-ConnBT-BT Phone Service", "Application Service-Connectivity-ConnBT-DCM Phone Service", "Application Service-Connectivity-aoa", "Application Service-Connectivity-Wlan Middle Service", "Application Service-Vehicle-Diagnosis", "Application Service-Vehicle-Energy Monitor", "Application Service-Vehicle-Fuel Consumption", "Application Service-Vehicle-DMS", "Application Service-Vehicle-Seat", "Application Service-Vehicle-Camera", "Application Service-Vehicle-Aircon", "Application Service-Vehicle-Cutomize", "Application Service-Vehicle-Meter", "Application Service-Misc-Setting-Delete Personal Data", "Application Service-Misc-Setting-Info Setting", "Application Service-Misc-Setting-Menu Service", "Application Service-Misc-Setting-Setting", "Application Service-Misc-ConnUtilityService-ConnMgr", "Application Service-Misc-ConnUtilityService-ConnUtil", "Application Service-Misc-ConnUtilityService-Service FlagMgr", "Application Service-Misc-CommArb-CommArbMEU", "Application Service-Misc-CommArb-CommArbDCU", "Application Service-Misc-Contents Manager", "Application Service-Misc-Network Manager", "Application Service-Misc-Misink", "Application Service-Misc-Software Update", "Application Service-Misc-Data Services", "Application Service-Misc-SPC Services", "Application Framework-Application Framework-Status Bar", "Application Framework-Application Framework-Notify Service", "Application Framework-Application Framework-Trinity"], "vals": ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "CAN\u901a\u8baf\u63a5\u6536\u4e0e\u53d1\u9001IF\u63d0\u4f9b", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "1.\u63a5\u6536DTV\u53d7\u4fe1level\u7684CAN\u8bca\u65ad\u547d\u4ee4\n2.\u6839\u636eCAN\u547d\u4ee4\u8f93\u5165\u7684\u53c2\u6570\u8fdb\u884cDTV\u53d7\u4fe1level\u68c0\u6d4b", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "DTV source\u5207\u6362", "-", "DTV\u53d7\u4fe1level\u68c0\u6d4b", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"]}];
                viewData.forEach(function (item, index) {
                    cataLogData.push({
                        "id": 'list_' + index,
                        "text": item.requirement_id + " 要件分析 - ユニークID: " + item.unique_id
                    });
                });
                $('#catalogTree').jstree({
                    'core': {
                        'check_callback': true,
                        'data': cataLogData
                    },
                    "plugins": ["search"],
                    "search": { "show_only_matches": true },
                }).on('ready.jstree', function () {
                    var t = $('#catalogTree').jstree(true);

                    t.deselect_all(true);
                    var to = false;
                    $('#searchCatalogTree').keyup(function () {
                        if (to) {
                            clearTimeout(to);
                        }
                        to = setTimeout(function () {
                            var v = $('#searchCatalogTree').val();
                            $('#catalogTree').jstree(true).search(v);
                        }, 1000);
                    });

                    $('#catalogTree').on('changed.jstree', function (e, data) {
                        showContent(e, data);
                    });
                });
            }, "json");
    }
}

$(function () {

    var _model = GetQueryString('model');
    var _id = GetQueryString('func_id');
    if (_model === 'definition') {
        // 设置title
        document.title = 'TAGL要件定義書';
        document.querySelector('.nav-title span').innerText = 'TAGL要件定義書';
    } else if (_model === 'analysis') {
        // 设置title
        document.title = 'TAGL要件分析書';
        document.querySelector('.nav-title span').innerText = 'TAGL要件分析書';
    }
    viewModel = _model;
    renderView(_model, _id);

});

