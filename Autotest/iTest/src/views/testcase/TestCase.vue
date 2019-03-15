<template>
    <div class="test-case">
        <div class="side-bar">
            <el-tree v-show="tree_visible" ref="testCaseTree" :data="tree_data" :load="load_node" lazy highlight-current 
            :props="defaultProps" highlight-current :expand-on-click-node="false" @node-click="click_tree_node">
            </el-tree>
        </div>

        <div class="content">
            <!-- <div class="breadcrumb-header">
                <el-breadcrumb separator-class="el-icon-arrow-right">
                    <el-breadcrumb-item v-for="(item, index) in backstage_breadcrumb" :key="index">
                        <router-link :to="item.redirect||item.path">{{generateTitle(item.name)}}</router-link>
                    </el-breadcrumb-item>
                </el-breadcrumb>
            </div> -->
            <!-- <keep-alive> -->
                <router-view></router-view>
            <!-- </keep-alive> -->
            
            
        </div>
    </div>
</template>
<script>
import { get_module_tree_node, get_proj_tree, get_proj_module_tree_node } from '@/api/testcase.js'
// import { get_project_list } from '@/api/backstage.js'
import { generateTitle } from '@/utils/i18n'
export default {
    name: 'testCase',
    data() {
        return {
            tree_data: [
                {
                    id: 0,
                    name: '测试'
                    // sub: []
                }
            ],
            defaultProps: {
                children: 'sub',
                label: 'name',
                isLeaf: 'leaf'
            },
            backstage_breadcrumb: [],
            tree_visible: true,
            proj_id: this.$store.getters.proj_id
        }
    },
    watch: {
        $route(route) {
            if (route.path == '/testCase/testCaseShow') {
                this.tree_visible = true
            } else {
                this.tree_visible = false
            }
        }
    },
    created() {
        if (this.$route.path == '/testCase/testCaseShow') {
            this.tree_visible = true
        } else {
            this.tree_visible = false
        }
        // this.$store.dispatch('setTreeNodeUniqueId', 0)
        // this.$store.dispatch('setTreeNodeLevel', 0)
        // this.$store.dispatch('setTreeNodeUniqueId', 0)
        // // this.getBreadcrumb()
        // console.log('created')
        // this.get_proj_data()
    },
    activated() {
        if (this.$store.getters.nav_active_index == '2') {
            this.proj_id = this.$store.getters.proj_id
            this.$store.dispatch('setTreeNodeLevel', 1)
            this.$store.dispatch('setTreeNodeUniqueId', 0)
            // this.getBreadcrumb()
            this.$store.dispatch('setTestCasePage', 1) // 在切换页面时，去除case page页码的记录
            this.get_proj_data()
        }
    },
    methods: {
        generateTitle,

        get_proj_data() {
            // 获得树结构的第一层数据
            const proj_id = this.proj_id
            get_proj_tree(proj_id).then(res => {
                let data = res.data
                this.tree_data = data
                // 调试中，可能有bug
                // this.$store.dispatch('setTreeNodeUniqueId', res.data[0].$treeNodeId)
                if(res.data.length != 0) {
                    this.$store.dispatch('setTreeNodeDataId', res.data[0].id)
                } else {
                    this.$store.dispatch('setTreeNodeDataId', 0)
                }
            })
        },
        getBreadcrumb() {
            let matched = this.$route.matched.filter(item => item.name)
            const first = matched[0]
            if (first && first.name !== 'homepage') {
                matched = [{ path: '/homepage', meta: { title: 'homepage' } }].concat(matched)
            }
            matched.splice(0, 1)
            this.backstage_breadcrumb = matched
        },
        click_tree_node(data, node) {
            this.$store.dispatch('setTreeNodeLevel', node.level)
            this.$store.dispatch('setTreeNodeUniqueId', data.$treeNodeId)
            this.$store.dispatch('setTreeNodeDataId', data.id)
            this.$store.dispatch('setTestPlanPage', 1)
            this.page = 1
        },
        load_node(node, resolve) {
            const load_resolve = resolve
            if (node.level === 1) {
                get_proj_module_tree_node(node.data.id).then(res => {
                    let data = res.data
                    load_resolve(data)
                })
            }
            if (node.level > 1) {
                get_module_tree_node(node.data.id).then(res => {
                    let data = res.data
                    load_resolve(data)
                })
            }
        }
    }
}
</script>
<style lang="scss" scoped>
</style>