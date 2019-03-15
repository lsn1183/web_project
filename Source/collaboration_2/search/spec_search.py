#coding=utf-8
import xlrd
import re
from elasticsearch import Elasticsearch
from elasticsearch import helpers
from elasticsearch import exceptions
# from flask import current_app

# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')


import importlib  
import sys  
importlib.reload(sys)

def is_num_by_except(num):
	try:
		int(num)
		return True
	except ValueError:
		return False

class excelText:
	modelSpecID = ""
	modelName = ""
	modelUrl = ""
	sheetNames = []
	sheetContents = []

class SpecSearch(object):
	__instance = None

	@staticmethod
	def instance():#public
		"""create a instance"""
		if SpecSearch.__instance is None:
			SpecSearch.__instance = SpecSearch()
		return SpecSearch.__instance

	def __init__(self):
		# curr_app = current_app._get_current_object()
		# ip = curr_app.config['ES_SERVER_IP']
		# port = curr_app.config['ES_SERVER_PORT']
		self.es = Elasticsearch(ip='192.168.64.128', port=9200)  #default ip = localhost, port = 9200, Can rewrite

	def get_index4proj(self, proj_name):#public
		if self.es.indices.exists(proj_name):
			return True
		else:
			return False

	#delete execl data
	def delete_document(self, index, spec_id):#public
		delete_body = {
			"query": { 
				"match": {
					"modelSpecID": str(spec_id)
				}
			}
		}
		try:
			self.es.delete_by_query(index, delete_body)
		except exceptions.ConflictError:
			print("not document")

	#add execl data
	def add_document4excel(self, proj_name, excel, spec_id, url=''):#public
		proj_name = proj_name.strip()
		if(self.__add_index4proj(proj_name)):
			self.__add_excel(proj_name, excel, url, str(spec_id))
		else:
			print ("add document failed!!!")

	def __add_index4proj(self, proj_name):#private
		if self.es.indices.exists(proj_name):
			return True
		else :
			return self.__create_proj_index(proj_name)

	def __add_excel(self, idx, excel, url, spec_id):#private
		contents = self.__dump_excel(excel, spec_id, url)
		excelAction = []
		for i in range(0, len(contents.sheetNames)):
			action = {
				"_index"        : idx,
				"_type"         : "fulltext",
				u"modelSpecID"  : contents.modelSpecID,
				u"modelName"    : contents.modelName,
				u"modelUrl"     : contents.modelUrl,
				u"sheetName"    : contents.sheetNames[i],
				u"sheetContent" : contents.sheetContents[i],
			}
			excelAction.append(action)
		helpers.bulk(self.es, excelAction)
		del excelAction[0:len(excelAction)]

	def __dump_excel(self, excel, modelSpecID, modelUrl):#private
		modelName = (excel.split("/"))[-1]
		wb = xlrd.open_workbook(excel)
		excelAction = excelText()
		print (modelName)
		excelAction.modelSpecID = modelSpecID
		excelAction.modelName = modelName
		excelAction.modelUrl = modelUrl
		del excelAction.sheetNames[:]
		del excelAction.sheetContents[:]

		for sheet_index in range(wb.nsheets):
			sheet = wb.sheet_by_index(sheet_index)
			excelAction.sheetNames.append(sheet.name)
			sheetContent = ""
			for rowindex in range(sheet.nrows):
				rowDatas = sheet.row_values(rowindex)
				cnt = 0
				if len(rowDatas) < 36:
					cnt = len(rowDatas)
				else:
					cnt = 36
				for i in range(0, cnt):
					data = str(rowDatas[i])
					data = data.replace('×', "")
					data = data.replace('○', "")
					sheetContent = sheetContent + data
				sheetContent = sheetContent + "\n"
			excelAction.sheetContents.append(sheetContent)

		return excelAction

	def __create_proj_index(self, index):#private
		index_body = {
			'settings': {
			# just one shard, no replicas
				'number_of_shards': 5,
				'number_of_replicas': 0,
				'index':{
					'analysis':{
						'analyzer':{
							'default':{
								'tokenizer':'ik_smart',     #分词器
							}
						},
						"search_analyzer": {
							'default':{
								'tokenizer':'ik_smart',     #分词器
							}
						}
					}
				}
			},
			'mappings': {
				'fulltext': {
					'dynamic'   : "strict",
					'properties': {
						'modelSpecID' : {'type': 'text'},
						'modelName'   : {'type': 'text'},
						'modelUrl'    : {'type': 'text'},
						'sheetName'   : {'type': 'text'},
						'sheetContent': {'type': 'text'}
					}
				}
			}
		}

		# create empty index
		try:
			self.es.indices.create(
				index=index,
				body=index_body,
			)
			return True
		except exceptions.RequestError as e:
			# ignore already existing index
			if e.error == 'resource_already_exists_exception':
				print (index + " index already exists!!!")
			else:
				print (index + " index creation failed!!!")
			return False

	#search query
	def fun_search(self, proj_name, query):#public
		proj_name = proj_name.strip()
		results = self.__search(proj_name, query)
		result_list = self.__hit_to_dict(results)
		return result_list

	def __search(self, proj_name, query):#private
		search_body = {
			"query": {
				"bool": {
					"should": [
						{
							"match_phrase": {
								"modelName":  {
									"query": query,
									"boost": 3
								}
							}
						},
						{
							"match_phrase": {
								"sheetName":  {
									"query": query,
									"boost": 1.5
								}
							}
						},
						{
							"match_phrase": {
								"sheetContent":  {
									"query": query,
									"boost": 1
								}
							}
						}
					]
				}
			},
		    "highlight": {
		        "fields" : {
		            "sheetContent" : {}
		        }
		    }
		}
		return self.es.search(index = proj_name, doc_type = "fulltext", body = search_body)

	def __hit_to_dict(self, hits):#private
		result_list = []
		if len(hits['hits']['hits']):
			for hit in hits['hits']['hits']:
				hit_dict = dict()
				hit_dict["file_name"] = hit['_source']['modelName']
				hit_dict["title"] = hit['_source']['sheetName']
				hit_dict["url"] = hit['_source']['modelUrl']
				Outline = ""
				if "highlight" in hit.keys():
					Outline = str(hit['highlight']['sheetContent']) \
					.replace("['", "").replace("']", "").replace('◆', "").replace('\', \'', "").replace('★', "") \
					.replace('\\u', "").replace("<em>", "").replace("</em>", "").replace('※', "").replace("\\n","※")
					Outline = re.sub(r"※+", "&#10;", Outline)
					hit_dict["Outline"] = Outline
				else:
					hit_dict["Outline"] = Outline
				result_list.append(hit_dict)
		else:
			hit_dict = dict()
			hit_dict["file_name"] = "None"
			hit_dict["title"] = "None"
			hit_dict["url"] = "None"
			hit_dict["Outline"] = "None"
			result_list.append(hit_dict)
		return result_list

