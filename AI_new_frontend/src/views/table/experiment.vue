<template>
    <div class="detail-container" v-if="loading===false">
        <div class="top">
            <el-button @click="ReturnToCourseInfo()" style="width:100px; height: 40px; position:fixed; left:70px">结束实验 </el-button>
            &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;
            <div class="timer" style="position: fixed; right:70px;">
                {{ formattedTime }}
            </div>
        </div>
        <iframe :src="url" style="width:100%; height:85%; position: fixed; top:15% ;left:0%"></iframe>
        <el-dialog title="是否保存实验" :visible.sync="showModal" width="40%" center>
            <div slot="footer" class="dialog-footer">
                <el-button type="primary" @click="confirmSave"> 保存 </el-button>
                <el-button @click="confirmQuit"> 不保存 </el-button>
            </div>
        </el-dialog>
    </div>
    <div class="detail-container" v-else>
        LOADING
        <el-dialog title="你确定要退出吗" :visible.sync="showModal" width="40%" center>
            <div slot="footer" class="dialog-footer">
                <el-button type="primary" @click="confirmSave"> 保存 </el-button>
                <el-button @click="confirmQuit"> 不保存 </el-button>
            </div>
        </el-dialog>
    </div>
</template>


<script>
import timer from '@/components/timer'
import user from '@/store/modules/user';
import axios from 'axios';
export default{
    components:{
        timer
    },
    data(){
        return {
            course_id: '',
            experiment_info: '',
            timer: null,
            time: 0,
            url: '',
            loading: false,
            showModal: false,
        }
    },
    methods:{
        getData(){
            this.loading = true
            let course_id = this.$route.query.course_id
            let user_id = localStorage.getItem('user_id')
            let formData = new FormData()
            formData.append('course_id', course_id)
            formData.append('user_id', user_id)
            this.$axios({
                method: 'post',
                url: '/teacher/create_experiment/',
                data: formData,
            }).then(
                res => {
                    console.log(res)
                    this.experiment_info = res.data.data
                    this.url = res.data.data.experiment_url
                    // this.url = 'http://39.105.203.95:8888/lab?token=123456789'
                    this.time = res.data.data.experiment_countdown
                    this.startCountdown()
                    this.loading = false
                }
            )
        },
        ReturnToCourseInfo(){
            let experiment_id = this.experiment_info.experiment_id
            let formData = new FormData()
            formData.append('experiment_id', experiment_id)
            this.showModal = true

            // this.$axios({
            //     method: 'post',
            //     url: '/teacher/delete_experiment/',
            //     data: formData,
            // }).then(
            //     res => {
            //         console.log(res)
            //         this.$router.push('/manage/course')
            //     }
            // )
        },
        handleTimeRemaining(time) {
            this.time = time
        },
        StartExperiment(){
            let course_id = this.course_info.course_id
            window.open(this.$router.resolve({ path: '/experiment', query:{ course_id:course_id } }).href, '_blank');
        },
                // 用户点击页面关闭按钮时调用
        attemptClose() {
            this.showModal = true;
        },
        // 用户在模态框中点击确定按钮时调用
        confirmSave() {
            let experiment_id = this.experiment_info.experiment_id
            
            let formData = new FormData()
            formData.append('experiment_id', experiment_id)
            formData.append('countdown', this.time)
            this.$axios({
                method: 'post',
                url: '/teacher/save_experiment/',
                data: formData,
            }).then(
                res => {
                    console.log(res)
                    window.close()
                }
            )
        },
        // 用户在模态框中点击取消按钮时调用
        confirmQuit() {
            let experiment_id = this.experiment_info.experiment_id
            
            let formData = new FormData()
            formData.append('experiment_id', experiment_id)
            this.$axios({
                method: 'post',
                url: '/teacher/delete_experiment/',
                data: formData,
            }).then(
                res => {
                    console.log(res)
                    window.close()
                }
            )
        },
        startCountdown() {
            this.timer = setInterval(() => {
                if (this.time > 0) {
                this.time--;
                } else {
                this.time = 0;
                clearInterval(this.timer);
                this.confirmQuit()
                }
            }, 1000);
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
    async created(){
        this.getData();
    },
}
</script>



<style lang="scss" scoped>
.top{
    display: flex;
    width:100%;
}

.detail {
  &-container {
    margin: 30px;
  }
  &-text {
    font-size: 30px;
    line-height: 46px;
  }
}
</style>