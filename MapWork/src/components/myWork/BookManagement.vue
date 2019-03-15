<template>
    <div class='Append-basic-temlate' id="book-manage">
        <div class="Append-basic-temlate-countent">
            <!-- <div class="header-top">
      </div>
      <div class="header">
      </div> -->
        </div>
        <div class="content-box">
            <div class="mid" v-loading="loading">
                <div class="mid-top" >
                    <div class="block-title">
                        <h2>{{input_title_name}}<i class="el-icon-question" title='请导入式样书' style="font-size:15px;height:20px;vertical-align:middle"></i></h2>
                    </div>
                    <div class="content-box-deep">
                        <div class="label-box">
                                <div class="label-box-text inline-black margin-right-input">
                                    <span>式样书类别</span>
                                </div>
                                <el-select :disabled="input_spec_type_flag" v-model="input_data.spec_type" placeholder="请选择式样书类别" @change="select_input" class="input-width">
                                    <el-option v-for="item in input_type_list" :key="item.fw_id" :label="item.spec_name" :value="item.spec_type" >
                                    </el-option>
                                </el-select>
                                <div class="label-box-text  margin-right-input">
                                    
                                    <span class="inline-black margin-right-input"  >文件</span>
                                    <el-upload style="display:contents;width:50%" ref="upload" :headers="http_header" :show-file-list="show_file_list_flag" :action="up_ip"  :data="input_data" :auto-upload="false"
                                     :on-success='up_success' :before-upload='before_upload' :on-error="up_error" :on-change='up_chang_file' :on-remove="up_remove" >
                                        <el-button size="small" style="width:220px" type="primary"  @click="upload_click_fun" :title="title_alert">上传</el-button>
                                    </el-upload>
                                </div>
                                
                                <div class="label-box-text  margin-right-input">
                                    <span class="inline-black margin-right-input"  >式样书章节号</span>
                                    <el-autocomplete class="input-width" :disabled="input_spec_num_flag" v-model="input_data.spec_num" :fetch-suggestions="querySearch_spec_num" 
                                    placeholder="请填写式样书章节号" @select="handleSelect_spec_num" v-on:input="handleSelect_spec_num"></el-autocomplete>
                                </div>
                                <div class="label-box-text  margin-right-input">
                                    <span class="inline-black margin-right-input">式样书名称</span>
                                    <el-input :disabled="input_spec_name_flag" v-model="input_data.spec_name" v-on:input="handleSelect_spec_name" placeholder="请填写式样书名称" class="input-width"></el-input>
                                    <p class="label-box-text-p">{{spec_name_alert_text}}</p>
                                </div>
                                
                                <div class="label-box-text  margin-right-input">
                                    <span class="inline-black margin-right-input">版本</span>
                                    <el-autocomplete class="input-width"  :disabled="input_spec_ver_flag" v-model="input_data.spec_ver" :fetch-suggestions="querySearch_spec_ver" 
                                    placeholder="请填写式样书版本" @select="handleSelect_spec_ver" v-on:input="handleSelect_spec_ver"></el-autocomplete>
                                </div>
                                
                        </div>
                    </div>
                </div>
                <div style="clear: both;"></div>
                <div class="footer">
                    <el-button size="mini" type="primary" :disabled="upload_determine_flag" @click="determine()">&nbsp;&nbsp;确&nbsp;&nbsp;&nbsp;定&nbsp;&nbsp;</el-button>
                    <el-button size="mini" type="primary" @click="cancel()">&nbsp;&nbsp;退&nbsp;&nbsp;&nbsp;出&nbsp;&nbsp;</el-button>
                    <!-- <el-button size="mini" type="primary" disabled @click="save()">&nbsp;&nbsp;保&nbsp;&nbsp;&nbsp;存&nbsp;&nbsp;</el-button> -->
                </div>
            </div>
            <div class="right">
            </div>
            <div id="img-dialog-box">

            </div>
        </div>
    </div>
