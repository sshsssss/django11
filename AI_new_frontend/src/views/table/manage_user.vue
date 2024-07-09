<template>
    <div class="app-container">
      <el-button @click="AddUserDialogOpen()" style="margin: 20px;" type="primary"> 新建用户 </el-button>
  
      <el-table
        v-loading="listLoading"
        :data="course_list"
        element-loading-text="Loading"
        border
        fit
        highlight-current-row
      >
        <el-table-column align="center" label="用户ID" width="80">
          <template slot-scope="scope">
            {{ scope.row.user_id}}
          </template>
        </el-table-column>
        <el-table-column label="用户名">
          <template slot-scope="scope">
            {{ scope.row.username }}
          </template>
        </el-table-column>
        <el-table-column label="密码">
          <template slot-scope="scope">
            {{ scope.row.password }}
          </template>
        </el-table-column>
        <el-table-column label="用户真名">
          <template slot-scope="scope">
            {{ scope.row.realname }}
          </template>
        </el-table-column>
        <el-table-column label="邮箱">
          <template slot-scope="scope">
            {{ scope.row.email}}
          </template>
        </el-table-column>
        <el-table-column label="手机号">
          <template slot-scope="scope">
            {{ scope.row.phone }}
          </template>
        </el-table-column>
        <el-table-column label="身份">
          <template slot-scope="scope">
            {{ scope.row.status}}
          </template>
        </el-table-column>
        <el-table-column align="center" label="操作" width="200">
          <template slot-scope="scope">
            <span>
              <el-button type="primary" @click="AlterDialogOpen(scope.row)"> 修改 </el-button>
              <el-button type="primary" @click="handleDelete(scope.row.user_id)"> 删除 </el-button>
            </span>
          </template>
        </el-table-column>
      </el-table>

      <el-dialog title="添加用户信息" :visible.sync="userDialogVisible" width="40%" center>
        <el-form ref="dataForm" :model="user_form" label-position="left" label-width="100px" style="width: 400px; margin-left: 50px">
            <el-form-item label="用户名" prop="com">
                <el-input v-model="user_form.username" clearable style="width: 300px; margin-left: 20px"/>
            </el-form-item>
            <el-form-item label="密码" prop="com">
                <el-input v-model="user_form.password" clearable style="width: 300px; margin-left: 20px"/>
            </el-form-item>
            <el-form-item label="用户真名" prop="com">
                <el-input v-model="user_form.realname" clearable style="width: 300px; margin-left: 20px"/>
            </el-form-item>
            <el-form-item label="邮箱" prop="com">
                <el-input v-model="user_form.email" clearable style="width: 300px; margin-left: 20px"/>
            </el-form-item>
            <el-form-item label="手机号" prop="com">
                <el-input v-model="user_form.phone" clearable style="width: 300px; margin-left: 20px"/>
            </el-form-item>
            <el-form-item label="用户身份">
                <el-radio-group v-model="user_form.status">
                    <el-radio :label="'teacher'">教师</el-radio>
                    <el-radio :label="'student'">学生</el-radio>
                </el-radio-group>
            </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
            <el-button @click="userDialogVisible = false"> 取消 </el-button>
            <el-button type="primary" @click="handleCreate()"> 提交 </el-button>
        </div>
        </el-dialog>

        <el-dialog title="修改用户信息" :visible.sync="alterDialogVisible" width="40%" center>
            <el-form ref="dataForm" :model="user_form" label-position="left" label-width="100px" style="width: 400px; margin-left: 50px">
                <el-form-item label="用户名" prop="com">
                    <el-input v-model="user_form.username" clearable style="width: 300px; margin-left: 20px"/>
                </el-form-item>
                <el-form-item label="密码" prop="com">
                    <el-input v-model="user_form.password" clearable style="width: 300px; margin-left: 20px"/>
                </el-form-item>
                <el-form-item label="用户真名" prop="com">
                    <el-input v-model="user_form.realname" clearable style="width: 300px; margin-left: 20px"/>
                </el-form-item>
                <el-form-item label="邮箱" prop="com">
                    <el-input v-model="user_form.email" clearable style="width: 300px; margin-left: 20px"/>
                </el-form-item>
                <el-form-item label="手机号" prop="com">
                    <el-input v-model="user_form.phone" clearable style="width: 300px; margin-left: 20px"/>
                </el-form-item>
                <el-form-item label="用户身份">
                    <el-radio-group v-model="user_form.status">
                        <el-radio :label="'teacher'">教师</el-radio>
                        <el-radio :label="'student'">学生</el-radio>
                    </el-radio-group>
                </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click="userDialogVisible = false"> 取消 </el-button>
                <el-button type="primary" @click="handleAlter()"> 提交 </el-button>
            </div>
        </el-dialog>
    </div>
  </template>
  
  <script>
  import { getList } from '@/api/table'
  import Axios from 'axios'
  export default {
    filters: {
      statusFilter(status) {
        const statusMap = {
          published: 'success',
          draft: 'gray',
          deleted: 'danger'
        }
        return statusMap[status]
      }
    },
    data() {
      return {
        list: [],
        listLoading: true,
        addDialogVisible: false,
        commitDialogVisible: false,
        deleteImageDialogVisible: false,
        user_form:{
          user_id: '',
          username: '',
          password: '',
          realname: '',
          email: '',
          phone: '',
          status: '',
        },
        image_list: [],
        container_name: '',
        new_image_name: '',
        new_container_name: '',
        course_list: [],
        userDialogVisible: false,
        alterDialogVisible: false
      }
    },
    created() {
      this.fetchData()
    },
    methods: {
      fetchData() {
        this.listLoading = true
        this.$axios({
            method: 'post',
            url: '/teacher/list_user/',
          }).then(
            res => {
              console.log(res)
              this.course_list = res.data.data
              this.listLoading = false
            }
          )
        // getList().then(response => {
        //   this.list = response.data.items
        //   this.listLoading = false
        // })
      },
      handleDelete(user_id){
        this.listLoading = true
        console.log(user_id)
        const formData = new FormData()
        formData.append('user_id', user_id)
        this.$axios({
            method: 'post',
            url: '/teacher/delete_user/',
            data: formData,
          }).then(
            res => {
              console.log(res)
              this.fetchData()
              this.listLoading = false
            }
          )
      },
      AddUserDialogOpen(){
        this.userDialogVisible = true
        this.user_form = {
          user_id: '',
          username: '',
          password: '',
          realname: '',
          email: '',
          phone: '',
          status: '',
        }
      },
      handleCreate(){
        this.listLoading = true
        const formData = new FormData()
        formData.append('username', this.user_form.username)
        formData.append('password', this.user_form.password)
        formData.append('realname', this.user_form.realname)
        formData.append('email', this.user_form.email)
        formData.append('phone', this.user_form.phone)
        formData.append('status', this.user_form.status)
        this.$axios({
            method: 'post',
            url: '/teacher/add_user/',
            data: formData,
          }).then(
            res => {
              console.log(res)
              this.fetchData()
              this.listLoading = false
              window.alert('新用户创建成功')
            }
          )
          this.userDialogVisible= false
      },
      AlterDialogOpen(row){
        this.alterDialogVisible = true
        this.user_form = {
          user_id: row.user_id,
          username: row.username,
          password: row.password,
          realname: row.realname,
          email: row.email,
          phone: row.phone,
          status: row.status,
        }
      },
      handleAlter(){
        this.listLoading = true
        const formData = new FormData()
        formData.append('user_id', this.user_form.user_id)
        formData.append('username', this.user_form.username)
        formData.append('password', this.user_form.password)
        formData.append('realname', this.user_form.realname)
        formData.append('email', this.user_form.email)
        formData.append('phone', this.user_form.phone)
        formData.append('status', this.user_form.status)
        this.$axios({
            method: 'post',
            url: '/teacher/alter_user/',
            data: formData,
          }).then(
            res => {
              console.log(res)
              this.fetchData()
              this.listLoading = false
              window.alert('用户信息修改成功')
            }
          )
          this.alterDialogVisible = false
      }
    }
  }
  </script>
  