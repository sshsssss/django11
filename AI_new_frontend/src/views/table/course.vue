<template>
  <div class="app-container">
    <el-button @click="CreateCourseOpen()" style="margin: 20px;" type="primary"> 创建新课程 </el-button>

    <el-table
      v-loading="listLoading"
      :data="course_list"
      element-loading-text="Loading"
      border
      fit
      highlight-current-row
    >
      <el-table-column align="center" label="实验ID" width="80">
        <template slot-scope="scope">
          {{ scope.row.course_id }}
        </template>
      </el-table-column>
      <el-table-column label="实验名称">
        <template slot-scope="scope">
          {{ scope.row.course_name }}
        </template>
      </el-table-column>
      <el-table-column label="实验创建人">
        <template slot-scope="scope">
          {{ scope.row.author_name }}
        </template>
      </el-table-column>
      <el-table-column label="实验章节">
        <template slot-scope="scope">
          {{ scope.row.course_chapter }}
        </template>
      </el-table-column>
      <el-table-column label="章节名称">
        <template slot-scope="scope">
          {{ scope.row.chapter_name }}
        </template>
      </el-table-column>
      <el-table-column label="难度">
        <template slot-scope="scope">
          {{ scope.row.course_difficulty }}
        </template>
      </el-table-column>
      <el-table-column label="限时">
        <template slot-scope="scope">
          {{ scope.row.course_limit_time }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="操作" width="200">
        <template slot-scope="scope">
          <span>
            <el-button type="primary" @click="handleEnter(scope.row)"> 进入 </el-button>
            <el-button type="primary" @click="handleDelete(scope.row.course_id)"> 删除 </el-button>
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
      new_image_name: '',
      new_container_name: '',
      course_list: []
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
          url: '/teacher/list_course/',
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
    handleEnter(row){
      console.log(row)
      this.$router.push({
        path:'/manage/course_detail',
        query:{
          course_id: row.course_id,
        }
      })
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
    handleDelete(course_id){
      this.listLoading = true
      console.log(course_id)
      const formData = new FormData()
      formData.append('course_id', course_id)
      this.$axios({
          method: 'post',
          url: '/teacher/delete_course/',
          data: formData,
        }).then(
          res => {
            console.log(res)
            this.fetchData()
            this.listLoading = false
          }
        )
    },
    CreateCourseOpen(){
      this.$router.push('/form/course_add')
    },
    handleCreate(){
      this.listLoading = true
      const formData = new FormData()
      formData.append('image_name', this.temp.image_name)
      formData.append('container_name', this.new_container_name)
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
    handleEdit(url){
      console.log(url)
      window.open(url, '_blank');
    }
  }
}
</script>
