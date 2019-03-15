<template>
    <div class="Append-basic-temlate" id="book-manage">
        <div class="Append-basic-temlate-countent"></div>
        <div class="content-box">
            <div class="mid">
                <div class="mid-top">
                    <div class="block-title" @keyup.enter="search_click(search_val)">
                        <el-autocomplete
                            class="inline-input"
                            v-model="search_val"
                            :fetch-suggestions="querySearch"
                            placeholder="输入搜索内容"
                            :trigger-on-focus="false"
                            @select="handleSelect"
                            style="width:100%"
                        >
                            <el-button
                                slot="append"
                                icon="el-icon-search"
                                @click="search_click(search_val)"
                            ></el-button>
                        </el-autocomplete>
                    </div>
                    <div class="content-box-deep">
                        <div class="label-box">
                            <div class="label-box-text"></div>
                            <el-table :data="tableData.hits" border v-loading="loading">
                                <el-table-column
                                    label="项目名"
                                    min-width="100"
                                    align="left"
                                    header-align="left"
                                >
                                    <template slot-scope="scope">
                                        <div>{{scope.row._source.project}}</div>
                                    </template>
                                </el-table-column>
                                <el-table-column
                                    label="番号名"
                                    min-width="100"
                                    align="left"
                                    header-align="left"
                                >
                                    <template slot-scope="scope">
                                        <div>{{scope.row._source.number}}</div>
                                    </template>
                                </el-table-column>
                                <el-table-column
                                    label="概略"
                                    align="left"
                                    header-align="left"
                                    min-width="500"
                                >
                                    <template slot-scope="scope">
                                        <div>{{scope.row._source.subject}}</div>
                                    </template>
                                </el-table-column>
                                <el-table-column
                                    label="详细"
                                    width="100"
                                    align="left"
                                    header-align="left"
                                >
                                    <template slot-scope="scope">
                                        <span
                                            class="go-doc-text"
                                            @click="view_fun(scope.row._source.number)"
                                        >查看详细</span>
                                    </template>
                                </el-table-column>
                            </el-table>
                        </div>
                        <div class="form-page">
				            <el-pagination @current-change="listPageChange" :current-page="page" :page-size="page_size" :page-sizes="[100, 200, 300, 400,500]"
                             layout="total, sizes, prev, pager, next, jumper" :total="changdu" @size-change="handleSizeChange"></el-pagination>
			            </div>
                    </div>
                </div>
                <div style="clear: both;"></div>
                <el-dialog :visible.sync="dialogVisible" width="90%" title="Bug详细内容">

                    <el-table :data="dialog_data" style="width: 100%" border :show-heade="flag">
                        <el-table-column prop="key_name" label="字段" width="200"></el-table-column>
                        <el-table-column prop="value" label="内容"></el-table-column>
                    </el-table>
                </el-dialog>

            </div>
        </div>
    </div>