</template>
<script>
export default {
    data () {
        return {
            up_ip: this.Ip + "/DSDocInput",
            tableData: [],
            project_list: [],
            upload_flag: true,
            title_alert: '只能上传pdf/excel文件',
            show_file_flag: false,
            input_type_list: [
                {
                    spec_name: "机能式样书",
                    spec_type: "FUNC"
                },
                {
                    spec_name: "要求式样书",
                    spec_type: "REQ"
                },
                {
                    spec_name: "操作式样书",
                    spec_type: "OPE"
                }
            ],
            input_data: {
                spec_type: '',
                spec_name: "",
                spec_num:'',
                spec_ver:'',
                proj_id: '',
                spec_id:0,
                file_name:"",
                replace:false,
            },
            select_input_spec_num:null,
            input_title_name:'式样书添加',
            show_file_list_name:'',
            input_spec_type_flag:false,
            input_spec_num_flag:false,
            input_spec_name_flag:false,
            input_spec_ver_flag:false,
            restaurants_spec_num:[],
            restaurants_spec_ver:[],
            spec_ver_list:[],
            state1:'',
            http_header:{},
            loading:false,
            upload_determine_flag:true,
            spec_name_alert_text:'',
            show_file_list_flag:true
        }

    },
    computed: {
        first_data () {
            return this.input_data.spec_type
        },
        second_data () {
            this.input_data.spec_ver = ''//当式样书名称在变化时，把版本信息初始化
            return this.input_data.spec_name
        },
        three_data () {
            return this.input_data.spec_num
        },
        four_data () {
            return this.input_data.spec_ver
        }
    },
    watch: {
        first_data (val) {
            if (this.input_data.spec_num != "" && this.input_data.spec_name != "" && this.input_data.spec_type != '' && this.input_data.spec_ver) {
                this.upload_flag = false
            } else {
                this.upload_flag = true
            }
        },
        second_data (val) {
            if (this.input_data.spec_num != "" && this.input_data.spec_name != "" && this.input_data.spec_type != ''&& this.input_data.spec_ver) {
                this.upload_flag = false
            } else {
                this.upload_flag = true
            }
        },
        three_data (val) {
            if (this.input_data.spec_num != "" && this.input_data.spec_name != "" && this.input_data.spec_type != ''&& this.input_data.spec_ver) {
                this.upload_flag = false
            } else {
                this.upload_flag = true
            }
        },
        four_data (val) {
            if (this.input_data.spec_num != "" && this.input_data.spec_name != "" && this.input_data.spec_type != ''&& this.input_data.spec_ver) {
                this.upload_flag = false
                if (this.input_data.file_name!='') {
                    this.upload_determine_flag = false
                }else{
                    this.upload_determine_flag = true
                }
            } else {
                this.upload_flag = true
                this.upload_determine_flag = true
            }

        },
    },
    created() {
        this.get_router_path_val_fun()        
    },
    destroyed() {
        if (sessionStorage.getItem('spec_name')) {
            sessionStorage.removeItem('spec_name')
        }
        
    },
    methods: {
        get_router_path_val_fun(){
            let route_data = JSON.parse(this.$route.query.data)
            // console.log(route_data,'==============')
            this.input_data.proj_id = route_data.proj_id
            if (Object.keys(route_data).length > 3 ) {
                this.input_spec_type_flag=true,
                this.input_spec_num_flag=true,
                this.input_spec_name_flag=true;
                // this.input_spec_ver_flag=true;
                this.input_data.spec_num = route_data.spec_num
                this.input_data.spec_type = route_data.spec_type
                this.input_data.spec_name = route_data.spec_name
                this.restaurants_spec_num = route_data.ver_list;
                // this.restaurants_spec_ver = route_data.ver_list
                // let route_data = JSON.parse(this.$route.query.data)
                this.input_data.spec_id = route_data.spec_id
                this.get_ver_list_fun(route_data.spec_id)
                sessionStorage.setItem('spec_name',JSON.stringify(this.input_data.spec_name))
                
            }else{
                this.input_data.spec_type = route_data.input_type
            }
            // console.log(route_data)
            this.select_input()
        },
        querySearch_spec_num(queryString, cb) {
            var restaurant = this.restaurants_spec_num;
            var results = queryString ? restaurant.filter(this.createFilter(queryString)) : restaurant;
            for (let item of results) {
                item.value = item.spec_num
            }//该组件的cb回调方法数据必须是value，所以必须把字段给重新赋值转换
            cb(results);// 调用 callback 返回建议列表的数据
        },
        createFilter(queryString) {
            return (restaurant) => {
                return (restaurant.spec_num.toLowerCase().indexOf(queryString.toLowerCase()) == 0);
            };
        },
        handleSelect_spec_num(item_spec_num){
            // console.log(item_spec_num,'item-select')
            // console.log(Object.keys(item),'item-select----')
            sessionStorage.setItem('spec_name','')  //session初始化
            this.input_data.spec_id = 0   //spec_id初始化
            this.select_input_spec_num = null
            // this.show_file_list_flag=false//输入框，一有改变就清空上传列表隐藏
            if (Object.keys(item_spec_num).includes('spec_num') == true) {
                this.input_data.spec_name = item_spec_num.spec_name
                this.restaurants_spec_ver = item_spec_num.ver_list.sort(this.sort_spec_ver("spec_ver"))
                this.input_data.spec_id = item_spec_num.spec_id
                sessionStorage.setItem('spec_name',JSON.stringify(item_spec_num.spec_name))
                this.select_input_spec_num = item_spec_num
            }else{//当用户是直接输入字符，进而判断是否与已有数据一致
                for (let items of this.restaurants_spec_num) {
                    if (item_spec_num == items.spec_num ) {//判断是否一致，给式样书明赋值
                        this.input_data.spec_name = items.spec_name
                        this.restaurants_spec_ver = items.ver_list.sort(this.sort_spec_ver("spec_ver"))
                        this.input_data.spec_id = items.spec_id
                        sessionStorage.setItem('spec_name',JSON.stringify(items.spec_name))
                        this.select_input_spec_num = items
                        break
                    }else{
                        this.input_data.spec_name = ''
                        sessionStorage.setItem('spec_name','')
                        
                    }
                }
            }
            this.input_data.spec_ver = ''//版本初始化
            this.spec_name_alert_text = ""  //提示语初始化
        },
        querySearch_spec_ver(queryString, cb){
            // console.log(this.restaurants_spec_ver,'this.restaurants_spec_ver----------------')
            var restaurant = this.restaurants_spec_ver;
            var results = queryString ? restaurant.filter(this.createFilter_spec_ver(queryString)) : restaurant;
            for (let item of results) {
                item.value = item.spec_ver
            }//该组件的cb回调方法数据必须是value，所以必须把字段给重新赋值转换
            cb(results);// 调用 callback 返回建议列表的数据
        },
        createFilter_spec_ver(queryString) {
            return (restaurant) => {
                return (restaurant.spec_ver.toLowerCase().indexOf(queryString.toLowerCase()) == 0);
            };
        },
        handleSelect_spec_ver(item){
            // console.log(this.restaurants_spec_ver,'-------')
            // console.log(this.input_data.spec_name == JSON.parse(window.sessionStorage.getItem('spec_name')));
            this.input_data.replace = false
            // this.show_file_list_flag=false//版本输入框，一有改变就清空上传列表隐藏
            for (let items of this.restaurants_spec_ver) {//当用户是直接输入字符，进而判断是否与已有数据一致
                if (item == items.spec_ver && this.input_data.spec_name == JSON.parse(window.sessionStorage.getItem('spec_name')) ) {
                    this.$confirm('是否要覆盖原版本？', '提示', {
                        confirmButtonText: '确定',
                        cancelButtonText: '取消',
                        type: 'warning'
                    }).then(() => {
                        this.input_data.replace = true
                        this.upload_flag = false
                    }).catch(()=>{
                        this.input_data.replace = false
                        this.upload_flag = true
                    })
                }else{
                    this.input_data.replace = false
                }
            }

        },
        handleSelect_spec_name(item){
            // console.log(item,'-----name')
            // console.log(this.select_input_spec_num,'========')
            // this.show_file_list_flag=false//版本输入框，一有改变就清空上传列表隐藏
            for (let spec_num_item of this.restaurants_spec_num) {
                // console.log(spec_num_item.spec_name == this.input_data.spec_name)
                if (spec_num_item.spec_name == this.input_data.spec_name  && spec_num_item.spec_num == this.input_data.spec_num) {
                    // this.spec_name_alert_text = "*该式样书名称已存在，请重命名！"
                    this.get_ver_list_fun(this.input_data.spec_id)  
                    break
                }else if(spec_num_item.spec_name == this.input_data.spec_name  && spec_num_item.spec_num !== this.input_data.spec_num){
                    this.spec_name_alert_text = "*该式样书名称已存在，请重命名！"
                    this.restaurants_spec_ver = []
                    
                    break
                }else{
                    this.spec_name_alert_text = ""
                    if (spec_num_item.spec_name == this.input_data.spec_name) {
                        this.get_ver_list_fun(this.input_data.spec_id)  
                    }else{
                        this.restaurants_spec_ver = []
                    }
                }
            }
            
        },
        up_chang_file(file, fileList){
            // console.log(file, fileList)
            this.show_file_list_flag=true//控制上传文件显示
            if (fileList.length > 1) {
                fileList.shift()
            }
            if (file) {
                this.input_data.file_name = file.name
                if (JSON.parse(this.$route.query.data).type) {
                    console.log(file.name.match( '(_[0-9]+_([0-9]+_)*)')[0].match('([0-9]+_([0-9]+)*)'),'------------')
                    this.input_data.spec_num = file.name.match('(_[0-9]+_([0-9]+_)*)')[0].match('([0-9]+_([0-9]+)*)')[0]
                    let len = file.name.indexOf('.')
                    this.input_data.spec_name = file.name.substring(0,len)
                    // console.log(len,'----------------',JSON.parse(this.$route.query.data))
                    this.handleSelect_spec_num(this.input_data.spec_num)//直接上传文件时候，章节号赋值调用监控章节号输入方法，匹配版本号显示列表
                }
                if (this.spec_name_alert_text !== '') {
                    return
                }
                if (this.input_data.spec_ver !== '') {
                    this.upload_determine_flag = false
                }else{
                    this.upload_determine_flag = true
                }
                return
            }
            this.upload_determine_flag = true

        },
        before_upload (file) {
            // 检查上传文件类型
            if (this.proj_id == '') {
                this.$message({
                    type: 'warning',
                    message: 'please select project!'
                })
                return false
            }
            let file_type = file.type,
                regexp_sheet = RegExp(/.sheet/i),
                regexp_pdf = RegExp(/pdf/i),
                regexp_sheet_xlsm = RegExp(/.ms-excel/i);
            if (file_type.search(regexp_sheet) !== -1) {
                this.loading=true
                return true
            } else if (file_type.search(regexp_pdf) !== - 1) {
                this.loading=true
                return true
            } else if (file_type.search(regexp_sheet_xlsm) !== - 1) {
                this.loading=true
                return true
            } else {
                this.$alert("您上传的文件格式不支持", '提示')
                return false
            }
        },
        up_remove(file, fileList){
            // console.log(file, fileList,'up_remove')
            if (fileList.length == 0) {
                this.upload_determine_flag = true
                this.input_data.file_name = ''
                return
            }
            this.upload_determine_flag = false
        },
        up_success (response, file, fileList) {
            // console.log(response, file, fileList,'response, file, fileList')
            if (response.result == 'OK') {
                this.$message({
                    type: 'success',
                    message: '上传成功!',
                    duration:0,
                    showClose: true,
                })
                this.loading=false
                this.upload_flag = true
                let route_data = JSON.parse(this.$route.query.data)
                if (Object.keys(route_data).length > 3) {//当上传成功后刷新input框-版本信息
                    this.get_ver_list_fun(route_data.spec_id)
                }else if(Object.keys(route_data).length <= 3 && this.input_data.spec_num != ''){
                    // this.get_ver_list_fun(route_data.spec_id)
                    if (this.input_data.spec_id) {
                        this.get_ver_list_fun(this.input_data.spec_id)
                    }
                }
            } else {
                this.loading=false
                this.show_file_list_flag=false
                if (response.result == 'NG') {
                    this.$alert(response.error, '错误提示')
                }
            }
            this.up_remove({},[])//上传完成后清掉上传开关，防止第二次用上一次的状态进行上传
        },
        up_error(err, file, fileList){
            // console.log(err, file, fileList)
            this.loading = false
            this.show_file_list_flag=false
        },
        get_project_list () {
            this.$axios.get(this.Ip + '/Project').then(res => {
                if (res.data.result == 'OK') {
                    this.project_list = res.data.content
                } else {
                    //do nothing
                    this.$message({
                        type: 'error',
                        message: 'requery project error',
                        showClose: true,
                    })
                    return
                }
            })
        },
        select_input () {
            this.upload_flag = true
            // console.log(this.input_data.proj_id,this.input_data.spec_type)
            this.$axios.get(this.Ip + "/DSDocSpecNum/"+ this.input_data.proj_id +'/' + this.input_data.spec_type ).then(res=>{//章节号数据请求
                // console.log(res,'================+++++++++++++++++++')
                if (res.data.result == 'OK') {
                    this.restaurants_spec_num = res.data.content                    
                } else {
                    //do nothing
                    if (res.data.result !== 'NG') {
                        this.$message({
                            type: 'error',
                            message: res.data.error
                        })
                    }
                    
                    return
                }
            })
        },
        upload_click_fun () {
            this.$refs.upload.clearFiles()//清除上传文件列表
            const token = window.sessionStorage.getItem('token')
            if (token) {
                this.http_header.token = token
                this.http_header.Authorization = 'Token ' + token;
            }
        },
      
        determine(){
            // console.log(this.input_data,'----------')
            let datas = {
                "proj_id": this.proj_id,
                "model_id": '',
                accessToken: window.sessionStorage.getItem('accessToken'),
                "username": window.sessionStorage.getItem('Uall')
            };
            this.$axios.post(this.Ip + "/UserRoleCactus", datas).then(res => {
                if (res.data.result == "OK") {
                    var userPermissionData = res.data.content
                    if (this.getCatusPurviewManage(userPermissionData, '式样书添加') == true) {
                        // to do
                        this.$refs.upload.submit();
                    } else {
                        this.$message({
                            type: "warning",
                            message: "您没有权限操作"
                        })
                    }
                } else {
                    // nothing to do
                    this.$message({
                        type: "warning",
                        message: res.data.error
                    })
                }
            })
        },
        
        cancel () {
            this.$router.push('/tagl/BookList');
        },
        get_ver_list_fun(val){
            // console.log(val)
            this.$axios.get(this.Ip + '/DSDocSpecById/'+ val).then(res=>{
                // console.log(res,'-------------------------------')
                if (res.data.result == 'OK') {
                    // this.restaurants_spec_ver.sort(sort_spec_ver("spec_ver"));
                    this.restaurants_spec_ver =res.data.content.sort(this.sort_spec_ver("spec_ver"));
                    // console.log(this.restaurants_spec_ver,'this.restaurants_spec_ver==============')
                } else if(res.data.result == 'NG'){
                    //do nothing
                    this.$message({
                        type: 'error',
                        message: '无数据'
                    })
                    return
                }
            })
        },
        sort_spec_ver(property){//数组对象排序方法
            return function(obj1,obj2){
                var value1 = obj1[property];
                var value2 = obj2[property];
                return value2 - value1;     // 降序
            }
        }
    }
}
</script>

