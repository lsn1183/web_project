<template>
    <div class="app-wrapper">
        <header>
            <div class="logo">
                <img src="../../assets/iTest.png" class="left-hmi-img" alt="商标" title="iTest">
                <span>测试项目</span>
                <el-select v-model="project_val" placeholder="请选择项目" size='mini' class="select" @visible-change="visible_change_fun" @change="handle_change">
                    <el-option v-for="item in project_list" :key="item.id" :label="item.name" :value="item.id">
                    </el-option>
                </el-select>
            </div>

            <top-nav></top-nav>
        </header>
        <div class="main-container">
            <keep-alive>
                <router-view></router-view>
            </keep-alive>
        </div>
    </div>
</template>
<script>
import TopNav from './nav/Nav'
import { get_project_list_fun } from '@/api/backstage'

export default {
    name: 'homepage',
    components: {
        TopNav
    },
    data() {
        return {
            titleName: 'iTest',
            project_list: [],
            project_val: ''
        }
    },
    mounted() {
        this.get_project_list_fun()
    },
    methods: {
        get_project_list_fun() {
            return new Promise((resolve, reject) => {
                get_project_list_fun()
                    .then(res => {
                        this.project_list = res.data
                        if (res.data.length !== 0) {
                            if (this.$store.getters.proj_id == 0) {
                                this.project_val = res.data[0].name
                                this.$store.dispatch('setProjId', res.data[0].id)
                                this.$store.dispatch('setProjName', res.data[0].name)
                            } else {
                                this.project_val = this.$store.getters.proj_name
                            }
                        }
                    })
                    .catch(() => {
                        reject()
                    })
            })
        },
        visible_change_fun(val) {
            if (val == true) {
                this.get_project_list_fun()
            }
        },
        handle_change(selected_id) {
            const len = this.project_list.length
            for (let i = 0; i < len; i++) {
                if(this.project_list[i].id == selected_id) {
                    this.$store.dispatch('setProjId', this.project_list[i].id)
                    this.$store.dispatch('setProjName', this.project_list[i].name)
                    this.$router.push('/homepage')
                    break
                }   
            }
        }
    }
}
</script>
<style lang="scss" scoped>
@import '@/styles/mixin.scss';
.app-wrapper {
    @include clearfix;
    position: relative;
    width: 100%;
    height: 100%;
    background-color: white;

    header {
        position: fixed;
        left: 0;
        top: 0;
        right: 0;
        width: 100%;
        // height: 60px;
        height: 40px;
        z-index: 100;
        box-shadow: 0 0 1px rgba(0, 0, 0, 0.25);
    }

    .main-container {
        position: absolute;
        top: 40px;
        // top: 60px;
        left: 0;
        right: 0;
        bottom: 0;
        overflow: hidden;
    }
    .logo {
        position: absolute;
        left: 20px;
        // top: 8px;
        width: 400px;
        height: 40px;
        font-size: 30px;
        color: #2c3e50;
        line-height: 40px;
        font-weight: bold;
        font-family: 'Dosis', 'Source Sans Pro', 'Helvetica Neue', Arial, sans-serif;
    }
    .logo > img {
        vertical-align: middle;
        margin-right: 0px;
        cursor: pointer;
        width: 106px;
        height: 23px;
    }
    .logo > span {
        // text-shadow: 0 0 6px green;
        // color: white;
        // margin-left: 66px;
        font-weight: normal;
        font-size: 14px;
        vertical-align: middle;
    }
    .select {
        width: 140px;
    }
}
</style>