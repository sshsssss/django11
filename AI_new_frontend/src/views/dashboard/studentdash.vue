<template>
  <div class="dashboard-container">
    <div class="dashboard-text">用户名: {{ userinfo.username }}</div>
    <div class="dashboard-text">姓名: {{ userinfo.realname }}</div>
    <div class="dashboard-text">邮箱: <el-input v-model="userinfo.email" clearable style="width: 300px;"/></div>
    <div class="dashboard-text">电话: <el-input v-model="userinfo.phone" clearable style="width: 300px;"/></div>
    <div class="dashboard-text"><el-button @click="handleChangeUserInfo"> 修改个人信息 </el-button></div>
    <div class="dashboard-text">原密码:<el-input
          :key="passwordType"
          ref="password"
          v-model="originpassword"
          :type="passwordType"
          name="password"
          tabindex="2"
          auto-complete="on"
          style="width: 300px;"
        />
    </div>
    <div class="dashboard-text">新密码:<el-input
          :key="passwordType"
          ref="password"
          v-model="changepassword"
          :type="passwordType"
          name="password"
          tabindex="2"
          auto-complete="on"
          style="width: 300px;"
        />
    </div>
    <div class="dashboard-text">确认密码:<el-input
          :key="passwordType"
          ref="password"
          v-model="surepassword"
          :type="passwordType"
          name="password"
          tabindex="2"
          auto-complete="on"
          style="width: 300px;"
        />
    </div>
    <div class="dashboard-text"><el-button @click="handleChangePassword"> 修改密码 </el-button></div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'Dashboard',
  data(){
    return{
      userinfo: {},
      originpassword: '',
      changepassword: '',
      surepassword: '',
    }
  },
  methods:{
    getInfo(){
      let user_id = localStorage.getItem('user_id');
      let formData = new FormData()
            formData.append('user_id', user_id)
            this.$axios({
                method: 'post',
                url: '/student/get_user_info/',
                data: formData,
            }).then(
                res => {
                    console.log(res)
                    this.userinfo = res.data.data
                }
            )
    }
  },
  created(){
    this.getInfo()
  }
}
</script>

<style lang="scss" scoped>
.dashboard {
  &-container {
    margin: 30px;
  }
  &-text {
    font-size: 30px;
    line-height: 46px;
  }
}
</style>
