class Arl {
	constructor(checkRule,checkData){
		this.checkRule = checkRule 
		this.checkData = checkData
	}
	check(checkingData,checkedData){
				let check_flag = false
				let checking_Data = JSON.parse(checkingData)
				let checked_Data = JSON.parse(checkedData)
				if(checking_Data.reason == checked_Data.reason){
					check_flag = true
				}
				delete checking_Data.reason
				delete checked_Data.reason
				if(JSON.stringify(checking_Data)==JSON.stringify(checked_Data)){
					return false
				}else{
						if(check_flag){
							return true
						}else{
							return false
						}
				}
	}
	
}
var ARL = new Arl();
export default ARL;