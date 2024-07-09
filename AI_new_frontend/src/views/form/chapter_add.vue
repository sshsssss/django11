<template>
  <div class="app-container">
    <el-button @click="addDialogOpen()"> 创建新章节 </el-button>

    <el-dialog title="添加新章节" :visible.sync="addDialogVisible" width="40%" center>
      <el-form ref="dataForm" :model="form" label-position="left" label-width="100px" style="width: 400px; margin-left: 50px">
        <el-form-item label="实验章节">
          第<el-input-number v-model="form.chapter_num" :min="1" :max="7"></el-input-number>章
        </el-form-item>
        <el-form-item label="章节名称" prop="com">
          <el-input v-model="form.chapter_name" clearable style="width: 300px; margin-left: 20px"/>
        </el-form-item>
        <el-form-item label="章节简介">
          <el-input v-model="form.chapter_intro" :rows="8" type="textarea" style="width:300px; margin-left: 20px"/>
        </el-form-item>
        注意：若章节序号和已有的重复，则会修改章节的名称和简介
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="addDialogVisible = false"> 取消 </el-button>
        <el-button type="primary" @click="handleCreate()"> 提交 </el-button>
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
      <el-table-column align="center" label="章节" width="95">
        <template slot-scope="scope">
          {{ scope.row.chapter_num }}
        </template>
      </el-table-column>
      <el-table-column label="章节名">
        <template slot-scope="scope">
          {{ scope.row.chapter_name }}
        </template>
      </el-table-column>
      <el-table-column label="章节简介">
        <template slot-scope="scope">
          {{ scope.row.chapter_intro }}
        </template>
      </el-table-column>
      <el-table-column align="center" prop="created_at" label="操作" width="200">
        <template slot-scope="scope">
          <span>
            <el-button type="primary" @click="handleDelete(scope.row.chapter_num)"> 删除 </el-button>
          </span>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
export default {
  data() {
    return {
      form: {
        chapter_num: 1,
        chapter_name: '',
        chapter_intro: '',
      },
      list:[],
      addDialogVisible: false,

    }
  },
  methods: {
    addDialogOpen(){
      this.addDialogVisible = true
    },
    handleCreate(){
      const formData = new FormData()
      formData.append('chapter_num', this.form.chapter_num)
      formData.append('chapter_name', this.form.chapter_name)
      formData.append('chapter_intro', this.form.chapter_intro)
      this.$axios({
          method: 'post',
          url: '/teacher/add_chapter/',
          data: formData,
        }).then(
          res => {
            console.log(res)
            window.alert(res.data.msg)
            this.fetchData()
          }
        )
      this.addDialogVisible = false
      this.form.chapter_name = ''
      this.form.chapter_num = 1
    },
    fetchData() {
      this.listLoading = true
      this.$axios({
          method: 'post',
          url: '/teacher/list_chapter/',
        }).then(
          res => {
            this.list = res.data.data
            this.listLoading = false
          }
        )
      // getList().then(response => {
      //   this.list = response.data.items
      //   this.listLoading = false
      // })
    },
    handleDelete(chapter_num){
      const formData = new FormData()
      formData.append('chapter_num', chapter_num)
      this.$axios({
          method: 'post',
          url: '/teacher/delete_chapter/',
          data: formData,
        }).then(
          res => {
            console.log(res)
            window.alert(res.data.msg)
            this.fetchData()
          }
        )
    },
  },
  created() {
    this.fetchData()
  },
}
</script>

<style scoped>
.line{
  text-align: center;
}
</style>