<style scoped>
.label-box-text-p{
    padding: 0 0 0 180px;
    font-size: 12px;
    color: red
}
.input-width{
    width: 541px
}
.inline-black {
    display: inline-block;
    width: 150px
}
.margin-left {
    margin-left: 42px;
}

.margin-right-input {
    margin-right: 21px;
}
.go-doc-text {
    cursor: pointer;
}
.go-doc-text:hover {
    color: #42b983;
}
.Append-basic-temlate {
    margin: 0 auto;
    width: 100%;
    height: 100%;
    /*overflow-y: scroll;*/
}
.Append-basic-temlate-countent {
    max-width: 300px;
    width: 15%;
    height: 100%;
    padding: 20px;
    float: left;
}
.header {
    height: 400px;
    padding: 10%;
    clear: both;
}
.content-box {
    float: left;
    width: 84%;
    padding-left: 1%;
    height: 100%;
    background-color: #fff;
    border-left: 2px solid rgba(216,231,223,.5);
    overflow: scroll;
    overflow-x: hidden;
}
.mid {
    position: relative;
    width: 80%;
    height: 100%;
    float: left;
    padding-right: 20px;
    background-color: #fff;
    border-right: 2px solid rgba(216,231,223,.5);
    /* overflow: scroll; */
    overflow-x: hidden;
}
.mid-top {
    position: absolute;
    top: 0;
    bottom: 55px;
    width: 100%;
    padding-right: 20px;
    overflow-y: scroll;
}
.footer {
    position: absolute;
    bottom: 40px;
    right: 20px;
}
.block-title {
    margin: 40px 0 20px 0;
}
h2 {
    font-size: 22px;
    font-weight: bolder;
    background-color: #6bcca0;
    color: white;
    padding-left: 10px;
    line-height: 25px;
}
.content-box-deep {
    padding-left: 20px;
    color: #606266

}
.label-box {
    width: 100%;
    /* margin: 20px; */
    /* overflow: hidden; */
}
.label-box-text {
    margin-top: 20px;
    margin-bottom: 20px;
    font-size: 14px;
}
.upload-demo {
    margin-top: 10px;
}
.upload-demo-box {
    width: 260px;
    height: 100px;
    /*display: inline-block;*/
}
.add-box {
    /*line-height: 100px;*/
    height: 100px;
    width: 100px;
    padding-top: 20px;
    text-align: center;
    border: 1px double #ccc;
    cursor: pointer;
    font-size: 14px;
    /*margin:20px auto;*/
    margin-top: 20px;
}
.active {
    background: #fff;
}
.up-data-btn {
    width: 330px;
    height: 320px;
    /* margin-left: 20px; */
    /*margin-top:20px;*/
    display: block;
    background: #fff;
    outline: none;
    border: 1px dashed #ccc;
    color: #ccc;
    font-size: 15px;
}
.upload-demo-box {
    width: 330px;
    height: 350px;
    vertical-align: bottom;
    display: inline-block;
}
.Sequence-img {
    width: 100%;
    height: 100%;
}
.img-box {
    width: 350px;
    height: 330px;
    margin-top: 10px;
    padding-right: 20px;
    position: relative;
    display: inline-block;
}
.img-box:hover {
    cursor: pointer;
    border: 1px solid transparent;
    -moz-border-top-colors: red blue white white black;
    -moz-border-right-colors: red blue white white black;
    -moz-border-bottom-colors: red blue white white black;
    -moz-border-left-colors: red blue white white black;
}

