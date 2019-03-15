<template>
    <div class="tinymce-container editor-container">
        <textarea class="tinymce-textarea" :id="tinymceId"></textarea>
        <div class="editor-custom-btn-container">
            <editorImage color="#1890ff" class="editor-upload-btn" @successCBK="imageSuccessCBK"></editorImage>
        </div>
    </div>
</template>

<script>
import '../../../static/tinymce/langs/zh_CN.js' // 引入的中文包
import editorImage from './components/editorImage'
import plugins from './plugins'
import toolbar from './toolbar'

export default {
    name: 'tinymce',
    components: { editorImage },
    props: {
        id: {
            type: String
        },
        value: {
            type: String,
            default: ''
        },
        toolbar: {
            type: Array,
            required: false,
            default() {
                return []
            }
        },
        menubar: {
            default: 'file edit insert view format table'
        },
        height: {
            type: Number,
            required: false,
            default: 360
        }
    },
    data() {
        return {
            hasChange: false,
            hasInit: false,
            tinymceId: this.id || 'vue-tinymce-' + +new Date()
        }
    },
    watch: {
        value(val) {
            if (!this.hasChange && this.hasInit) {
                this.$nextTick(() => window.tinymce.get(this.tinymceId).setContent(val))
            }
        }
    },
    mounted() {
        this.initTinymce()
    },
    activated() {
        this.initTinymce()
    },
    deactivated() {
        this.destroyTinymce()
    },
    methods: {
        initTinymce() {
            const _this = this
            window.tinymce.init({
                selector: `#${this.tinymceId}`, // selector理解为class、ID等，以此使用tinymce样式
                height: this.height, // 高度
                // language: 'zh_CN', // 语言，可自行下载中文
                body_class: 'panel-body',
                object_resizing: false, // 这个选项允许打开/关闭图像、表格或媒体对象的调整句柄。默认启用，允许调整表和图像的大小
                toolbar: this.toolbar.length > 0 ? this.toolbar : toolbar, // 工具栏，可根据需求配置
                menubar: this.menubar, // 启动菜单栏并显示配置选项
                plugins: plugins, // 插件，可自行根据现实内容配置
                end_container_on_empty_block: true, // 如果在一个空的内部块元素中按下enter键，这个选项允许您分割当前的容器块元素。
                powerpaste_word_import: 'clean',
                code_dialog_height: 450, // 设置了代码对话框的内部可编辑区域高度
                code_dialog_width: 1000, // 设置了代码对话框的内部可编辑区域宽度
                advlist_bullet_styles: 'square',
                advlist_number_styles: 'default',
                imagetools_cors_hosts: ['www.tinymce.com', 'codepen.io'],
                default_link_target: '_blank',
                link_title: false,
                // initinstancecallback选项允许在每次初始化编辑器实例时指定要执行的函数名。这个函数的格式是initInstance（编辑器），其中编辑器是编辑器实例对象引用。
                init_instance_callback: editor => {
                    if (_this.value) {
                        editor.setContent(_this.value)
                    }
                    _this.hasInit = true
                    editor.on('NodeChange Change KeyUp SetContent', () => {
                        this.hasChange = true
                        this.$emit('input', editor.getContent())
                    })
                }
            })
        },
        destroyTinymce() {
            if (window.tinymce.get(this.tinymceId)) {
                window.tinymce.get(this.tinymceId).destroy()
            }
        },
        setContent(value) {
            window.tinymce.get(this.tinymceId).setContent(value)
        },
        getContent() {
            window.tinymce.get(this.tinymceId).getContent()
        },
        imageSuccessCBK(arr) {
            const _this = this
            arr.forEach(v => {
                window.tinymce.get(_this.tinymceId).insertContent(`<img class="wscnph" src="${v.url}" >`)
            })
        }
    },
    destroyed() {
        this.destroyTinymce()
    }
}
</script>

<style scoped>
.tinymce-container {
    position: relative;
}
.tinymce-container >>> .mce-fullscreen {
    z-index: 10000;
}
.tinymce-textarea {
    visibility: hidden;
    z-index: -1;
}
.editor-custom-btn-container {
    position: absolute;
    right: 4px;
    top: 4px;
    /*z-index: 2005;*/
}
.editor-upload-btn {
    display: inline-block;
}
</style>
