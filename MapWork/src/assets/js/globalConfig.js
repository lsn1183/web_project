export default {
  install(Vue, options) {
    // 全局变量
    Vue.prototype.globalData = {
      userName: "",
      passWord: "",
      adaptivePageHeight: window.innerHeight - 200,
      Roles: {
        "Admin": "",
        "Test_PMO": "",
        "Test_PL": "",
        "Test_GL": "",
        "DL": "",
        "SGL": "",
        "GL": "",
        "Developer": ""
      },
      // 提示语,状态+页面+具体模块
      hint: {
        "success": "成功",
        "fail": "失败",
        "warning": "警告",
        "warning_editForm_uploadFile": "警告,此操作上传文件需清空url和文本框。",
        "warning_editForm_tag": "警告,有必填tag没选。",
        "correctContent": "内容正确",
        "incorrectContent": "内容不正确",
        "jumpSuccess": "跳转成功",
        "jumpFail": "跳转失败",
        "quit": "页面信息已发生变更，离开会使信息丢失, 是否继续?",
        "delete": "此操作将永久删除该文件或内容, 是否继续?",
        "jump": "页面信息已发生变更, 是否跳转?"
      }
    };
    // 全局函数:
    // 用户权限请求
    Vue.prototype.getUserPermission = function (id) {
      let user_id = Number(id)
      let userPermissionArr = []
      let accessToken = window.sessionStorage.getItem("accessToken")
      window.sessionStorage.removeItem('UserPermission')
      this.$axios.get(this.Ip + "/UserPermission/" + user_id).then(res => {
         
        if (res.data.result == "OK") {
          userPermissionArr = res.data.content
          window.sessionStorage.setItem("UserPermission", JSON.stringify(userPermissionArr))
        } else {
        //   this.$message({
        //     type: "error",
        //     message: "您暂无角色，部分操作受限！"
        //   })
        }
      })
    };
    // 权限调用：传入权限名称
    Vue.prototype.userPurviewManage = function (manageName) {
      let userPermissionData = JSON.parse(window.sessionStorage.getItem("UserPermission"))
      let manageNameArr = []
      if (manageName) {
        manageNameArr.push(manageName)
        if (userPermissionData && userPermissionData.length != 0) {
          for (const name of manageNameArr) {
            for (const iterator of userPermissionData) {
              if (iterator == name) {
                return true
              }
            }
            return false
          }
        } else {
        //   this.$message({
        //     type: "warning",
        //     message: "您暂无任何操作权限！"
        //   })
        }
      } else {
        this.$message({
          type: "error",
          message: "调用该方法，需传入权限名字"
        })
      }
      },
    Vue.prototype.windowOnresize = function () {
      this.globalData.adaptivePageHeight = window.innerHeight - 200
      const that = this
      window.onresize = () => {
        return (() => {
          that.globalData.adaptivePageHeight = window.innerHeight - 200
        })()
      }
      },
      Vue.prototype.beforeUpload=function(file){
        let type=file.type
        // 判断上传文件格式是否为图片
        if (type.search("image") != -1) {
            this.dialogTableVisible = true;
            return true
        } else {
            this.$message({
                type:"error",
                message:"上传的图片格式不正确"
            })
            return false
        }
    };
    // Catus服务器权限，manageName:传入权限名称
    Vue.prototype.getCatusPurviewManage = function (userPermissionData,manageName) {
        if (manageName) {
            if (userPermissionData.length != 0) {
                    for (const iterator of userPermissionData) {
                        if (iterator == manageName) {
                            return true
                        }
                    }
                    return false
            } else {
                this.$message({
                    type: "warning",
                    message: "您没有权限操作"
                })
            }
        } else {
            this.$message({
            type: "error",
            message: "调用该方法，需传入权限名字"
            })
        }
    }
    
  }
}
