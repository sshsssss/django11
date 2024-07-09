<template>
    <div class="app-container">
      <div class="bgtop">
        <div style="position: absolute; top: 170px; left: 0; font-size: 54px; color: #fff; font-weight: 400; width: 700px; margin: 0 auto; right: 0; text-align: center; ">人工智能实验平台</div>
      </div>
      <el-collapse v-model="activeNames">
        <el-collapse-item 
          v-for="(chapter, index) in chapter_list" 
          :key="index" 
          :name="index.toString()"
          >
          <template slot="title">
            <div class="title" style="  line-height: 70px;
                                          height: 70px;
                                          font-size: 22px !important;
                                          background: #D5E8FF;
                                          padding-left: 40px;">
                                            第 {{ chapter.chapter_num }} 章 &nbsp;&nbsp;&nbsp;{{ chapter.chapter_name }}
                                          </div>
          </template>
          <div class="experiment-intro">
            <div class="introduction">
              <h3>
                章节介绍 
              </h3>
              <p> {{ chapter.chapter_intro }} </p>
            </div>
          </div>
          <div class="experiment-box">
            <div v-for="(course, key) in course_list[index]" :key="key" @click="handleEnter(course)" style="margin: 20px;">
              <el-card class="box-card">
                <div class="left" style="width:120px">
                  <img src="~@/assets/exp_hep.png" style="width:112px; height: 145px;">
                </div>
                <div class="right" style="width: 220px; position: relative; top:-170px; left:125px">
                  <span class="icon">实验</span>
                  <span class="hep-title">{{course.course_name}}</span>
                  <span class="time">{{ course.course_limit_time }}小时</span>
                </div>
              </el-card>
            </div>
          </div>
        </el-collapse-item>
    </el-collapse>
      <!-- <el-table
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
      <el-table-column label="实验章节">
        <template slot-scope="scope">
          {{ scope.row.course_chapter }}
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
            <el-button type="primary" @click="handleEnter(scope.row)"> 进入实验 </el-button>
          </span>
        </template>
      </el-table-column>
      </el-table> -->
    </div>
  </template>
  
  <script>
  import { getList } from '@/api/table'
  
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
        course_list: null,
        listLoading: false,
        chapter_list: null,
        activeNames: [],
      }
    },
    created() {
      this.fetchData()
      this.listChapter()
    },
    methods: {
      fetchData() {
        this.$axios({
          method: 'post',
          url: '/student/list_course_by_chapter/',
        }).then(
          res => {
            console.log(res)
            this.course_list = res.data.data
            this.listLoading = false
          }
        )
      },
      handleEnter(row){
            console.log(row)
            this.$router.push({
                path:'/experiment_detail',
                query:{
                    course_id: row.course_id,
                }
            })
      },
      listChapter() {
        this.$axios({
            method: 'post',
            url: '/teacher/list_chapter/',
          }).then(
            res => {
              this.chapter_list = res.data.data
            }
          )
        // getList().then(response => {
        //   this.list = response.data.items
        //   this.listLoading = false
        // })
      },
    },
    computed: {
        formattedTime() {
        const hours = Math.floor(this.time / 3600);
        const minutes = Math.floor((this.time % 3600) / 60);
        const seconds = this.time % 60;

        return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        },
    },
  }
  </script>

<style scoped>
.bgtop{
  position: relative;
  height: 400px;
  padding: 0;
  background: url("~@/assets/AIbg2.png");;
}

.el-collapse {
    background-color: #D5E8FF !important;
}

.experiment-intro{
  border: 1px solid #B0D4FF;
  margin: 20px 40px 0;
  padding: 20px;
  color: #888A91;
  font-size: 16px;
}


.experiment-intro .introduction{
  display: flex;

}

.el-collapse-item__wrap {
    background-color: #D5E8FF !important;
}

.experiment-box{
  display: flex;
  margin: 20px;
}

h3::after {
    content: "";
    display: inline-block;
    width:80px;
    height: 7px;
    background: #5282f7;
    position: relative;
    left: -81px;
    opacity: .3;
    top: 5px;
}

span.icon {
    display: inline-block;
    color: #3964FF;
    width: 44px;
    height: 20px;
    border: 1px solid #3964FF;
    line-height: 20px;
    text-align: center;
    border-radius: 2px;
    margin-top: 20px;
}

p{
  flex: 1;
}

.hep-title {
    color: #333;
    font-size: 18px !important;
    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 3;
    overflow: hidden;
    margin-top: 10px;
    margin-bottom: 25px;
    min-height: 68px;
}

.text {
    font-size: 14px;
  }

  .item {
    padding: 18px 0;
  }

  .box-card {
    width: 360px;
    background: #fff;
    margin-top: 20px;
    height: 200px;
    display: flex;
    cursor: pointer;
  }
  span.time{
    font-size: 16px !important;
  }

   /deep/.el-collapse {
      background-color: #D5E8FF !important;
    }
    /deep/.el-collapse,.el-collapse-item__wrap {
      border: 40px solid white;
      width: 100%;
      position: relative;
      left:0;
    }
    /deep/ .el-collapse-item__header {
        color: black;
        background-color: #D5E8FF !important;
        height: 80px;
    }
    /deep/ .el-collapse-item__content {
        color: black;
        background-color: #e1edfd !important;
        position: relative;
        top:-20px;
    }


</style>