.img_icon {
    position: absolute;
    right: 0px;
    top: 0;
    font-size: 24px;
    cursor: pointer;
}
.dialog_img {
    display: block;
    margin: 0 auto;
}
.dialog-title span {
    font-size: 20px;
    margin-right: 20px;
    cursor: pointer;
    color: #42b983;
}
.dialog-title {
    height: 30px;
    line-height: 30px;
    width: 170px;
    margin: 0 auto;
}
.dialogimg {
    display: block;
    margin: 0 auto;
}
.textarea-name {
    font-size: 12px;
    font-family: "\5FAE\8F6F\96C5\9ED1";
}
@media screen and (max-width: 1366px) {
    .up-data-btn {
        width: 230px;
        height: 240px;
        /* margin-left: 20px; */
        display: block;
        background: #fff;
        outline: none;
        border: 1px dashed #ccc;
        color: #ccc;
        font-size: 15px;
    }
    .upload-demo-box {
        width: 250px;
        height: 250px;
        vertical-align: bottom;
        display: inline-block;
    }
    .upload-demo {
        margin-top: 10px;
    }
    .img-box {
        width: 250px;
        height: 250px;
        margin-top: 10px;
        margin-right: 20px;
        position: relative;
        display: inline-block;
    }
}
@media screen and (max-width: 1334px) {
    .Append-basic-temlate-countent {
        max-width: 300px;
        min-width: 200px;
        width: 15%;
        height: 100%;
        padding: 20px;
        float: left;
    }
    .content-box {
        float: left;
        width: 80%;
        height: 100%;
        overflow-y: scroll;
        /*border: 1px solid red;*/
    }
}
@media screen and (max-width: 1024px) {
    .Append-basic-temlate {
        width: 1024px;
    }
    .header-top {
        display: none;
    }
    .Append-basic-temlate-countent {
        width: 180px;
        height: 100%;
        float: left;
    }
    .header {
        height: 100%;
        width: 180px;
        clear: both;
    }
    .content-box {
        float: left;
        width: 820px;
        height: 100%;
        overflow-y: scroll;
        /*border: 1px solid red;*/
    }
    .up-data-btn {
        width: 160px;
        height: 170px;
    }
    .upload-demo-box {
        width: 180px;
        height: 180px;
        vertical-align: bottom;
        display: inline-block;
    }
    .upload-demo {
        margin-top: 0;
    }
    .img-box {
        width: 180px;
        height: 170px;
        margin-top: 10px;
        margin-right: 10px;
        position: relative;
        display: inline-block;
    }
}
</style>
