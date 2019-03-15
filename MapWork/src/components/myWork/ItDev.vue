<template>
	<div id='USERs'>
		<div class="bnt-app">
            <span class="append-span" @click="add_knowledge_classify">[ 添加知识点分类 ]</span>
		</div>
		<div class="custom-tree-container">
			<div>
				<el-tree
				:data="classificationData"
				node-key="id"
				:props="defaultProps"
				:expand-on-click-node="true"
                @node-drag-start="handleDragStart"
                @node-drag-enter="handleDragEnter"
                @node-drag-leave="handleDragLeave"
                @node-drag-over="handleDragOver"
                @node-drag-end="handleDragEnd"
                @node-drop="handleDrop"
                draggable
                :allow-drop="allowDrop"
                :allow-drag="allowDrag">
				<span class="custom-tree-node" slot-scope="{ node, data }" :title="data.remark">
					<span style="width:100px">
						{{ data.tag }} {{data.required == false ? "" : "[必填]"}}
					</span>
					<span class="icon_operation">
						<i class="el-icon-plus" @click.stop="() => append(node,data)"></i>
                        <i class="el-icon-edit" @click.stop="() => edit_tag(node, data)"></i>
                        <i class="el-icon-delete" @click.stop="() => remove(node, data)"></i>
					</span>
				</span>
				</el-tree>
			</div>
		</div>

		<!-- confirm_delete Dialog -->
		<el-dialog title="删除知识点" :visible.sync="TAG_del_flag" width="30%"
		:before-close="handleClose">
			<span>确定要删除此条知识点吗？</span>
			<span slot="footer" class="dialog-footer">
				<el-button type="primary" @click="confirm_delete()">确 定</el-button>
				<el-button @click="cancel()">取 消</el-button>
			</span>
		</el-dialog>
		
		<!-- Add Dialog -->
		<el-dialog title="添加知识点" :visible.sync="TAG_add_content_flag" width="30%"
		:before-close="handleClose">
		<!-- 新增TAG维度 -->
			<el-form ref="form" :model="sizeForm" label-width="30%" >
				<el-form-item label="新增内容">
					<el-input v-model="sizeForm.tag"></el-input>
				</el-form-item>
                <el-form-item label="备注">
					<el-input v-model="sizeForm.remark" type="textarea" rows=6></el-input>
				</el-form-item>
                <el-form-item label="必填">
					<el-checkbox v-model="sizeForm.required"></el-checkbox>
				</el-form-item>
			</el-form>
			<span slot="footer" class="dialog-footer">
				<el-button type="primary" @click="add_content_dialog()">确 定</el-button>
				<el-button @click="cancel()">取 消</el-button>
			</span>
		</el-dialog>

		<!-- edit Dialog -->
		<el-dialog title="更新内容" :visible.sync="TAG_change_class_flag" width="30%"
		:before-close="handleClose">
			<el-form ref="form" :model="changeForm" label-width="30%">
        <el-form-item label="知识点">
					<el-input v-model="changeForm.tag"></el-input>
				</el-form-item>
            <el-form-item label="必填">
                <el-checkbox v-model="changeForm.required"></el-checkbox>
			</el-form-item>
			</el-form>
			<span slot="footer" class="dialog-footer">
				<el-button type="primary" @click="edit()">确 定</el-button>
				<el-button @click="cancel()">取 消</el-button>
			</span>
		</el-dialog>
	</div>
</template>

