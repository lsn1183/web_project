import Handsontable from 'handsontable-pro'
function customCellStyle(instance, td, row, col, prop, value, cellProperties) {
  Handsontable.dom.empty(td);
  td.style.background = 'rgb(255, 205, 156)'
  td.innerText  = value
  return td
}
function PartsNameCellStyle(instance, td, row, col, prop, value, cellProperties) {
  Handsontable.dom.empty(td);
  td.innerText  = value
  td.style.background = 'rgb(172, 255, 196)'
  return td
}
function firstColumnCellStyle(instance, td, row, col, prop, value, cellProperties) {
  Handsontable.dom.empty(td);
  td.innerText  = value
  td.style.background = 'rgb(201, 255, 255)'
  return td
}

function imgCellRenderer(instance, td, row, col, prop, value, cellProperties) {
  const escaped = Handsontable.helper.stringify(value);
  
  const rowData = instance.getSourceDataAtRow(row)
  if(rowData['display_parts_type'] == 'ImageBase') {
    let img = document.createElement('IMG');
    img.style.width = '84px'
    img.style.height = '48px'
    img.src = `http://192.168.25.20:8888/${value}` ;

    Handsontable.dom.addEvent(img, 'mousedown', function(event) {
      event.preventDefault();
    });
    Handsontable.dom.empty(td);
    td.appendChild(img);
  } else {
    Handsontable.renderers.TextRenderer.apply(this, arguments);
  }

  return td;
}



export const columns = [
  {
    data: 'display_chapter',
    readOnly: true,
    renderer: firstColumnCellStyle
  },
  {
    data: 'display_sub_chapter',
    readOnly: true,
    renderer: customCellStyle
  },
  {
    data: 'parts_number',
    readOnly: true,
    renderer: customCellStyle
  },
  {
    data: 'display_state_no',
    type: 'text',
    renderer: PartsNameCellStyle,
  },
  {
    data: 'parts_name',
    type: 'text',
    // validator: ipValidatorRegexp,
    allowInvalid: true
  },
  {
    data: 'display_content',
    type: 'text',
    renderer: imgCellRenderer,
    readOnly: true
  },
  {
    data: 'display_formula',
    type: 'text'
  },
  {
    data: 'display_condition_branch',
    type: 'text'
  },
  {
    data: 'display_condition_phrase',
    type: "autocomplete",
    source: [],
    strict: false,
    filter: false,
    trimDropdown: false
  },

  {
    data: 'display_action',
    type: "autocomplete",
    source: [],
    strict: false,
    filter: false,
    trimDropdown: false
  },
  {
    data: 'display_property_type',
    type: "autocomplete",
    source: [],
    strict: false,
    filter: false,
    trimDropdown: false
  },
  {
    data: 'data_range',
    type: 'text'
  },
  {
    data: 'display_remark',
    type: 'text'
  },
  {
    data: 'whiteColumn',
    type: 'text',
    readOnly: true
  },
  {
    data: 'display_uuid',
    type: 'text'
  },
  {
    data: 'display_parts_type',
    type: 'text'
  },
  {
    data: 'display_property',
    type: 'text'
  },
  {
    data: 'display_action_model',
    type: 'text'
  },
  {
    data: 'display_condition_model_branch',
    type: 'text'
  },
  {
    data: 'display_condition_code',
    type: 'text'
  },
  {
    data: 'string_id',
    type: 'text',
    readOnly: true
  },
  {
    data: 'display_default_value',
    type: 'text'
  }
]

export const nestedHeaders = [
  ['1', '1', 'NO.', {label: 'Parts Name', colspan: 2}, 'Display Content', 'Formula', {label: 'Display Condition', colspan: 2}, 'Display in Such Condition', 'Property Type', 'Data Range', 'Remark',
    '   ', 'UUID', 'Parts Type', 'Property', 'Add Display Condition In View Model', {label: 'DisplayCondition In View Model', colspan: 2}, 'String Id', 'DefaultValue']
]

export function afterGetColHeader(col, TH) {
  const textAlign = 'text-align'
  TH.style[textAlign] = 'left'
  if (col < 0) {
      TH.style.backgroundColor = '#f0f0f0'
  } else if (col < 1) {
      TH.style.backgroundColor = 'rgb(201, 255, 255)'
  }else if (col < 13) {
    TH.style.backgroundColor = 'rgb(255, 205, 156)'
  } else if (col < 14) {
    TH.style.backgroundColor = 'rgb(255, 255, 255)'
  } else {
    TH.style.backgroundColor = 'rgb(255, 192, 0)'
  }
}
export function afterGetRowHeader(row, TH) {
  TH.style.backgroundColor = '#f0f0f0'
}

// const datumWidth = 50
// const cellWidthArr = [1, 1, 1, 1, 4, 6, 3, 1, 6, 6, 6, 3, 4, 2, 1,3,3,5,1,4,2,2]
// const colWidth = []
// for(let item of cellWidthArr) {
//   colWidth.push(datumWidth * item)
// }