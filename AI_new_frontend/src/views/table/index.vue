<template>
  <div class="app-container">
    <div class="buttons" style="margin: 20px;"> 
      <el-button @click="CreateDialogOpen()" type="primary"> 创建新容器 </el-button>
      <el-button @click="CommitDialogOpen()" type="primary"> 构建新镜像 </el-button>
      <el-button @click="DeleteImageDialogOpen()" type="primary"> 删除镜像 </el-button>
    </div>

    <el-dialog title="添加新容器" :visible.sync="addDialogVisible" width="40%" center>
      <el-form ref="dataForm" :model="temp" label-position="left" label-width="100px" style="width: 400px; margin-left: 50px">
        <el-form-item label="基础镜像" prop="com">
          <el-select v-model="temp.image_name" placeholder="请选择" style="width: 300px; margin-left: 20px">
            <el-option
              v-for="item in image_list"
              :key="item"
              :label="item"
              :value="item">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="新容器名称" prop="com">
          <el-input v-model="new_container_name" clearable style="width: 300px; margin-left: 20px"/>
        </el-form-item>
        <el-form-item label="配置" prop="com">
          <el-select v-model="config" placeholder="请选择" style="width: 300px; margin-left: 20px">
            <el-option
              v-for="item in config_list"
              :key="item"
              :label="item"
              :value="item">
            </el-option>
          </el-select>
        </el-form-item>

      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="addDialogVisible = false"> 取消 </el-button>
        <el-button type="primary" @click="handleCreate()"> 提交 </el-button>
      </div>
    </el-dialog>
    
    <el-dialog title="添加新镜像" :visible.sync="commitDialogVisible" width="40%" center>
      <el-form ref="dataForm" :model="temp" label-position="left" label-width="100px" style="width: 400px; margin-left: 50px">
        <el-form-item label="容器名称" prop="com">
          <el-select v-model="container_name" placeholder="请选择" style="width: 300px; margin-left: 20px">
            <el-option
              v-for="item in list"
              :key="item.name"
              :label="item.name"
              :value="item.name">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="新镜像名称" prop="com">
          <el-input v-model="new_image_name" clearable style="width: 300px; margin-left: 20px"/>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="commitDialogVisible = false"> 取消 </el-button>
        <el-button type="primary" @click="handleCommit()"> 提交 </el-button>
      </div>
    </el-dialog>

    <el-dialog title="删除镜像" :visible.sync="deleteImageDialogVisible" width="40%" center>
      <el-form ref="dataForm" :model="temp" label-position="left" label-width="100px" style="width: 400px; margin-left: 50px">
        <el-form-item label="镜像名称" prop="com">
          <el-select v-model="temp.image_name" placeholder="请选择" style="width: 300px; margin-left: 20px">
            <el-option
              v-for="item in image_list"
              :key="item"
              :label="item"
              :value="item">
            </el-option>
          </el-select>
        </el-form-item>

      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="deleteImageDialogVisible = false"> 取消 </el-button>
        <el-button type="primary" @click="handleDeleteImage()"> 提交 </el-button>
      </div>
    </el-dialog>

    <el-table
      v-loading="listLoading"
      :data="list"
      element-loading-text="Loading"
      border
      fit
      highlight-current-row
    >
      <el-table-column align="center" label="ID" width="160">
        <template slot-scope="scope">
          {{ scope.row.id }}
        </template>
      </el-table-column>
      <el-table-column label="创建者">
        <template slot-scope="scope">
          {{ scope.row.author_name }}
        </template>
      </el-table-column>
      <el-table-column label="容器名">
        <template slot-scope="scope">
          {{ scope.row.name }}
        </template>
      </el-table-column>
      <el-table-column align="center" prop="created_at" label="操作" width="200">
        <template slot-scope="scope">
          <span>
            <el-button type="primary" @click="handleEdit(scope.row)"> 进入 </el-button>
            <el-button type="primary" @click="handleDelete(scope.row.name)"> 删除 </el-button>
          </span>
        </template>
      </el-table-column>
    </el-table>
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
      temp:{
        image_name: ''
      },
      image_list: [],
      container_name: '',
      author_id:'',
      new_image_name: '',
      new_container_name: '',
      config_list: [
        '0.5核CPU 1G内存',
        '1核CPU 2G内存',
        '2核CPU 4G内存',
        '4核CPU 8G内存',
        '8核CPU 16G内存',
      ],
      config: '',
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
          url: '/teacher/show_container/',
        }).then(
          res => {
            this.list = res.data.data
            console.log(res.data.data)
            this.listLoading = false
          }
        )
      // getList().then(response => {
      //   this.list = response.data.items
      //   this.listLoading = false
      // })
    },
    handleStart(container_name){
      this.listLoading = true
      const formData = new FormData()
      formData.append('container_name', container_name)
      console.log(container_name)
      this.$axios({
          method: 'post',
          url: '/teacher/start_container/',
          data: formData,
        }).then(
          res => {
            console.log(res)
            this.fetchData()
            this.listLoading = false
          }
        )
    },
    handleStop(container_name){
      this.listLoading = true
      const formData = new FormData()
      formData.append('container_name', container_name)
      console.log(container_name)
      this.$axios({
          method: 'post',
          url: '/teacher/stop_container/',
          data: formData,
        }).then(
          res => {
            console.log(res)
            this.fetchData()
            this.listLoading = false
          }
        )
    },
    handleDelete(container_name){
      this.listLoading = true
      let author_id = localStorage.getItem('user_id')
      const formData = new FormData()
      formData.append('container_name', container_name)
      formData.append('author_id', author_id)
      console.log(container_name)
      console.log(author_id)
      this.$axios({
          method: 'post',
          url: '/teacher/delete_container/',
          data: formData,
        }).then(
          res => {
            console.log(res)
            this.fetchData()
            this.listLoading = false
          }
        )
    },
    CreateDialogOpen(){
      this.addDialogVisible = true
      this.$axios({
          method: 'post',
          url: '/teacher/show_images/',
        }).then(
          res => {
            console.log(res)
            this.image_list = res.data.data
          }
        )
    },
    handleCreate(){
      this.listLoading = true
      let author_id = localStorage.getItem('user_id')
      const formData = new FormData()
      formData.append('image_name', this.temp.image_name)
      formData.append('container_name', this.new_container_name)
      formData.append('author_id', author_id)
      formData.append('config', this.config)
      this.$axios({
          method: 'post',
          url: '/teacher/add_new_container/',
          data: formData,
        }).then(
          res => {
            console.log(res)
            this.fetchData()
            this.listLoading = false
            window.alert('新容器创建成功')
          }
        )
        this.addDialogVisible = false
        this.temp.image_name = ''
    },
    CommitDialogOpen(){
      this.commitDialogVisible = true
      this.$axios({
          method: 'post',
          url: '/teacher/show_images/',
        }).then(
          res => {
            console.log(res)
            this.image_list = res.data.data
          }
        )
    },
    handleCommit(){
      this.listLoading = true
      const formData = new FormData()
      formData.append('container_name', this.container_name)
      formData.append('new_image_name', this.new_image_name)
      this.$axios({
          method: 'post',
          url: '/teacher/add_new_image/',
          data: formData,
        }).then(
          res => {
            console.log(res)
            this.fetchData()
            this.listLoading = false
            window.alert('新镜像创建成功')
          }
        )
        this.commitDialogVisible = false
        this.container_name = ''
        this.new_image_name = ''
    },
    DeleteImageDialogOpen(){
      this.deleteImageDialogVisible = true
      this.$axios({
          method: 'post',
          url: '/teacher/show_images/',
        }).then(
          res => {
            console.log(res)
            this.image_list = res.data.data
          }
        )
    },
    handleDeleteImage(){
      this.listLoading = true
      const formData = new FormData()
      formData.append('image_name', this.temp.image_name)
      this.$axios({
          method: 'post',
          url: '/teacher/delete_image/',
          data: formData,
        }).then(
          res => {
            console.log(res)
            this.fetchData()
            this.listLoading = false
            window.alert(res.data.msg)
          }
        )
        this.deleteImageDialogVisible = false
        this.temp.image_name = ''
    },
    handleEdit(row){
      // console.log(url)
      // window.open(url, '_blank');
      this.$router.push({
        path:'/manage/container_detail',
        query:{
          container_id: row.id,
        }
      })
    }
  }
}
</script>
