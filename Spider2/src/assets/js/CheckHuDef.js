import CheckBase from './CheckBase'

class CheckHuDef extends CheckBase{
	constructor(){
		super()
		this.checkRule = {
			'option':[this.checkOptionFormat],
		}
	}
	
	getCheckRule(){
		return this.checkRule 
	}
	
	checkOptionFormat(huDataDict){
		let ret = {
			'result':'NG',
			'reason':'checkOptionFormat is error'
		}
		
		if(huDataDict>111){
			ret['result'] = 'OK'
		}
		return ret
	}
	
	checkStatusFormat(huDataDict){
		let ret = {
			'result':'NG',
			'reason':'Unknown'
		}
		return ret
	}
	
	checkStatusSeqNumber(huDataDict){
		let ret = {
			'result':'NG',
			'reason':'Unknown'
		}
		return ret
	}
	
	
}

export default CheckHuDef;