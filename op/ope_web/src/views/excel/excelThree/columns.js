import Handsontable from 'handsontable-pro'
function firstColumnCellStyle(instance, td, row, col, prop, value, cellProperties) {
  td.innerHTML = value
  td.style.background = 'rgb(201, 255, 255)'
  return td
}
function customCellStyle(instance, td, row, col, prop, value, cellProperties) {
  td.innerHTML = value
  td.style.background = 'rgb(255, 205, 156)'
  return td
}
function PartsNameCellStyle(instance, td, row, col, prop, value, cellProperties) {
  td.innerHTML = value
  td.style.background = 'rgb(172, 255, 196)'
  return td
}

export const columns = [
  { // 3
    data: 'action_chapter',
    readOnly: true,
    renderer: firstColumnCellStyle
  },
  { // 1
    data: 'action_sub_chapter',
    readOnly: true,
    renderer: customCellStyle
  },
  { //NO.
    data: 'action_no',
    readOnly: true,
    renderer: customCellStyle
  },
  { //Button Name1
    data: 'action_state_no',
    type: 'text',
    renderer: PartsNameCellStyle
  },
  { //Button Name2
    data: 'action_btn_name',
    type: 'text'
  },
  { //Ope Type
    data: 'action_ope_type',
    type: "autocomplete",
    source: [],
    strict: false,
    filter: false,
    trimDropdown: false
  },
  { // Formula
    data: 'action_formula',
    type: 'text'
  },
  { //Condition of Action1
    data: 'active_condition_branch',
    type: 'text'
  },
  { //Condition of Action2
    data: 'active_condition_phrase',
    type: "autocomplete",
    source: [],
    strict: false,
    filter: false,
    trimDropdown: false
  },
  { //Action in Such Condition
    data: 'action_action',
    type: "autocomplete",
    source: [],
    strict: false,
    filter: false,
    trimDropdown: false
  },
  { //Transition
    data: 'action_trans',
    type: 'text',
    readOnly: true
  },
  { //Sound
    data: 'action_sound',
    type: 'text'
  },
  { //空白列
    data: 'twelve',
    type: 'text'
  },
  { //Remark
    data: 'action_remark',
    type: 'text'
  },
  { // 空白列
    data: 'fourteen',
    type: 'text',
    readOnly: true
  },
  { //UUID
    data: 'action_uuid',
    type: 'text'
  },
  { //Parts Type
    data: 'action_parts_type',
    type: 'text'
  },
  { //Event
    data: 'action_event',
    type: 'text'
  },
  { // View Model1
    data: 'active_condition_model_branch',
    type: 'text'
  },
  { //View Mode2
    data: 'active_condition_code',
    type: 'text'
  },
  { // Func of Model
    data: 'action_action_model',
    type: 'text'
  },
  { //Observer
    data: 'action_observer',
    type: 'text'
  },
  { //Reply
    data: 'action_reply',
    type: 'text'
  },
  { //TransType
    data: 'action_trans_type',
    type: 'text',
    readOnly: true
  },
  { // TransID
    data: 'action_trans_id',
    type: 'text',
    readOnly: true
  }
]

export function afterGetColHeader(col, TH) {
  if(TH.parentNode !== null) {
    let TR = TH.parentNode;
    let THEAD = TR.parentNode;
    let headerLevel = (-1) * THEAD.childNodes.length + Array.prototype.indexOf.call(THEAD.childNodes, TR);
    const textAlign = 'text-align'
    TH.style[textAlign] = 'left'
    if (headerLevel === -1 ) {
      if (col < 0) {
          TH.style.backgroundColor = '#f0f0f0'
      }else if(col < 1) {
          TH.style.backgroundColor = 'rgb(201, 255, 255)'
      }else if(col < 14) {
          TH.style.backgroundColor = 'rgb(255, 205, 156)'
      } else if(col < 15) {
          TH.style.backgroundColor = 'rgb(255, 255, 255)'
      } else {
          TH.style.backgroundColor = 'rgb(255, 192, 0)'
      }
    } else if(headerLevel === -2){
      if (col < 0) {
          TH.style.backgroundColor = '#f0f0f0'
      }else if(col < 1) {
          TH.style.backgroundColor = 'rgb(201, 255, 255)'
      }else if(col < 11) {
          TH.style.backgroundColor = 'rgb(255, 205, 156)'
      } else {
          TH.style.backgroundColor = 'rgb(255, 255, 255)'
      }
    } else {
      if (col < 0) {
          TH.style.backgroundColor = '#f0f0f0'
      }else if(col < 11) {
          TH.style.backgroundColor = 'rgb(201, 255, 255)'
      } else {
          TH.style.backgroundColor = 'rgb(255, 255, 255)'
      }
    }
  }
}
export function afterGetRowHeader(row, TH) {
  TH.style.backgroundColor = '#f0f0f0'
}
export const nestedHeaders = [
  ['3', {label: 'Soft Button Action', colspan: 13}, '' ,{label: '', colspan: 10}],
  ['3', '1', {label: 'Normal', colspan: 12}, '' ,{label: '', colspan: 10}],
  ['3', '1', 'NO.', {label: 'Button Name', colspan: 2}, 'Ope Type', 'Formula', {label: 'Condition of Action', colspan: 2}, 'Action in Such Condition', 'Transition', 'Sound', '', 'Remark',
    '   ', 'UUID', 'Parts Type', 'Event', {label: 'View Model', colspan: 2}, 'Func of Model', 'Observer', 'Reply', 'TransType', 'TransID']
]

// const datumWidth = 50
// const cellWidthArr = [1, 1, 1, 1, 6, 2, 3, 1, 6, 8, 3, 3, 3, 4, 2, 1, 3, 3, 1, 4, 2, 3, 2, 2, 2]
// const colWidth = []
// for(let item of cellWidthArr) {
//   colWidth.push(datumWidth * item)
// }