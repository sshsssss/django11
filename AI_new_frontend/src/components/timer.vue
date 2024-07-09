<template>
    <div>
      <button v-if="timer === null" @click="startTimer">开始</button>
      <button v-else @click="stopTimer">停止</button>
      <p>{{ hours }} : {{ minutes }} : {{ seconds }}</p>
    </div>
  </template>
  
  <script>
  export default {
    props: ['startTime'],
    data() {
      return {
        timer: null,
        time: this.startTime
      };
    },
    watch: {
        // 监听startTime的变化，开始倒计时
        startTime: function(val) {
          this.time = val;
          this.startTimer();
        },
    },
    computed: {
      hours() {
        return Math.floor(this.time / 3600);
      },
      minutes() {
        return Math.floor((this.time % 3600) / 60);
      },
      seconds() {
        return this.time % 60;
      },
    },
    methods: {
      startTimer() {
        this.timer = setInterval(() => {
          // 时间未耗尽则继续计时
          if (this.time > 0) {
            this.time--;
          } else {
            // 否则停止计时
            this.stopTimer();
          }
        }, 1000);
      },
      stopTimer() {
        clearInterval(this.timer);
        this.timer = null;
        let alert = "剩余" + this.time + "秒"
        window.alert(alert)
        this.$emit('time-remaining', this.time); // 发送剩余时间到父组件
      },
    },
    beforeDestroy() {
      this.stopTimer();
    },
    created(){
      this.startTimer()
    }
  };
  </script>