<template>
<div class="drbfm-table">
    <el-table :data="drbfm_data" style="width: 100%" :span-method="objectSpanMethod" :row-class-name="table_row_class_name">
        <el-table-column prop="change_content" label="部品名 ／変更点 ／理由"  align='left' header-align='center'>
            <template slot-scope="scope">
                <span v-html="scope.row.change_content">
                </span>
            </template>
        </el-table-column>
        <el-table-column prop="model_name" label="機　　能" align='center'></el-table-column>

        <el-table-column label="変更に関わる心配点（故障ﾓｰﾄﾞ）" align='center'>
            <el-table-column prop="failuremode" label="変更がもたらす 機能の喪失、 商品性の欠如" align='center'>
            </el-table-column>
        </el-table-column>
    </el-table>
</div>    
</template>
<script>
export default {
    name: 'DRBFM_preview',
    props: ['prop_drbfm_data'],
    data() {
        return {
            drbfm_data: [],
            column_row_offset: {
                change_content: [],
                model_name: [],
                failuremode: [],
            },
            now_col_row_num: {},
            now_col_offset: {}
        }
    },
    methods: {
        transfer_data_structure() {
            const data = JSON.parse(JSON.stringify(this.prop_drbfm_data))
            let transfer_data = []

            data.forEach((item, index) => {
                this.column_row_offset.change_content.push(item.row_num)
                for (let model_item of item.model_list) {
                    this.column_row_offset.model_name.push(model_item.failuremode_list.length)
                    for (let failure_mode of model_item.failuremode_list) {
                        this.column_row_offset.failuremode.push(1)
                        transfer_data.push({
                            change_content: item.change_content.replace(/\n/g, "<br/>"),
                            model_name: model_item.model_name,
                            failuremode: failure_mode,
                            row_index: index
                        })
                    }
                }
            })
            this.drbfm_data = transfer_data
        },
        table_row_class_name({ row, rowIndex }) {
            if (row.row_index %2 === 0) {
                return ''
            } else{
                return 'success-row'
            }
        },
        objectSpanMethod({ row, column, rowIndex, columnIndex }) {
            if (!this.now_col_row_num[column.property]) {
                this.now_col_row_num[column.property] = Object.assign([], this.column_row_offset[column.property])
                let a = this.now_col_row_num[column.property].shift()
                this.now_col_offset[column.property] = a
                return {
                    rowspan: a,
                    colspan: 1
                }
            } else if (rowIndex >= this.now_col_offset[column.property]) {
                let a = this.now_col_row_num[column.property].shift()
                this.now_col_offset[column.property] += a
                return {
                    rowspan: a,
                    colspan: 1
                }
            } else {
                return {
                    rowspan: 0,
                    colspan: 0
                }
            }
        }
    },
    created() {
        this.transfer_data_structure()
    },
    mounted() {
        
    }
}
</script>

<style>
</style>
