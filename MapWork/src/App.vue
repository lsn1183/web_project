<template>
    <div id="app">
        <router-view></router-view>
    </div>
</template>

<script>
import 'babel-polyfill'
export default {
    name: 'App'
}
</script>

<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}
body,
html {
    font-family: '微软雅黑';
}
/* 公用组件样式修改 */
.el-select .el-input.is-focus .el-input__inner,
.el-select .el-input__inner:focus {
    border-color: #dcdfe6;
}
.el-select-dropdown__item.selected {
    color: #42b983;
}
.el-select .el-input.is-focus .el-input__inner {
    color: #42b983;
}
.el-tree--highlight-current .el-tree-node.is-current > .el-tree-node__content {
    background-color: white;
    color: #42b983;
    font-weight: bold;
}
/* MyWork页面 */
#my-tree .el-tree--highlight-current .el-tree-node.is-current > .el-tree-node__content {
    background-color: white;
    color: #42b983;
    font-weight: bold;
}
#my-tree .el-tree--highlight-current .el-tree-node.is-current > .el-tree-node__content .el-tree-node__label {
    font-size: 14px;
}
#my-tree .el-tree--highlight-current .el-tree-node.is-current > .el-tree-node__content {
    background-color: white;
    color: #42b983;
    font-weight: 700;
}
#my-tree .el-tree-node__content span {
    max-width: 150px;
    /* overflow: hidden; */
    white-space: nowrap;
    text-overflow: ellipsis;
    font-size: 14px;
    vertical-align: middle;
}
.gray_col .el-textarea__inner{
    background-color: #FAFAFA;
}
/*consider*/

.drbfm-table .el-table .success-row {
    background: #FAFAFA;
}

.drbfm-table .el-table--enable-row-hover .el-table__body tr {
    pointer-events: none;
}

#consider .el-carousel__indicators--outside button span {
    display: inline-block;
    width: 48px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

#consider .show-t2 .el-carousel__indicators--outside button {
    height: 15px;
    color: red;
}

#consider .el-carousel__arrow {
    background-color: rgba(10, 105, 48, 0.21);
}

#consider .el-carousel__arrow:hover {
    background-color: rgba(10, 105, 48, 0.41);
}
/*basic_designel*/

#badesign-design .el-table td {
    padding: 0;
}
#badesign_design .el-table th {
    padding: 3px 0 3px 0;
}
#Framework-template .el-table th {
    padding: 3px 0 3px 0;
}
#Framework-template .el-table td {
    padding: 0;
}
#Model-template .el-table td {
    padding: 0;
}
#Model-template .el-table th {
    padding: 3px 0 3px 0;
}
#badesign_design .el-dialog__body {
    padding-top: 10px;
}

.el-input__inner:focus {
    border-color: #dcdfe6;
}
/*add-form页面*/
#add-form .el-form-item__content {
    width: auto;
    margin-left: 71px;
}
#add-form .el-upload-dragger {
    height: 108px;
}
#add-form .el-tree__empty-text {
    position: relative;
}
#add-form .el-upload-dragger {
    width: 100%;
    overflow: visible;
}
#add-form .el-form-item {
    margin-bottom: 8px;
    width: 80%;
}
/* authorManage页面 */
#authorManage .el-tabs__content {
    height: 100%;
}
#authorManage .custom-tree-container .el-table thead.is-group th {
    background: white;
}

