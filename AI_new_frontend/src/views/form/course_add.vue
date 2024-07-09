<template>
  <div class="app-container">
    <el-form ref="form" :model="form" label-width="120px">
      <el-form-item label="课程名称">
        <el-input v-model="form.course_name" />
      </el-form-item>
      <el-form-item label="使用镜像">
        <el-select v-model="form.use_image_name" placeholder="请选择" style="width: 300px; margin-left: 20px">
            <el-option
              v-for="item in list"
              :key="item"
              :label="item"
              :value="item">
            </el-option>
          </el-select>
      </el-form-item>
      <el-form-item label="实验限时">
        <el-input-number v-model="form.course_limit_time" :min="1" :max="100"></el-input-number> 小时
      </el-form-item>
      <!-- <el-form-item label="实验章节">
        第<el-input-number v-model="form.course_chapter" :min="1" :max="7"></el-input-number>章
      </el-form-item> -->
      <el-form-item label="章节">
        <el-select v-model="form.course_chapter" placeholder="请选择" style="width: 300px; margin-left: 20px">
            <el-option
              v-for="item in chapter_list"
              :key="item.chapter_num"
              :label="item.chapter_name"
              :value="item.chapter_num">
            </el-option>
          </el-select>
      </el-form-item>
      <el-form-item label="难度">
        <el-radio-group v-model="form.course_difficulty">
          <el-radio :label="'简单'">简单</el-radio>
          <el-radio :label="'中等'">中等</el-radio>
          <el-radio :label="'困难'">困难</el-radio>
        </el-radio-group>
      </el-form-item>
      <el-form-item label="课程简介">
        <el-input v-model="form.course_intro" :rows="8" type="textarea" style="width:800px"/>
      </el-form-item>
      <el-form-item label="课程目标">
        <el-input v-model="form.course_aim" :rows="8" type="textarea" style="width:800px"/>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSubmit">创建课程</el-button>
        <el-button @click="onCancel">取消</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      form: {
        course_name: '',
        use_image_name: '',
        course_limit_time: 1,
        course_difficulty: '',
        course_chapter: 1,
        course_intro: '',
        course_aim: '',
      },
      list:[],
      chapter_list:[],
    }
  },
  methods: {
    onSubmit() {
      let author_id = localStorage.getItem("user_id")
      const formData = new FormData()
      formData.append('course_name', this.form.course_name)
      formData.append('author_id', author_id)
      formData.append('use_image_name', this.form.use_image_name)
      formData.append('course_limit_time', this.form.course_limit_time)
      formData.append('course_difficulty', this.form.course_difficulty)
      formData.append('course_chapter', this.form.course_chapter)
      formData.append('course_intro', this.form.course_intro)
      formData.append('course_aim', this.form.course_aim)
      this.$axios({
          method: 'post',
          url: '/teacher/create_course/',
          data: formData,
        }).then(
          res => {
            console.log(res)
            window.alert('新课程创建成功')
          }
        )
      this.$router.push('/manage/course')
    },
    onCancel() {
      this.$router.push("/manage/course")
    },
    fetchData() {
      this.listLoading = true
      this.$axios({
          method: 'post',
          url: '/teacher/show_images/',
        }).then(
          res => {
            this.list = res.data.data
            this.listLoading = false
          }
        )
        this.$axios({
          method: 'post',
          url: '/teacher/list_chapter/',
        }).then(
          res => {
            this.chapter_list = res.data.data
            this.listLoading = false
          }
        )
      // getList().then(response => {
      //   this.list = response.data.items
      //   this.listLoading = false
      // })
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

