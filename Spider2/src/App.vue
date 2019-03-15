<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>
import 'babel-polyfill'
export default {
  name: 'app'
}
</script>

<style>
	*{
		margin:0;
		padding:0;
		box-sizing: border-box;
	}
	::-webkit-scrollbar-thumb{
	   background-color:#ccc;
	   height:50px;
	   outline-offset:-2px;
	   outline:2px solid rgb(243,243,243);
	   -webkit-border-radius:4px;
	   border: 2px solid rgb(243,243,243);
	}

	/*--- Click the scroll bar to display the style --*/
	::-webkit-scrollbar-thumb:hover{
	   background-color:#ccc;
	   height:50px;
	   -webkit-border-radius:4px;
	}

	/*---Scroll bar size--*/
	::-webkit-scrollbar{
	   width:8px;
	   height:8px;
	}

	/*---滚动框背景样式--*/
	::-webkit-scrollbar-track-piece{
	   background-color:#fff;
	   -webkit-border-radius:0;
	}
	.el-tree{
		border: 0 none;
	}


	#team_table .el-table th>.cell {
   	 word-wrap: normal;
   	 text-overflow: ellipsis;
   	 line-height: 30px;
   	 width: 100%;
   	 box-sizing: border-box;
   	text-align: center;
	}
	#new .el-table th>.cell{
		word-wrap: normal;
   	 text-overflow: ellipsis;
   	 line-height: 30px;
   	 width: 100%;
   	 box-sizing: border-box;
   	text-align: center;
	}
	.t_lar .el-table__body-wrapper{
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
	 #team_table .el-table {
	    overflow: hidden;
	    width: 100%;
	    max-width: 100%;
	    background-color: #fff;
	    /* border: 1px solid #dfe6ec; */
	    font-size: 14px;
	    color: #1f2d3d;
	    border-left: solid 1px #dfe6ec;
	}
	#new_head .el-table::before {
	    left: 0;
	    bottom: 0;
	    width: 100%;
	     height: 0px;
	}
	#team_table .el-table td, .el-table th{
		height: 0px;
	}
	#team_table .el-table .cell, .el-table th>div {
	    padding-left: 0px;
	    padding-right: 0px;
	    box-sizing: border-box;
	    text-overflow: ellipsis;
	}
	#new .el-table .cell, .el-table th>div {
	    padding-left: 0px;
	    padding-right: 0px;
	    box-sizing: border-box;
	    text-overflow: ellipsis;
	}

.history_content .el-button .el-button--text{
	color: #42b983;
}
#myTree .el-tree--highlight-current .el-tree-node.is-current>.el-tree-node__content {
    background-color: white;
    color: #42b983;
    font-weight: bold;

}
#myTree .el-tree-node__content{
	margin-left:16px;
}
#myTree  .el-tree  .el-tree__empty-block .el-tree__empty-text{
	position: absolute;
	top: 50%;
	left:50px;
}
#myTree .el-tree .el-loading-mask  .el-loading-spinner{
	margin-left: 55px;
	width: 0;
}
#myTree .el-tree--highlight-current .el-tree-node.is-current>.el-tree-node__content .el-tree-node__label{
	font-size:14px;
}
.head_center .el-table__body-wrapper {
    overflow: hidden;
    position: relative;
}
#new .el-table td, .el-table th {
    height: 0px;
    min-width: 0;
    text-overflow: ellipsis;
    vertical-align: middle;
}
.t_lar .el-table {
    overflow: hidden;
    width: 100%;
    max-width: 100%;
    background-color: #fff;
    /* border: 1px solid #dfe6ec; */
    font-size: 14px;
    color: #1f2d3d;
}
.t_lar .el-table th {
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
#team_table .el-table__body-wrapper {
    height: 92.5%;
    overflow: auto;
    position: relative;
    overflow-x: hidden;
}
#ARLlist .BTN #BTN_top .el-input__inner {
		height: 29px;
}
#myWork .tit_sh .tree_log .el-input__icon+ .el-input__inner{
		height: 24px;
}
#dialog  .title_arl .el-input__icon+ .el-input__inner{
		height: 24px;
}
#dialog  .title_arl .el-input{
		width: 180px;
}
#check_rule_left ul li .el-button{
	width: 180px;
}

#header .el-menu--horizontal .el-menu-item {

	    float: left;
	    height: 40px;
	    line-height: 40px;
	    margin: 0;
	    cursor: pointer;
	    position: relative;
	    box-sizing: border-box;
	    /*border-bottom: 5px solid transparent;*/
	    margin-left: 10px;
	    margin-right: 10px;
}
	#header .el-menu--horizontal.el-menu--dark .el-submenu .el-menu-item.is-active, .el-menu-item.is-active {
	    border-bottom: 5px solid #42b983;
	}
	#treeMap ._v-container>._v-content>.loading-layer{
		display: none;
	}
	#header li#heng.el-menu-item.is-active {
	    border-bottom: 5px solid #42b983;
	}
	#header li#user.el-menu-item.is-active {
	    border-bottom: 5px solid #42b983;
	}
	 #header .el-menu--horizontal>.el-menu-item:hover, .el-menu--horizontal>.el-submenu.is-active .el-submenu__title, .el-menu--horizontal>.el-submenu:hover .el-submenu__title {
    border-bottom: 5px solid #42b983;
	}
