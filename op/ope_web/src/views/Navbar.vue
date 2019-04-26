<template>
    <div class="navbar-container">
        <scroll-pane class="tags-view-wrapper" ref="scrollPane">
            <ul>
                <li
                    @click="showImg()"
                    @mouseenter="imgVisible=true"
                    @mouseleave="imgVisible=false"
                    class="nav-item"
                >图</li>
                <li
                    :class="{'active-item':index=== activeIndex}"
                    :key="index"
                    @click="addClass(index)"
                    class="nav-item"
                    v-for="(item, index) of navItemArr"
                >{{item}}</li>
            </ul>
        </scroll-pane>
        <image-view v-show="imgVisible"></image-view>
    </div>
</template>
<script>
import ScrollPane from '@/components/ScrollPane'
import ImageView from '@/components/ImageView'
export default {
    name: "navbar",
    components: {
        ScrollPane,
        ImageView
    },
    data() {
        return {
            activeIndex: 0,
            navItemArr: [
                '1.View of Screen',
                '2.View of Soft Button',
                '3.Soft Button Action',
                '4.Hard Key Action',
                '5.Initialized Status',
                '6.Action on Status change',
                '7.Action on Transition',
                '8.Trigger Action'
            ],
            imgVisible: false
        };
    },
    methods: {
        addClass(index) {
            this.activeIndex = index
            const address = '/item' + (index + 1)
            const pathObj = {
                path: address,
                query: this.$route.query
            }
            this.$router.push(pathObj)
        }
    },
    created() {
        this.activeIndex = Number(this.$route.path.slice(-1)) - 1
    }
}
</script>
<style scoped>
.navbar-container {
    transition: right 0.28s;
    width: 101px !important;
    height: 100%;
    position: fixed;
    top: 0;
    right: 0;
    bottom: 0;
    z-index: 2000;
    overflow: hidden;
    border-left: 1px solid #dfdfdf;
    background-color: #fff;
    padding: 10px;
    display: flex;
}
ul,
li {
    list-style: none;
    width: 100%;
    text-align: center;
    margin: 0 auto;
}
.nav-item {
    width: 70px;
    height: 70px;
    margin-bottom: 10px;
    border: 1px solid #dfdfdf;
    cursor: pointer;
    white-space: normal;
    word-break: keep-all;
    word-wrap: break-word;
}
.active-item {
    background-color: aquamarine;
}
</style>