</template>
<script>
export default {
    data() {
        return {
            adaptivePageHeight: window.innerHeight - 300,
            search_val: "",
            search_val_copy: "",
            tableData: [],
            list_data: [],
            dialogVisible: false,
            dialog_data: [],
            dialog_title_name: "",
            flag: false,
            page:1,
            page_size:50,
            changdu:0,
            loading:false
        };
    },
    computed: {
        search_modul() {
            return this.search_val;
        }
    },
    watch: {
        search_modul(val) {
            this.search_val_copy = val; //预先存储一个完整搜索框输入值，用于后面字符串切割使用
        }
    },
    mounted() {
        this.get_project_list();
    },
    methods: {
        querySearch(string, cb) {
            var regNull = /\s+/g; //空格
            if (string !== "") {
                // console.log(string,'string')
                var results = this.querySearchFilter(string, this.list_data);
                cb(results); // 调用 callback 返回建议列表的数据
            }
        },
        querySearchFilter(String, filter_data) {
            var regNull = /\s+/g; //空格
            //判断输入框中是否输入了空格，不等于-1代表有空格
            let queryString = ""; //声明一个传入搜索方法的变量
            if (String.search(regNull) !== -1) {
                //存在空格，存在空格就要切割最后一个空格后面的字符，传入搜索函数继续搜索新字段
                // console.log('空格输入进来了')
                var reg_null = /\s$/ //最后一个空格出现的
                let search_string_flag = reg_null.test(String)//空格字符最后出现的位置
                if (search_string_flag != true) {//判断最后一个是不是空格字符，如果不是则切割数组，取最后一个元素作为搜索字符。
                    queryString = String.trim()
                        .split(regNull)
                        .pop()
                }else{//否则清空数据，空格字符不提示搜索内容
                    queryString = null
                    filter_data = []
                }
            } else {  //无空格
                queryString = String;
            }
            // console.log(queryString,'queryString----------')
            return queryString ? filter_data.filter(this.createFilter(queryString)) : filter_data;
        },
        createFilter(queryString) {
            // console.log(queryString,'querying')
            return restaurant => {
                return restaurant.value.search(RegExp(queryString, "i")) !== -1;
            };
        },
        handleSelect(item) {
            let substring_stop_index =
                this.search_val_copy.lastIndexOf(" ") + 1;
            this.search_val =
                this.search_val_copy.substring(0, substring_stop_index) +
                item.value; //拼接搜索框字符串
        },
        get_project_list() {
            this.$axios
                .get(
                    this.Ip +
                        "/GetKeyListByUser/" +
                        sessionStorage.getItem("Uall")
                )
                .then(res => {
                    // console.log(res.data.content,'-----------')
                    if (res.data.result == "OK") {
                        this.list_data = res.data.content.map(item => {
                            return {
                                value: item
                            };
                        });
                        this.list_data.push({
                            value: "number:"
                        });
                    } else {
                    }
                    // console.log(this.list_data,'-----------===========')
                });
        },

        search_click(val) {
            if (!val) {
                return this.$alert("搜索内容不能为空");
            }
            let value = {
                value: this.search_val,
                user: sessionStorage.getItem("Uall"),
                size: this.page_size,
                page: this.page
            };
            this.search_fun(value)
        },
        search_fun(value){
            // console.log(value, "=============value");
            this.loading = true
            this.$axios.post(this.Ip + "/BugSearch", value).then(res => {
                // console.log(res.data);
                if (res.data.result == "OK") {
                    this.tableData = res.data.content.hits;
                    this.changdu = res.data.content.hits.total
                    this.page = value.page
                    // console.log(this.page,'===========page')
                    this.loading = false
                } else {
                    this.changdu = 0
                    this.loading = false
                }
            });
        },
        listPageChange(page_num){
            // console.log(page_num,'page_num')
            let value = {
                value: this.search_val,
                user: sessionStorage.getItem("Uall"),
                size: this.page_size,
                page: page_num
            };
            this.search_fun(value)
        },
        handleSizeChange(page_size) {
            let value = {
                value: this.search_val,
                user: sessionStorage.getItem("Uall"),
                size: page_size,
                page: this.page
            };
            this.search_fun(value)
        },
        clear_click() {},
        view_fun(number_val) {
            this.dialogVisible = true;
            this.dialog_title_name = number_val;
            let data = {
                value: "number:" + number_val,
                user: sessionStorage.getItem("Uall")
            };
            this.$axios.post(this.Ip + "/AnyPlaceInfo", data).then(res => {
                // console.log(res,'aaaaaaaa')
                let res_data = res.data.content;
                this.dialog_data = [];
                for (let i = 0; i < res_data.key_list.length; i++) {
                    this.dialog_data.push({
                        key_name: res_data.key_list[i],
                        value: res_data.value_list[i]
                    });
                }
                
            });
        },
        
    }
};
</script>

<style scoped>
.dialog-left {
    float: left;
    width: 200px;
    font-size: 12px;
}

.dialog-left-ul li {
    padding: 0 0 0 5px;
    border-left: 1px solid #ebeef5;
    border-top: 1px solid #ebeef5;
    border-bottom: 0px solid #ebeef5;
    /* height: 25px; */
    line-height: 25px;
}

