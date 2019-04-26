
var setting = {
    width: '100%',
    height: document.body.scrollHeight - 80,
    // stretchH: "all", //根据宽度横向扩展，last:只扩展最后一列，none：默认不扩展,自动展开宽度100%，
    colHeaders: true, //显示表头
    rowHeaders: false, //显示序号
    comments: true, //添加注释
    manualColumnResize: true, //手动更改列距
    data: [], //表格总数据
    columns: [], //表格头部prop配置
    colHeaders: null, //自定义列表头or 布尔值
    nestedHeaders: undefined,
    contextMenu: {}, //右键
    language: "zh-CN", // 右键显示菜单语言类型
    fillHandle: true, //选中拖拽复制 possible values: true, false, "horizontal", "vertical"
    fixedRowsTop: 0, //固定上边列数
    customBorders: [], //添加边框
    // hiddenColumns: {
    //     indicators: true
    // },
    afterOnCellMouseDown: () => {

    },
    afterChange: (changes, source) => { },
    colWidths: [],
    manualRowResize: true, //控制行的大小
    // rowHeights: [30],
    fixedColumnsLeft: 1, //固定列
    // observeChanges: true,
    // observeDOMVisibility: true,
    cells: (row, col) => {
    },
    fillHandle: {
        //选中拖拽复制 possible values: true, false, "horizontal", "vertical"
        direction: "vertical",
        autoInsertRow: false
    },
    dropdownMenu: false,
    filters: false,
    asyncUpdates: true,
    autoWrapRow: true, //自动换行
    autoRowSize: {
        syncLimit: 500,
        allowSampleDuplicates: true
    },
    autoColumnSize: {
        syncLimit: 500,
        allowSampleDuplicates: true
    },
}
export default setting