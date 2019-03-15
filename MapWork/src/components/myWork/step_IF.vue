<template>
    <div id="add-if">
        
        <div class="div-center">
            <div class="div-title"><h2 class="title">I/F</h2></div>
            <div class="div-input">
                
            </div>  
        </div>
        <div class="div-center">
            <div class="div-title">I/F名:</div>
            <div class="div-input">
                <el-input v-model="file_form[0].if_name" ></el-input>
            </div>  
        </div>

        <div class="div-center">
            <div class="div-title">参数:</div>
            <div class="div-input">
                <el-input v-model="file_form[0].parameter"></el-input>
            </div>  
        </div>

        <div class="div-center">
            <div class="div-title">返回值:</div>
            <div class="div-input">
                <el-input v-model="file_form[0].return_val"></el-input>
            </div>  
        </div>
        <div class="div-center">
            <div class="div-title">接口说明:</div>
            <div class="div-input">
                <el-input v-model="file_form[0].description"></el-input>
            </div>  
        </div>

        <div class="div-center">
            <div class="div-title"></div>
            <div class="div-input" style="text-align: right;">
                <el-button @click="subIFData()" type="primary">确定</el-button>
                <el-button @click="cancel()"  type="primary">取消</el-button>
            </div>  
        </div>
	</div>
</template>

<script>
require('../../assets/js/jquery-1.8.3.min.js')
export default {
    data() {
        return {
            fileList2: [],
            textarea_val: '',
            active: Number(window.sessionStorage.getItem('Step')),
            IF: {
                doc_id: 0,
                parent_sec_id: 0,
                sec_type: 'IF',
                content: [
                    {
                        sec_id: Number(window.sessionStorage.getItem('IFId')),
                        content: ''
                    }
                ]
            },
            file_form: [{
                doc_id: Number(window.sessionStorage.getItem('DocId')),
                if_name: '',
                parameter: '',
                return_val: '',
                description: ''
            }]
        }
    },
    mounted() {},
    methods: {
        subIFData() {
            if (this.file_form.if_name === '') {
                this.$message({
                    showClose: false,
                    message: 'I/F名不能为空',
                    type: 'warning'
                })
                return
            } else if (this.file_form.return_val === '') {
                this.$message({
                    showClose: false,
                    message: '返回值不能为空',
                    type: 'warning'
                })
                return
            } else if (this.file_form.description === '') {
                this.$message({
                    showClose: false,
                    message: '接口说明不能为空',
                    type: 'warning'
                })
                return
            } else {
                this.$axios
                    .post(this.Ip + '/DsDocIf', this.file_form)
                    .then(res => {
                        if (res.data.result == 'OK') {
                            this.$message({
                                showClose: false,
                                message: '添加成功',
                                type: 'success'
                            })
                             this.$router.push('/tagl/File_design/Preview/'+window.sessionStorage.getItem('DocId'))
                        } else {
                            this.$message({
                                showClose: true,
                                message: '添加失败',
                                type: 'error',
                                duration:0,
                            })
                        }
                    })
                    .catch(err => {
                        this.$message({
                                showClose: true,
                                message: '服务异常',
                                type: 'error',
                                duration:0,
                            })
                    })
            }
        },
        cancel() {
            this.$confirm(this.globalData.hint.quit, '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            })
                .then(() => {
                    this.$router.push('/tagl/File_design/Preview/'+window.sessionStorage.getItem('DocId'))
                })
                .catch(() => {})
        }
    }
}
</script>

<style scoped>
#add-if {
    /* margin: 20px; */
    margin: 0 auto;
    /* width: 800px; */
    margin-top: 6%;
}
.div-center {
    text-align: center;
    padding: 17px 0;
}
.div-title {
    display: inline-block;
    width: 90px;
    text-align: right;
    margin-right: 20px;
    color: #4d4d4d;
    font-weight: bold;
}
.div-title-ex {
    width: 127px;
    font-size: 18px;
    margin-right: 13px;
}
.div-input {
    display: inline-block;
    width: 500px;
}
#add-if .el-button {
    padding: 10px 20px;
}
#add-if .el-input__inner {
    height: 36px;
    line-height: 36px;
}
</style>