.dialog-right-ul li {
    padding: 0 0 0 5px;
    border-left: 1px solid #ebeef5;
    border-right: 1px solid #ebeef5;
    border-top: 1px solid #ebeef5;
    border-bottom: 0px solid #ebeef5;
    /* height: 50px; */
    line-height: 25px;
    /* white-space:nowrap; */
    /* text-overflow:ellipsis;
    overflow:hidden; */

    word-wrap: break-word;
    word-break: break-all;
    overflow: scroll;
}

.dialog-right {
    display: inline-block;
    width: 80%;
    font-size: 12px;
}

ul,
li {
    list-style: none;
}

.go-doc-text {
    padding-right: 10px;
}

.go-doc-text:hover {
    color: #42b983;
    cursor: pointer;
}

.Append-basic-temlate {
    margin: 0 auto;
    width: 100%;
    height: 100%;
    /*overflow-y: scroll;*/
}

.Append-basic-temlate-countent {
    max-width: 300px;
    width: 15%;
    height: 100%;
    padding: 20px;
    float: left;
}

.content-box {
    float: left;
    width: 85%;
    padding-left: 1%;
    height: 98%;
    color: #606266;
    background-color: #fff;
    border-left: 2px solid rgba(216, 231, 223, 0.5);
    overflow: scroll;
    overflow-x: hidden;
}

.mid {
    position: relative;
    width: 101%;
    height: 100%;
    float: left;
    padding-right: 20px;
    background-color: #fff;
    border-right: 2px solid rgba(216, 231, 223, 0.5);
    overflow: scroll;
    overflow-x: hidden;
}

.mid-top {
    position: absolute;
    top: 0;
    bottom: 55px;
    width: 100%;
    padding-right: 20px;
    /* overflow-y: scroll; */
}

.footer {
    position: absolute;
    bottom: 20px;
    right: 20px;
}

.block-title {
    margin: 20px 0 0px 0;
}

h2 {
    font-size: 22px;
    font-weight: bolder;
    background-color: #6bcca0;
    color: white;
    padding-left: 10px;
    line-height: 25px;
}

.label-box {
    width: 100%;
    overflow: hidden;
}

.label-box-text {
    margin-top: 20px;
    margin-bottom: 20px;
    font-size: 14px;
}

.label-box-text span {
    cursor: pointer;
}

.upload-demo {
    margin-top: 10px;
}

.upload-demo-box {
    width: 260px;
    height: 100px;
    /*display: inline-block;*/
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
    margin-top: 20px;
}

.active {
    background: #fff;
}

.up-data-btn {
    width: 330px;
    height: 320px;
    /* margin-left: 20px; */
    /*margin-top:20px;*/
    display: block;
    background: #fff;
    outline: none;
    border: 1px dashed #ccc;
    color: #ccc;
    font-size: 15px;
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
    margin-top: 10px;
    padding-right: 20px;
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
}

.dialog_img {
    display: block;
    margin: 0 auto;
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

.dialogimg {
    display: block;
    margin: 0 auto;
}

.textarea-name {
    font-size: 12px;
    font-family: "\5FAE\8F6F\96C5\9ED1";
}

@media screen and (max-width: 1366px) {
    .up-data-btn {
        width: 230px;
        height: 240px;
        /* margin-left: 20px; */
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
        margin-top: 10px;
    }

    .img-box {
        width: 250px;
        height: 250px;
        margin-top: 10px;
        margin-right: 20px;
        position: relative;
        display: inline-block;
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

    .content-box {
        float: left;
        width: 80%;
        height: 100%;
        overflow-y: scroll;
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

    .Append-basic-temlate-countent {
        width: 180px;
        height: 100%;
        float: left;
    }

    .content-box {
        float: left;
        width: 820px;
        height: 100%;
        overflow-y: scroll;
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

    .upload-demo {
        margin-top: 0;
    }

    .img-box {
        width: 180px;
        height: 170px;
        margin-top: 10px;
        margin-right: 10px;
        position: relative;
        display: inline-block;
    }
}
</style>
