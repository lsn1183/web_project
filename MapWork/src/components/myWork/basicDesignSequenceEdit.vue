<template>
    <div class="wrapper">
        <div class="tree-box">
            <ul class="tree-ul">
                <li v-for="(node,index) in treeArr" class="tree-li">
                    <p @click="firstScrollTop(index)" class="first-title">
                        <i class="el-icon-caret-right"></i> {{node.node_name}}
                    </p>
                    <ul class="child_ul">
                        <li class="child-tree-li" v-for="(child_node, child_index) in node.child_node">
                            <p @click="secondScrillTop(index, child_index)" class="second-title">
                                {{child_node.node_name}}
                            </p>
                        </li>
                    </ul>
                </li>
            </ul>
        </div>
        <div class="content-box">
            <h1 class="title_h1">{{title}}</h1>
            <p class="title-detail">
                <span>由hongcz创建，最终由liuxd修改于2018-11-27</span>
            </p>

            <!-- Usecase -->
            <div class="Usecase-box Asa-box">
                <h3 class="title-h3">
                    <span>Sequence</span>
                    <span class="append-span" style="margin-left: 20px;" @click="addSequence()">[ 添加 ]</span>
                </h3>
                <p class="message" v-show="isEmptyArr">暂无数据</p>
                <!-- Usecase 子元素块 -->
                <div class="msg-box" v-for="(item, index) of subData.section_list">
                    <h4 class="title-h4">
                        <span>Sequence{{ index + 1 }}</span>
                        <div style="display: inline-block; margin-left: 20px; width: 300px;height: 24px;">
                            <el-input placeholder="请输入sequence名称" size="mini" clearable v-model="item.sec_title"></el-input>
                        </div>
                        <span class="append-span" @click="delUsecase(index)">&nbsp;[ 删除 ]</span>
                    </h4>
                    <div class="content-size">
                        <span>Sequence说明 : </span>
                        <div class="editor">
                            <mavon-editor v-model="item.explain" :editable='true' :subfield='true' defaultOpen='edit' :toolbarsFlag='true' :scrollStyle='true' :toolbars="toolbars"></mavon-editor>
                        </div>
                    </div>
                    <div class="content-size">
                        <span>Sequence图 : </span>
                        <div class="editor">
                            <div class="img-box-ex" v-for='(src, index_img) in item.content'>
                                <img :src="src.url" alt="" @click="showImgDialog(src.url)" class="Sequence-img">
                                <i class="el-icon-close img_icon" style="float:right" @click='deleteImg(item.content, index_img)'></i>
                            </div>
                            <div class="upload-demo-box">
                                <el-upload class="upload-demo" :action='upImgIp' :on-preview="handlePreview" :before-upload="beforeUpload" :on-success='uploadSuccessHandler' :show-file-list='false'>
                                    <button @click='get_index(index)' class="up-data-btn">
                                        <i class="el-icon-picture"></i>点击上传</button>
                                </el-upload>
                            </div>
                        </div>
                    </div>
                    <div class="content-size">
                        <span>补足说明 : </span>
                        <div class="editor">
                            <mavon-editor v-model="item.complement" :editable='true' :subfield='true' defaultOpen='edit' :toolbarsFlag='true' :scrollStyle='true' :toolbars="toolbars"></mavon-editor>
                        </div>
                    </div>

                    <div class="content-size" v-if="docType == 'DETAIL'">
                        <span>Activity</span>
                        <span class="append-span" style="margin-left: 20px;" @click="addActivity(index)">[ 添加 ]</span>

                        <div v-for='(activityItem, activityIndex) in item.Activity'>
                            <div class="content-size">
                                <span> Activity{{activityIndex+1}}</span>
                                <div style="display: inline-block; margin-left: 20px; width: 300px;height: 24px;">
                                    <el-input placeholder="请输入Activity名称" size="mini" clearable v-model="activityItem.sec_title"></el-input>
                                </div>
                                <span class="append-span" style="margin-left: 6px;" @click='delActivity(index, activityIndex)'>&nbsp;[ 删除 ]</span>
                            </div>

                            <div class="content-size">
                                <span>Activity{{ activityIndex + 1}}说明 : </span>
                                <div class="editor">
                                    <mavon-editor v-model="activityItem.explain" :editable='true' :subfield='true' defaultOpen='edit' :toolbarsFlag='true' :scrollStyle='true' :toolbars="toolbars"></mavon-editor>
                                </div>
                            </div>
                            <div class="content-size">
                                <span>Activity图 : </span>
                                <div class="editor">
                                    <div class="img-box-ex" v-for='(src, index_img) in activityItem.content'>
                                        <img :src="src.url" alt="" @click="showImgDialog(src.url)" class="Sequence-img">
                                        <i class="el-icon-close img_icon" style="float:right" @click='deleteActivityImg(activityItem.content, index_img)'></i>
                                    </div>
                                    <div class="upload-demo-box">
                                        <el-upload class="upload-demo" :action='upImgIp' :on-preview="handlePreview" :before-upload="beforeUpload" :on-success='uploadActivitySuccess' :show-file-list='false'>
                                            <button @click='getActivityIndex(index, activityIndex)' class="up-data-btn">
                                                <i class="el-icon-picture"></i>点击上传</button>
                                        </el-upload>
                                    </div>
                                </div>
                            </div>
                            <div class="content-size">
                                <span>Activity{{ activityIndex + 1}} 补足说明 : </span>
                                <div class="editor">
                                    <mavon-editor v-model="activityItem.complement" :editable='true' :subfield='true' defaultOpen='edit' :toolbarsFlag='true' :scrollStyle='true' :toolbars="toolbars"></mavon-editor>
                                </div>
                            </div>

                        </div>
                    </div>

                    <div class="content-size">
                        <span>资源 : </span>
                        <div class="editor">
                            <el-table :data="item.Resource" border>
                                <el-table-column label="名称" prop="rsc_name" width="220" align='center'>
                                </el-table-column>
                                <el-table-column label="内容">
                                    <template slot-scope="scope">
                                        <div v-if="scope.row.rsc_name === 'CPU' || scope.row.rsc_name === '内存'? false : true" style="display:flex;justify-content: space-around;">
                                            <el-input type="textarea" v-model="scope.row.val" :autosize="{ minRows: 1, maxRows:4}"></el-input>
                                        </div>
                                        <div v-if="scope.row.rsc_name === 'CPU' || scope.row.rsc_name === '内存'? true : false" style="display:flex;justify-content: space-around;">
                                            <el-select v-model="scope.row.operator" placeholder="请选择" size="small">
                                                <el-option v-for="item in standardOptions" :key="item.value" :label="item.label" :value="item.value">
                                                </el-option>
                                            </el-select>
                                            <el-input v-model="scope.row.value" size="small" type="text" @focus="checkout(scope.row)" @blur="clearInterval" onkeypress="return event.keyCode>=48&&event.keyCode<=57" placeholder="请输入数字"></el-input>
                                            <el-select v-model="scope.row.unit" placeholder="请选择单位" v-if="scope.row.rsc_name === 'CPU' ? true : false" size="small" title="CPU单位">
                                                <el-option v-for="item in CPU_unit" :key="item.value" :label="item.label" :value="item.value">
                                                </el-option>
                                            </el-select>
                                            <el-select v-model="scope.row.unit" placeholder="请选择单位" v-if="scope.row.rsc_name === '内存'? true : false" size="small" title="内存单位">
                                                <el-option v-for="item in memory_unit" :key="item.value" :label="item.label" :value="item.value">
                                                </el-option>
                                            </el-select>
                                        </div>

                                    </template>
                                </el-table-column>
                            </el-table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div id="img-dialog-box">
            <el-dialog :visible.sync="dialogTableVisible">
                <p class="dialog-title">
                    <span>
                        <i class="el-icon-circle-plus" @click='enlargeImg()'></i>
                    </span>
                    <span>{{show_num}}%</span>
                    <span>
                        <i class="el-icon-remove" @click='shrinkImg()'></i>
                    </span>
                </p>
                <img :src="imgSrc" alt="" class='dialog-img'>
            </el-dialog>
        </div>
        <div class="footer">
            <el-button size="mini" type="primary" @click="confirm()">&nbsp;&nbsp;确&nbsp;&nbsp;&nbsp;定&nbsp;&nbsp;</el-button>
            <el-button size="mini" type="primary" @click="cancel()">&nbsp;&nbsp;退&nbsp;&nbsp;&nbsp;出&nbsp;&nbsp;</el-button>
        </div>
    </div>