#authorManage table .el-input__inner {
    border-width: 0;
}
#authorManage .el-tabs-left .el-tabs__header {
    width: 15%;
}
#authorManage .el-tabs__nav-wrap {
    margin-right: 1px;
    padding-top: 20px;
}
#authorManage .el-tabs__item {
    text-align: left;
    padding-left: 35px;
}
#authorManage .div-input .el-input__suffix {
    right: 10px;
}
#authorManage .highlight-col table .cell {
    text-align: center;
}
/* add-file-title页面 */
#add-file-title .el-upload {
    width: 148px;
    text-align: normal;
}
/* homepage页面 */
#homepage .el-menu--horizontal .el-menu-item {
    float: left;
    position: relative;
    height: 40px;
    line-height: 40px;
    margin: 0;
    box-sizing: border-box;
    margin-left: 50px;
    margin-right: 10px;
    padding: 0 5px;
    cursor: pointer;
    color: #909399;
}
#homepage .el-menu-item.is-active,
.el-menu-item.is-active {
    border-bottom: 2px solid #42b983;
}
#treeMap ._v-container > ._v-content > .loading-layer {
    display: none;
}
#homepage .el-menu--horizontal > .el-menu-item:hover,
.el-menu--horizontal > .el-submenu.is-active .el-submenu__title,
.el-menu--horizontal > .el-submenu:hover .el-submenu__title {
    border-bottom: 2px solid #42b983;
}
#homepage .el-menu--horizontal .el-submenu .el-submenu__title {
    height: 40px;
    line-height: 40px;
    margin-left: 10px;
    margin-right: 10px;
}
#homepage .el-menu-item,
.el-submenu__title {
    height: 56px;
    line-height: 56px;
    font-size: 14px;
    color: #48576a;
    padding: 0;
    cursor: pointer;
    position: relative;
    transition: border-color 0.3s, background-color 0.3s, color 0.3s;
    box-sizing: border-box;
    white-space: nowrap;
}
#homepage #nav ul li ul li {
    float: none;
    height: 40px;
    line-height: 40px;
    cursor: pointer;
    position: relative;
    box-sizing: border-box;
    margin: 0;
    padding: 0 26px;
    font-size: 12px;
}
#homepage .el-menu--horizontal .el-submenu > .el-menu {
    position: absolute;
    top: 45px;
    left: 0;
    border: 1px solid #d1dbe5;
    padding: 5px 0px;
    background-color: #fff;
    z-index: 100;
    min-width: 100%;
    box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.12), 0 0 6px 0 rgba(0, 0, 0, 0.04);
}
#nav .el-submenu .el-menu-item {
    height: 50px;
    line-height: 50px;
    padding: 0;
    min-width: 100%;
}
#homepage .header .el-icon-caret-right:before {
    content: '\E606';
    position: absolute;
    color: #42b983;
    left: 8px;
}
#homepage #nav #first_show div:hover {
    border-bottom: 5px solid #42b983;
}
#homepage #nav .el-menu--horizontal .el-submenu {
    float: left;
    position: relative;
    margin-left: 50px;
}

#Scene .el-textarea__inner {
    border: 1px solid white;
    border-radius: 0;
}
#Scene .el-textarea__inner:focus {
    border: 1px solid #42b983;
}

::-webkit-scrollbar-thumb {
    background-color: #ccc;
    height: 50px;
    outline-offset: -2px;
    outline: 2px solid rgb(243, 243, 243);
    border: 2px solid rgb(243, 243, 243);
}

/*--- Click the scroll bar to display the style --*/
::-webkit-scrollbar-thumb:hover {
    background-color: #ccc;
    height: 50px;
}

/*---Scroll bar size--*/
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

/*---滚动框背景样式--*/
::-webkit-scrollbar-track-piece {
    background-color: #fff;
}
.el-tree {
    border: 0 none;
}

#table-OA .cell {
    padding: 0;
}
#team-table .el-table th > .cell {
    word-wrap: normal;
    text-overflow: ellipsis;
    line-height: 30px;
    width: 100%;
    box-sizing: border-box;
    text-align: center;
}
#new .el-table th > .cell {
    word-wrap: normal;
    text-overflow: ellipsis;
    line-height: 30px;
    width: 100%;
    box-sizing: border-box;
    text-align: center;
}
.t-lar .el-table__body-wrapper {
    overflow: hidden;
    position: relative;
    margin-top: -19px;
}
#new .el-table__empty-block {
    position: relative;
    min-height: 0px;
    text-align: center;
    width: 100%;
    height: 100%;
}
#team-table .el-table {
    overflow: hidden;
    width: 100%;
    max-width: 100%;
    background-color: #fff;
    /* border: 1px solid #dfe6ec; */
    font-size: 14px;
    color: #1f2d3d;
    border-left: solid 1px #dfe6ec;
}
#new-head .el-table::before {
    left: 0;
    bottom: 0;
    width: 100%;
    height: 0px;
}

#team-table .el-table td,
.el-table th {
    height: 0px;
}

#team-table .el-table .cell,
.el-table th > div {
    padding-left: 0px;
    padding-right: 0px;
    box-sizing: border-box;
    text-overflow: ellipsis;
}

#new .el-table .cell,
.el-table th > div {
    padding-left: 0px;
    padding-right: 0px;
    box-sizing: border-box;
    text-overflow: ellipsis;
}

