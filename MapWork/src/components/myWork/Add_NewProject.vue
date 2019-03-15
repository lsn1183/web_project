<template>
	<div id="File-Modle-box" >
		<div class="tree-box">
			<div class="technicalDoc">
                <ul class="project-title" :class="{Light:fpm_id==0}" @click="getAllFramwork()">平台管理</ul>
                <ul class="project-title" :class="{Light:fpm_id==1}" @click="getAllProgect()">项目管理</ul>
                <ul class="project-title" :class="{Light:fpm_id==2}" @click="getAllModle()">模块信息管理</ul>
                <ul class="project-title" :class="{Light:fpm_id==3}" @click="getModuleRelationship()">模块关系管理</ul>

			</div>
		</div>
		<div class="content-box" >
			<!-- <basicdt></basicdt> -->
            <router-view></router-view>
		</div>
	</div>
</template>

<script>
import basicdt from './Add_ProjectTemplate'
export default {
    data() {
        return {
            FrameworkList:[],
            fpm_id:0,
        }
    },
    mounted() {
        if(this.$store.state.fpm_id==0){
            this.getAllFramwork()
        }else if(this.$store.state.fpm_id==1){
            this.getAllProgect()
        }else if(this.$store.state.fpm_id==2){
            this.getAllModle()
        }else if(this.$store.state.fpm_id==3){
            this.getModuleRelationship()
        }else {
            // do nothing
        }
        // this.getFramework()

    },
    computed:{
        Fpm_id(val){
            return this.$store.state.fpm_id
        },

    },
    watch:{
        fpm_id(val){
            this.$store.state.fpm_id = val
        },
        Fpm_id(val){
            this.fpm_id = val
        }
    },
    components: {
        basicdt: basicdt
    },
    methods: {
        getAllFramwork(){
            // if (this.userPurviewManage('平台管理') == true) {
                this.fpm_id = 0
                this.$store.state.high_type="3-4-1"
                window.sessionStorage.setItem('activeIndex2', '3-4-1')
                window.sessionStorage.setItem('diffTitleType', 'platformManagement')
                this.$router.push('/tagl/Add_NewProject/FramworkTemplate')
            // } else {
            //     this.$message({
            //         type: "warning",
            //         message: "您没有操作权限！"
            //     })
            // }
        },
        getAllProgect(){
            // if (this.userPurviewManage('项目管理') == true) {
                this.fpm_id = 1
                this.$store.state.high_type="3-4-2"
                window.sessionStorage.setItem('activeIndex2', '3-4-2')
                window.sessionStorage.setItem('diffTitleType', 'projectManagement')
                this.$router.push('/tagl/Add_NewProject/ProjectTemplate')
            // } else {
            //     this.$message({
            //         type: "warning",
            //         message: "您没有操作权限！"
            //     })
            // }  
        },
        getModuleRelationship() {
            this.fpm_id = 3
            this.$store.state.high_type="3-4-6"
            window.sessionStorage.setItem('activeIndex2', '3-4-6')
            window.sessionStorage.setItem('diffTitleType', 'ModuleRelationship')
            this.$router.push('/tagl/Add_NewProject/ModuleRelationship')
        },
        getAllModle(){
            // if (this.userPurviewManage('模块管理') == true) {
                this.fpm_id = 2
                this.$store.state.high_type="3-4-3"
                window.sessionStorage.setItem('activeIndex2', '3-4-3')
                window.sessionStorage.setItem('diffTitleType', 'moduleManagement')
                if (this.$route.query.page) {
                    let routeValue={path:'/tagl/Add_NewProject/ModelTemplate',query:{page:this.$route.query.page}}
                    this.$router.push(routeValue)
                }else{
                    this.$router.push('/tagl/Add_NewProject/ModelTemplate')
                }
            // } else {
            //     this.$message({
            //         type: "warning",
            //         message: "您没有操作权限！"
            //     })
            // }
        },
        getFramework(){
            this.$axios.get(this.Ip+"/Framework").then(res=>{
                if(res.data.result=="OK"){
                    this.FrameworkList = res.data.content
                }else{

                }
            })
            .catch(res=>{

            })
        },
        getFw(val){
            this.fw_id = val
        },
        editNodeKeyType() {},
        reqTreeData() {},
        appendTreeNode(val) {},
        handleDoc() {},
        handleNodeClick(data, node) {}
    }
}
</script>

<style scoped>
ul, ol, li {
    list-style: none;
    font-size: 14px;
    color: #606266;
}
#File-Modle-box {
    width: 100%;
    height: 100%;
    min-width: 1024px;
    overflow: hidden;
}
.tree-box {
    float: left;
    margin: 0;
    padding: 0;
    width: 15%;
    height: 100%;
    background-color: none;
}
.title {
    color: #333;
    font-size: 14px;
    font-weight: bold;
    margin-top: 20px;
    margin-left: 15px;
}
.technicalDoc {
    margin-left: 0;
    padding-left: 20px;
    height: 100%;
    margin-right: 0;
    padding-right: 0;
    padding-top: 20px;
    border-right: 2px solid rgba(216, 231, 223, 0.5);
}

.el-icon-arrow-left {
    cursor: pointer;
    margin-left: 0px;
    padding: 0;
}
.content-box {
    float: right;
    height: 100%;
    width: 85%;    
}
.project-title{
    padding-left: 15px;
    cursor: pointer;
    list-style: none;
    line-height: 35px;
}
.project-title:hover{
    background-color: #E2EDF9;
}
.leaf{
    padding-left: 15px;
    cursor: pointer;
    list-style: none;
    line-height: 22px;
}
.leaf:hover{
    background-color: #E2EDF9;
}
.Light{
    color: #6bcca0;
    border-right: 2px solid #6bcca0;
}
@media screen and (max-width: 1024px) {
    .tree-box {
        width: 180px;
    }
    .content-box {
        width: 840px;
    }
    .tree-box {
        width: 20%;
    }
    .content-box {
        width: 80%;    
    }
}
@media screen and (max-width: 1366px) {
    .tree-box {
        width: 180px;
    }
    .content-box {
        width: 840px;
    }
    .tree-box {
        width: 20%;
    }
    .content-box {
        width: 80%;    
    }
}
</style>

