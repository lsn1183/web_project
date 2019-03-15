<template>
    <div class="backstage-manage">
        <div class="backstage-manage-tree">
            <el-menu :default-active="backstage_active_index" class="el-menu-vertical-demo">
                <el-menu-item v-for="(item, index) in sidebar_list" :key="index" :index="item.name" @click="go_various_manage(item.path, index)">
                    <span slot="title">{{item.label}}</span>
                </el-menu-item>
            </el-menu>
        </div>

        <div class="backstage-manage-container">
            <!-- <div class="breadcrumb-header">
                <el-breadcrumb separator-class="el-icon-arrow-right">
                    <el-breadcrumb-item  v-for="(item, index) in backstage_breadcrumb" :key="index">
                        <span v-if='index == 0'>{{generateTitle(item.name)}}</span>
                        <router-link v-else :to="item.redirect||item.path">{{generateTitle(item.name)}}</router-link>
                    </el-breadcrumb-item>
                </el-breadcrumb>
            </div> -->
            <keep-alive>
                <router-view></router-view>
            </keep-alive>
        </div>
    </div>
</template>
<script>
import { generateTitle } from '@/utils/i18n'
export default {
    name: 'backstage',
    methods: {
        generateTitle,
        go_various_manage(path, index) {
            this.$store.dispatch('setBackstageActiveIndex', (index + 1).toString())
            this.$router.push(path)
        },
        get_breadcrumb() {
            let matched = this.$route.matched.filter(item => item.name)
            const first = matched[0]
            if (first && first.name !== 'homepage') {
                matched = [{ path: '/homepage', meta: { title: 'homepage' } }].concat(matched)
            }
            matched.splice(0, 1)
            this.backstage_breadcrumb = matched
        }
    },
    created() {
        this.backstage_active_index = this.$route.path.split('/')[2]
        this.get_breadcrumb()
    },
    watch: {
        $route() {
            this.backstage_active_index = this.$route.path.split('/')[2]
            this.get_breadcrumb()
        }
    },
    data() {
        return {
            backstage_breadcrumb: [
                {
                    name: '后台管理',
                    path: ''
                }
            ],
            backstage_active_index: '1',
            sidebar_list: [
                {
                    label: '项目管理',
                    index: '1',
                    path: '/backstage/projectManage',
                    name: 'projectManage'
                },
                {
                    label: '模块管理',
                    index: '2',
                    path: '/backstage/moduleManage',
                    name: 'moduleManage'
                },
                {
                    label: '国家管理',
                    index: '3',
                    path: '/backstage/countryManage',
                    name: 'countryManage'
                },
                {
                    label: '仕向地管理',
                    index: '4',
                    path: '/backstage/landManage',
                    name: 'landManage'
                },
                {
                    label: '自定义字段管理',
                    index: '5',
                    path: '/backstage/customManage',
                    name: 'customManage'
                },
                {
                    label: '关键字管理',
                    index: '6',
                    path: '/backstage/keywordManage',
                    name: 'keywordManage'
                },
                {
                    label: '用户角色管理',
                    index: '7',
                    path: '/backstage/RoleManage',
                    name:'RoleManage'
                },{
                    label: '权限管理',
                    index: '8',
                    path: '/backstage/PersonnelManage',
                    name:'PersonnelManage'
                },
            ]
        }
    }
}
</script>
<style lang="scss" scoped>
.backstage-manage {
    height: 100%;
    position: relative;

    .backstage-manage-tree {
        float: left;
        width: 250px;
        height: 100%;
        min-width: 250px;
        max-width: 250px;
        box-sizing: border-box;

        @media screen and (max-width: 1280px) {
            width: 200px;
            min-width: 200px;
            max-width: 200px;
        }
        padding: 0 0 0 10px;
        border-right: 2px solid rgba(216, 231, 223, 0.5);
    }

    .backstage-manage-container {
        float: left;
        width: calc(100% - 250px);
        height: 100%;
        padding: 20px 0 0 20px;
        box-sizing: border-box;
        position: relative;
    }
    @media screen and (max-width: 1280px) {
        .backstage-manage-container {
            width: calc(100% - 200px);
        }
    }
}
</style>