.history-content .el-button .el-button--text {
    color: #42b983;
}
.head-center .el-table__body-wrapper {
    overflow: hidden;
    position: relative;
}
#new .el-table td,
.el-table th {
    height: 0px;
    min-width: 0;
    text-overflow: ellipsis;
    vertical-align: middle;
}
.t-lar .el-table {
    overflow: hidden;
    width: 100%;
    max-width: 100%;
    background-color: #fff;
    /* border: 1px solid #dfe6ec; */
    font-size: 14px;
    color: #1f2d3d;
}
.t-lar .el-table th {
    height: 0px;
    min-width: 0;
    text-overflow: ellipsis;
    vertical-align: middle;
}
#new .el-table {
    overflow: hidden;
    width: 100%;
    max-width: 100%;
    background-color: #fff;
    border: 0px solid #dfe6ec;
    font-size: 14px;
    color: #1f2d3d;
}
#team-table .el-table__body-wrapper {
    height: 92.5%;
    overflow: auto;
    position: relative;
    overflow-x: hidden;
}

#dialog .title_arl .el-input__icon + .el-input__inner {
    height: 24px;
}
#dialog .title_arl .el-input {
    width: 180px;
}
#check-rule-left ul li .el-button {
    width: 180px;
}

/* change el-button style */
.el-button--primary:focus,
.el-button--primary:hover {
    background: #42b983;
    border-color: #42b983;
    color: #fff;
}
.el-button--primary {
    color: #fff !important;
    background-color: #42b983;
    border-color: #42b983;
}
.el-button--default {
    border: 1px solid #42b983;
    color: #42b983;
}
.el-button--default:focus,
.el-button--default:hover {
    border-color: #42b983;
    color: #42b983;
}
.el-button--text:focus,
.el-button--text:hover {
    color: #42b983;
}
/*分页器*/

.el-pagination .el-pager li.active {
    border-color: #42b983;
    background-color: #42b983;
    color: white;
}
.el-pager li:hover {
    color: #42b983;
}

.el-menu--horizontal .el-menu .el-menu-item.is-active,
.el-menu--horizontal .el-menu .el-submenu__title.is-active {
    border-bottom: none;
    color: #42b983;
}
.el-checkbox__input.is-checked .el-checkbox__inner {
    background-color: #42b983;
    border-color: #42b983;
}
.el-checkbox__input.is-checked .is-focus .el-checkbox__inner {
    border-color: #42b983;
}
.el-checkbox__inner:hover {
    border-color: #42b983;
}
#dialog .el-button,
.el-textarea__inner {
    font-size: 12px;
    font-family: '微软雅黑';
}
/*提示对话框样式*/
.el-message-box__wrapper .el-message-box .el-message-box__btns button:nth-child(1) {
    margin-left: 10px;
}
.el-message-box__wrapper .el-message-box .el-message-box__btns .el-button {
    float: right;
    margin-bottom: 15px;
}

/*消息提示*/
.message-icon-info {
    background: url(assets/img/Icon/message_icon_info.png);
    width: 40px;
    height: 40px;
    position: absolute;
    left: -12px;
    top: -10px;
}
/*警告提示*/
.message-icon-warning {
    background: url(assets/img/Icon/message_icon_warning.png);
    width: 40px;
    height: 40px;
    position: absolute;
    left: -12px;
    top: -10px;
}
.el-message__group {
    padding-left: 40px;
}
/*对话框样式*/
.el-form-item__content {
    width: 50%;
}
.el-dialog--small {
    width: 22%;
    top: 34% !important;
}

.el-upload {
    width: 100%;
    text-align: left;
}
#book-manage .el-upload{
    width: auto;
    text-align: left;    
}
#arl-title .el-cascader .el-input__inner {
    width: 100%;
    font-weight: normal;
}
#arl-title .el-cascader .el-cascader__label {
    font-weight: normal;
    font-size: 14px;
    line-height: 40px;
}
.table-tr-down > .el-table__header {
    text-align: center;
}
.table-tr-down .el-table_1_column_4:last-of-type div.cell {
    display: flex;
}
.table-tr-down .el-table .cell .el-button--text:hover {
    color: red;
}
.s-section div.el-upload {
    display: block;
}
#CheckListDialog .el-table th.is-leaf {
    border: 0px solid #dfe6ec;
    line-height: 0;
}
#CheckListDialog .el-table {
    font-size: 12px;
}
#table-check-list .el-input__inner {
    font-size: 16px;
}

.el-select-dropdown .el-select-dropdown__wrap {
    max-height: 380px;
}
.el-menu--horizontal {
    border: none;
}

#File-Modle .el-dialog {
    width: 90%;
    /*height: 78%;*/
}
#File-Modle .el-dialog__body {
    min-height: 700px;
}

