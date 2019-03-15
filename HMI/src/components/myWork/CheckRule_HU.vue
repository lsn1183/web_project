<template>
	<div id="CheckRule">
		<div id="CheckRule_header">
			<table border="1" style="border-collapse: collapse;text-align: center;width: 100%;height: 64px;border: solid 1px #dfe6ec;">
				<th style="border:solid 1px #dfe6ec;background-color:#eef1f6;">							
					<tr>
						<td style="width:60%;height: 32px;border:solid 1px #dfe6ec;" colspan="3">检查项</td>	
						<td style="width:40%;height: 64px;border:solid 1px #dfe6ec;vertical-align: middle;padding-right: 17.5%;" rowspan="2">检查内容</td>												
					</tr>
					<tr >
						<td style="width:20%;height: 32px;border:solid 1px #dfe6ec;">大项</td>
						<td style="width:20%;height: 32px;border:solid 1px #dfe6ec;">中项</td>
						<td style="width:20%;height: 32px;border:solid 1px #dfe6ec;">小项</td>
						<td style="border:solid 1px #dfe6ec;"></td>
					</tr>	
				</th>
			</table>
		</div>
		<div id="CheckRule_body">
			<table border="1" style="border-collapse: collapse;text-align: center;width: 83%;border: solid 1px #dfe6ec;font-size: 14px;overflow: scroll;" >
				<tr>
					<td style="border:solid 1px #dfe6ec;">													
							<tr>
								<td style="width:20%;border:solid 1px #dfe6ec;" rowspan="11" align="left">ARLから転記</td>		
								<td style="width:40%;border:solid 1px #dfe6ec;" colspan="2">ARLID</td>
								<td style="width:40%;border:solid 1px #dfe6ec;" rowspan="5" align="left">[一致性]必须与ARL表一致</td>
								<td style="border:solid 1px #dfe6ec;"></td>
							</tr>
							<tr>																
								<td style="border:solid 1px #dfe6ec;" colspan="2">大分類</td>										
							</tr>
							<tr>																
								<td style="border:solid 1px #dfe6ec;" colspan="2">中分類</td>
							</tr>
							<tr>																
								<td style="border:solid 1px #dfe6ec;" colspan="2">小分類</td>
							</tr>
							<tr>																
								<td style="border:solid 1px #dfe6ec;" colspan="2">詳細</td>
							</tr>
							<tr>																
								<td style="border:solid 1px #dfe6ec;" colspan="2">基本要件</td>
								<td style="border:solid 1px #dfe6ec;">-</td>
							</tr>
							<tr>																
								<td style="border:solid 1px #dfe6ec;" rowspan="5">ARL要件</td>
								<td style="border:solid 1px #dfe6ec;">要件</td>
								<td style="border:solid 1px #dfe6ec;" rowspan="5" align="left">[一致性]必须与ARL表一致</td>
							</tr>
							<tr>																
								<td style="border:solid 1px #dfe6ec;">状態</td>
							</tr>
							<tr>																
								<td style="border:solid 1px #dfe6ec;">トリガ</td>
							</tr>
							<tr>																
								<td style="border:solid 1px #dfe6ec;">動作</td>
							</tr>
							<tr>																
								<td style="border:solid 1px #dfe6ec;">備考</td>
							</tr>							
					</td>	
				</tr>


				<tr>
					<td style="border:solid 1px #dfe6ec;">							
							<tr>
								<td style="width:60%;border:solid 1px #dfe6ec;" colspan="3" align="left">H/U要件定義ID</td>									
								<td style="width:40%;border:solid 1px #dfe6ec;" align="left">[唯一性]ID必须唯一</td>	
								<td style="border:solid 1px #dfe6ec;"></td>
							</tr>
							<tr>
								<td style="border:solid 1px #dfe6ec;" colspan="3" align="left">ユニークID</td>
								<td style="border:solid 1px #dfe6ec;" align="left">必须 <font color="#FF0000">数字</font></td>																										
							</tr>
						
					</td>							
				</tr>


				<tr>
					<td style="border:solid 1px #dfe6ec;">
						
							<tr>
								<td style="width:20%;border:solid 1px #dfe6ec;" rowspan="6" align="left" >オプション項目</td>									
								<td style="width:40%;border:solid 1px #dfe6ec;" colspan="2">AMP</td>
								<td style="width:40%;border:solid 1px #dfe6ec;" rowspan="6" align="left">必须 <font color="#FF0000">数字[0,3]</font></td>	
								<td style="border:solid 1px #dfe6ec;"></td>	
							</tr>
							<tr>
								<td style="border:solid 1px #dfe6ec;" colspan="2">DSRC</td>																		
							</tr>
							<tr>
								<td style="border:solid 1px #dfe6ec;" colspan="2">DCM</td>																		
							</tr>
							<tr>
								<td style="border:solid 1px #dfe6ec;" colspan="2">RSE</td>																		
							</tr>
							<tr>
								<td style="border:solid 1px #dfe6ec;" colspan="2">TouchPad</td>																		
							</tr>
							<tr>
								<td style="border:solid 1px #dfe6ec;" colspan="2">SeparateDisp</td>																		
							</tr>

						
					</td>							
				</tr>

				<tr>
					<td style="border:solid 1px #dfe6ec;">
					
							<tr>
								<td style="width:60%;border:solid 1px #dfe6ec;" colspan="3" align="left">システム構成</td>									
								<td style="width:40%;border:solid 1px #dfe6ec;" rowspan="2" align="left">-</td>
								<td style="border:solid 1px #dfe6ec;"></td>	
							</tr>
							<tr>
								<td style="border:solid 1px #dfe6ec;" colspan="3" align="left">関連基本要件</td>																		
							</tr>
							<tr>
								<td style="border:solid 1px #dfe6ec;" colspan="3" align="left">除外</td>																		
								<td style="border:solid 1px #dfe6ec;" align="left">必须 <font color="#FF0000">空</font></td>	
							</tr>
						
					</td>								
				</tr>

				<tr>
					<td style="border:solid 1px #dfe6ec;">
							<tr>
								<td style="width:20%;border:solid 1px #dfe6ec;" rowspan="6" align="left">責務分担</td>									
								<td style="width:20%;border:solid 1px #dfe6ec;" rowspan="4">H/U(DCU/MEU)</td>
								<td style="width:20%;border:solid 1px #dfe6ec;">状態</td>
								<td style="width:40%;border:solid 1px #dfe6ec;" align="left">
									格式1：字符个数=1，必须是 <font color="#FF0000">-</font><BR/>
									格式2：字符个数>1，任意字符
								</td>
								<td style="border:solid 1px #dfe6ec;"></td>			
							</tr>
							<tr>
								<td style="border:solid 1px #dfe6ec;">トリガー</td>	
								<td style="border:solid 1px #dfe6ec;" align="left">		
									格式1：字符个数=1，必须是 <font color="#FF0000">-</font><BR/>
									格式2：字符个数>3；起始必须是 <font color="#FF0000">(数字)</font>；<font color="#FF0000">( ) 数字</font>必须是半角
								</td>																		
							</tr>
							<tr>
								<td style="border:solid 1px #dfe6ec;">動作</td>
								<td style="border:solid 1px #dfe6ec;" align="left">
									格式1：字符个数=1，必须是 <font color="#FF0000">-</font><BR/>
									格式2：字符个数>3；起始必须是 <font color="#FF0000">(数字)</font>；<font color="#FF0000">( ) 数字</font>必须是半角
								</td>																				
							</tr>
							<tr>
								<td style="border:solid 1px #dfe6ec;">H/U分類ID</td>
								<td style="border:solid 1px #dfe6ec;" align="left">必须 <font color="#FF0000">数字</font></td>																																				
							</tr>

							<tr>
								<td style="border:solid 1px #dfe6ec;" colspan="2">H/U以外のＭＭ部品</td>
								<td style="border:solid 1px #dfe6ec;" rowspan="2" align="left">
									格式1：字符个数=1，必须是 <font color="#FF0000">-</font><BR/>
									格式2：字符个数=2，必须是 <font color="#FF0000">-※</font><BR/>
									格式3：字符个数>3；任意字符<BR/>																				
								</td>																																			
							</tr>
							<tr>
								<td style="border:solid 1px #dfe6ec;" colspan="2">他部署設計部品(部品名は参考)</td>																												
							</tr>		
					
					</td>							
				</tr>

				<tr>
					<td style="border:solid 1px #dfe6ec;">							
							<tr>
								<td style="width:60%;border:solid 1px #dfe6ec;" colspan="3" align="left">備考</td>									
								<td style="width:40%;border:solid 1px #dfe6ec;">-</td>
								<td style="border:solid 1px #dfe6ec;"></td>		
							</tr>
					
					</td>							
				</tr>

				<tr>
					<td style="border:solid 1px #dfe6ec;">
						
							<tr>
								<td style="width:20%;border:solid 1px #dfe6ec;" align="left" rowspan="10">機能配置を判断したエビデンス</td>									
								<td style="width:20%;border:solid 1px #dfe6ec;">001 システム仕様書</td>
								<td style="width:20%;border:solid 1px #dfe6ec;">
									章/ページ番号<BR/>
									Chapter/Section or Page No
								</td>
								<td style="width:40%;border:solid 1px #dfe6ec;" align="left">必须 <font color="#FF0000">数字</font> 或 <font color="#FF0000">.</font></td>
								<td style="border:solid 1px #dfe6ec;"></td>												
							</tr>
							<tr>									
								<td style="border:solid 1px #dfe6ec;" rowspan="5">003 共通アプリ・AVC-LAN仕様書</td>
								<td style="border:solid 1px #dfe6ec;">
									章/ページ番号<BR/>
									Chapter/Section or Page No
								</td>										
								<td style="border:solid 1px #dfe6ec;" rowspan="5" align="left">
									格式1：字符个数=1，必须是 <font color="#FF0000">-</font><BR/>
									格式2：必须 <font color="#FF0000">包含数字</font><BR/>										
								</td>									
							</tr>
							<tr>									
								<td style="border:solid 1px #dfe6ec;">
									シーケンス仕様<BR/>
									Sequence spec.
								</td>									
							</tr>	
							<tr>									
								<td style="border:solid 1px #dfe6ec;">
									シーケンス番号<BR/>
									Sequence No.
								</td>									
							</tr>	
							<tr>									
								<td style="border:solid 1px #dfe6ec;">
									コマンドガイド<BR/>
									Command guide</td>									
							</tr>		
							<tr>									
								<td style="border:solid 1px #dfe6ec;">OPC</td>									
							</tr>
							<tr>									
								<td style="border:solid 1px #dfe6ec;" rowspan="2">
									318 DCU-MEU間連携仕様書<BR/>
									DCU-MEU interaction spec.</td>
								<td style="border:solid 1px #dfe6ec;">
									機能配置・機能仕様<BR/>
									Function location and spec. 
								</td>
								<td style="width: 50%;border:solid 1px #dfe6ec;" rowspan="4" align="left">必须 <font color="#FF0000">非空</font></td>																			
							</tr>
							<tr>									
								<td style="border:solid 1px #dfe6ec;">
									章/ページ番号<BR/>
									Chapter/Section or Page No
								</td>									
							</tr>
							<tr>									
								<td style="border:solid 1px #dfe6ec;" rowspan="2">
									その他資料<BR/>
									Other document.</td>
								<td style="border:solid 1px #dfe6ec;">
									ドキュメント名 ※トヨタ仕様の場合は仕様番号も記載する事 
								</td>																		
							</tr>
							<tr>									
								<td style="border:solid 1px #dfe6ec;">
									章/ページ番号<BR/>
									Chapter/Section or Page No
								</td>												
							</tr>							
					</td>							
				</tr>

				<tr>
					<td style="border:solid 1px #dfe6ec;">							
							<tr>
								<td style="width:60%;border:solid 1px #dfe6ec;" colspan="3" align="left">テスト結果</td>
								<td style="width:40%;border:solid 1px #dfe6ec;" align="left">-</td>
								<td style="border:solid 1px #dfe6ec;"></td>		
							</tr>
							<tr>
								<td style="width:60%;border:solid 1px #dfe6ec;" colspan="3" align="left">未要件分析</td>																		
								<td style="width:40%;border:solid 1px #dfe6ec;" align="left">必须是 <font color="#FF0000">○</font></td>									
							</tr>
							<tr>
								<td style="width:60%;border:solid 1px #dfe6ec;" colspan="3" align="left">備考1</td>
								<td style="width:40%;border:solid 1px #dfe6ec;" rowspan="4" align="left">-</td>		
							</tr>	
							<tr>
								<td style="width:60%;border:solid 1px #dfe6ec;" colspan="3" align="left">備考2</td>									
							</tr>	
							<tr>
								<td style="width:60%;border:solid 1px #dfe6ec;" colspan="3" align="left">要件漏れチェック</td>									
							</tr>
							<tr>
								<td style="width:60%;border:solid 1px #dfe6ec;" colspan="3" align="left">最終修正担当s</td>									
							</tr>	
							<tr>
								<td style="width:60%;border:solid 1px #dfe6ec;" colspan="3" align="left">日付</td>
								<td style="width:40%;border:solid 1px #dfe6ec;" align="left">必须是 <font color="#FF0000">yy-mm-dd</font></td>		
							</tr>		
																																																				<tr>
								<td style="width:60%;border:solid 1px #dfe6ec;" colspan="3" align="left">変更理由</td>
								<td style="width: 50%;border:solid 1px #dfe6ec;" rowspan="4" align="left">必须 <font color="#FF0000">非空</font></td>
							</tr>
					</td>							
				</tr>
			</table>
		</div>
	</div>		
</template>

<script>
	export default{
		data(){
			return{
				// check_flag: true,
				// check_btn_flag : true,

			}
		},
		methods:{
			check(){
				this.check_flag = true
				this.check_btn_flag = true
			}
		}
	}
</script>

<style scoped>
	 #CheckRule
	 {
	 	position: absolute;
	    width: 100%;
	    height: 100%;
	    margin-top: 83px;
	    margin-left: 28px;
	 }
	 #CheckRule_header{
		position: absolute;
	    left: 0%;
	    top: -63px;
	    right: 8px;
	    z-index: 2;
	    background-color: white;
	}
	#CheckRule_body{
		height: 88%;
	    overflow-y: auto;
	    overflow-x: hidden;
	    border-bottom: 1px solid #dfe6ec;
	}
</style>