<script scoped>
require('../../assets/js/jquery-1.8.3.min.js')
let id = 1000
export default {
    name: 'User',
    mounted: function() {
        this.get_TAG_data()
    },
    data() {
        return {
            defaultProps: {
                children: 'sub_tags',
                label: 'tag'
            },
            classificationData: [],
            maxexpandId: 95,
            ss: [],
            tabledata1: [],
            TAG_add_class_flag: false,
            TAG_add_content_flag: false,
            TAG_change_class_flag: false,
            TAG_change_flag: false,
            TAG_del_flag: false,
            del_id: '',
            sizeForm: {
                parent_tag_id: null,
                tag: '',
                remark: '',
                required: false
            },
            changeForm: {
                parent_tag_id: null,
                tag: '',
                tag_id: '',
                remark: '',
                required: false
            },
            pwd: '',
            current_del_id: null,
            newAddType: null,
            AddTagTypeName: '',
            AddTagContentName: '',
            current_edit_type: '',
            AddtionparentTagId: null,
            DelTagId: null,
            editTagId: null,
            optTagType: '',
            showRemark: 0
        }
    },
    methods: {
        handleDragStart(node, ev) {
            this.changeForm.tag_id = node.data.tag_id
            this.changeForm.tag = node.data.tag
        },
        handleDragEnter(draggingNode, dropNode, ev) {},
        handleDragStart(node, ev) {
            this.changeForm.tag_id = node.data.tag_id
            this.changeForm.tag = node.data.tag
        },
        handleDragEnter(draggingNode, dropNode, ev) {},
        handleDragLeave(draggingNode, dropNode, ev) {},
        handleDragOver(draggingNode, dropNode, ev) {},
        handleDragEnd(draggingNode, dropNode, dropType, ev) {},
        handleDrop(draggingNode, dropNode, dropType, ev) {
            this.changeForm.parent_tag_id = dropNode.data.tag_id
            this.$axios
                .put(this.Ip + '/TagTree/' + this.changeForm.tag_id, this.changeForm)
                .then(res => {
                    if (res.data.result == 'OK') {
                        this.optTagType = 'edit'
                        this.get_TAG_data()
                        this.$notify({
                            type: 'success',
                            message: '修改成功'
                        })
                    } else {
                        this.$confirm('提交失败')
                            .then(_ => {
                                this.TAG_change_flag = false
                                this.TAG_change_class_flag = false
                            })
                            .catch(_ => {})
                    }
                })
                .catch(err => {})
        },
        allowDrop(draggingNode, dropNode, type) {
            return true
        },
        allowDrag(draggingNode) {
            return true
        },
        get_TAG_data() {
            // 设置homepage导航条默认高亮
            window.sessionStorage.setItem('activeIndex2', '1-2-4')
            let that = this
            this.$axios
                .get(this.Ip + '/TagTree/normal')
                .then(res => {
                    if (res.data.result == 'OK') {
                        let resData = JSON.parse(JSON.stringify(res.data.content))
                        this.classificationData = resData
                        this.$emit('receiveAction')
                        // if (this.optTagType == 'add') {
                        //     if (this.AddtionparentTagId === 0) {
                        //         function addTag(resData, resId) {
                        //             for (let i = 0; i < resData.length; i++) {
                        //                 let tagIdFlag = false
                        //                 for (let j = 0; j < resId.length; j++) {
                        //                     if (resData[i].tag_id === resId[j].tag_id) {
                        //                         tagIdFlag = true
                        //                         break
                        //                     }
                        //                 }
                        //                 if (tagIdFlag === false) {
                        //                     resId.push(resData[i])
                        //                     return
                        //                 }
                        //             }
                        //         }
                        //         addTag(resData, this.classificationData)
                        //     } else {
                        //         (function addTag(resData, resId) {
                        //             let index = 0
                        //             for (index; index < resData.length; index++) {
                        //                 if (resData[index].tag_id === that.AddtionparentTagId) {
                        //                     console.log(resData[index].tag_id, 'resData')
                        //                     for (let i = 0; i < resData[index].sub_tags.length; i++) {
                        //                         let tagIdFlag = false
                        //                         for (let j = 0; j < resId[index].sub_tags.length; j++) {
                        //                             if (resData[index].sub_tags[i].tag_id === resId[index].sub_tags[j].tag_id) {
                        //                                 tagIdFlag = true
                        //                                 break
                        //                             }
                        //                         }
                        //                         console.log(tagIdFlag,'tagIdFlag')
                        //                         if (tagIdFlag === false) {
                        //                             console.log(resId[index].sub_tags,'------------')
                        //                             console.log(resData[index].sub_tags[i], '============')
                        //                             resId[index].sub_tags.push(resData[index].sub_tags[i])
                        //                             console.log(resId[index].sub_tags)
                                                    
                        //                             return
                        //                         }
                        //                     }
                        //                 }
                        //                 if (resData[index].sub_tags.length != 0) {
                        //                     addTag(resData[index].sub_tags, resId[index].sub_tags)
                        //                 }
                        //             }
                        //         })(resData, this.classificationData)
                        //         console.log(this.classificationData, 'this')
                        //     }
                        // } else if (this.optTagType == 'delete') {
                        //     // delTagOK(resData)
                        //     //删除TAG DelTagId
                        //     ;(function delTag(val) {
                        //         for (let index = 0; index < val.length; index++) {
                        //             if (that.DelTagId == val[index].tag_id) {
                        //                 val.splice(index, 1)
                        //                 return
                        //             }
                        //             if (val[index].sub_tags.length != 0) {
                        //                 delTag(val[index].sub_tags)
                        //             }
                        //         }
                        //     })(this.classificationData)
                        // } else if (this.optTagType == 'edit') {
                        //     // editTagOk(resData)
                        //     ;(function editTagName(resVal, val) {
                        //         for (let index = 0; index < val.length; index++) {
                        //             if (that.editTagId == resVal[index].tag_id) {
                        //                 val[index].tag = resVal[index].tag
                        //                 val[index].remark = resVal[index].remark
                        //                 val[index].required = resVal[index].required
                        //                 return
                        //             }
                        //             if (resVal[index].sub_tags.length != 0) {
                        //                 editTagName(resVal[index].sub_tags, val[index].sub_tags)
                        //             }
                        //         }
                        //     })(resData, this.classificationData)
                        // } else {
                        //     // function getLeafCountTree(json) {
                        //     //   if(json.sub_tags.length == 0){
                        //     //     json.childrenNum = 1;
                        //     //     return 1;
                        //     //   }else {
                        //     //     var leafCount = 0;
                        //     //     for(var i = 0; i < json.sub_tags.length;i++) {
                        //     //       leafCount = leafCount + getLeafCountTree(json.sub_tags[i]);
                        //     //     }
                        //     //     json.childrenNum = leafCount;
                        //     //     return leafCount;
                        //     //   }
                        //     // }
                        //     // for(var k=0;k<resData.length;k++){
                        //     //   getLeafCountTree(resData[k])
                        //     // }

                        //     this.classificationData = JSON.parse(JSON.stringify(resData))
                        // }
                    } else {
                        //request error
                    }
                })
                .catch(err => {})
        },
        add_class_dialog() {
            this.sizeForm = {
                parent_tag_id: null,
                tag: '',
                remark: '',
                required: false
            }
            if (this.sizeForm.tag == '') {
                this.$message({
                    message: 'Tag内容不能为空',
                    type: 'warning',
                    showClose: true,
                    duration: 0
                })
                return
            }
            this.sizeForm.parent_tag_id = 0
            this.$axios
                .post(this.Ip + '/TagTree', this.sizeForm)
                .then(res => {
                    if (res.data.result == 'OK') {
                        this.sizeForm = {
                            parent_tag_id: null,
                            tag: '',
                            remark: '',
                            required: false
                        }
                        this.get_TAG_data()
                        this.TAG_add_class_flag = false
                        this.$message({
                            type: 'success',
                            message: '添加成功',
                            showClose: true,
                            duration: 2000
                        })
                    } else {
                        this.$confirm('提交失败')
                            .then(_ => {
                                this.sizeForm = {
                                    parent_tag_id: null,
                                    tag: '',
                                    remark: '',
                                    required: false
                                }
                                this.TAG_add_class_flag = false
                            })
                            .catch(_ => {})
                    }
                })
                .catch(err => {})
        },
        add_content_dialog() {
            if (this.sizeForm.tag == '') {
                this.$message({
                    message: '新增内容不能为空',
                    type: 'warning',
                    showClose: true,
                    duration: '0'
                })
                return
            }
            this.$axios
                .post(this.Ip + '/TagTree', this.sizeForm)
                .then(res => {
                    if (res.data.result == 'OK') {
                        this.sizeForm = {
                            parent_tag_id: null,
                            tag: '',
                            remark: '',
                            required: false
                        }
                        this.get_TAG_data()
                        this.TAG_add_content_flag = false
                        this.$message({
                            type: 'success',
                            message: '添加成功',
                            showClose: true,
                            duration: 2000
                        })
                    } else {
                        this.$confirm('提交失败')
                            .then(_ => {
                                this.sizeForm = {
                                    parent_tag_id: null,
                                    tag: '',
                                    remark: '',
                                    required: false
                                }
                                this.TAG_add_content_flag = false
                            })
                            .catch(_ => {})
                    }
                })
                .catch(err => {})
        },
        edit_dialog(index, row) {
            this.TAG_change_flag = true
            this.changeForm.tag = row.tag
            this.changeForm.tag_id = row.tag_id
            this.changeForm.parent_tag_id = row.parent_tag_id
        },
        edit() {
            if (this.changeForm.tag === '') {
                this.$message({
                    message: '知识点不能为空',
                    type: 'warning',
                    showClose: true,
                    duration: '0'
                })
                return
            }
            this.$axios
                .put(this.Ip + '/TagTree/' + this.changeForm.tag_id, this.changeForm)
                .then(res => {
                    if (res.data.result == 'OK') {
                        this.get_TAG_data()
                        this.TAG_change_flag = false
                        this.TAG_change_class_flag = false
                        this.$message({
                            type: 'success',
                            message: '修改成功',
                            showClose: true,
                            duration: 2000
                        })
                    } else {
                        this.$confirm('提交失败')
                            .then(_ => {
                                this.TAG_change_flag = false
                                this.TAG_change_class_flag = false
                            })
                            .catch(_ => {})
                    }
                    // this.TAG_change_flag =false
                })
                .catch(err => {})
        },
        edit_parent(name, id) {
            this.TAG_change_class_flag = true
            this.changeForm.tag = name
            this.changeForm.tag_id = id
            this.changeForm.parent_tag_id = 0
        },
        Delete_Dialog(index, row) {
            this.TAG_del_flag = true
            this.del_id = row.tag_id
        },
        confirm_delete() {
            this.$axios
                .delete(this.Ip + '/TagTree/' + this.current_del_id)
                .then(res => {
                    if (res.data.result == 'OK') {
                        this.del_id = ''
                        this.get_TAG_data()
                        this.TAG_del_flag = false
                        this.$message({
                            type: 'success',
                            message: '删除成功',
                            showClose: true,
                            duration: 2000
                        })
                    } else {
                        this.TAG_del_flag = false
                        this.$message({
                            type: 'warning',
                            message: '此条知识点关联相关文档，无法删除'
                        })
                    }
                })
                .catch(err => {
                    this.$message({
                            type: 'warning',
                            message: '服务异常'
                        })
                })
        },
        del_prent(name, id) {
            this.TAG_del_flag = true
            this.del_id = id
        },
        handleClose(done) {
            done()
            this.sizeForm = {
                parent_tag_id: null,
                tag: '',
                remark: '',
                required: false
            }
            this.contentForm = {}
        },
        cancel() {
            this.sizeForm = {
                parent_tag_id: null,
                tag: '',
                remark: '',
                required: false
            }
            this.TAG_add_content_flag = false
            this.TAG_add_class_flag = false
            this.TAG_change_class_flag = false
            this.TAG_change_flag = false
            this.TAG_del_flag = false
        },
        append(node, data) {
            this.sizeForm = {
                parent_tag_id: null,
                tag: '',
                remark: '',
                required: false
            }
            this.AddtionparentTagId = data.tag_id
            this.TAG_add_content_flag = true
            this.sizeForm.parent_tag_id = data.tag_id
            // this.sizeForm.required = data.required
            this.optTagType = 'add'
            
        },
        add_knowledge_classify() {
            this.sizeForm = {
                parent_tag_id: 0,
                tag: '',
                remark: '',
                required: false
            }
            this.newAddType = 'TAGType'
            this.TAG_add_content_flag = true
            this.sizeForm.parent_tag_id = 0
            this.AddtionparentTagId = 0
            this.optTagType = 'add'
            
        },
        remove(node, data) {
            this.TAG_del_flag = true
            this.current_del_id = data.tag_id
            this.DelTagId = data.tag_id
            this.optTagType = 'delete'
        },

        edit_tag(node, data) {
            this.editTagId = data.tag_id
            this.TAG_change_class_flag = true
            this.changeForm.tag = data.tag
            this.changeForm.tag_id = data.tag_id
            this.changeForm.parent_tag_id = data.parent_tag_id
            this.changeForm.required = data.required
            this.changeForm.remark = data.remark
            this.optTagType = 'edit'
        }
    }
}
</script>