</template>
<script>
require('../../assets/js/jquery-1.8.3.min.js')
export default {
    data() {
        return {
            arr: [],
            treeArr: [
                {
                    node_name: 'Sequence',
                    child_node: []
                }
            ],
            defaultProps: { label: 'node_name', children: 'child_node' },
            toolbars: {
                bold: true, // 粗体
                italic: true, // 斜体
                header: true, // 标题
                underline: true, // 下划线
                mark: true, // 标记
                superscript: true, // 上角标
                quote: true, // 引用
                ol: true, // 有序列表
                table: true,
                ishljs: true,
                code: true, // code
                subfield: true, // 是否需要分栏
                fullscreen: true, // 全屏编辑
                undo: true, // 上一步
                trash: true // 清空
            },
            loading: false,
            upImgIp: this.Ip + '/UploadImage',
            dialogTableVisible: false,
            index: 0,
            img_num: 0,
            show_num: 100,
            imgSrc: '',
            fileList: [],
            subData: {
                sec_id: 0,
                sec_type: 'SEQUENCE',
                commit_user: window.sessionStorage.getItem('Uall'),
                section_list: [
                    // {
                    //     sec_id: 0,
                    //     sec_title: '',
                    //     content: [],
                    //     explain: '',
                    //     complement: '',
                    //     micro_ver: 0,
                    //     Resource: [
                    //         {
                    //             sec_id: 0,
                    //             number: 'uc1',
                    //             explain: 'explain',
                    //             func_id: '',
                    //             micro_ver: 0
                    //         }
                    //     ],
                    //     Activity: []
                    // }
                ]
            },
            index: 0,
            activityIndex: 0,
            usecaseId: 21005,
            resourceArr: [],
            timer: null,
            standardOptions: [
                {
                    value: '不低于',
                    label: '不低于'
                },
                {
                    value: '不高于',
                    label: '不高于'
                }
            ],
            CPU_unit: [
                {
                    value: 'MIPS',
                    label: 'MIPS'
                }
            ],
            memory_unit: [
                {
                    value: 'KB',
                    label: 'KB'
                },
                {
                    value: 'MB',
                    label: 'MB'
                },
                {
                    value: 'GB',
                    label: 'GB'
                },
                {
                    value: 'TB',
                    label: 'TB'
                }
            ],
            isEmptyArr: false,
            title: '',
            docType: 'BASIC',
            title: ''
        }
    },
    created() {
        this.usecaseId = this.$route.params.usecaseId
        this.title = this.$route.params.title
        this.subData.sec_id = this.$route.params.usecaseId
        this.getResourceArr()
    },
    mounted() {
        this.getSequence()
        // window.addEventListener('scroll', this.scrollHandler, true)
    },
    destoryed() {
        // window.removeEventListener('scroll', this.scrollHandler)
    },
    watch: {},
    methods: {
        check_data_diff(val) {
            let check_data = val
            if (check_data.length === 0) {
                return true
            } else {
                for (let item of val) {
                    for (let i = 0; i < item.Resource.length; i++) {
                        if (item.Resource[i].type == 'checkbox') {
                            if (
                                (item.Resource[i].unit !== null &&
                                    item.Resource[i].unit !== '' &&
                                    (item.Resource[i].operator !== null && item.Resource[i].operator !== '') &&
                                    item.Resource[i].value !== null) ||
                                ((item.Resource[i].unit === null || item.Resource[i].unit === '') &&
                                    (item.Resource[i].operator === null || item.Resource[i].operator === '') &&
                                    item.Resource[i].value === null)
                            ) {
                                if (typeof item.Resource[i].value === 'string') {
                                    if (item.Resource[i].value === '0') {
                                        item.Resource[i].value = 0
                                    } else if (item.Resource[i].value === '') {
                                        item.Resource[i].value = null
                                    }
                                }
                            } else {
                                this.$message({
                                    showClose: true,
                                    message: 'Sequence' + (i + 1) + '中的Resource填写不完整',
                                    type: 'error',
                                    duration: 0
                                })
                                return false
                            }
                        }
                    }
                }
                return true
            }
        },
        uploadActivitySuccess(response, file, fileList) {
            if (response.result == 'OK') {
                this.$message({
                    type: 'success',
                    message: '上传成功!'
                })
                this.subData.section_list[this.index].Activity[this.activityIndex].content.push({
                    name: 'img',
                    url: response.content
                })
            } else {
                this.$alert('图片未上传成功，请重新上传', '提示')
            }
        },
        getActivityIndex(index, activityIndex) {
            
            this.index = index
            this.activityIndex = activityIndex
                   
        },
        addActivity(index) {
            
            const tempActivityObj = {
                sec_id: 0,
                sec_title: '',
                content: [],
                explain: '',
                complement: '',
                micro_ver: 0
            }
            this.subData.section_list[index].Activity.push(tempActivityObj)
                
        },
        handleContent() {
            if (this.subData.section_list.length == 0) {
                this.isEmptyArr = true
            } else {
                this.isEmptyArr = false
            }
        },
        checkout(obj) {
            this.timer = setInterval(() => {
                if (obj.value === '') {
                    obj.value = null
                }
                if (obj.value) {
                    if (obj.value.length >= 10) {
                        obj.value = obj.value.slice(0, 9)
                    }
                    var reg = /[^0-9]/g
                    obj.value = Number(obj.value.toString().replace(reg, ''))
                }
            }, 100)
        },
        clearInterval() {
            clearInterval(this.timer)
        },
        getSequence() {
            this.$axios
                .get(this.Ip + '/DsUcSub/' + this.usecaseId + '/SEQUENCE')
                .then(res => {
                    if (res.data.result == 'NG') {
                        // do nothing
                        // this.$message({
                        //     showClose: true,
                        //     message: '',
                        //     type: 'error',
                        //     duration: 0
                        // })
                    } else {
                        console.log(res.data.content, 'res.data.content')
                        const tempSequenceArr = res.data.content.section_list
                        for (let i = 0; i < tempSequenceArr.length; i++) {
                            tempSequenceArr[i].content = JSON.parse(tempSequenceArr[i].content)
                            tempSequenceArr[i].Activity = tempSequenceArr[i].Activity.map(item => {
                                item.content = JSON.parse(item.content)
                                return item
                            })
                        }
                        this.subData.section_list = tempSequenceArr
                        this.subData.sec_id = res.data.content.usecase_id
                        this.treeArr[0].child_node = tempSequenceArr.map((item, index) => {
                            return {
                                node_name: 'Sequence' + (index + 1)
                            }   
                        })
                    }

                    this.handleContent()
                    this.$nextTick(() => {
                        let len = document.getElementsByClassName('auto-textarea-input').length
                        if (len > 0) {
                            document.getElementsByClassName('auto-textarea-input')[len - 1].blur() // 获取textarea 不一定是auto-textarea-input
                            $('.content-box').scrollTop(0)
                        }
                    })
                })
                .catch(() => {
                    this.$message({
                        showClose: true,
                        message: '服务异常',
                        type: 'error',
                        duration: 0
                    })
                })
        },
        getResourceArr() {
            this.$axios
                .get(this.Ip + '/Resource')
                .then(res => {
                    if (res.data.result == 'OK') {
                        for (let ii_data of res.data.content) {
                            this.resourceArr.push({
                                resource_id: ii_data.resource_id,
                                rsc_name: ii_data.rsc_name,
                                val: ''
                            })
                        }
                    }
                })
                .catch(() => {
                    this.$message({
                        showClose: true,
                        message: '服务异常',
                        type: 'error',
                        duration: 0
                    })
                })
        },
        cancel() {
            this.$router.push({ path: '/tagl/File_design/Preview_seq/' + this.usecaseId })
        },
        confirm() {
            const data = this.subData
            if (!this.check_data_diff(data.section_list)) {
                return
            }
                this.$axios
                    .post(this.Ip + '/DsUcSub', data)
                    .then(res => {
                        if (res.data.result == 'OK') {
                            // 成功，跳转页面
                            this.$message({
                                showClose: true,
                                message: '添加成功',
                                type: 'success'
                            })
                            this.$router.push({ path: '/tagl/File_design/Preview_seq/' + this.usecaseId })
                        } else {
                            // 异常报错
                            this.$message({
                                showClose: true,
                                message: res.data.error,
                                type: 'error',
                                duration: 0
                            })
                        }
                    })
                    .catch(err => {
                        this.$message({
                            showClose: true,
                            message: '服务异常',
                            type: 'error',
                            duration: 0
                        })
                    })
                
        },
        addSequence() {
            const data = {
                sec_id: 0,
                sec_title: '',
                content: [],
                explain: '',
                complement: '',
                micro_ver: 0,
                Resource: [],
                Activity: []
            }
            for (let i_resource of this.resourceArr) {
                data.Resource.push({
                    resource_id: i_resource.resource_id,
                    rsc_name: i_resource.rsc_name,
                    val: '',
                    unit: null,
                    value: null,
                    operator: null
                })
            }
            const child_node_data = {
                node_name: 'Sequence' + (this.treeArr[0].child_node.length + 1)
            }
            this.treeArr[0].child_node.push(child_node_data)
            this.subData.section_list.push(data)
            this.handleContent()
            this.$nextTick(() => {
                let len = this.treeArr[0].child_node.length
                document.getElementsByClassName('auto-textarea-input')[len - 1].blur() // 获取textarea 不一定是auto-textarea-input
                $('.first-title').css({ color: '#606266' })
                $('.second-title').css({ color: '#606266' })
                $('.tree-li')
                    .eq(0)
                    .find('.second-title')
                    .eq(len - 1)
                    .css({ color: '#42b983' })
                let sTop = $('.Asa-box')
                    .eq(0)
                    .find('.msg-box')
                    .eq(len - 1)[0].offsetTop
                $('.content-box').animate({ scrollTop: sTop }, 500, function() {})
            })
        },
        delUsecase(index) {
            
            this.treeArr[0].child_node.splice(index, 1)
            this.subData.section_list.splice(index, 1)
            this.treeArr[0].child_node = this.treeArr[0].child_node.map((item, index_child) => {
                item.node_name = 'Sequence' + (index_child + 1)
                return item
            })
            this.handleContent()
                  
            
        },
        delActivity(index, activityIndex) {
            
            this.subData.section_list[index].Activity.splice(activityIndex, 1)
                    
        },
        deleteImg(img_list, img_index) {
            this.$confirm(this.globalData.hint.delete, '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(() => {
                img_list.splice(img_index, 1)
            })
        },
        deleteActivityImg(img_list, img_index) {
            
            this.$confirm(this.globalData.hint.delete, '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(() => {
                img_list.splice(img_index, 1)
            })
                        
        },
        showImgDialog(data) {
            this.$axios.get(this.Ip + '/ImageSize/' + data).then(res => {
                if (res.data.result == 'OK') {
                    this.dialogTableVisible = true
                    this.imgSrc = data
                    this.img_num = 0
                    this.show_num = 100
                    let img_width = res.data.content.long
                    $('.dialogimg').width(img_width)
                }
            })
        },
        handlePreview(file) {
            this.dialogTableVisible = true
            this.imgSrc = file.url
        },
        uploadSuccessHandler(response, file, fileList) {
            if (response.result == 'OK') {
                this.$message({
                    type: 'success',
                    message: '上传成功!'
                })
                this.subData.section_list[this.index].content.push({
                    name: 'img',
                    url: response.content
                })
            } else {
                this.$alert('图片未上传成功，请重新上传', '提示')
            }
        },
        get_index(index) {
            this.index = index
        },
        realFunc() {
            // const scrollTop = $('.content-box').scrollTop()
            // const nav_height = 60
            // let len = this.treeArr[0].child_node.length
            // console.log('1111111111111111')
            // console.log($('.msg-box').eq(0).offset().top - 60, '66666666')
            // return
            // if ($('.msg-box').eq(0).offset().top - 60 > scrollTop) {
            //     $('.first-title').css({ color: '#606266' })
            //     $('.second-title').css({ color: '#606266' })
            //     $('.first-title')
            //         .eq(0)
            //         .css({ color: '#42b983' })
            //     return
            // }
            // console.log('222222222222222')
            // for(let i = 0;i < len; i++) {
            //     let distanceOfTop = $('.msg-box').eq(i).offset().top - 60
            //     if(distanceOfTop > 0 && i != 0) {
            //         $('.first-title').css({ color: '#606266' })
            //         $('.second-title').css({ color: '#606266' })
            //         $('.second-title')
            //             .eq(i - 1)
            //             .css({ color: '#42b983' })
            //         console.log(i, '4444444444444444444')
            //         return
            //     }
            // }
            // console.log('3333333333333')
            // $('.first-title').css({ color: '#606266' })
            // $('.second-title').css({ color: '#606266' })
            // $('.second-title')
            //     .eq(len -1)
            //     .css({ color: '#42b983' })
        },
        scrollHandler() {
            // let timeout;
            // let func = this.realFunc()
            // return function() {
            //     clearTimeout(timeout);
            //     // 指定 xx ms 后触发真正想进行的操作 handler
            //     timeout = setTimeout(func, 500);
            // }
        },
        firstScrollTop(index) {
            $('.first-title').css({ color: '#606266' })
            $('.second-title').css({ color: '#606266' })
            $('.first-title')
                .eq(index)
                .css({ color: '#42b983' })
            let sTop = document.getElementsByClassName('Asa-box')[index].offsetTop
            $('.content-box').animate({ scrollTop: sTop }, 500, function() {})
        },
        secondScrillTop(index, second) {
            $('.first-title').css({ color: '#606266' })
            $('.second-title').css({ color: '#606266' })
            $('.tree-li')
                .eq(index)
                .find('.second-title')
                .eq(second)
                .css({ color: '#42b983' })
            let sTop = $('.Asa-box')
                .eq(index)
                .find('.msg-box')
                .eq(second)[0].offsetTop
            $('.content-box').animate({ scrollTop: sTop }, 500, function() {})
        },
        upSuccess(response, file, fileList) {
            if (response.result == 'OK') {
                this.$message({
                    type: 'success',
                    message: '上传成功!'
                })
                this.img_flag = false
                this.file_form.content = ''
                this.file_form.content = this.Ip + '/DownFile/' + response.content
            } else {
                this.$alert('图片未上传成功，请重新上传', '提示')
            }
        },
        enlargeImg() {
            let width_first_img = $('.dialog-img').width() * 0.1
            let mum = this.img_num + 1
            this.show_num = this.show_num + mum * 10
            let img_width = $('.dialog-img').width() + mum * width_first_img
            $('.dialog-img').width(img_width)
        },
        shrinkImg() {
            let mum = this.img_num - 1

            if (this.show_num > 10) {
                let width_first_img = $('.dialog-img').width() * 0.1
                if (mum <= 0) {
                    mum = 1
                    let img_width = $('.dialog-img').width() - mum * width_first_img
                    $('.dialog-img').width(img_width)
                    this.show_num = this.show_num - mum * 10
                } else {
                    let img_width = $('.dialog-img').width() - mum * width_first_img
                    $('.dialog-img').width(img_width)
                    this.show_num = this.show_num + mum * 10
                }
            } else {
                this.$message({
                    message: '图片已缩至最小'
                })
            }
        }
    }
}
</script>

