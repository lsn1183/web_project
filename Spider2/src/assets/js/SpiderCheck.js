import CheckHUDef from './CheckHuDef'
class SpiderCheck {
	constructor(){
	}
	getModule(moduleName){
		let retModule = null
		switch (moduleName) {
			case 'HUDef':
				retModule = new CheckHUDef()
			break;
//			case 'TAGLDef':
//				CheckTAGLDef.check(checkRule,checkData)
//			break;
//			case 'TAGLAna': 
//				CheckTAGLAna.check(checkRule,checkData)
//			break;
		}
		return retModule;
	}
	doCheck(moduleName, checkType, checkData){
		let ret = {
			'result':'NG',
			'reason':'Unknown'
		}
		let checkModule = this.getModule(moduleName)
		if (checkModule == null) {
			ret['reason'] = 'Modulename is error'
			return ret
		}
		let checkRule = checkModule.getCheckRule()
		if (checkType in checkRule){
//			let checkResult = true;
			let checkResult;
			let checkRetBool = true
			for (let checkFunc of checkRule[checkType]){
				checkResult = checkFunc(checkData)
				checkRetBool = checkResult && (checkResult['result'] == 'OK')
				if (checkRetBool == false){
					ret['reason'] = checkResult['reason']
//					console.log(ret,'ret result is error')
					return ret
				}
			}	
		}
		else {
			ret['reason'] = 'Checktype is error'
			return ret
		}
		
		ret['result'] = 'OK'
		ret['reason'] = 'Success'
//		console.log(ret,'ret result is OK')
		return ret	
	}
}
export default SpiderCheck;
