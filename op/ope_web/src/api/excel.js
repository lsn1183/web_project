import request from '@/api/request'

export function getExcelData(gid, itemId) {
  return request({
    url: `/Chapter/${gid}/${itemId}`,
    method: 'GET'
  })
}

export function saveExcelData(type, data) {
  return request({
    url: `/Chapter/update/${type}`,
    method: 'POST',
    data
  })
}

export function getOpeInfo(gid) {
  return request({
    url: `/Ope/${gid}`,
    method: 'GET'
  })
}

export function getSelectedData(type, projId) {
  return request({
    url: `/Ope/${type}/${projId}`,
    method: 'GET'
  })
}