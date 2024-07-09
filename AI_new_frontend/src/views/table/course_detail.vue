<template>
    <div class="detail-container">
        <el-button @click="ReturnToCourseInfo()" type="primary">返回 </el-button>
        <div style="margin: 15px;">
            <div class="detail-text">实验名称：<div style="width:80%">{{ course_info.course_name }}</div></div>
            <div class="detail-text">实验难度：<div style="width:80%">{{ course_info.course_difficulty }}</div></div>
            <div class="detail-text">实验章节：<div style="width:80%">第{{ course_info.course_chapter }}章 {{course_info.chapter_name }}</div></div>
            <div class="detail-text">实验限时：<div style="width:80%">{{ course_info.course_limit_time }}小时</div></div>
            <div class="detail-text">实验简介：<div style="width:80%">{{ course_info.course_intro }}</div></div>
            <div class="detail-text">实验目标：<div style="width:80%">{{ course_info.course_aim }}</div></div>
          </div>
      <div class="detail-text">
        <el-button @click="StartExperiment()" v-if="status==='uncreated'" type="primary" style="margin: 10px;">开始实验 </el-button>
        <el-button @click="StartExperiment()" v-if="status==='running'" type="primary" style="margin: 10px;">进入实验 </el-button>
        <el-button @click="DeleteExperiment()" v-if="status==='running'" type="danger" style="margin: 10px;">结束实验</el-button>
        <el-button @click="uploadExpVisible()" type="primary" style="margin: 10px;">上传实验文件 </el-button>
        <div class="timer"  v-if="status==='running'" style="margin: 10px;">
            实验剩余时间：{{ formattedTime }}
        </div>
        <div style="margin: 10px;">实验得分： {{ course_info.score }}</div>
      </div>
            <el-table 
                :data="files_uploaded_to_teacher" 
                v-loading="uplistLoading"
                @selection-change="handleExpFileSelectionChange"
                style="width: 100%"
                :height="300">
                <el-table-column
                type="selection"
                :selectable="isSelectable"
                width="55">
                </el-table-column>
                <el-table-column 
                prop="name" 
                label="文件名">
                <template slot-scope="scope">
                    {{ scope.row}}
                </template>
                </el-table-column>
                <el-table-column 
                prop="name" 
                label="操作">
                <template slot-scope="scope">
                    <el-button @click="downloadFile(scope.row)" type="primary">下载文件</el-button>
                    <el-button @click="deleteFile(scope.row)" type="danger">删除文件</el-button>
                </template>
                </el-table-column>
            </el-table>
            <h3>学生已上传实验文件：</h3>
            <el-table 
                :data="users_have_uploaded" 
                v-loading="userlistLoading"
                style="width: 100%"
                :height="300">
                <el-table-column 
                prop="name" 
                label="用户ID">
                <template slot-scope="scope">
                    {{ scope.row.user_id}}
                </template>
                </el-table-column>
                <el-table-column 
                prop="name" 
                label="用户名">
                <template slot-scope="scope">
                    {{ scope.row.realname}}
                </template>
                </el-table-column>
                <el-table-column 
                prop="name" 
                label="分数">
                <template slot-scope="scope">
                    {{ scope.row.score}}
                </template>
                </el-table-column>
                <el-table-column 
                prop="name" 
                label="操作">
                <template slot-scope="scope">
                    <el-button @click="viewFile(scope.row)">查看</el-button>
                    <el-button @click="rate(scope.row)"  type="primary">评分</el-button>
                </template>
                </el-table-column>
            </el-table>

        <el-dialog title="上传实验文件" :visible.sync="uploadDialogVisible" width="40%"center>
            <el-table 
                :data="uploaded_files" 
                @selection-change="handleSelectionChange"
                v-loading="listLoading"
                style="width: 100%"
                :height="300">
                <el-table-column
                type="selection"
                :selectable="isSelectable"
                width="55">
                </el-table-column>
                <el-table-column 
                prop="name" 
                label="文件名">
                <template slot-scope="scope">
                    {{ scope.row.filename}}
                </template>
                </el-table-column>
                <el-table-column 
                prop="path" 
                label="文件路径">
                <template slot-scope="scope">
                    {{ scope.row.path}}
                </template>
                </el-table-column>
            </el-table>
        <div slot="footer" class="dialog-footer">
            <el-button @click="uploadDialogVisible = false"> 取消 </el-button>
            <el-button type="primary" @click="handleSubmit()"> 提交 </el-button>
        </div>
        </el-dialog>

        <el-dialog title="评分" :visible.sync="rateDialogVisible" width="40%"center>
            <el-form ref="dataForm" :model="form" label-position="left" label-width="100px" style="width: 400px; margin-left: 50px">
                <el-form-item label="分数" prop="com">
                    <el-input-number v-model="form.score" :min="0" :max="100"></el-input-number>
                </el-form-item>
            </el-form>

        <div slot="footer" class="dialog-footer">
            <el-button @click="rateDialogVisible = false"> 取消 </el-button>
            <el-button type="primary" @click="handleRate()"> 提交 </el-button>
        </div>
        </el-dialog>


        <el-dialog title="查看用户实验文件" :visible.sync="userfileDialogVisible" width="40%"center>
            <el-table 
                :data="user_files" 
                v-loading="listLoading"
                style="width: 100%"
                :height="300">
                <el-table-column 
                prop="name" 
                label="文件名">
                <template slot-scope="scope">
                    {{ scope.row }}
                </template>
                </el-table-column>
                <el-table-column 
                prop="path" 
                label="操作">
                <template slot-scope="scope">
                    <el-button @click="downloadStudentFile(scope.row)">下载文件</el-button>
                </template>
                </el-table-column>
            </el-table>
        </el-dialog>

    </div>