<style scoped>
html,
body {
    font-family: '微软雅黑';
}
.message {
    margin-right: 50px;
    text-align: center;
    padding: 20px;
    font-size: 14px;
    color: #5e6d82;
    border: 1px solid #ebeef5;
    margin-top: 10px;
}
.wrapper {
    width: 100%;
    height: 100%;
    min-width: 1024px;
    color: #606266;
    overflow: hidden;
}
.tree-box {
    position: relative;
    top: 1px;
    left: 0;
    z-index: 999;
    margin: 0;
    padding: 0;
    width: 15%;
    height: 98%;
    background-color: white;
    border-right: 2px solid rgba(216, 231, 223, 0.5);
    overflow-y: auto;
    padding-left: 20px;
}
.content-box {
    position: absolute;
    top: 0;
    right: 0;
    left: 15%;
    bottom: 80px;
    width: 85%;
    overflow-y: auto;
    padding-left: 20px;
    padding-bottom: 20px;
}
.title_h1 {
    font-weight: bold;
    font-size: 24px;
    margin-top: 10px;
}
.title-detail {
    font-size: 12px;
    color: #5e6d82;
    text-align: left;
    height: 20px;
    line-height: 20px;
    margin-top: 10px;
}
.block-box,
.Class-box,
.Usecase-table,
.Usecase-box,
.Std-box,
.IF-box {
    margin-top: 10px;
}
.IF-box {
    margin-bottom: 40px;
}
.title-h3 {
    font-size: 22px;
    font-weight: 500;
    height: 25px;
    line-height: 25px;
    font-weight: bold;
}
.title-h4 {
    font-size: 18px;
    padding-top: 10px;
    /*font-weight: 500*/
}
.append-span {
    height: 25px;
    line-height: 25px;
    font-size: 14px;
    cursor: pointer;
    font-weight: 500;
}

