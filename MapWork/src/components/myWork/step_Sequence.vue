<template>
    <div class='Append-basic-temlate'>
        <div class="Append-basic-temlate-countent">
            <div class="header-top">
            </div>
            <div class="header">
            </div>
        </div>

        <div class="content-box">
            <div class="middle">
                <div class="middle-top">
                    <div class="sequence-title">
                        <h2 style="fontSize: 22px;fontWeight:bolder;backgroundColor:#6bcca0; color: white;lineHeight: 25px;height:25px">
                            <span style="lineHeight:25px;float:left;paddingLeft: 10px;">Sequence</span>
                            <i class="el-icon-question" style="fontSize:15px; lineHeight:25px;float:left;marginLeft:5px" title="请提供Sequence信息（描述Sequence图的文字说明、Sequence图、以及Sequence使用的资源）"></i>
                            <el-button size="mini" type="text" @click='append_content(index=1)' style='color:#ffffff;marginLeft:5px' v-show="true"> [ 添加 ]</el-button>
                        </h2>
                    </div>
                    <div class="lable-box">
                        <div class="lable-box-content" v-for='(item,index) in SEQUENCE.content' v-show="show_content_flag">
                            <div class="NB" style="margin:10px auto;font-size: 18px;">
                                Sequence{{index+1}}
                                <el-button size="mini" type="text" @click='append_content(index)' style='color:#000'> [ 添加 ]</el-button>
                                <el-button size="mini" type="text" @click='delete_content(index)' style='marginLeft:5px;color:#000'> [ 删除 ]</el-button>
                            </div>
                            <div style="margin:10px 20px;font-size: 16px;">
                                Sequence{{index+1}}名称
                            </div>
                            <el-input class='textarea-name' placeholder="请输入Sequence的描述名称" v-model="item.content[0].title">
                            </el-input>

                            <div style="margin:0px 20px;font-size: 16px;">
                                Sequence{{index+1}}说明
                            </div>
                            <el-input class='textarea-name' type="textarea" :autosize="{ minRows:2, maxRows:10}" placeholder="请输入Sequence的描述说明" v-model="item.content[0].val">
                            </el-input>

                            <div style="margin:10px 20px;font-size: 16px;">
                                关联UseCase
                            </div>

                            <div class="squence-usecase">
                                <!-- 必须勾选，不勾选报错 -->
                                <el-checkbox-group v-model="item.rel_id_list">
                                    <span v-for='(item_usecase, index) in doc_usecase_list' class="check-span" :key="index">
                                        <el-checkbox :label="item_usecase.sec_id">
                                            {{item_usecase.number}}
                                        </el-checkbox>
                                    </span>
                                </el-checkbox-group>
                            </div>

                            <p class="sequence-number">Sequence{{index+1}}图片</p>

                            <div class="img-box" v-for='(src,index_img) in item.content[0].fileList'>
                                <img :src="src.url" alt="" @click="show_to_pic(src.url)" class="Sequence-img">
                                <i class="el-icon-close img_icon" style="float:right" @click='delete_img(index,index_img)'></i>
                            </div>
                            <div class="upload-demo-box">
                                <el-upload class="upload-demo" :action='Up_Img_Ip' :on-preview="handlePreview" :before-upload="beforeUpload" :on-success='up_success' :show-file-list='false'>
                                    <button @click='get_index(index)' class="up-data-btn">
                                        <i class="el-icon-picture"></i>点击上传</button>
                                </el-upload>
                            </div>

                            <!-- Activity图/Flow図 -->
                            <div class="Activity" v-if='type_flag'>
                                <p style="margin:20px 20px;fontSize:18px;">
                                    Activity
                                    <el-button size="mini" type="text" style='color:#000' @click='append_activity(index)'> [ 添加 ]</el-button>
                                    <!-- <el-button size="mini"  type="text" style='marginLeft:5px;color:#000' @click='delete_activity(index,activity_index)'> [ 删除 ]</el-button> -->
                                </p>

                                <div class="Activity_box" v-for='(activity_item,activity_index) in item.activity_list'>
                                    <div style="margin:10px 20px;font-size: 16px;">
                                        Activity{{activity_index+1}}
                                        <el-button size="mini" type="text" style='color:#000' @click='append_activity(index)'> [ 添加 ]</el-button>
                                        <el-button size="mini" type="text" style='marginLeft:5px;color:#000' @click='delete_activity(index,activity_index)'> [ 删除 ]</el-button>
                                    </div>
                                    <div style="margin:10px 20px;font-size: 16px;">
                                        Activity{{activity_index+1}}说明
                                    </div>
                                    <el-input class='textarea-name' type="textarea" :autosize="{ minRows:2, maxRows:10}" placeholder="请输入Activity图/Flow図的描述说明" v-model="activity_item.content[0].val">
                                    </el-input>

                                    <p class="sequence-number">Activity{{activity_index+1}}图片</p>

                                    <div class="img-box" v-for='(src,index_img) in activity_item.content[0].fileList'>
                                        <img :src="src.url" alt="" @click="show_to_pic(src.url)" class="Sequence-img">
                                        <i class="el-icon-close img_icon" style="float:right" @click='delete_img_activity(index,activity_index,index_img)'></i>
                                    </div>
                                    <div class="upload-demo-box">
                                        <el-upload class="upload-demo" :action='Up_Img_Ip' :on-preview="handlePreview" :before-upload="beforeUpload" :on-success='up_success_activity' :show-file-list='false'>
                                            <button @click='get_index(index,activity_index)' class="up-data-btn">
                                                <i class="el-icon-picture"></i>点击上传</button>
                                        </el-upload>
                                    </div>
                                </div>
                            </div>
                            <p style="margin:20px 20px;fontSize:18px;">Resource</p>
                            <el-table :data="item.resource_list" border style="marginTop:30px;margin-left: 20px;margin-right:20px;width: 87%">
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
                            <div class="btn-box">
                            </div>
                        </div>
                        <p class="message" v-show="show_content_flag_null">暂无数据</p>
                    </div>
                </div>
                <div style="clear: both;"></div>
                <div class="footer">
                    <el-button size="mini" type="primary" @click="save()">&nbsp;&nbsp;保&nbsp;&nbsp;&nbsp;存&nbsp;&nbsp;</el-button>
                    <el-button size="mini" type="primary" @click="cancel()">&nbsp;&nbsp;退&nbsp;&nbsp;&nbsp;出&nbsp;&nbsp;</el-button>
                    <el-button size="mini" type="primary" @click="finish()">&nbsp;&nbsp;确&nbsp;&nbsp;&nbsp;定&nbsp;&nbsp;</el-button>
                </div>
            </div>
            <div class="right">
                <div class="leftCheck">

                </div>
            </div>

            <div id="img-dialog-box">
                <el-dialog :visible.sync="dialogTableVisible">
                    <p class="dialog-title">
                        <span>
                            <i class="el-icon-circle-plus" @click='big_img()'></i>
                        </span>
                        <span>{{show_num}}%</span>
                        <span>
                            <i class="el-icon-remove" @click='s_img()'></i>
                        </span>
                    </p>
                    <img :src="img_src" alt="" class='dialog-img'>
                </el-dialog>
            </div>
            <!-- new ADDshow -->

        </div>
    </div>
