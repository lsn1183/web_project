<template>
    <div id="add-project">
        <div class="add-project-steps">
            <el-steps :active="active" finish-status="success"  align-center >
                <el-step class="jump" title="输入项目名称" id="1">1</el-step>
                <el-step class="jump" title="选择框架" id="2">2</el-step>
                <el-step class="jump" title="选择技术文档" id="3">3</el-step>
                <el-step class="jump" title="选择模块" id="4">4</el-step>
            </el-steps>
        </div>
        <div class="add-project-content">
            <router-view></router-view>
        </div>
    </div>
</template>
<script>
require('../../../assets/js/jquery-1.8.3.min.js')
export default {
    mounted () {
        var self = this
        $('.jump').on('click', function(e) {
            self.jump($(this).attr('id'))
        });  
    },
    computed: {
        stepId(val) {
            if(parseInt(window.sessionStorage.getItem('step_id')) == 4) {
                this.active = 4
            }
            return this.$store.state.step_id
        }
    },
    watch: {
        stepId(val) {
            this.active = parseInt(window.sessionStorage.getItem('step_id'))   
        }
    },
    data () {
        return {
            active: 0
        }
    },
    methods: {
        jump(val) {
                switch (val) {
                    case '1': 
                        if(window.sessionStorage.getItem('step_id') >= val) {
                            this.$router.push('/tagl/Add_Project_Step_One')
                        }
                        break;
                    case '2':
                        if(window.sessionStorage.getItem('step_id') >= val) {
                            this.$router.push('/tagl/Add_Project_Step_Two')
                        }
                        break;
                    case '3':
                        if(window.sessionStorage.getItem('step_id') >= val) {
                            this.$router.push('/tagl/Add_Project_Step_Three')
                        }
                        break;
                    case '4':
                        if(window.sessionStorage.getItem('step_id') >= val) {
                            this.$router.push('/tagl/Add_Project_Step_Four')
                        }
                        break;
                    default:
                        break;
                }
        }
    }
}
</script>
<style>
#add-project {
    margin: 0 auto;
    width: 80%;
    height: 100%;
}
.add-project-steps {
    padding-top: 20px
}
.add-project-content {
    overflow-y: scroll;
}
</style>
