import handsontable from 'handsontable-pro'
//工数不同状态表格样式
function noneCellRenderer(instance, td, row, col, prop, value, cellProperties) {
    handsontable.renderers.TextRenderer.apply(this, arguments);
}

function checkingCellRenderer(instance, td, row, col, prop, value, cellProperties) {
    handsontable.renderers.TextRenderer.apply(this, arguments);
    td.style.background = '#85ce61';
    td.style.color = '#fff'
}

function issueCellRenderer(instance, td, row, col, prop, value, cellProperties) {
    handsontable.renderers.TextRenderer.apply(this, arguments);
    td.style.background = '#d73a4a';
    td.style.color = '#fff'
}

function acceptCellRenderer(instance, td, row, col, prop, value, cellProperties) {
    handsontable.renderers.TextRenderer.apply(this, arguments);
    td.style.background = '#7057ff';
    td.style.color = '#fff'
}

handsontable.renderers.registerRenderer('noneCellRenderer', noneCellRenderer)
handsontable.renderers.registerRenderer('checkingCellRenderer', checkingCellRenderer)
handsontable.renderers.registerRenderer('issueCellRenderer', issueCellRenderer)
handsontable.renderers.registerRenderer('acceptCellRenderer', acceptCellRenderer)

//自定义表格编辑样式
// export class CustomEditor extends Handsontable.editors.TextEditor {
//     constructor(props) {
//         super(props);
//     }

//     createElements() {
//         super.createElements();

//         this.TEXTAREA = document.createElement('input');
//         this.TEXTAREA.className = 'handsontableInput';
//         Handsontable.dom.empty(this.TEXTAREA_PARENT);
//         this.TEXTAREA_PARENT.appendChild(this.TEXTAREA);
//     }
// }

export function cells(row, col) {
    let cellProperties = {}
    let data = this.instance.getSourceData()
    if(data.length == 0) {
        return cellProperties
    }
    const colProp = this.instance.colToProp(col)
    
    if(typeof colProp == 'number') { //有bug, 渲染在添加nestedHeaders之前
        return cellProperties
    }
    const splitArr = colProp.split('.')
    const splitArrLen = splitArr.length - 1
    if (splitArr[splitArrLen] == 'days') {
        let status = ''
        let value = data[row]
        for (let i = 0; i < splitArrLen; i++) {
            let key = splitArr[i]
            value = value[key]
        }
        switch (value.issue_status) {
            case 'none': // 从来没有被指摘
                cellProperties.renderer = 'noneCellRenderer'
                break

            case 'issue': //指摘
                cellProperties.renderer = 'issueCellRenderer'
                break

            case 'checking': //指摘回复完了，等待确认
                cellProperties.renderer = 'checkingCellRenderer'
                break

            case 'accept': //曾经被指摘
                cellProperties.renderer = 'acceptCellRenderer'
                break

            default:
                cellProperties.renderer = 'noneCellRenderer'
                break
        }
    }
    return cellProperties
}
var handleHotBeforeOnCellMouseDown = function(event, coords, element) {
    if (coords.row < 0) { //禁止表头事件
        event.stopImmediatePropagation();
    }
};
handsontable.hooks.add('beforeOnCellMouseDown',
    handleHotBeforeOnCellMouseDown);

export let Handsontable = handsontable