</template>

<script>
import showLeftCheck from './step_showLeftCheck'
require('../../assets/js/jquery-1.8.3.min.js')
export default {
    components: {
        showLeftCheck: showLeftCheck
    },
    data() {
        return {
            img_num: 0,
            show_num: 100,
            fileList2: [],
            append_to_body: true,
            dialogTableVisible: true,
            img_src: '',
            textarea_val: '',
            active: Number(window.sessionStorage.getItem('Step')),
            index: 0,
            showTreeData: {
                one: [],
                scene: []
            },
            show_flag: false,
            show_content_flag: false,
            show_content_flag_null: false,
            SEQUENCE: {
                doc_id: 0,
                // micro_ver: Number(window.sessionStorage.getItem('ver')),
                commit_user: window.sessionStorage.getItem('Uall'),
                sec_type: 'SEQUENCE',
                content: [],
                considers: [],
                rel_id_list: []
            },
            resource_list: [],
            Up_Img_Ip: this.Ip + '/UploadImage',
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
            timer: null,
            get_data: '',
            save_data: '',
            type_flag: false,
            activity_index: '',
            dbrfmFlag: false,
            docListData: [],
            bugListData: [],
            active_index: null,
            doc_usecase_list: [],
            rel_id_list: [],
            sec_id_list: []
        }
    },
    created() {
        this.get_doc_all_usecase()
    },
    mounted() {
        this.SEQUENCE.doc_id = window.sessionStorage.getItem('DocId')
        // this.get_consider()
        this.load_up()
        this.get_msg()
        var self = this
        setTimeout(() => {
            $('.jump').on('click', function(e) {
                self.jump_to($(this).text())
            })
        }, 10)
        // this.showTree()
        if (window.sessionStorage.getItem('DocType') != 'BASIC') {
            this.type_flag = true
        }
        if (this.$route.query.params) {
            this.dbrfmFlag = this.$route.query.params
        }
    },
    methods: {
        get_doc_all_usecase() {
            this.$axios
                .get(this.Ip + '/AllUsecase/' + window.sessionStorage.getItem('DocId'))
                .then(res => {
                    this.doc_usecase_list = res.data.content
                    this.sec_id_list = res.data.content.map(item => item.sec_id)
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
        // 获取考虑点数据
        // get_consider() {
        //     let sec_id = window.sessionStorage.getItem('stepTwoSecId')
        //     this.$axios.get(this.Ip + '/DSConsider/' + sec_id).then(res => {
        //         // console.log(res,"考虑点获取")
        //         if (res.data.result == 'OK') {
        //             for (let item of res.data.content) {
        //                 item.show_flag = false
        //             }
        //             this.SEQUENCE.considers = res.data.content
        //         }
        //     })
        // },
        // Resource
        get_msg() {
            this.$axios.get(this.Ip + '/Resource').then(res => {
                if (res.data.result == 'OK') {
                    for (let ii_data of res.data.content) {
                        this.resource_list.push({
                            resource_id: ii_data.resource_id,
                            rsc_name: ii_data.rsc_name,
                            val: ' '
                        })
                    }
                }
            })
        },

        handlePreview(file) {
            this.dialogTableVisible = true
            this.img_src = file.url
        },
        cancel() {
            let SEQUENCE_data = JSON.parse(JSON.stringify(this.SEQUENCE))
            for (let item of this.SEQUENCE.considers) {
                delete item.show_flag
            }
            this.save_data = JSON.stringify(this.SEQUENCE)
            if (this.save_data == this.get_data) {
                window.sessionStorage.removeItem('Step')
                this.$router.push('/tagl/File_design/Preview/' + window.sessionStorage.getItem('DocId'))
            } else {
                this.$confirm(this.globalData.hint.quit, '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                })
                    .then(() => {
                        window.sessionStorage.removeItem('Step')
                        this.$router.push('/tagl/File_design/Preview/' + window.sessionStorage.getItem('DocId'))
                    })
                    .catch(() => {
                        this.SEQUENCE = SEQUENCE_data
                    })
            }
        },
        LinkURL(data) {
            window.open(data.url)
        },
        hidden_and_show(index) {
            switch (index) {
                case 1:
                    if (
                        $('.leftCheck-content')
                            .eq(0)
                            .css('display') == 'none'
                    ) {
                        $('.leftCheck-content')
                            .eq(0)
                            .css({ display: 'block' })
                    } else {
                        $('.leftCheck-content')
                            .eq(0)
                            .css({ display: 'none' })
                    }
                    break
                case 2:
                    if (
                        $('.leftCheck-content')
                            .eq(1)
                            .css('display') == 'none'
                    ) {
                        $('.leftCheck-content')
                            .eq(1)
                            .css({ display: 'block' })
                    } else {
                        $('.leftCheck-content')
                            .eq(1)
                            .css({ display: 'none' })
                    }
                    break
                case 3:
                    if (
                        $('.leftCheck-content')
                            .eq(2)
                            .css('display') == 'none'
                    ) {
                        $('.leftCheck-content')
                            .eq(2)
                            .css({ display: 'block' })
                    } else {
                        $('.leftCheck-content')
                            .eq(2)
                            .css({ display: 'none' })
                    }
                    break
                case 4:
                    if (
                        $('.leftCheck-content')
                            .eq(3)
                            .css('display') == 'none'
                    ) {
                        $('.leftCheck-content')
                            .eq(3)
                            .css({ display: 'block' })
                    } else {
                        $('.leftCheck-content')
                            .eq(3)
                            .css({ display: 'none' })
                    }
                    break
                case 5:
                    if (
                        $('.leftCheck-content')
                            .eq(4)
                            .css('display') == 'none'
                    ) {
                        $('.leftCheck-content')
                            .eq(4)
                            .css({ display: 'block' })
                    } else {
                        $('.leftCheck-content')
                            .eq(4)
                            .css({ display: 'none' })
                    }
                    break
            }
        },
        jump_to(index) {
            if (!this.check_data_diff(this.SEQUENCE.content)) {
                return
            }
            switch (index) {
                case 'Usecase(必填)':
                    this.JumpAndSave()
                    this.$router.push({ path: '/tagl/step1', query: { params: this.dbrfmFlag } })
                    break
                case '式样书(必填)':
                    this.JumpAndSave()
                    this.$router.push({ path: '/tagl/step2', query: { params: this.dbrfmFlag } })
                    break
                case '场景(必填)':
                    // console.log(222)
                    this.JumpAndSave()
                    this.$router.push({ path: '/tagl/step3', query: { params: this.dbrfmFlag } })
                    break
                case '变更变化点(必填)':
                    this.JumpAndSave()
                    this.$router.push({ path: '/tagl/step4', query: { params: this.dbrfmFlag } })
                    break
                // case 'Sequence(必填)':
                //     if (this.check_data_diff(this.SEQUENCE.content)) {
                //         this.JumpAndSave()
                //         this.$router.push({ path: '/tagl/step5', query: { params: this.dbrfmFlag } })
                //     }
                //     break
                case 'Statemachine(选填)':
                    this.JumpAndSave()
                    this.$router.push({ path: '/tagl/step6', query: { params: this.dbrfmFlag } })
                    break
                case 'DRBFM(必填)':
                    this.JumpAndSave()
                    this.$router.push({ path: '/tagl/step7', query: { params: this.dbrfmFlag } })
                    break
                case '1Usecase(必填)':
                    if (this.active == 0) {
                        this.$router.push('/tagl/step1')
                    }
                    break
                case '2式样书(必填)':
                    if (this.active == 1) {
                        this.$router.push('/tagl/step2')
                    }
                    break
                case '3场景(必填)':
                    if (this.active == 2) {
                        this.$router.push('/tagl/step3')
                    }
                    break
                case '4Sequence(必填)':
                    if (this.active == 3) {
                        this.$router.push('/tagl/step4')
                    }
                    break
                case '5Statemachine(选填)':
                    if (this.active < 5) {
                        this.next_step()
                        // this.$router.push('/tagl/step5')
                    }
                    break
                case '6DRBFM(必填)':
                    if (this.active == 5) {
                        this.$router.push('/tagl/step6')
                    }
                    break
            }
        },
        // getBuglist() {
        //     let sec_id = window.sessionStorage.getItem('stepTwoSecId')
        //     this.$axios.get(this.Ip + '/KnowledgeDoc/' + sec_id).then(res => {
        //         if (res.data.result == 'OK') {
        //             this.bugListData = res.data.content.bug_list
        //             this.docListData = res.data.content.knowledge_docs
        //         } else {
        //             this.bugListData = []
        //             this.docListData = []
        //         }
        //     })
        // },
        // showTree() {
        //     this.showTreeData.scene = []
        //     this.showTreeData.one = []
        //     this.show_flag = false
        //     this.$axios
        //         .get(this.Ip + '/Section/' + window.sessionStorage.getItem('stepTwoSecId') + '/SCENES')
        //         .then(res => {
        //             if (res.data.result == 'OK') {
        //                 for (let i_data of res.data.content) {
        //                     this.showTreeData.scene.push(i_data.scene)
        //                     this.show_flag = true
        //                     // this.getBuglist()
        //                 }
        //             }
        //         })
        //     this.$axios
        //         .get(this.Ip + '/Section/' + window.sessionStorage.getItem('stepTwoSecId') + '/SPEC')
        //         .then(res => {
        //             if (res.data.result == 'OK') {
        //                 for (let i_data of res.data.content) {
        //                     this.showTreeData.one.push(i_data)
        //                 }
        //             }
        //         })
        //     // if (window.sessionStorage.getItem('showTreeData') != null) {
        //     //     let stepTwoData = JSON.parse(window.sessionStorage.getItem('showTreeData'))
        //     //     this.showTreeData.one = stepTwoData.one
        //     // }
        // },
        go_doc_text(val) {
            var datas = {}
            datas.doc_id = val
            let data = {
                'data':datas,
                'server_ip':this.Ip
            }
            window.sessionStorage.setItem('listDocID', JSON.stringify(data))
            window.open('../../../static/DocList-item.html')
        },
        link_to_sequence(index) {
            let jump = document.querySelectorAll('.NB')
            // 获取需要滚动的距离
            let total = jump[index].offsetTop
            let distance = $('.middle-top').scrollTop()
            let step = total / 50
            if (total > distance) {
                smoothDown()
            } else {
                let newTotal = distance - total
                step = newTotal / 50
                smoothUp()
            }
            function smoothDown() {
                if (distance < total) {
                    distance += step
                    $('.middle-top').scrollTop(distance)
                    setTimeout(smoothDown, 10)
                } else {
                    $('.middle-top').scrollTop(total)
                }
            }
            function smoothUp() {
                if (distance > total) {
                    distance -= step
                    $('.middle-top').scrollTop(distance)
                    setTimeout(smoothUp, 10)
                } else {
                    $('.middle-top').scrollTop(total)
                }
            }
        },
        link_to_sequence_append() {
            let jump = document.querySelectorAll('.NB')
            if (jump.length !== 0) {
                // 获取需要滚动的距离
                let total = jump[jump.length - 1].offsetTop + 813
                let distance = $('.middle-top').scrollTop()
                let step = total / 50
                if (total > distance) {
                    smoothDown()
                } else {
                    let newTotal = distance - total
                    step = newTotal / 50
                    smoothUp()
                }
                function smoothDown() {
                    if (distance < total) {
                        distance += step
                        $('.middle-top').scrollTop(distance)
                        setTimeout(smoothDown, 10)
                    } else {
                        $('.middle-top').scrollTop(total)
                    }
                }
                function smoothUp() {
                    if (distance > total) {
                        distance -= step
                        $('.middle-top').scrollTop(distance)
                        setTimeout(smoothUp, 10)
                    } else {
                        $('.middle-top').scrollTop(total)
                    }
                }
            }
        },
        get_index(index, activity_index) {
            this.index = index
            this.activity_index = activity_index
        },
        show_content() {
            this.show_content_flag = true
        },
        load_up() {
            this.$axios
                .get(this.Ip + '/Section/' + window.sessionStorage.getItem('DocId') + '/SEQUENCE')
                .then(res => {
                    if (res.data.result == 'OK') {
                        for (let i = 0; i < res.data.content.content.length; i++) {
                            for (let item of res.data.content.content) {
                                for (let subItem of item.resource_list) {
                                    if (subItem.type === 'checkbox') {
                                        if (subItem.value === 0) {
                                            subItem.value += ''
                                        }
                                    }
                                }
                            }
                            res.data.content.content[i].content = JSON.parse(res.data.content.content[i].content)
                        }
                        this.SEQUENCE.content = res.data.content.content
                        for (let i = 0; i < this.SEQUENCE.content.length; i++) {
                            for (let k = 0; k < this.SEQUENCE.content[i].activity_list.length; k++) {
                                let data = JSON.parse(this.SEQUENCE.content[i].activity_list[k].content)
                                this.SEQUENCE.content[i].activity_list[k].content = data
                            }
                        }
                        // this.SEQUENCE.micro_ver = res.data.micro_ver
                        this.show_content_flag = true
                    } else {
                        this.show_content_flag = true
                        this.show_content_flag_null = true
                    }
                    let sequence_copy = JSON.parse(JSON.stringify(this.SEQUENCE))
                    for (let item of sequence_copy.considers) {
                        delete item.show_flag
                    }
                    this.get_data = JSON.stringify(sequence_copy)
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
        // 上传图片
        up_success(response, file, fileList) {
            if (response.result == 'OK') {
                this.$message({
                    type: 'success',
                    message: '上传成功!'
                })
                this.SEQUENCE.content[this.index].content[0].fileList.push({
                    name: 'img',
                    url: response.content
                })
            } else {
                this.$alert('图片未上传成功，请重新上传', '提示')
            }
        },
        up_success_activity(response, file, fileList) {
            if (response.result == 'OK') {
                this.$message({
                    type: 'success',
                    message: '上传成功!'
                })
                this.SEQUENCE.content[this.index].activity_list[this.activity_index].content[0].fileList.push({
                    name: 'img',
                    url: response.content
                })
            } else {
                this.$alert('图片未上传成功，请重新上传', '提示')
            }
        },
        delete_img(index, index_img) {
            this.$confirm(this.globalData.hint.delete, '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(() => {
                this.SEQUENCE.content[index].content[0].fileList.splice(index_img, 1)
            })
        },
        delete_img_activity(index, activity_index, index_img) {
            this.$confirm(this.globalData.hint.delete, '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(() => {
                this.SEQUENCE.content[index].activity_list[activity_index].content[0].fileList.splice(index_img, 1)
            })
        },
        // 添加
        append_content(index) {
            this.show_content_flag_null = false
            if (this.show_content_flag == false) {
                this.show_content_flag = true
            } else {
                var new_content_obj = {
                    title: '',
                    sec_id: 0,
                    content: [{ fileList: [], val: '' }],
                    resource_list: [],
                    activity_list: [
                        // {
                        //     sec_id: 0,
                        //     sec_type:'Activity',
                        //     micro_ver: 0,
                        //     content:[{ fileList: [], val: ''}]
                        // }
                    ],
                    rel_id_list: JSON.parse(JSON.stringify(this.sec_id_list))
                }
                for (let i_resource of this.resource_list) {
                    new_content_obj.resource_list.push({
                        resource_id: i_resource.resource_id,
                        rsc_name: i_resource.rsc_name,
                        val: '',
                        unit: null,
                        value: null,
                        operator: null
                    })
                }
                this.SEQUENCE.content.push(new_content_obj)
                this.link_to_sequence_append()
            }
        },
        append_activity(index) {
            var new_content_obj = {
                sec_id: 0,
                sec_type: 'Activity',
                micro_ver: 0,
                content: [{ fileList: [], val: '' }]
            }
            this.SEQUENCE.content[index].activity_list.push(new_content_obj)
        },
        delete_activity(index, activity_index) {
            this.$confirm(this.globalData.hint.delete, '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(() => {
                this.SEQUENCE.content[index].activity_list.splice(activity_index, 1)
            })
            
        },
        delete_content(index) {
            this.$confirm(this.globalData.hint.delete, '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(() => {
                this.SEQUENCE.content.splice(index, 1)
                if (this.SEQUENCE.content.length == 0) {
                    this.show_content_flag_null = true
                }
            })
        },
        show_to_pic(data) {
            this.$axios.get(this.Ip + '/ImageSize/' + data).then(res => {
                if (res.data.result == 'OK') {
                    this.dialogTableVisible = true
                    this.img_src = data
                    this.img_num = 0
                    this.show_num = 100
                    let img_width = res.data.content.long
                    $('.dialogimg').width(img_width)
                }
            })
        },

        big_img() {
            let width_first_img = $('.dialog-img').width() * 0.1
            let mum = this.img_num + 1
            this.show_num = this.show_num + mum * 10
            let img_width = $('.dialog-img').width() + mum * width_first_img
            $('.dialog-img').width(img_width)
        },
        s_img() {
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
        },
        check_data_diff(val) {
            let check_data = val
            if (check_data.length === 0) {
                return true
            } else {
                for (let item of this.SEQUENCE.content) {
                    for (let subItem of item.resource_list) {
                        if (subItem.type == 'checkbox') {
                            if (
                                (subItem.unit !== null &&
                                    subItem.unit !== '' &&
                                    (subItem.operator !== null && subItem.operator !== '') &&
                                    subItem.value !== null) ||
                                ((subItem.unit === null || subItem.unit === '') &&
                                    (subItem.operator === null || subItem.operator === '') &&
                                    subItem.value === null)
                            ) {
                                if (typeof subItem.value === 'string') {
                                    if (subItem.value === '0') {
                                        subItem.value = 0
                                    } else if (subItem.value === '') {
                                        subItem.value = null
                                    }
                                }
                            } else {
                                this.$message({
                                    showClose: true,
                                    message: 'Resource填写不完整',
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
        JumpAndSave() {
            this.SEQUENCE.doc_id = window.sessionStorage.getItem('DocId')
            this.$axios
                .post(this.Ip + '/Section', this.SEQUENCE)
                .then(res => {
                    if (res.data.result == 'OK') {
                        // window.sessionStorage.setItem('ver', res.data.micro_ver)
                    }
                })
                .catch(err => {})
        },
        save() {
            if (this.check_data_diff(this.SEQUENCE.content)) {
                this.SEQUENCE.doc_id = window.sessionStorage.getItem('DocId')
                console.log(this.SEQUENCE, '保存数据')
                this.$axios
                    .post(this.Ip + '/Section', this.SEQUENCE)
                    .then(res => {
                        if (res.data.result == 'OK') {
                            this.load_up()
                            this.$message({
                                type: 'success',
                                message: '保存成功!'
                            })
                        } else {
                            this.$message({
                                showClose: true,
                                message: '保存失败:' + res.data.error,
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
            }
        },
        finish() {
            if (this.check_data_diff(this.SEQUENCE.content)) {
                this.SEQUENCE.doc_id = window.sessionStorage.getItem('DocId')
                this.$axios
                    .post(this.Ip + '/Section', this.SEQUENCE)
                    .then(res => {
                        if (res.data.result == 'OK') {
                            this.$router.push('/tagl/File_design/Preview/' + window.sessionStorage.getItem('DocId'))
                            this.$message({
                                type: 'success',
                                message: '保存成功!'
                            })
                        } else {
                            this.$message({
                                showClose: true,
                                message: '保存失败:' + res.data.error,
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
            }
        },
        toggle_class(item, index) {
            item.show_flag = !item.show_flag
            this.active_index = index

            this.$nextTick(() => {
                if (!item.show_flag) {
                    let text_height = $('.consider-msg-box')
                        .eq(index)
                        .find('.show-TBD-elli')
                        .height()
                    $('.consider-msg-box')
                        .eq(index)
                        .find('.el-textarea__inner')
                        .height(10)
                } else {
                    let text_height = $('.consider-msg-box')
                        .eq(index)
                        .find('.show-TBD-content')
                        .height()
                    if (text_height > 30) {
                        $('.consider-msg-box')
                            .eq(index)
                            .find('.el-textarea__inner')
                            .height(text_height)
                    }
                }
            })
        }
    }
}
</script>

<style scoped>
.Append-basic-temlate {
    margin: 0 auto;
    width: 100%;
    height: 100%;
}
.Append-basic-temlate-countent {
    max-width: 300px;
    width: 15%;
    height: 100%;
    padding: 20px;
    float: left;
}
.header-top {
    height: 100px;
}
.header {
    height: 400px;
    padding: 10%;
    clear: both;
}
.active {
    background: #fff;
}
.content-box {
    float: left;
    width: 84%;
    padding-left: 1%;
    border-left: 1px solid #c0c4cc;
    height: 100%;
    /*overflow-y: scroll;*/
}
.sequence-title {
    margin: 40px 0 0 0;
}

.upload-demo {
    margin-top: 20px;
}
.title,
.textarea-name {
    display: block;
    /*width: 60%;*/
    padding: 10px 20px;
    /*margin: 0 auto;*/
}

.title {
    width: 80%;
    font-size: 16px;
    /*margin: 0 auto;*/
}

.middle {
    position: relative;
    width: 80%;
    height: 100%;
    float: left;
    padding-right: 20px;
    border-right: 1px solid #ccc;
}
.middle-top {
    position: absolute;
    top: 0;
    bottom: 55px;
    width: 100%;
    padding-right: 20px;
    overflow-y: scroll;
}
.footer {
    position: absolute;
    bottom: 20px;
    right: 29px;
}
.right {
    width: 20%;
    height: 100%;
    float: left;
    overflow-y: scroll;
    overflow-x: hidden;
}
.lable-box {
    overflow: hidden;
}
.lable-box-content {
    width: 100%;
    margin: 20px 20px;
    padding-right: 20px;
    border-bottom: 1px solid #c0c4cc;
    padding-bottom: 20px;
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
    margin-left: 20px;
}
.add-box:hover {
    /*line-height: 100px;*/
    height: 100px;
    width: 100px;
    padding-top: 20px;
    text-align: center;
    border: 1px double #67c23a;
    color: #67c23a;
    cursor: pointer;
}

.dialog-img {
    display: block;
    margin: 0 auto;
}
.consider {
    width: 100%;
    margin: 20px 0;
    margin-top: 20px;
}
.consider-msg-box {
    /* height: 50px;
    line-height: 50px; */
    width: 100%;
    border: 1px solid #ebeef5;
    cursor: pointer;
    transition: all 0.3s linear;
    -moz-transition: all 0.3s linear; /* Firefox 4 */
    -webkit-transition: all 0.3s linear; /* Safari 和 Chrome */
    -o-transition: all 0.3s linear;
}
.consider-msg-box:hover {
    background: rgb(245, 247, 250);
}
.left-size,
.left-ipt {
    display: inline-block;
}
.left-size {
    font-size: 14px;
    /*font-weight: bold;*/
    width: 100%;
    /* margin-right: 5%; */
    height: 50px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    cursor: pointer;
    line-height: 50px;
    vertical-align: middle;
}
.left-ipt {
    width: 54%;
}

.show-TBD-content {
    display: inline-block;
    width: 100%;
    margin-right: 1%;
    cursor: pointer;
    vertical-align: middle;
    word-wrap: break-word;
    font-size: 14px;
    color: #606266;
    /* padding: 10px 10px 10px 0; */
}

.show-TBD-elli {
    /* display: inline-block;
    width: 100%;
    cursor: pointer;
    font-size: 14px;
    min-height: 50px;
    display: flex;
    align-items: center; */
    display: inline-block;
    width: 100%;
    margin-right: 1%;
    cursor: pointer;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    vertical-align: middle;
    font-size: 14px;
    color: #606266;
}
.squence-usecase {
    border-radius: 4px;
    border: 1px solid #dcdfe6;
    margin: 20px 20px;
    overflow-y: scroll;
    overflow-x: hidden;
    padding: 10px;
    max-height: 300px;
}

.check-span {
    display: block;
    margin: 5px 0;
    min-width: 20%;
    width: 25%;
    float: left;
}

.up-data-btn {
    width: 330px;
    height: 320px;
    margin-left: 20px;
    display: block;
    background: #fff;
    outline: none;
    border: 1px dashed #ccc;
    color: #ccc;
    font-size: 15px;
    /*display: inline-block;*/
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
    padding-left: 20px;
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
    /*font-weight: bold;*/
}

.sequence-number {
    color: #333;
    margin: 10px 20px 0 20px;
    font-size: 16px;
}
.NB {
    margin: 20px auto;
    font-size: 18px;
}
.leftCheck {
    background-color: white;
    font-size: 14px;
    font-weight: 500;
    padding: 10px;
    width: 220px;
    margin-top: 20px;
    overflow-y: hidden;
    overflow-x: hidden;
}
.leftCheck-title {
    font-weight: 500;
    margin-top: 5px;
}
.leftCheck-title:hover {
    cursor: pointer;
}
.leftCheck ul li {
    list-style: none;
    margin-top: 5px;
    margin-left: 20px;
    color: #000;
    width: 200px;
    font-size: 14px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    transition: all 0.5s linear;
    -moz-transition: all 0.5s linear; /* Firefox 4 */
    -webkit-transition: all 0.5s linear; /* Safari 和 Chrome */
    -o-transition: all 0.5s linear;
    padding-left: 5px;
    padding-bottom: 5px;
    cursor: pointer;
}
.leftCheck ul li:hover {
    background: #6bcca0;
}
.leftCheck .leftCheck-title-ex li:hover {
    background: white;
}
.append_span {
    height: 25px;
    line-height: 25px;
    font-size: 14px;
    cursor: pointer;
}
.message {
    margin-left: 20px;
    text-align: center;
    padding: 20px;
    font-size: 14px;
    color: #5e6d82;
    border: 1px solid #ebeef5;
    margin-top: 10px;
}
.consider-title {
    font-weight: 600;
    margin: 20px 0;
    font-size: 18px;
    padding-left: 10px;
    background-color: rgb(107, 204, 160);
    color: white;
    height: 25px;
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
.Activity_box {
    margin-left: 20px;
}
.leftCheck-title:hover {
    background: #6bcca0;
}
@media screen and (max-width: 1366px) {
    .up-data-btn {
        width: 230px;
        height: 240px;
        margin-left: 20px;
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
        margin-top: 0;
    }
    .img-box {
        width: 250px;
        height: 250px;
        margin-right: 20px;
        position: relative;
        display: inline-block;
    }
    .check-span {
        display: block;
        margin: 5px 0;
        min-width: 20%;
        width: 30%;
        float: left;
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
    .content_box {
        float: left;
        width: 80%;
        height: 100%;
        /*overflow-y: scroll;*/
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
    .header {
        height: 100%;
        padding: 10%;
        clear: both;
    }
    .content_box {
        float: left;
        width: 820px;
        height: 100%;
        /*overflow-y: scroll;*/
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
    .img-box {
        width: 180px;
        height: 170px;
        margin-right: 10px;
        position: relative;
        display: inline-block;
    }
    .check-span {
        display: block;
        margin: 5px 0;
        min-width: 20%;
        width: 50%;
        float: left;
    }
}
</style>