.content-size {
    margin-top: 10px;
}

.editor {
    width: 95%;
    margin-top: 10px;
}
.v-note-wrapper {
    min-height: 100px;
}
.msg-box,
.img-box {
    margin-top: 10px;
}
.img-box {
    overflow: auto;
}
.bottom-box {
    position: absolute;
    left: 0;
    height: 50px;
    width: 100%;
    bottom: 0;
    background-color: rgb(237, 249, 245);
}
.right-btn {
    width: 50px;
    height: 50px;
    float: right;
    background-color: rgb(225, 237, 233);
    cursor: pointer;
}
/*树*/
ul,
li {
    list-style: none;
}
.tree-ul {
    overflow: hidden;
    width: 100%;
    padding-left: 20px;
}
.child_ul {
    overflow: hidden;
    padding-left: 10px;
}
.tree-li {
    margin-top: 10px;
    font-weight: bold;
    cursor: pointer;
}
.tree-li p {
    height: 24px;
    line-height: 24px;
}
.child-tree-li {
    margin-top: 5px;
    margin-left: 20px;
    font-weight: 500;
    font-size: 14px;
}
.img-box-ex {
    width: 330px;
    height: 330px;
    margin-right: 20px;
    /* padding-left: 20px; */
    position: relative;
    display: inline-block;
    box-sizing: border-box;
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
.dialog-img {
    display: block;
    margin: 0 auto;
}
.upload-demo-box {
    width: 330px;
    height: 330px;
    vertical-align: top;
    display: inline-block;
}
.upload-demo {
    /* margin-top: 20px; */
}
.up-data-btn {
    width: 330px;
    height: 330px;
    /* margin-left: 20px; */
    display: block;
    background: #fff;
    outline: none;
    border: 1px dashed #ccc;
    color: #ccc;
    font-size: 15px;
    /*display: inline-block;*/
}
.Sequence-img {
    width: 100%;
    height: 100%;
}
.img_icon {
    position: absolute;
    right: 0px;
    top: 0;
    font-size: 24px;
    cursor: pointer;
    /*font-weight: bold;*/
}
.img-box-ex:hover {
    cursor: pointer;
    border: 1px solid transparent;
}
.append-span {
    height: 25px;
    line-height: 25px;
    font-size: 14px;
    cursor: pointer;
    font-weight: 500;
}
.append-span:hover {
    color: #42b983;
}
.footer {
    position: absolute;
    bottom: 20px;
    right: 29px;
}
@media screen and (max-width: 1024px) {
    .wrapper {
        width: 1024px;
    }
    .tree-box {
        width: 20%;
    }
    .content-box {
        left: 20%;
    }
    .up-data-btn {
        width: 160px;
        height: 170px;
    }
    .upload-demo-box {
        width: 180px;
        height: 180px;
        vertical-align: top;
        display: inline-block;
    }
    .img-box-ex {
        width: 180px;
        height: 170px;
        margin-right: 10px;
        position: relative;
        display: inline-block;
    }
}
@media screen and (max-width: 1366px) {
    .up-data-btn {
        width: 230px;
        height: 230px;
        /* margin-left: 20px; */
        display: block;
        background: #fff;
        outline: none;
        border: 1px dashed #ccc;
        color: #ccc;
        font-size: 15px;
    }
    .upload-demo-box {
        width: 230px;
        height: 230px;
        vertical-align: top;
        display: inline-block;
    }
    .upload-demo {
        margin-top: 0;
    }
    .img-box-ex {
        width: 230px;
        height: 230px;
        margin-right: 20px;
        position: relative;
        display: inline-block;
    }
}
</style>