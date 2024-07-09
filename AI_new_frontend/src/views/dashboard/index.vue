<template>
  <div class="dashboard-container">
    <div class="dashboard-text">name: {{ realname }}</div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'Dashboard',
  data(){
    return{
      realname: '',
    }
  },
  methods:{
    getInfo(){
      this.realname = localStorage.getItem('realname');
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
