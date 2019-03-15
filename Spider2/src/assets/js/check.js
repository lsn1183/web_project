	function Base(){

	}
	var checkRule = {
		'param1':'/^\d[0,6]/',
		'param2':'/^\d[6,10]/',
	};
	Base.prototype.DisCheckType = function(checkType,checkRule,checkData){
		switch (checkType) {
			case 'Base':
				this.CheckBase(checkRule,checkData)
			break;
			case 'ARL':
				this.CheckARL(checkRule,checkData)
			break;
			case 'HU':
				this.CheckHU(checkRule,checkData)
			break;
			case 'TAGLDef':
				this.CheckTAGLDef(checkRule,checkData)
			break;
			case 'TAGLAna': 
				this.CheckTAGLAna(checkRule,checkData)
			break;
		}
	}
	
	Base.prototype.CheckBase = function(checkRule,checkData){
		console.log('CheckBase')
		for(var i in checkRule){
			console.log(i)
			consoel.log(checkRule(i))
		}
	}
	Base.prototype.CheckARL = function(checkRule,checkData){
		this.CheckBase();
		console.log('CheckARL')
	}
	Base.prototype.CheckHU = function(checkRule,checkData){
		this.CheckBase();
		console.log('CheckHU')
	}
	Base.prototype.CheckTAGLDef = function(checkRule,checkData){
		this.CheckBase();
		console.log('CheckTAGLDef')
	}
	Base.prototype.CheckTAGLAna = function(checkRule,checkData){
		this.CheckBase();
		console.log('CheckTAGLAna')
	}

	var base = new Base()
 	export default base