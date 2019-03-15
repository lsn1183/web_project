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
								<td style="width:60%;border:solid 1px #dfe6ec;" colspan="3" align="left">TAGL要件定義ID</td>											
								<td style="width:40%;border:solid 1px #dfe6ec;" align="left">[唯一性]ID必须唯一</td>
								<td style="border:solid 1px #dfe6ec;"></td>
							</tr>
							<tr>
								<td style="border:solid 1px #dfe6ec;" colspan="3" align="left">ユニークID</td>
								<td style="border:solid 1px #dfe6ec;" align="left">必须 <font color="#FF0000">数字</font></td>																										
							</tr>
							<tr>																
								<td style="width:20%;border:solid 1px #dfe6ec;" rowspan="13" align="left">H/U要件定義書から転記</td>
								<td style="width:40%;border:solid 1px #dfe6ec;" colspan="2">H/U要件定義ID</td>
								<td style="width:40%;border:solid 1px #dfe6ec;" rowspan="13" align="left">[一致性]必须与HU表一致</td>
							</tr>
							<tr>																
								<td style="border:solid 1px #dfe6ec;" colspan="2">ユニークID</td>																		
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
							</tr>	
							<tr>																
								<td style="border:solid 1px #dfe6ec;" colspan="2">関連基本要件</td>									
							</tr>
							<tr>																
								<td style="border:solid 1px #dfe6ec;" colspan="2">除外</td>									
							</tr>
							<tr>																
								<td style="width:20%;border:solid 1px #dfe6ec;" rowspan="3">H/U(DCU/MEU)</td>
								<td style="width:20%;border:solid 1px #dfe6ec;">状態</td>									
							</tr>														
							<tr>																									
								<td style="border:solid 1px #dfe6ec;">トリガー</td>									
							</tr>	
							<tr>																									
								<td style="border:solid 1px #dfe6ec;">動作</td>									
							</tr>	
							<tr>																									
								<td style="border:solid 1px #dfe6ec;" colspan="2">備考(HU要件定義)</td>									
							</tr>
					</td>	
				</tr>

				<tr>
					<td style="border:solid 1px #dfe6ec;">
					
							<tr>
								<td style="width:60%;border:solid 1px #dfe6ec;" colspan="3" align="left">DCU/MEUどちらの想定か</td>									
								<td style="width:40%;border:solid 1px #dfe6ec;" align="left">
									必须是 <font color="#FF0000">DCU</font> 或 <font color="#FF0000">MEU</font> <BR/>																				
								</td>
								<td style="border:solid 1px #dfe6ec;"></td>	
							</tr>
							<tr>
								<td style="width:20%;border:solid 1px #dfe6ec;" rowspan="6" align="left">責務分担</td>
								<td style="width:20%;border:solid 1px #dfe6ec;" rowspan="3">TAGL-PF</td>
								<td style="width:20%;border:solid 1px #dfe6ec;">状態</td>
								<td style="width:60%;border:solid 1px #dfe6ec;" align="left">
									格式1：字符个数=1，必须是 <font color="#FF0000">-</font><BR/>
									格式2：字符个数>1，任意字符
								</td>																											
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
								<td style="border:solid 1px #dfe6ec;" colspan="2">抽象デバイス</td>
								<td style="border:solid 1px #dfe6ec;" align="left">
									格式1：字符个数=1，必须是 <font color="#FF0000">-</font><BR/>
									格式2：字符个数=2，必须是 <font color="#FF0000">-※</font><BR/>
									格式3：字符个数>3；任意字符<BR/>																				
								</td>	
							</tr>
							<tr>
								<td style="border:solid 1px #dfe6ec;" colspan="2">備考</td>									
								<td style="border:solid 1px #dfe6ec;" rowspan="2" align="left">										
									格式1：字符个数=1，必须是 <font color="#FF0000">-</font><BR/>
									格式2：字符个数>1，任意字符
								</td>
							</tr>
							<tr>								
								<td style="border:solid 1px #dfe6ec;" colspan="2">責務分担の特記事項</td>
							</tr>								
					</td>								
				</tr>

				<tr>
					<td style="border:solid 1px #dfe6ec;">						
							<tr>
								<td style="width:20%;border:solid 1px #dfe6ec;" rowspan="3" align="left">参考文献</td>									
								<td style="width:40%;border:solid 1px #dfe6ec;" colspan="2">参考ウォークスルー図</td>
								<td style="width:40%;border:solid 1px #dfe6ec;" rowspan="3" align="left">
									格式1：字符个数=1，必须是 <font color="#FF0000">-</font><BR/>
									格式2：字符个数>1，任意字符																				
								</td>
								<td style="border:solid 1px #dfe6ec;"></td>	
							</tr>
							<tr>
								<td style="border:solid 1px #dfe6ec;" colspan="2">参考HAL設計書</td>																										
							</tr>
							<tr>
								<td style="border:solid 1px #dfe6ec;" colspan="2">その他仕様（リファハード仕様等</td>																										
							</tr>																
					</td>								
				</tr>

				<tr>
					<td style="border:solid 1px #dfe6ec;">						
							<tr>
								<td style="width:60%;border:solid 1px #dfe6ec;" colspan="3" align="left">リファレンスハード上での実現可否</td>	
								<td style="width:40%;border:solid 1px #dfe6ec;" align="left">必须是 <font color="#FF0000">〇 △ X</font></td>	
								<td style="border:solid 1px #dfe6ec;"></td>	
							</tr>	
							<tr>
								<td style="border:solid 1px #dfe6ec;" colspan="3" align="left">詳細分析可否</td>		
								<td style="width:40%;border:solid 1px #dfe6ec;" align="left">必须是 <font color="#FF0000">X</font></td>																															
							</tr>	
							<tr>
								<td style="border:solid 1px #dfe6ec;" colspan="3" align="left">未要件分析</td>		
								<td style="width:40%;border:solid 1px #dfe6ec;" align="left">必须是 <font color="#FF0000">〇</font></td>																																
							</tr>	
							<tr>
								<td style="border:solid 1px #dfe6ec;" colspan="3" align="left">更新日</td>	
								<td style="width:40%;border:solid 1px #dfe6ec;" align="left">必须是 <font color="#FF0000">yy-mm-dd</font></td>																																
							</tr>		
							<tr>
								<td style="border:solid 1px #dfe6ec;" colspan="3" align="left">変更理由</td>
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
				this.check_flag = false
				this.check_btn_flag = false
			}
		}
	}
</script>

<style scoped>
	 #CheckRule
	 {
	 	position: absolute;
	    width: 100%;
	    /*height: 100%;*/
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
