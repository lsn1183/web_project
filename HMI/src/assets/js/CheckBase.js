class CheckBase {
	constructor() {
	}
	
	getCheckRule(){
		
	}
	
	check(checkRule, checkName, ...checkData){
			let correctFlag = true
			for(let i in checkRule[checkName]){
				correctFlag = correctFlag&&checkRule[checkName][i](checkData)
			}
			return correctFlag
	}
}

export default CheckBase;