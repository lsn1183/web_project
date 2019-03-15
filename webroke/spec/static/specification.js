var translation2 = {
    'version': '版本',
    'spec_file_name': '文件名',
    'language': '语言',
    'summary': '概要',
    'premise': '前提',
    'call_condition': '呼出',
};


var searchResultHeader = {
    1: {
        "req_spec": "req_spec",
        "req_spec_no": "req_spec_no",
        "version": "版本",
        "req_spec_name": "式样名",
        "req_spec_file_name": "文件名",
        "spec_chapter_num": "章节号",
        "spec_chapter_title": "章节名",
    },
    2: {
        "spec_chapter_title": "要求式样书章节标题",
        "spec_chapter_num": "式样书章节号",
        "id": "id",
        "func_content": "机能内容",
    },
    3: {
        "parent_chapter_num": "章节号",
        "id": "机能ID",
        "parsed_content": "机能内容",
    }
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

(function ($, undefined) {
    "use strict";
    $.jstree.plugins.noclose = function () {
        this.close_node = $.noop;
    };
})(jQuery);


var specDefData;
var analysisData;

function showModel(el) {
    event.preventDefault();
    var func_id = $(el).parents(".jstree-node").attr("id");
    $.get('/doctree/model.html',
        {
            func_id: func_id,
        },
        function (jsonDT, textStatus) {
            var snippet = ` 
                                        <div class="modal fade" id="myModal" tabindex="-1" role="dialog" >
                                            <div class="modal-dialog" role="document">
                                                <div class="modal-content">
                                                    <div class="modal-header">
                                                        <button type="button" class="close" data-dismiss="modal" ><span >&times;</span>
                                                        </button>
                                                    </div>
                                                    <div class="modal-body">
                                                    <input type="text" id="searchModelTree" value="" placeholder="search model">
                                                        <div id="modelTree">
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                        `;
            $("#modal1").html(snippet);
            if (!$.isEmptyObject(jsonDT)) {
                $('#myModal').modal('show');
            }
            $('#modelTree').jstree({
                'core': {
                    'data': jsonDT['data'],
                    'themes': {
                        'icons': false,
                    },
                },
                "plugins": ["noclose", "search"],
                "search": {"show_only_matches": true, "show_only_matches_children": true},
            }).on('ready.jstree', function () {
                $(this).jstree('open_all');
            });
            var to = false;
            $('#searchModelTree').keyup(function () {
                if (to) {
                    clearTimeout(to);
                }
                to = setTimeout(function () {
                    var v = $('#searchModelTree').val();
                    $('#modelTree').jstree(true).search(v);
                }, 250);
            });

        }, "json");
}

function moreInfoTip() {
    var tmpSTR1 = "";
    if ($(this).text() == "仕向地") {
        tmpSTR1 += "查看仕向地";
        return tmpSTR1;
    }
}


function testTypeicon(test_type,iconSize) {

    var tmpHtml = "";
    if (test_type == "CANNOTTEST") {
        tmpHtml += '<svg width="' + iconSize + '" height="' + iconSize + '">';
        tmpHtml += '<rect width="' + iconSize + '" height="' + iconSize + '" style="fill:#FFFFFF;stroke:#000000;stroke-width:1"/>';
        tmpHtml += '<line x1="' + iconSize + '" y1="0" x2="0" y2="' + iconSize + '" style="stroke:#000000;stroke-width:1"/>';
        tmpHtml += '</svg>';
    } else if (test_type == "COMMON") {
        tmpHtml += '<svg width="' + iconSize + '" height="' + iconSize + '">';
        tmpHtml += '<rect width="' + iconSize + '" height="' + iconSize + '" style="fill:#FFFFFF;stroke:#000000;stroke-width:1"/>';
        tmpHtml += '</svg>';
    }
    return tmpHtml;
}

function func_number(number) {
    var tmpHtml = "";
    if (!(number == null || number == "")) {
        tmpHtml += '<div id="func_number">' + number + '</div>';
    }
    return tmpHtml;
}

function func_more(dict, translation) {
    var tmpHtml = "";
    if (dict["has_model"] == true||dict["spec_req_title"].length > 0||dict["spec_def_count"] > 0 || dict["spec_analysis_count"] > 0) {
        tmpHtml += '<div id="func_more" class="dropdown">';
        tmpHtml += '<a id="drop" href="" class="dropdown-toggle" data-toggle="dropdown">' + translation[dict['func_type']] + '<span class="caret"></span></a>';
        tmpHtml += '<ul class="dropdown-menu" >';
        if(dict["has_model"] == true){
            tmpHtml += '<li><a href="" data-toggle="tooltip" data-placement="right"  onclick="showModel(this)">仕向地</a></li>';
        }
        if(dict["spec_req_title"].length > 0){
            tmpHtml += '<li class="dropdown-submenu">';
            tmpHtml += '<a onclick="return false;">要求式样书</a>';
            tmpHtml += '<ul class="dropdown-menu">';
            for(var i=0;i<dict["spec_req_title"].length;i++){
                if(dict["spec_req_title"][i][1]==="None"){
                    tmpHtml += '<li><a onclick="return false;">'+dict["spec_req_title"][i][0]+'</a></li>';
                }else{
                    tmpHtml += '<li><a onclick="window.open(\''+dict["spec_req_title"][i][1]+'\', \'_blank\');">'+dict["spec_req_title"][i][0]+'</a></li>';
                }
            }
            tmpHtml += '</ul>';
            tmpHtml += '</li>';
        }
        if(dict["spec_def_count"] > 0){
            tmpHtml += '<li><a onclick="window.open(\'/doctree/dataView.html?func_id='+dict["func_id"]+'&amp;model=definition\', \'_blank\');" data-toggle="tooltip" data-placement="right">要件定义</a></li>';
        }
        if(dict["spec_analysis_count"] > 0){
            tmpHtml += '<li><a onclick="window.open(\'/doctree/dataView.html?func_id='+dict["func_id"]+'&amp;model=analysis\', \'_blank\');" data-toggle="tooltip" data-placement="right">要件分析</a></li>';
        }
        tmpHtml += '</ul>';
        tmpHtml += '</div>';
    } else {
        tmpHtml += '<div id="func_more">';
        tmpHtml += translation[dict['func_type']];
        tmpHtml += '</div>';
    }
    return tmpHtml;

}



function showContent(e, data) {
    var translation;
    $.get('/doctree/translation.html', function (data) {
        translation = data;
    }, "json");
    $.get('/doctree/contentData.html',
        {"id": data.node.id},
        function (jsonDT, textStatus) {
            var snippet = '<h1>' + data.node.text + '</h1>';
            var contentTreeData = [];
            if (jsonDT['type'] == '0') {
                var v1 = jsonDT['data']["version"].split(".");
                v1[1] = v1[1] - 1;
                var v2 = jsonDT['data']["version"].split(".");
                v2[1] = v2[1] - 2;
                snippet += `
                        <h4>
                            <div id="spec_file_info" class="dropdown">
                                <a id="drop" href="" class="dropdown-toggle" data-toggle="dropdown">${translation2['version']}<span class="caret"></span></a>
                                <ul class="dropdown-menu">
                                    <li><a href="" data-toggle="tooltip" data-placement="right" >${v1.join(".")}</a></li>
                                    <li><a href="" data-toggle="tooltip" data-placement="right" >${v2.join(".")}</a></li>
                                    
                                </ul>
                            </div>
                            ${jsonDT['data']["version"]}
                        </h4>
                        <h4><div id="spec_file_info">${translation2['spec_file_name']}</div>${jsonDT['data']['spec_file_name']}</h4>
                        <h4><div id="spec_file_info">${translation2['language']}</div>${jsonDT['data']['language']}</h4>
                        `;
            } else if (jsonDT['type'] == '1') {
                snippet += '<table class="table table-striped table-bordered pre-scrollable" >';
                for (var i = 0; i < jsonDT['data'].length; i++) {
                    if (i == 0) {
                        t = 'th';
                    } else {
                        t = 'td';
                    }
                    snippet += '<tr>';
                    snippet += '<' + t + '>';
                    for (var j = 0; j < jsonDT['data'][i]['name'].length; j++) {
                        if (jsonDT['data'][i]['name'][j]['dataType'] == 'STR' || jsonDT['data'][i]['name'][j]['dataType'] == 'REFERENCE') {
                            snippet += jsonDT['data'][i]['name'][j]['dataValue'].join() + '<br/>';
                        }
                    }
                    snippet += '</' + t + '>';
                    snippet += '<' + t + '>';
                    for (var j = 0; j < jsonDT['data'][i]['definition'].length; j++) {
                        if (jsonDT['data'][i]['definition'][j]['dataType'] == 'STR' || jsonDT['data'][i]['definition'][j]['dataType'] == 'REFERENCE') {
                            snippet += jsonDT['data'][i]['definition'][j]['dataValue'].join() + '<br/>';
                        }
                    }
                    snippet += '</' + t + '>';
                    snippet += '</tr>';
                }
                snippet += '</table>';
            } else if (jsonDT['type'] == '2') {
                snippet += '<div id="contentTree"></div><br><br><br><br><br><br><br><br>';
                for (var i = 0; i < jsonDT['data'].length; i++) {
                    var iconSize = parseFloat($("body").css('font-size'));
                    var tmptxt = "";
                    if (jsonDT['data'][i]['func_content'] == '') {

                        tmptxt += testTypeicon(jsonDT['data'][i]['test_type'],iconSize);
                        tmptxt += func_number(jsonDT['data'][i]['id']);
                        tmptxt += func_more(jsonDT['data'][i], translation);
                    } else {
                        if (jsonDT['data'][i]['func_type'] == 'TABLE') {

                            var r = 1;
                            var c = 1;
                            tmptxt += testTypeicon(jsonDT['data'][i]['test_type'],iconSize);
                            tmptxt += func_number(jsonDT['data'][i]['id']);
                            tmptxt += func_more(jsonDT['data'][i], translation);
                            tmptxt += '<div id="func_content">';

                            var ii = 0;
                            var foundTableDT = false;
                            for (; ii < jsonDT['data'][i]['func_content'].length; ii++) {
                                tmptxt += '<p>';
                                for (var iii = 0; iii < jsonDT['data'][i]['func_content'][ii].length; iii++) {
                                    if (jsonDT['data'][i]['func_content'][ii][iii]['dataType'] == 'STR' || jsonDT['data'][i]['func_content'][ii][iii]['dataType'] == 'REFERENCE') {
                                        tmpSTR = jsonDT['data'][i]['func_content'][ii][iii]['dataValue'].join();
                                        if (/COLS.*ROWS/.test(tmpSTR)) {
                                            foundTableDT = true;
                                            c = tmpSTR.split(';')[0].split(']')[1];
                                            r = tmpSTR.split(';')[1].split(']')[1];
                                            break;
                                        } else {
                                            tmptxt += tmpSTR + ' ';
                                        }
                                    }
                                }
                                if (foundTableDT) {
                                    break;
                                }
                                tmptxt += '</p>';

                            }
                            if (foundTableDT) {
                                tmptxt += '<table class="table table-striped table-bordered pre-scrollable" >';
                                for (var j = 0; j < r; j++) {
                                    tmptxt += '<tr>';
                                    if (j == 0) {
                                        t = 'th';
                                    } else {
                                        t = 'td';
                                    }
                                    for (var k = 0; k < c; k++) {
                                        if (jsonDT['data'][i]['func_content'][j + ii + 1][k].length == 0) {
                                            tmptxt += '<' + t + '></' + t + '>';
                                        } else {
                                            tmptxt += '<' + t + '>';
                                            for (var l = 0; l < jsonDT['data'][i]['func_content'][j + ii + 1][k].length; l++) {
                                                if (jsonDT['data'][i]['func_content'][j + ii + 1][k][l]['dataType'] == 'STR' || jsonDT['data'][i]['func_content'][j + ii + 1][k][l]['dataType'] == 'REFERENCE') {
                                                    tmptxt += jsonDT['data'][i]['func_content'][j + ii + 1][k][l]['dataValue'].join() + '<br/>';
                                                }
                                            }
                                            tmptxt += '</' + t + '>';
                                        }
                                    }
                                    tmptxt += '</tr>';
                                }
                                tmptxt += '</table>';
                            }
                            tmptxt += '</div>';
                        } else {
                            tmptxt += testTypeicon(jsonDT['data'][i]['test_type'],iconSize);
                            tmptxt += func_number(jsonDT['data'][i]['id']);
                            tmptxt += func_more(jsonDT['data'][i], translation);
                            tmptxt += '<div id="func_content">';
                            for (var j = 0; j < jsonDT['data'][i]['func_content'].length; j++) {
                                tmptxt += '<p>';
                                for (var k = 0; k < jsonDT['data'][i]['func_content'][j].length; k++) {
                                    if (jsonDT['data'][i]['func_content'][j][k]['dataType'] == 'STR' || jsonDT['data'][i]['func_content'][j][k]['dataType'] == 'REFERENCE') {
                                        tmptxt += jsonDT['data'][i]['func_content'][j][k]['dataValue'].join() + ' ';
                                    } else if (jsonDT['data'][i]['func_content'][j][k]['dataType'] == 'IMG') {
                                        for (var l = 0; l < jsonDT['data'][i]['func_content'][j][k]['dataValue'].length; l++) {
                                            tmptxt += '<img src="/doctree/img.html?img=' + jsonDT['data'][i]['func_content'][j][k]['dataValue'][l].split('/')[1] + '">';
                                        }
                                    }
                                }
                                tmptxt += '</p>';
                            }
                            tmptxt += '</div>';
                        }
                    }
                    contentTreeData.push({
                        "id": jsonDT['data'][i]['func_id'],
                        "parent": jsonDT['data'][i]['parent_function_id'],
                        "text": tmptxt,
                    });
                }
            }

            $("#main").html(snippet);
            $('#contentTree').jstree({
                'core': {
                    'data': contentTreeData,
                    'themes': {
                        'icons': false,
                    },
                },
                plugins: ["noclose"],
            }).on('ready.jstree', function () {
                $(this).jstree('open_all');
                //$('#contentTree .jstree-anchor').each(function () {
                //    $(this).contents().unwrap();
                //});
                $("[data-toggle='tooltip']").tooltip({
                    container: 'body',
                    title: moreInfoTip,
                    html: true,
                });
            });
        }, "json");
}

$('#catalogTree').jstree({
    'core': {
        'check_callback': true,
        'data': [{ "id": "33_1642", "text": "4.2.5.14.4.:DTV受信レベル測定実施" }]
    },
    "plugins": ["search"],
    "search": {"show_only_matches": true},
});

$(function () {

    var to = false;
    $('#searchCatalogTree').keyup(function () {
        if (to) {
            clearTimeout(to);
        }
        to = setTimeout(function () {
            $('#catalogTree').jstree(true).search($('#searchCatalogTree').val());
        }, 1000);
    });

    $('#catalogTree').on('changed.jstree', function (e, data) {
        showContent(e, data);
    });

});