.usecase .mgleft_box .el-textarea {
    width: 54.5%;
}
#basic-degign-step-one .step-one-content .el-tree .el-tree-node.is-current > .el-tree-node__content {
    background-color: white;
    color: #42b983;
    font-weight: bold;
}
#basic-degign-step-one .el-tree-node__content .el-tree-node__expand-icon.is-leaf {
    display: none;
}
/* #basic-degign-step-one .el-select .el-input.is-focus .el-input__inner,.el-select .el-input__inner:focus{
    border-color: #dcdfe6
} */
/* #File-Modle_box .el-tree--highlight-current .el-tree-node.is-current > .el-tree-node__content {
    background-color: white;
    color: #42b983;
    font-weight: bold;
}
#File-Modle_box .el-tree-node__content {
    vertical-align: middle;
}
#File-Modle_box .el-tree-node__content span{
  max-width: 150px;
  white-space: nowrap;
  text-overflow:ellipsis;
  font-size:14px;
} */
.el-table thead.is-group th {
    background: #edf9f5;
}
#PreviewBody div.el-switch > span.el-switch__label.el-switch__label--left.is-active > span {
    color: #dcdfe6;
}
#PreviewBody .I_F span.el-switch__label--left.el-switch__label {
    color: #42b983;
}
.el-table th{
    background-color: #edf9f5;
}
.el-table td,
.el-table th {
    padding: 5px 0;
}
.el-message-box__status::before {
    color: #42b983;
}
.el-message-box__title {
    font-family: '微软雅黑';
    color: black;
}
.el-message-box__content {
    font-family: '微软雅黑';
    color: black;
}
#img-dialog-box .el-dialog {
    width: 98%;
    overflow: hidden;
    overflow: scroll;
    margin-top: 20px !important;
}
.el-dialog__headerbtn .el-dialog__close {
    font-size: 24px;
    color: #000;
}
.el-tabs__item.is-active {
    color: #42b983;
}
.el-tabs__item:hover {
    color: #42b983;
}
.el-tabs__active-bar {
    background-color: #42b983;
}
.el-breadcrumb__inner.is-link:hover {
    color: #42b983;
}
.el-checkbox__input.is-checked + .el-checkbox__label {
    color: #42b983;
}

.doc-exhibition .doc-exhibition-content .el-tree-node__content > .el-tree-node__expand-icon {
    display: none;
}
.doc-exhibition .doc-exhibition-aside .el-tree-node__content > .el-tree-node__expand-icon {
    display: none;
}
.doc-exhibition .el-tree-node__content {
    cursor: default;
}
.el-button--text {
    color: #42b983;
}

/*prewive*/
.view-box .el-input.el-input--suffix .el-input__inner {
    height: 26px;
}
/*.view-box .el-input{
    height: 26px;
}*/

.doc-exhibition .doc-exhibition-content .el-tree .el-tree-node {
    box-sizing: border-box;
    border: solid 2px white;
}

.doc-exhibition .doc-exhibition-content .el-tree .el-tree-node {
    box-sizing: border-box;
    border: solid 2px white;
}

.doc-exhibition .doc-exhibition-content .el-tree-node__content:hover {
    /* background-color: #fdf59a; */
    color: #42b983;
}
#editor .v-note-wrapper .v-note-panel .v-note-show .v-show-content{
    background:rgb(237,249,245);
}

/* .doc-exhibition .doc-exhibition-content .el-tree>.el-tree-node>.el-tree-node__content {
    background-color: #42b983
} */
/* 媒体查询设置 */
@media screen and (max-width: 1366px) {
    #my-work .el-tree-node__content span {
        font-size: 12px;
    }
    .el-table {
        font-size: 12px;
    }
    .el-pager li {
        font-size: 12px;
    }
    .el-pagination button,
    .el-pagination span:not([class*='suffix']) {
        font-size: 12px;
    }
    #my-tree .el-tree-node__content span {
        font-size: 12px;
    }
    .el-tabs__item {
        font-size: 12px;
    }
    #my-tree .project-title {
        font-size: 12px;
    }
    .el-button {
        font-size: 12px;
    }
    .el-form-item__label {
        font-size: 14px;
    }
}
@media screen and (max-width: 1024px) {
    #my-work .el-tree-node__content span {
        font-size: 12px;
    }
    .el-table {
        font-size: 12px;
    }
    .el-pager li {
        font-size: 12px;
    }
    .el-pagination button,
    .el-pagination span:not([class*='suffix']) {
        font-size: 12px;
    }
    #my-tree .el-tree-node__content span {
        font-size: 12px;
    }
    .el-form-item__label {
        font-size: 14px;
    }
}
.textarea-name .el-input__inner {
    font-family: '\5FAE\8F6F\96C5\9ED1';
    font-size: 12px;
}

</style>
