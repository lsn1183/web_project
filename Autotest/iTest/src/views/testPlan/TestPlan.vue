<template>
        <router-view></router-view>
</template>
<script>
import { generateTitle } from '@/utils/i18n'
export default {
    name: 'test-plan',
    data() {
        return {
            backstage_breadcrumb: []
        }
    },
    watch: {
        $route() {
            this.getBreadcrumb()
        }
    },
    created() {},
    activated() {
        if (this.$store.getters.nav_active_index == '3') {
            this.$store.dispatch('setTestPlanPage', 1) // 在切换页面时，去除test plan page页码的记录
        }
    },
    methods: {
        generateTitle,

        getBreadcrumb() {
            let matched = this.$route.matched.filter(item => item.name)
            const first = matched[0]
            if (first && first.name !== 'homepage') {
                matched = [{ path: '/homepage', meta: { title: 'homepage' } }].concat(matched)
            }
            matched.splice(0, 1)
            this.backstage_breadcrumb = matched
        }
    }
}
</script>
<style lang="scss" scoped>
.test-case {
    height: 100%;
    position: relative;

    .side-bar {
        float: left;
        width: 250px;
        height: 100%;
        overflow: scroll;
        box-sizing: border-box;
        padding: 15px 0 0 10px;

        @media screen and (max-width: 1280px) {
            width: 200px;
        }
        border-right: 2px solid rgba(216, 231, 223, 0.5);
    }

    .content {
        float: left;
        width: 100%;
        height: 100%;
        padding: 20px 0 0 20px;
        box-sizing: border-box;
        position: relative;
    }
    @media screen and (max-width: 1280px) {
        .content {
            width: calc(100% - 200px);
        }
    }
}
@media screen and (max-width: 1024px) {
    .collapsible .filters-content .filters-content-field .input-text {
        margin-left: 0;
        padding-left: 5px;
    }
}
</style>