<style scoped>
body,
html,
ul,
li {
    margin: 0;
    padding: 0;
    list-style: none;
}
.a_group {
    color: #42b983;
    cursor: pointer;
}
#USERs {
    position: relative;
    width: 100%;
    height: 100%;
}

.fl {
    float: left;
}

.active {
    color: #42b983;
    font-weight: bold;
}
.right {
    position: absolute;
    left: 80px;
    right: 0;
    top: 60px;
    bottom: 22px;
    overflow: auto;
    height: 100%;
    /* min-width: 724px; */
    /*display: flex;*/
}

.right .table > .el-table::before {
    height: 0;
}

.custom-tree-node {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 14px;
    padding-right: 8px;
}
.custom-tree-container {
    margin-left: 25px;
    width: 70%;
    overflow: scroll;
    height: 92%;
}
.fl {
    float: right;
}
.bnt-app {
    padding-top: 10px;
    margin-left: 25px;
    width: 70%;
    font-size: 14px;
    position: relative;
    height: 45px;
}
.append-span {
    position: absolute;
    right: 0;
    height: 25px;
    line-height: 25px;
    font-size: 14px;
    cursor: pointer;
    font-weight: 500;
}
@media only screen and (max-width: 1280px) {
    .right {
        position: absolute;
        left: 80px;
        right: 0;
        top: 60px;
        bottom: 22px;
        overflow: auto;
        height: 100%;
        /* min-width: 824px; */
        /*display: flex;*/
    }
    .custom-tree-container {
        padding-left: 25px;
        width: 98%;
        overflow: scroll;
        height: 92%;
        padding-right: 0;
        margin-left: 0;
    }
    .bnt-app {
        padding: 10px 40 0 25px;
        width: 98%;
        font-size: 14px;
        position: relative;
        height: 45px;
        margin-left: 0;
    }
    .append-span {
        position: absolute;
        right: 0;
        height: 25px;
        line-height: 25px;
        font-size: 14px;
        cursor: pointer;
        font-weight: 500;
    }
}
</style>
