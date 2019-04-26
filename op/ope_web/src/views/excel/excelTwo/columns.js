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
  {
    data: 'active_chapter',
    readOnly: true,
    renderer: firstColumnCellStyle
  },
  {
    data: 'active_sub_chapter',
    readOnly: true,
    renderer: customCellStyle
  },
  { //NO.
    data: 'active_no',
    readOnly: true,
    renderer: customCellStyle
  },
  { //Button Name 1
    data: 'active_state_no',
    renderer: PartsNameCellStyle
  },
  { //Button Name 2
    data: 'active_btn_name',
  },
  { //Formula
    data: 'active_formula',
    type: 'text'
  },
  { //Condition1
    data: 'active_condition_branch',
    type: 'text'
  },
  { //Condition2
    data: 'active_condition_phrase',
    type: "autocomplete",
    source: [],
    strict: false,
    filter: false,
    trimDropdown: false
  },
  { //Display in Such Condition
    data: 'active_action',
    type: "autocomplete",
    source: [],
    strict: false,
    filter: false,
    trimDropdown: false
  },
  { //Property Type
    data: 'active_property_type',
    type: "autocomplete",
    source: [],
    strict: false,
    filter: false,
    trimDropdown: false
  },
  { //DuringDriving
    data: 'active_during_driving',
    type: 'text'
  },
  { //Remark
    data: 'active_remark',
    type: 'text'
  },
  { //空白列
    data: 'thirteen',
    readOnly: true,
    readOnly: true
  },
  { //UUID
    data: 'active_uuid',
    type: 'text'
  },
  { //Parts Type
    data: 'active_parts_type',
    type: 'text'
  },
  { //Property
    data: 'active_property',
    type: 'text'
  },
  { //Add Display Condition In View Model
    data: 'active_action_model',
    type: 'text'
  },
  { //Display Condition In View Model1
    data: 'active_condition_model_branch',
    type: 'text'
  },
  { //Display Condition In View Model2
    data: 'active_condition_code',
    type: 'text'
  },
  {
    data: 'twenty',
    type: 'text'
  },
  { //DefaultValue
    data: 'active_default_value',
    type: 'text',
  }
]

export function afterGetColHeader(col, TH) {
  if(TH.parentNode !== null) {
    var TR = TH.parentNode;
    var THEAD = TR.parentNode;
    var headerLevel = (-1) * THEAD.childNodes.length + Array.prototype.indexOf.call(THEAD.childNodes, TR);
    const textAlign = 'text-align'
    TH.style[textAlign] = 'left'
    if (headerLevel === -1 ) {
        if (col < 0) {
            TH.style.backgroundColor = '#f0f0f0'
        }else if(col < 1) {
            TH.style.backgroundColor = 'rgb(201, 255, 255)'
        }else if(col < 12) {
            TH.style.backgroundColor = 'rgb(255, 205, 156)'
        } else if(col < 13) {
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
  ['2', {label: 'Soft Button Action', colspan: 11}, '' ,{label: '', colspan: 8}],
  ['2', '1', {label: 'Normal', colspan: 10}, '' ,{label: '', colspan: 8}],
  ['2', '1', 'NO.', {label: 'Button Name', colspan: 2}, 'Formula', {label: 'Condition', colspan: 2}, 'Display in Such Condition', 'Property Type', 'DuringDriving', 'Remark',
    '   ', 'UUID', 'Parts Type', 'Property', 'Add Display Condition In View Model', {label: 'DisplayCondition In View Model', colspan: 2}, '   ', 'DefaultValue']
]

// const datumWidth = 50
      // const cellWidthArr = [1, 1, 1, 1, 8, 3, 1, 6, 8, 6, 3, 4, 2, 1,3,3,5,1,4,2,2]
      // const colWidth = []
      // for(let item of cellWidthArr) {
      //   colWidth.push(datumWidth * item)
      // }