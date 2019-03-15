<template>
    <div class="upload-container">
        <el-button icon='el-icon-upload' size="mini" @click=" dialogVisible=true" type="primary">上传图片
        </el-button>
        <el-dialog :visible.sync="dialogVisible">
            <el-upload class="editor-slide-upload" accept="image/*" :action="upload_picture_address" :multiple="true"
            :file-list="fileList" :show-file-list="true" list-type="picture-card" :on-remove="handle_remove"
            :on-success="handle_success" :on-error="handle_error" :before-upload="before_upload">
                <el-button size="small" type="primary">点击上传</el-button>
            </el-upload>
            <span slot="footer">
                <el-button type="primary" @click="handle_submit()" size="small">{{$t('table.confirm')}}</el-button>
                <el-button @click="dialogVisible = false" size="small">{{$t('table.cancel')}}</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
// import { getToken } from 'api/qiniu'
import interface_address from '@/utils/address'
export default {
    name: 'editorSlideUpload',
    props: {
        // color: {
        //   type: String,
        //   default: '#1890ff'
        // }
    },
    data() {
        return {
            dialogVisible: false,
            listObj: {},
            fileList: [],
            upload_picture_address: interface_address + 'api/1.0/testcase/UploadImg'
        }
    },
    methods: {
        check_all_success() {
            return Object.keys(this.listObj).every(item => this.listObj[item].hasSuccess)
        },
        handle_submit() {
            const arr = Object.keys(this.listObj).map(v => this.listObj[v])
            if (!this.check_all_success()) {
                this.$message('请等待所有图片上传成功 或 出现了网络问题，请刷新页面重新上传！')
                return
            }
            this.$emit('successCBK', arr)
            this.listObj = {}
            this.fileList = []
            this.dialogVisible = false
        },
        handle_success(response, file) {
            const uid = file.uid
            const objKeyArr = Object.keys(this.listObj)

            for (let i = 0, len = objKeyArr.length; i < len; i++) {
                if (this.listObj[objKeyArr[i]].uid === uid) {
                    this.listObj[objKeyArr[i]].url = interface_address + 'api/1.0/testcase' + response.result.url
                    this.listObj[objKeyArr[i]].hasSuccess = true
                    return
                }
            }
        },
        handle_error(err, file) {
            const uid = file.uid
            const objKeyArr = Object.keys(this.listObj)

            for (let i = 0, len = objKeyArr.length; i < len; i++) {
                if (this.listObj[objKeyArr[i]].uid === uid) {
                    delete this.listObj[objKeyArr[i]]
                    this.$message({
                        message: '该图片上传异常，请重新上传图片！',
                        type: 'error'
                    })
                    return
                }
            }
        },
        handle_remove(file) {
            const uid = file.uid
            const objKeyArr = Object.keys(this.listObj)
            for (let i = 0, len = objKeyArr.length; i < len; i++) {
                if (this.listObj[objKeyArr[i]].uid === uid) {
                    delete this.listObj[objKeyArr[i]]
                    return
                }
            }
        },
        before_upload(file) {
            const _self = this
            const _URL = window.URL || window.webkitURL
            const fileName = file.uid
            this.listObj[fileName] = {}
            return new Promise((resolve) => {
                const img = new Image()
                img.src = _URL.createObjectURL(file) //createObjectURL用于在浏览器上预览本地图片或视频
                img.onload = function() {
                    _self.listObj[fileName] = {
                        // 将本地图片的信息储存咋listObj中，上传成功之后渲染到富文本框中
                        hasSuccess: false,
                        uid: file.uid,
                        width: this.width,
                        height: this.height
                    }
                }
                resolve(true)
            })
        }
    }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
</style>