#header .el-menu--horizontal .el-submenu .el-submenu__title {
	    height: 40px;
	    line-height: 40px;
	    margin-left: 10px;
	    margin-right: 10px;
	}
	#header .el-menu-item, .el-submenu__title {
    height: 56px;
    line-height: 56px;
    font-size: 14px;
    color: #48576a;
    padding: 0;
    cursor: pointer;
    position: relative;
    transition: border-color .3s,background-color .3s,color .3s;
    box-sizing: border-box;
    white-space: nowrap;
}
#header #nav ul li ul li{
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
	#header .el-menu--horizontal .el-submenu>.el-menu {
    position: absolute;
    top: 45px;
    left: 0;
    border: 1px solid #d1dbe5;
    padding: 5px 0px;
    background-color: #fff;
    z-index: 100;
    min-width: 100%;
    box-shadow: 0 2px 4px 0 rgba(0,0,0,.12), 0 0 6px 0 rgba(0,0,0,.04);

	}
	#nav .el-submenu .el-menu-item {
    height: 50px;
    line-height: 50px;
    padding: 0;
    min-width: 100%;
	}
/* change el-button style */
.el-button--primary:focus, .el-button--primary:hover {
    background: #42b983;
    border-color: #42b983;
    color: #fff;
	}
	.el-button--primary {
    color: #fff !important;
    background-color: #42b983;
    border-color: #42b983;
 }
 .el-button--default{
    border: 1px solid #42b983;
    color: #42b983;
 }
 .el-button--default:focus, .el-button--default:hover {
    border-color: #42b983;
    color: #42b983;
	}
	.el-button--default {
     color: none;
}
.el-button--text:focus, .el-button--text:hover {
    color: #42b983;
	}
	.el-button--text {
     color: #42b983;
  }
  /*分页器*/


     .el-pagination .el-pager li.active {
     border-color: #42b983;
     background-color: #42b983;
     color: white;
  }
  	 .el-pager li:hover{
  	 color: #42b983;
  }
#header .el-icon-caret-right:before {
    content: "\E606";
    position: absolute;
    color: #42b983;
    left: 8px;
}
#header #nav #first_show div:hover{
	border-bottom: 5px solid #42b983;
}
#header #nav .el-menu--horizontal .el-submenu {
    float: left;
    position: relative;
    margin-left: 60px;
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
#dialog .el-button, .el-textarea__inner{
		font-size: 12px;
		font-family: "微软雅黑";
	}
	/*提示对话框样式*/
	.el-message-box__wrapper .el-message-box .el-message-box__btns button:nth-child(1) {
    margin-left: 10px;
	}
	.el-message-box__wrapper .el-message-box .el-message-box__btns .el-button {
	    float: right;
	    margin-bottom: 15px;
	}
#HUWorkerDialog .el-cascader__label {
    line-height: 40px;
    font-size: 14px;
    font-weight: bold;
    width: 370px;
    background: rgba(238,241,246,.2);
}

#HUWorkerDialog .el-textarea__inner {
    resize: vertical;
    border: 1px solid #bfcbd9;
    border-radius: 0;
}
#HUWorkerDialog .el-input__inner{
	border: 0px solid black;
}
#HUWorkerDialog .el-cascader .el-input, .el-cascader .el-input__inner {
    cursor: pointer;
    width: 370px;
}
#HUWorkerDialog .el-textarea.is-disabled .el-textarea__inner {
    background-color: #fbfdff;
    border-color: #d1dbe5;
    color: #bbb;
    cursor: not-allowed;
}
/*消息提示*/
	.message_icon_info {
		background: url(assets/img/Icon/message_icon_info.png);
    width: 40px;
    height: 40px;
    position: absolute;
    left: -12px;
    top: -10px;
	}
	/*警告提示*/
	.message_icon_warning {
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
	#myWork .group .el-input__inner{
		height:29px
	}
	.el-upload{
		width: 100%;
		text-align: normal
	}
	#arl_title  .el-cascader .el-input__inner{
		width: 100%;
		font-weight: normal;
	}
	#arl_title  .el-cascader .el-cascader__label{
		font-weight: normal;
		font-size: 14px;
		line-height:40px;
	}
  	/*ImportExport-Table表格样式*/
  	.table_tr_down>.el-table__header{
    	text-align: center;
  	}
  	.table_tr_down .el-table_1_column_4:last-of-type div.cell{
    	display: flex;
    	/*align-content: center;*/
  	}
  	.table_tr_down .el-table .cell .el-button--text:hover{
    	color: red;
  	}
  	.s_section div.el-upload {
    	display: block;
  	}
	#CheckListDialog .el-table th.is-leaf {
	    border: 0px solid #dfe6ec;
	    line-height: 0;
	}
	#CheckListDialog .el-table {
   		font-size: 12px;
	}
  #table_check_list .el-input__inner{
    font-size: 16px;
  }
</style>
