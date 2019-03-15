<template>
    <div class="Asa-content">
		<el-collapse v-model="activeNames">
		  <el-collapse-item title="要求式样目录" name="1">
		    <table border="0" cellspacing="0" cellpadding="0">
				<tr><td>カテゴリ</td><td>{{item.category_name}}</td></tr>
				<tr><td>大分類</td><td>{{item.major_category}}</td></tr>
				<tr><td>中分類</td><td>{{item.medium_catetory}}</td></tr>
				<tr><td>小分類(System configuration)</td><td>{{item.small_category}}</td></tr>
				<tr><td>詳細(Related Basic Requirements)</td><td>{{item.detail}}</td></tr>
				<tr><td>機能・開発項目の概要説明</td><td>{{item.dev_summary}}</td></tr>
				<tr><td>Summary of Function and Development item</td><td>{{item.summary}}</td></tr>
				<tr><td>補足</td><td>{{item.extra_info}}</td></tr>
			</table>
		  </el-collapse-item>
		  <el-collapse-item title="要求式样书" name="2">
		  	<table border="0" cellspacing="0" cellpadding="0">
				<tr><td>SubID</td><td>{{item.sub_id}}</td></tr>
				<tr><td>要件ID</td><td>{{item.arl_id}}</td></tr>
				<tr><td>転記してきた要件</td><td>{{item.from_info}}</td></tr>
				<tr><td>備考、不明点</td><td>{{item.memo}}</td></tr>
				<tr><td>除外</td><td>{{item.except}}</td></tr>
				<tr><td>状態</td><td>{{item.status}}</td></tr>
				<tr><td>トリガー</td><td>{{item.trigger}}</td></tr>
				<tr><td>動作</td><td>{{item.action}}</td></tr>
			</table>
		  </el-collapse-item>
		  <el-collapse-item title="目的分类" name="3">
		    <table border="0" cellspacing="0" cellpadding="0">
				<tr><td>ユーザー</td><td>{{itemdestCategory.user}}</td></tr>
				<tr><td>ディーラー</td><td>{{itemdestCategory.dealer}}</td></tr>
				<tr><td>開発者</td><td>{{itemdestCategory.developer}}</td></tr>
				<tr><td>サプライヤー</td><td>{{itemdestCategory.supplier}}</td></tr>
				<tr><td>社内規定</td><td>{{itemdestCategory.company_rule}}</td></tr>
				<tr><td>法規（自工会等を含む)</td><td>{{itemdestCategory.law}}</td></tr>
				<tr><td>過去不具合対応</td><td>{{itemdestCategory.history_problem}}</td></tr>
				<tr><td>目的、背景、ポリシー</td><td>{{itemdestCategory.dest_background}}</td></tr>
			</table>
		  </el-collapse-item>
		  <el-collapse-item title="HMI仕様書" name="4">
		  	<table border="0" cellspacing="0" cellpadding="0">
				<tr><td>仕様書番号</td><td>{{itemHMIbook.book_no}}</td></tr>
				<tr><td>ディーラー</td><td>{{itemHMIbook.version}}</td></tr>
				<tr><td>ファイル名</td><td>{{itemHMIbook.file_name}}</td></tr>
				<tr><td>章</td><td>{{itemHMIbook.chapter}}</td></tr>
				<tr><td>Page</td><td>{{itemHMIbook.page}}</td></tr>
			</table>
		  </el-collapse-item>
		  <el-collapse-item title="機能仕様書" name="5">
		  	<table border="0" cellspacing="0" cellpadding="0">
				<tr><td>仕様書番号</td><td>{{itemFuncbook.book_no}}</td></tr>
				<tr><td>ディーラー</td><td>{{itemFuncbook.version}}</td></tr>
				<tr><td>ファイル名</td><td>{{itemFuncbook.file_name}}</td></tr>
				<tr><td>章</td><td>{{itemFuncbook.chapter}}</td></tr>
				<tr><td>Page</td><td>{{itemFuncbook.page}}</td></tr>
			</table>
		  </el-collapse-item>
		  <el-collapse-item title="其它仕様書" name="6">
		  	<table border="0" cellspacing="0" cellpadding="0">
				<tr><td>I/F仕様</td><td>{{item.IF_book}}</td></tr>
				<tr><td>Center仕様</td><td>{{item.Centent_book}}</td></tr>
				<tr><td>其它仕様</td><td>{{item.Other_book}}</td></tr>
				<tr><td>同件管理</td><td>{{item.Similar_book}}</td></tr>
			</table>
		  </el-collapse-item>
		  <el-collapse-item title="ModelList" name="7" class="table_se">
		  	<table  border="0" cellspacing="0" cellpadding="0">
	            <tr>
	            	<td rowspan="6" style="width: 15%;">Japan</td>
	            	<td rowspan="5">Toyota</span></td>
	                <td>T_EMV (ディスプレイ一体)</td>
	                <td style="width: 35%;">{{item.model_list[0]}}</td>
	            </tr>
	            <tr>
	                <td>T_EMV (Toyota Touch Separate Display)</td>
	                <td>{{item.model_list[1]}}</td>
	            </tr>
	            <tr>
	                <td>T1MEUなし</td>
	                <td>{{item.model_list[2]}}</td>
	            </tr>
	            <tr>
	               <td>T1＋MEU Low</td>
	                <td>{{item.model_list[3]}}</td>
	            </tr>
	            <tr>
	               <td>T1＋MEU High</td>
	                <td>{{item.model_list[4]}}</td>
	            </tr>
	            <tr>
	               <td>Lexus</td>
	                <td>L2</td>
	                <td>{{item.model_list[5]}}</td>
	            </tr>
	        </table>
	        <table  border="0" cellspacing="0" cellpadding="0" class="table_se">
	        	<tr>
	            	<td rowspan="6" style="width: 15%;">N.America</td>
	            	<td rowspan="4">Toyota</span></td>
	                <td>TO</td>
	                <td style="width: 35%;">{{item.model_list[6]}}</td>
	           </tr>
	            <tr>
	               <td>T1</td>
	                <td>{{item.model_list[7]}}</td>
	            </tr>
	            <tr>
	               <td>T2</td>
	                <td>{{item.model_list[8]}}</td>
	            </tr>
	            <tr>
	               <td>T_EMV(Toyota Touch Separate Display)</td>
	                <td>{{item.model_list[9]}}</td>
	            </tr>
	            <tr>
	               <td  rowspan="2">Lexus</td>
	                <td >L1</td>
	                <td>{{item.model_list[10]}}</td>
	            </tr>
	            <tr>
	                <td>L2</td>
	                <td>{{item.model_list[11]}}</td>
	            </tr>
	        </table>
	        <table  border="0" cellspacing="0" cellpadding="0" class="table_se">
	        	<tr>
	            	<td rowspan="6" style="width: 15%;">Europe/Russia</td>
	            	<td rowspan="3">Toyota</span></td>
	                <td>T1</td>
	                <td style="width: 35%;">{{item.model_list[12]}}</td>
	          </tr>
	            <tr>
	               <td>T2</td>
	                <td>{{item.model_list[13]}}</td>
	            </tr>
	            <tr>
	               <td>T_EMV(Toyota Touch Separate Display)</td>
	                <td>{{item.model_list[14]}}</td>
	            </tr>
	            <tr>
	               <td rowspan="3">Lexus</td>
	                <td>L1</td>
	                <td>{{item.model_list[15]}}</td>
	            </tr>
	            <tr>
	            	
	                <td>L1.5</td>
	                <td>{{item.model_list[16]}}</td>
	            </tr>
	            <tr>
	                <td>L2</td>
	                <td>{{item.model_list[17]}}</td>
	            </tr>
	        </table>
	        <table  border="0" cellspacing="0" cellpadding="0" class="table_se">
	        	<tr>
	            	<td rowspan="6" style="width: 15%;">China</td>
	            	<td rowspan="2">Toyota</span></td>
	                <td>T1</td>
	                <td style="width: 35%;">{{item.model_list[18]}}</td>
	            </tr>
	            <tr>
	               <td>T2</td>
	                <td>{{item.model_list[19]}}</td>
	            </tr>
	            <tr>
	               <td rowspan="3">Lexus</td>
	                <td>L1</td>
	                <td>{{item.model_list[20]}}</td>
	            </tr>
	            <tr>
	                <td>L1.5</td>
	                <td>{{item.model_list[21]}}</td>
	            </tr>
	            <tr>
	                <td>L2</td>
	                <td>{{item.model_list[22]}}</td>
	            </tr>
	        </table>
	        <table  border="0" cellspacing="0" cellpadding="0" class="table_se">
	        	<tr>
	            	<td rowspan="3" style="width: 15%;">Hong Kong</td>
	            	<td>Toyota</span></td>
	                <td>T1</td>
	                <td style="width: 35%;">{{item.model_list[23]}}</td>
	           </tr>
	            <tr>
	               <td rowspan="2">Lexus</td>
	                <td>L1</td>
	                <td>{{item.model_list[24]}}</td>
	            </tr>
	            <tr>
	                <td>L2</td>
	                <td>{{item.model_list[25]}}</td>
	            </tr>
	        </table>
	        <table  border="0" cellspacing="0" cellpadding="0" class="table_se">
	        	<tr>
	            	<td rowspan="5" style="width: 15%;">SouthEast Asia / Thailand</td>
	            	<td rowspan="3" >Toyota</span></td>
	                <td>T1</td>
	                <td style="width: 35%;">{{item.model_list[26]}}</td>
	            </tr>
	            <tr>
	               <td>T2</td>
	                <td>{{item.model_list[27]}}</td>
	            </tr>
	            <tr>
	               <td>T_EMV(Toyota Touch Separate Display)</td>
	                <td>{{item.model_list[28]}}</td>
	            </tr>
	            <tr>
	               <td rowspan="2">Lexus</td>
	                <td>L1</td>
	                <td>{{item.model_list[29]}}</td>
	            </tr>
	            <tr>
	                <td>L2</td>
	                <td>{{item.model_list[30]}}</td>
	            </tr>
	        </table>
	        <table  border="0" cellspacing="0" cellpadding="0" class="table_se">
	        	<tr>
	            	<td rowspan="5" style="width: 15%;">Middle East</td>
	            	<td rowspan="3" >Toyota</span></td>
	                <td>T1</td>
	                <td style="width: 35%;">{{item.model_list[31]}}</td>
	            </tr>
	            <tr>
	               <td>T2</td>
	                <td>{{item.model_list[32]}}</td>
	            </tr>
	            <tr>
	               <td>T_EMV(Toyota Touch Separate Display)</td>
	                <td>{{item.model_list[33]}}</td>
	            </tr>
	            <tr>
	               <td rowspan="2">Lexus</td>
	                <td>L1</td>
	                <td>{{item.model_list[34]}}</td>
	            </tr>
	            <tr>
	                <td>L2</td>
	                <td>{{item.model_list[35]}}</td>
	            </tr>
	        </table>
	        <table  border="0" cellspacing="0" cellpadding="0" class="table_se">
	        	<tr>
	            	<td rowspan="5" style="width: 15%;">South and Central America</td>
	            	<td rowspan="3" >Toyota</span></td>
	                <td>T1</td>
	                <td style="width: 35%;">{{item.model_list[36]}}</td>
	            </tr>
	            <tr>
	               <td>T2</td>
	                <td>{{item.model_list[37]}}</td>
	            </tr>
	            <tr>
	               <td>T_EMV(Toyota Touch Separate Display)</td>
	                <td>{{item.model_list[38]}}</td>
	            </tr>
	            <tr>
	               <td rowspan="2">Lexus</td>
	                <td >L1</td>
	                <td>{{item.model_list[39]}}</td>
	            </tr>
	            <tr>
	                <td>L2</td>
	                <td>{{item.model_list[40]}}</td>
	            </tr>
	        </table>
	        <table  border="0" cellspacing="0" cellpadding="0" class="table_se">
	            <tr>
	               <td rowspan="5" style="width: 15%;">Oceania</td>
	            	<td rowspan="3">Toyota</td>
	                <td>T1</td>
	                <td style="width: 35%;">{{item.model_list[41]}}</td>
	            </tr>
	            <tr>
	               <td>T2</td>
	                <td>{{item.model_list[42]}}</td>
	            </tr>
	            <tr>
	               <td>T_EMV(Toyota Touch Separate Display)</td>
	                <td>{{item.model_list[43]}}</td>
	            </tr>
	            <tr>
	               <td rowspan="2">Lexus</td>
	                <td>L1</td>
	                <td>{{item.model_list[44]}}</td>
	            </tr>
	            <tr>
	                <td>L2</td>
	                <td>{{item.model_list[45]}}</td>
	            </tr>
	        </table>
	        <table  border="0" cellspacing="0" cellpadding="0" class="table_se">
	            <tr>
	               <td rowspan="4" style="width: 15%;">Korea</td>
	            	<td rowspan="2">Toyota</td>
	                <td>T1</td>
	                <td style="width: 35%;">{{item.model_list[46]}}</td>
	            </tr>
	            <tr>
	                <td>T2</td>
	                <td>{{item.model_list[47]}}</td>
	            </tr>
	            <tr>
	                <td rowspan="2">Lexus</td>
	                <td>L1</td>
	                <td>{{item.model_list[48]}}</td>
	            </tr>
	            <tr>
	                <td>L2</span>
	                </td>
	                <td>{{item.model_list[49]}}</td>
	            </tr>
	        </table>
	        <table  border="0" cellspacing="0" cellpadding="0" class="table_se">
	            <tr>
	                <td rowspan="5" style="width: 15%;">South Africa</td>
	            	<td rowspan="3">Toyota</td>
	                <td>T1</td>
	                <td>{{item.model_list[50]}}</td>
	            </tr>
	            <tr>
	               <td>T2</td>
	                <td>{{item.model_list[51]}}</td>
	            </tr>
	            <tr>
	               <td>T_EMV(Toyota Touch Separate Display</td>
	                <td>{{item.model_list[52]}}</td>
	            </tr>
	            <tr>
	               <td rowspan="2">Lexus</td>
	                <td>L1</td>
	                <td>{{item.model_list[53]}}</td>
	            </tr>
	            <tr>
	                <td>L2</td>
	                <td>{{item.model_list[54]}}</td>
	            </tr>
	        </table>
	        <table  border="0" cellspacing="0" cellpadding="0" class="table_se">
	            <tr>
	               <td rowspan="5" style="width: 15%;">Taiwan</td>
	            	<td rowspan="3" >Toyota</td>
	                <td >T1</td>
	                <td style="width: 35%;">{{item.model_list[55]}}</td>
	            </tr>
	            <tr>
	               <td>T2</td>
	                <td>{{item.model_list[56]}}</td>
	            </tr>
	            <tr>
	               <td>T_EMV(Toyota Touch Separate Display)</td>
	                <td>{{item.model_list[57]}}</td>
	            </tr>
	            <tr>
	               <td rowspan="2">Lexus</td>
	                <td>L1</td>
	                <td>{{item.model_list[58]}}</td>
	            </tr>
	            <tr>
	                <td>L2</td>
	                <td>{{item.model_list[59]}}</td>
	            </tr>
	        </table>
	        <table  border="0" cellspacing="0" cellpadding="0" class="table_se">
	            <tr>
	               <td rowspan="5" style="width: 15%;">India</span>
	                </td>
	            	<td rowspan="3">Toyota</td>
	                <td>T1</td>
	                <td>{{item.model_list[60]}}</td>
	            </tr>
	            <tr>
	               <td>T2</td>
	                <td>{{item.model_list[61]}}</td>
	            </tr>
	                
	            <tr>
	               <td>T_EMV(Toyota Touch Separate Display)</td>
	                <td>{{item.model_list[62]}}</td>
	            </tr>
	            <tr>
	               <td rowspan="2">Lexus</td>
	                <td>L2</td>
	                <td>{{item.model_list[63]}}</td>
	            </tr>
	        </table>
		  </el-collapse-item>
		  <el-collapse-item title="管理用メモ" name="8">
		    <table border="0" cellspacing="0" cellpadding="0">
	            <tr>
	               <td>担当</td>
	               <td>{{itemmanageMemo.user}}</td>
	            </tr>
	            <tr>
	               <td>未要件分析</td>
	               <td>{{itemmanageMemo.no_analyze}}</td>
	            </tr>
	            <tr>
	               <td>要件漏れ</td>
	               <td>{{itemmanageMemo.miss_content}}</td>
	            </tr>
	            <tr>
	               <td>システム構成ID</td>
	               <td>{{item.system_id}}</td>
	            </tr>
	        </table>
		  </el-collapse-item>
		</el-collapse>
        <div class="fixed">
			<button type="submit" @click='back' class="back">返回</button>
		</div>
    </div>
</template>

<script>
    export default{
      name : 'Asacontent',
      data:function(){
        return{
          itemHMIbook:{},
          item:{model_list:[]},
          itemdestCategory:{},
          itemFuncbook:{},
          itemmanageMemo:{},
          ID:this.$route.params.ARL_id,
          res:'',
          activeNames: ['1','2','3','4'],
     	  model_list:[]
        }
      },
      created(){
      	for(var i=0;i<63;i++){
      		this.item.model_list.push("")
      	}
      	if(this.ID !=""){
      	  this.$axios.get(this.Ip+"/ARLContent/"+this.ID).then(res => {
            this.item=res.data.content
            this.itemHMIbook=res.data.content.HMI_book[0];
            this.itemFuncbook=res.data.content.func_book[0];
            this.itemdestCategory=res.data.content.dest_category;
            this.itemmanageMemo=res.data.content.manage_memo;	
          })	
      	}     
     },
     methods:{
	 	back(){
	             this.$router.push({name:'List'})
				}
     		}
    }
    
</script>

<style scoped>
    *{margin: 0;padding: 0}
    ul,li{list-style: none;}
    a{text-decoration: none;}
    .Asa-content{
      width: 90%;
      height: 100%;
      overflow: scroll;
      margin: 0 auto 30px;
    }
    td{
  	width: 33%;
    text-align: center;
    height: 30px;
    word-break: break-all;
    border: 1px solid #dfe6ec;
    color: #48576a;
  }
  table{
	width: 100%;
    color: #48576;
    background: #fff;
    font-size: 14px;
  }
    .fixed{
  	width: 60px;
    height: 22%;
    position: fixed;
    right: 5%;
    bottom: 35%;
  }
  .back{
  	width: 53px;
    height: 55px;
    text-align: center;
    padding: 10px;
    cursor: pointer;
    border-radius: 50%;
    background: #20a0ff;
    margin: 25% 0;
    opacity: 0.5;
    border: 0 none;
    outline: none;
    color: #fff;
  }
  .back:hover{
	opacity: 1;
	color: white;
	} 
</style>