</template>


<script>
import timer from '@/components/timer'
import axios from 'axios';
export default{
    components:{
        timer
    },
    data(){
        return {
            course_id: '',
            course_info: '',
            timer: null,
            time: 0,
            config_list: [
                '0.5核CPU 1G内存',
                '1核CPU 2G内存',
                '2核CPU 4G内存',
                '4核CPU 8G内存',
                '8核CPU 16G内存',
            ],
            config: '1核CPU 2G内存',
            uploadDialogVisible: false,
            uploaded_files: [],
            files_uploaded_to_teacher: [],
            selectedFiles: [],
            selectedExpFiles: [],
            listLoading: false,
            uplistLoading: false,
            userlistLoading: false,
            users_have_uploaded: [],
            user_files: [],
            userfileDialogVisible: false,
            current_rate_student: '',
            rateDialogVisible: false,
            form: {
                score: 0
            },
            status: ''
        }
    },
    methods:{
        getData(){
            let course_id = this.$route.query.course_id
            let formData = new FormData()
            let user_id = localStorage.getItem('user_id')
            formData.append('course_id', course_id)
            formData.append('user_id', user_id)
            this.$axios({
                method: 'post',
                url: '/teacher/get_course_info/',
                data: formData,
            }).then(
                res => {
                    console.log(res)
                    this.course_info = res.data.data
                    console.log(res.data.data.course_limit_time)
                    this.time = res.data.data.experiment_countdown
                    this.status = res.data.data.experiment_status
                    if(res.data.data.experiment_status === 'running'){
                        this.startCountdown()
                    }
                }
            )
        },
        ReturnToCourseInfo(){
            this.$router.push("/manage/course")
        },
        handleTimeRemaining(time) {
            console.log('剩余时间:', time);
        },
        StartExperiment(){
            let course_id = this.course_info.course_id
            let user_id = localStorage.getItem('user_id')
            let formData = new FormData()
            formData.append('course_id', course_id)
            formData.append('user_id', user_id)
            var loadingInstance = this.$loading({
                lock: true,
                text: '实验环境正在创建中，请稍后',
                spinner: 'el-icon-loading',
                background: 'rgba(0, 0, 0, 0.7)'
            });
            this.$axios({
                method: 'post',
                url: '/teacher/create_experiment/',
                data: formData,
            }).then(
                res => {
                    loadingInstance.close()
                    console.log(
                        res.data.data.experiment_url
                    )
                    window.open(res.data.data.experiment_url, '_blank');
                    location.reload()
                }
            )
            // window.open(this.$router.resolve({ path: '/experiment', query:{ course_id:course_id } }).href, '_blank');
        },
        DeleteExperiment(){
            let course_id = this.course_info.course_id
            let user_id = localStorage.getItem('user_id')
            let formData = new FormData()
            formData.append('course_id', course_id)
            formData.append('user_id', user_id)
            var loadingInstance = this.$loading({
                lock: true,
                text: '删除实验中，请稍后',
                spinner: 'el-icon-loading',
                background: 'rgba(0, 0, 0, 0.7)'
            });
            this.$axios({
                method: 'post',
                url: '/teacher/delete_experiment_by_course_user/',
                data: formData,
            }).then(
                res => {
                    console.log(res)
                    loadingInstance.close()
                    location.reload()
                }
            )
        },
        loadExpFiles(){
            this.listLoading = true
            const formData = new FormData()
            let user_id = localStorage.getItem('user_id')
            let course_id = this.$route.query.course_id
            formData.append('user_id', user_id)
            formData.append('course_id', course_id)
            this.$axios({
                method: 'post',
                url: '/teacher/load_experiment_files/',
                data: formData,
            }).then(res => {
                console.log(res)
                this.uploaded_files = res.data.data
                this.listLoading = false
            })
        },
        loadUploadedExpFiles(){
            this.uplistLoading = true
            const formData = new FormData()
            let user_id = localStorage.getItem('user_id')
            let course_id = this.$route.query.course_id
            formData.append('user_id', user_id)
            formData.append('course_id', course_id)
            this.$axios({
                method: 'post',
                url: '/teacher/list_user_files_uploaded/',
                data: formData,
            }).then(res => {
                console.log(res)
                this.files_uploaded_to_teacher = res.data.data
                this.uplistLoading = false
            })
        },
        loadUsers(){
            this.userlistLoading = true
            const formData = new FormData()
            let course_id = this.$route.query.course_id
            formData.append('course_id', course_id)
            this.$axios({
                method: 'post',
                url: '/teacher/list_users_have_uploaded/',
                data: formData,
            }).then(res => {
                console.log(res)
                this.users_have_uploaded = res.data.data
                this.userlistLoading = false
            })
        },
        uploadExpVisible(){
            this.uploadDialogVisible = true
            this.loadExpFiles()
        },
        viewFile(row){
            let user_id = row.user_id
            this.userfileDialogVisible = true
            this.loadUserExpFile(user_id)
            this.current_rate_student = user_id
        },
        loadUserExpFile(user_id){
            this.uplistLoading = true
            const formData = new FormData()
            let course_id = this.$route.query.course_id
            formData.append('user_id', user_id)
            formData.append('course_id', course_id)
            this.$axios({
                method: 'post',
                url: '/teacher/list_user_files_uploaded/',
                data: formData,
            }).then(res => {
                console.log(res)
                this.user_files = res.data.data
                this.uplistLoading = false
            })
        },
        handleSelectionChange(selected) {
            this.selectedFiles = selected.map(file => file.path);
            console.log(this.selectedFiles)
        },
        handleExpFileSelectionChange(selected){
            this.selectedExpFiles= selected.map(file => file.path);
            console.log(this.selectedExpFiles)
        },
        isSelectable(file) {
            // 这个函数决定哪些文件可以被选中
            // 不写代表允许所有文件被选中
            return true;
        },
        handleSubmit(){
            const formData = new FormData();
            let user_id = localStorage.getItem('user_id')
            let course_id = this.$route.query.course_id
            formData.append('user_id', user_id)
            formData.append('course_id', course_id)
            formData.append('file_paths', JSON.stringify(this.selectedFiles))
            this.$axios({
                method: 'post',
                url: '/teacher/upload_exp_file/',
                data: formData,
                }).then(response => {
                console.log(response)
                window.alert(response.data.msg)
                this.loadUploadedExpFiles()
                this.uploadDialogVisible = false
                })
                .catch(error => console.log(error));
        },    
        downloadFile(filename) {
            let user_id = localStorage.getItem('user_id')
            let course_id = this.$route.query.course_id
            console.log(filename)
            let formData = new FormData();
            formData.append('user_id', user_id);
            formData.append('course_id', course_id);
            formData.append('filename', filename);

            this.$axios({
                method: 'post',
                url: '/teacher/download_file/', 
                data: formData,
                responseType: 'blob',
            })
            .then((response) => {
                const url = window.URL.createObjectURL(new Blob([response.data]));
                const link = document.createElement('a');
                link.href = url;
                link.setAttribute('download', filename);
                document.body.appendChild(link);
                link.click();
            })
            .catch((error) => {
                console.error(error);
            });
        },
        downloadStudentFile(filename) {
            let user_id = this.current_rate_student
            let course_id = this.$route.query.course_id
            console.log(filename)
            let formData = new FormData();
            formData.append('user_id', user_id);
            formData.append('course_id', course_id);
            formData.append('filename', filename);

            this.$axios({
                method: 'post',
                url: '/teacher/download_file/', 
                data: formData,
                responseType: 'blob',
            })
            .then((response) => {
                const url = window.URL.createObjectURL(new Blob([response.data]));
                const link = document.createElement('a');
                link.href = url;
                link.setAttribute('download', filename);
                document.body.appendChild(link);
                link.click();
            })
            .catch((error) => {
                console.error(error);
            });
        },
        deleteFile(filename) {
            let user_id = localStorage.getItem('user_id')
            let course_id = this.$route.query.course_id
            console.log(filename)
            const formData = new FormData();
            formData.append('user_id', user_id);
            formData.append('course_id', course_id);
            formData.append('filename', filename);

            this.$axios({
                method: 'post',
                url: '/teacher/delete_exp_file/', 
                data: formData,
            })
            .then((response) => {
                window.alert(response.data.msg)
                this.loadUploadedExpFiles()
            })
            .catch((error) => {
                console.error(error);
            });
        },
        rate(row){
            this.current_rate_student = row.user_id
            console.log(row.user_id)
            this.rateDialogVisible = true
        },
        handleRate(){
            let user_id = this.current_rate_student
            let course_id = this.$route.query.course_id
            let score = this.form.score
            const formData = new FormData();
            formData.append('user_id', user_id);
            formData.append('course_id', course_id);
            formData.append('score', score);
            this.$axios({
                method: 'post',
                url: '/teacher/rate_experiment/', 
                data: formData,
            })
            .then((response) => {
                window.alert(response.data.msg)
                this.loadUsers()
                this.getData()
                this.rateDialogVisible = false
            })
            .catch((error) => {
                console.error(error);
            });
        },
        startCountdown() {
            this.timer = setInterval(() => {
                if (this.time > 0) {
                this.time--;
                } else {
                this.time = 0;
                clearInterval(this.timer);
                }
            }, 1000);
        },

    },
    async created(){
        this.getData()
        this.loadUploadedExpFiles()
        this.loadUsers()
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



<style lang="scss" scoped>
.detail {
  &-container {
    margin: 30px;
  }
  &-text {
    font-size: 20px;
    line-height: 36px;
    white-space: pre-wrap;
    display:flex;
  }
}
</style>