if __name__ == '__main__':
	obj = SpecSearch.instance()
	# obj.add_document4excel("17cy", "/home/yan/project/Demo/func_2_06_POI.xls", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.delete_document("17cy", 206)
	result_list = obj.fun_search("17cy", "poi")
	# for result in result_list:
	# 	print (result['file_name'], result["title"], result["url"])

	# obj.add_document4excel("17cy", "/home/yan/data/Func/[001]SP_MT_104_17CYVehicleParamsManagementSheet_370B_v15_0402.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/[001]SP_MT_125_17CYVehicleParamsManagementSheet_625B_v22_1001.xlsx.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/[001]SP_MT_153_17CYVehicleParamsManagementSheet_733B_v15_0102.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/[001]SP_MT_156_17CYPlusVehicleParamsManagementSheet_773B_v22_1001.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/[001]SP_MT_159_17CYPlusVehicleParamsManagementSheet_805B_v22_1000.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/[001]SP_MT_160_17CYPlusVehicleParamsManagementSheet_791B_v22_1000.xlsx.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/[001]SP_MT_161_17CYPlusVehicleParamsManagementSheet_700B_v22_1000.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/[001]SP_MT_162_17CYVehicleParamsManagementSheet_777B_v15_0002.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/[001]SP_MT_1169_17CYPlusVehicleParamsManagementSheet_645B_22_1000.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/4.8.9.2. 時計調整_表示日時の参考例.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/15-110-1-06846.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/16-505-10-00091_UI.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/17cy_BrowserContentsOperation.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/17cy_BrowserFunctionList.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/17cy_DiagKeyTrace_Info_007.xls", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/17cy_Pio_Guidance_Phrase_Pattern(CN).xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/17cy_Pio_Guidance_Phrase_Pattern(general).xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/17cy_Pio_Voice_ID_list(CN).xls", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/17cy_Pio_Voice_ID_list(general).xls", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/17cy_RegPoint_ImportExport_Format.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/19CY_PreCV適合機種リスト_20180705.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/20181220【原紙_レビュー依頼宛先設定】_車パラ確認依頼リスト.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/AllWords_VR_0.91.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/CarPlay機博d様書問連の結果反映.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/CharacterTableOVS.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/【func_4_37_Customize指摘修正2】func_5_1_02_Bluetooth.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_1_Glossary.xls", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_2_01_Map.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_2_02_Route.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_2_03_Guide.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_2_04_Demo.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_2_05_Highway.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_2_06_POI.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_2_07_RegPoint.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_2_09_Location.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_2_10_交通情報(RTIC).xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_2_11_渋滞予測.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_2_13_DataUpdate.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_2_14_ECO_TOYOTA_MOP.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_2_17_交通情報(TMC).xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_2_21_ProgramUpdate.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_2_23_GpsSensor.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_3_01_SourceSelection.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_3_02_AvSystemSetting.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_3_03_AudioSetting.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_3_04_AvDisplay.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_3_05_Radio.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_3_07_DTV.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_3_08_DISC.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_3_11_AUX.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_3_12_USB.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_3_13_BTAudio.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_3_14_iPod .xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_3_17_Camera.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_3_25_01_Apps_Common.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_3_25_02_Apps_MirrorLink_Miracast.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_3_25_03_Apps_TSL.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_3_25_04_Apps_CarPlay.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_3_25_05_Apps_CarLife.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_3_25_06_Apps_AndroidAuto.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_3_25_Apps.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_3_31_RSE.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_4_01_Setting.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_4_02_Diagnosis_1.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_4_02_Diagnosis_2.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_4_03_VoiceRecog.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_4_04_VoicePlay.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_4_06_Opening.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_4_07_Security.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_4_08_System.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_4_10_Maintenance.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_4_13_KeyPad.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_4_14_CustomKey.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_4_16_QRcode.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_4_17_CarSensor.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_4_19_Personalize.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_4_20_Orbis.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_4_32_meter.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_4_36_AirConditioner.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_4_37_Customize.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_4_37_Customize_New.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_4_38_ClearanceSonar.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_4_39_EnergyFlowDisplay.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_4_40_DriveModeSelect.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_4_41_PneumaticSeat.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_4_44_RemoteService.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_4_46_ElectronicOwnersManual.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_4_48_Weather.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_4_49_TimerCharge.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_5_1_02_Bluetooth.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_5_1_04_Handsfree.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_5_1_06_Phonebook_1.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_5_1_06_Phonebook_2.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_5_1_07_Phonelink.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_5_1_11_MobileAssistant.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_5_1_12_DataCommunicationCommon.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_5_1_12_DataCommunicationCommon_DataCom.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_5_1_12_DataCommunicationCommon_USB.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_5_1_12_DataCommunicationCommon_Wi-Fi.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_5_1_13_Mail.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_5_6_01_Helpnet.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_5_6_02_VehicleInformationUtilization.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_5_6_03_ToyotaProbe.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_5_6_05_ToyotaComAplCommon.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_5_7_01_G-BOOK_Common.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_5_7_02_G-BOOK_Communication.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_5_7_03_G-BOOK_Menu.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_5_7_04_G-BOOK_Application.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_5_7_05_G-BOOK_Operator.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_5_7_06_G-BOOK_MyRequest.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_5_7_07_G-BOOK_Viewer.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_5_7_08_G-BOOK_Navi.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_5_7_09_G-BOOK_CDF.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_5_7_10_G-BOOK_Contract.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_5_7_11_G-BOOK_AutoML.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_5_7_12_G-BOOK_SMS.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_5_7_12_G-BOOK_SMS (1).xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_5_7_13_G-BOOK_Security.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_5_7_G-BOOK.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_6_01_Message.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_9_01_01_DCU-MEU_Outline.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_9_02_01_DCU-MEU_USB_Device.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_9_02_02_DCU-MEU_HIDClassDriverSpecification.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_9_02_03_01_DCU-MEU_LogicalUnitList.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_9_02_03_02_DCU-MEU_LogicalUnitBlockDiagram.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_9_02_03_DCU-MEU_ApparatusControlDriveProtocolSpec.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_9_02_04_DCU-MEU_TCPIP.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_9_03_01_01_DCU-MEU_Wakeup_DCU_Only.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_9_03_01_DCU-MEU_Wakeup.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_9_03_02_DCU-MEU_DeviceAuthentication.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_9_03_03_DCU-MEU_NetworkManager.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_9_03_04_DCU-MEU_FileTransport.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_9_03_06_DCU-MEU_Diag.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_9_03_07_DCU-MEU_TSL.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_9_03_08_DCU-MEU_G-BOOK.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_9_03_09_DCU-MEU_BT_HF.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_9_03_10_DCU-MEU_HMISpec.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_9_03_12_DCU-MEU_NavigationSystem.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_9_03_13_DCU-MEU_VoiceRecog.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_9_03_14_DCU-MEU_Setting.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_9_03_15_DCU-MEU_ProgramUpdate.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_9_03_17_DCU-MEU_SPPLink.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_9_03_18_DCU-MEU_meter.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_9_03_19_DCU-MEU_DataService.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_9_03_20_DCU-MEU_ApplicationDelivery.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_9_03_21_DCU-MEU_RemoteService.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_9_03_24_DCU-MEU_VehicleIndividualParameterSynchronization.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_9_04_01_DCU-MEU_SequenceList.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_9_05_01_DCU-MEU_CommandList.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_99_01_maintenance_ModePassword.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_99_02_maintenance_CaptureStatus.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_99_03_maintenance_ErrorLog.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_99_05_maintenance_AllLog.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_99_07_maintenance_ChangeTime.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_99_09_maintenance_APL_LOG_Setting.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_99_11_maintenance_AutoKeyTest.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_99_12_maintenance_DebugSerial.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_99_13_maintenance_CpuUsage_Output.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_99_21_maintenance_MemoryUsageDisplay.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_99_26_maintenance_DesignCheck.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_99_38_maintenance_ALL_Debug_Off.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_99_39_maintenance_AuthenticationThrough.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_99_40_maintenance_MemoryLeak.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_99_46_maintenance_NaviDebug.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_99_47_maintenance_PhonebookDebug.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_99_48_maintenance_NACOMDebug.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_99_49_maintenance_TestAudioInput.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_99_50_maintenance_TestAudioOutput.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_99_51_maintenance_VoicerecogDebugLog.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_99_53_maintenance_BlinkResetDisplay.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_99_54_maintenance_SlaveTestMode.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_99_56_maintenance_StringIDTestMode.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_99_57_maintenance_LogBatchOutput.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_99_58_maintenance_VersionInformation.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_99_59_maintenance_MEU_Disconnect.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_99_60_maintenance_NoMap.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_99_61_maintenance_ShowImgTxtFrame.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_99_62_maintenance_CNCOMDebug.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_99_63_maintenance_XMModuleInit.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_99_64_maintenance_HDRadioDataDiag.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_99_65_maintenance_XMModuleReset.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/func_99_66_maintenance_Loudness.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/FunctionSetting.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/FunctionTest_5_1_12_DataCommunicationCommon.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/ID51_攔懠摦嶌惍棟_Pana.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/MaintenanceMenu_EditServiceTime.xls", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/Material_CoverArt.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/Material_eCode.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/Material_InternalStorageSave.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/Material_LogicalUnit.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/Material_MaintenanceFeatureList.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/Material_Memory見積もり.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/Material_OFF処理.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/Material_OpenSourceSoftware.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/Material_OpenSourceSoftware.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/Material_Performance.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/Material_PowerOFF.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/Material_ReBootRequest.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/Material_SlaveTest.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/Material_SoftwareBlock.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/Material_SoftwareBlock_ver20.0900.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/Memory見積もり結果.xls", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/PES-S-165-U-Y2設計基準書(固有).xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/PES-S-165-V-Y1設計基準書(共通).xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/PES-S-165-W-Y1設計基準書(共通).xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/POI_Category_VR_0.91.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_13_VRCommandList.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_14_VRCommand_and_Response(EU).xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_14_VRCommand_and_Response(NA).xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_14_VRCommand_and_Response(OTHER).xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_17_割り込み動作.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_89_17CYVehicleParamsManagementSheet_950A.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_90_17CYVehicleParamsManagementSheet_010B.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_90_17CYVehicleParamsManagementSheet_010B_v15_0001.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_91_17CYVehicleParamsDefaultValue_010B.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_92_17CYVehicleParamsDefaultValue_950A.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_93_【010B】Lineup and Combination of the devices.xls", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_94_【950A】Lineup and Combination of the devices.xls", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_95_【278B】Lineup and Combination of the devices.xls", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_96_【180B】Lineup and Combination of the devices.xls", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_98_17CYVehicleParamsManagementSheet_200B.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_99_VRHintWordsList.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_100_17CYVehicleParamsDefaultValue_200B.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_101_17CYVehicleParamsManagementSheet_180B.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_102_17CYVehicleParamsManagementSheet_278B.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_102_17CYVehicleParamsManagementSheet_278B_v15_0002.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_103_17CYVehicleParamsManagementSheet_150B.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_104_17CYVehicleParamsManagementSheet_370B.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_105_LogSetItemList.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_106_17CYVehicleParamsManagementSheet_395B.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_107_17CYVehicleParamsManagementSheet_240B.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_108_17CYVehicleParamsDefaultValue_395B.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_109_17CYVehicleParamsDefaultValue_278B.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_110_17CYVehicleParamsManagementSheet_511B.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_111_17CYVehicleParamsDefaultValue_511B.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_112_17CYVehicleParamsManagementSheet_100B.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_113_17CYVehicleParamsDefaultValue_370B.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_114_17CYVehicleParamsDefaultValue_150B.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_115_17CYVehicleParamsDefaultValue_180B.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_116_17CYVehicleParamsManagementSheet_280B.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_117_17CYVehicleParamsManagementSheet_310B.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_118_17CYVehicleParamsDefaultValue_280B.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_119_17CYVehicleParamsDefaultValue_310B.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_120_17CYVehicleParamsManagementSheet_150B(164B).xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_121_17CYVehicleParamsManagementSheet_488B.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_122_17CYVehicleParamsManagementSheet_480B.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_123_17CYPlusVehicleParamsManagementSheet_550B.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_123_17CYPlusVehicleParamsManagementSheet_550B_v22_0800.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_123_17CYPlusVehicleParamsManagementSheet_550B_v22_0900.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_123_17CYVehicleParamsManagementSheet_550B.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_125_17CYPlusVehicleParamsManagementSheet_625B_v22_0800.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_125_17CYVehicleParamsManagementSheet_625B.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_125_17CYVehicleParamsManagementSheet_625B_v22_0900.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_126_17CYVehicleParamsManagementSheet_585B.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_128_17CYVehicleParamsManagementSheet_555B.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_129_17CYVehicleParamsManagementSheet_603B.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_130_17CYPlusVehicleParamsManagementSheet_683B_v22_0800.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_130_17CYPlusVehicleParamsManagementSheet_683B_v22_0900.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_130_17CYVehicleParamsManagementSheet_683B.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_131_17CYPlusVehicleParamsManagementSheet_400B.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_131_17CYPlusVehicleParamsManagementSheet_400B_v22_0800.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_131_17CYPlusVehicleParamsManagementSheet_400B_v22_0900.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_131_17CYVehicleParamsManagementSheet_400B.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_132_17CYPlusVehicleParamsManagementSheet_643B.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_132_17CYPlusVehicleParamsManagementSheet_643B_v22_1000.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_132_17CYVehicleParamsManagementSheet_643B.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_133_17CYVehicleParamsManagementSheet_575B.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_136_17CYPlusVehicleParamsManagementSheet_570B.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_137_17CYVehicleParamsManagementSheet_636B.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_138_17CYPlusVehicleParamsManagementSheet_500B_ｖ22_0800.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_138_17CYVehicleParamsManagementSheet_500B.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_139_17CYPlusVehicleParamsManagementSheet_675B_v22_0801.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_139_17CYPlusVehicleParamsManagementSheet_675B_v22_0802.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_139_17CYPlusVehicleParamsManagementSheet_675B_v22_0900.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_139_17CYVehicleParamsManagementSheet_675B.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_140_17CYPlusVehicleParamsManagementSheet_350B_v22_0800.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_140_17CYPlusVehicleParamsManagementSheet_350B_v22_0900.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_140_17CYVehicleParamsManagementSheet_350B.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_141_17CYPlusVehicleParamsManagementSheet_360B.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_141_17CYPlusVehicleParamsManagementSheet_360B_v22_0800.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_141_17CYPlusVehicleParamsManagementSheet_360B_v22_0900.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_141_17CYVehicleParamsManagementSheet_360B.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_143_17CYVehicleParamsManagementSheet_657B.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_144_17CYPlusVehicleParamsManagementSheet_656B.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_144_17CYPlusVehicleParamsManagementSheet_656B_v22_0900.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_145_17CYVehicleParamsManagementSheet_545B.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_146_17CYPlusVehicleParamsManagementSheet_722B.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_147_17CYPlusVehicleParamsManagementSheet_405B.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_147_17CYPlusVehicleParamsManagementSheet_405B_v22_0800.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_147_17CYPlusVehicleParamsManagementSheet_405B_v22_0900.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_148_17CYVehicleParamsManagementSheet_667B.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_149_17CYPlusVehicleParamsManagementSheet_610B_v22_0800.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_149_17CYPlusVehicleParamsManagementSheet_610B_v22_1000.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_150_17CYVehicleParamsManagementSheet_494B.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_151_17CYVehicleParamsManagementSheet_703B.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_152_17CYPlusVehicleParamsManagementSheet_415B_v22_0800.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_153_17CYVehicleParamsManagementSheet_733B_v15_0002.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_154_17CYVehicleParamsManagementSheet_743B_v15_0001.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_155_17CYPlusVehicleParamsManagementSheet_357B_v22_0900.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_156_17CYPlusVehicleParamsManagementSheet_773B_v22_0900.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_156_17CYPlusVehicleParamsManagementSheet_773B_v22_1000.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_157_17CYPlusVehicleParamsDefaultValue_AllModel_v22_0900.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_158_17CYPlusVehicleParamsManagementSheet_689B_v22_1000.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_159_17CYPlusVehicleParamsManagementSheet_805B_v22_1000.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_160_17CYPlusVehicleParamsManagementSheet_791B_v22_1000.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_161_17CYPlusVehicleParamsManagementSheet_700B_v22_1000.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_162_17CYVehicleParamsManagementSheet_777B_v15_0002.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_1160_17CYVehicleParamsManagementSheet_421B.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_1161_17CYPlusVehicleParamsDefaultValue_AllModel.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_1162_17CYVehicleParamsManagementSheet_152B_T0北米.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_1163_17CYVehicleParamsManagementSheet_152B_T2北米.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_1164_17CYVehicleParamsManagementSheet_152B_T2豪州.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_1165_17CYPlusVehicleParamsManagementSheet_310B_T2韓国.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_1166_17CYPlusVehicleParamsManagementSheet_180B_T2東南アジア.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_1168_17CYVehicleParamsManagementSheet_716B.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_1169_17CYPlusVehicleParamsManagementSheet_645B.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/SP_MT_1169_17CYPlusVehicleParamsManagementSheet_645B_22_1000.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/T-EMV_儅僀僐儞抂巕攝抲_Ver.0.07.xlsx", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/車両パラメータ管理表の運用.xls", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/メモリ地点入出力フォーマット.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
	# obj.add_document4excel("17cy", "/home/yan/data/Func/【指摘修正】func_5_1_02_Bluetooth.xlsm", 206, '/home/yan/project/Demo/func_2_06_POI.html')
