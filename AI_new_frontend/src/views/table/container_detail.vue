<template>
  <div>
    <el-button type="primary" @click="handleReturn()" style="margin: 15px;"> 返回容器列表 </el-button>
    <div style="margin: 15px;">
      <div class="detail-text">名称：{{ container_info.container_name}} </div>
      <div class="detail-text">配置：{{ container_info.cpu_num }}核CPU, {{ container_info.mem_size }}G内存 </div>
      <div class="detail-text">SSH端口: {{ container_info.ssh_port }}</div>
      <div class="detail-text">HTTP端口: {{ container_info.http_port }}</div>
      <div class="detail-text">SSH命令: ssh root@39.105.203.95 -p {{ container_info.ssh_port }}</div>
      <div class="detail-text">SSH密码: {{ container_info.ssh_password }}</div>
    </div>
    <div >
      <h3 style="position: relative; left:15px">上传文件至镜像：<el-button type="primary" @click="handleEnter()"> 进入容器创建新文件/预载软件 </el-button></h3>
      <div class="upload-box" style="margin: 15px;">
        选择文件：<input type="file" ref="singleFile" multiple @change="handleSingleFileUpload" style="margin: 15px;"/>
          <el-button v-on:click="submitSingleFile()" :disabled="listLoading" style="margin: 15px;" type="primary">上传文件</el-button>
        选择文件夹：<input type="file" ref="folderFiles" multiple webkitdirectory @change="handleFileUpload" style="margin: 15px;"/>
          <el-button v-on:click="submitFile()" :disabled="listLoading" style="margin: 15px;" type="primary">上传文件夹</el-button>
          <div class="fileUpload">
            指定文件上传路径：
            <el-input placeholder="请输入路径，注意路径不以/结尾，文件夹名不以.开头" v-model="path" style="width: 70%;">
              <template slot="prepend"> {{ container_info.workdir }}/ </template>
            </el-input>
          </div>
      </div>
    </div>
    <!-- <ul v-if="uploaded_files.length > 0">
      <li v-for="(file, index) in uploaded_files" :key="index">
        {{ file.filename }} &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;  {{ file.path }}  
        <button @click="onDelete(file.path)">Delete</button>
      </li>
    </ul> -->
    <div>
      <div style="margin: 15px;">
        <h3>管理已上传文件&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <el-button @click="onDeleteSelectedFiles" type="danger">删除所选文件</el-button></h3>
        <el-table 
          :data="uploaded_files" 
          v-loading="listLoading"
          @selection-change="handleSelectionChange"
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
          <el-table-column 
            prop="operation" 
            label="操作">
            <template slot-scope="scope">
              <el-button @click="onDelete([scope.row.path])" type="danger">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>
  </div>
</template>
  
<script>
import tarStream from 'tar-stream';
import tar from 'tar-js';
import buffer from 'buffer/';
import bl from 'bl';
export default {
  data() {
    return {
      singleFile: [], //files uploading
      folderFiles: [],
      tarData: null,
      selectedFiles: [],
      uploaded_files:[], //已上传的文件
      container_info: {},
      path: '',
      listLoading: true,
    };
  },
  methods: {
    handleSelectionChange(selected) {
      this.selectedFiles = selected.map(file => file.path);
    },
    loadFiles(name){
      this.listLoading = true
      const formData = new FormData()
      let user_id = localStorage.getItem('user_id')
      formData.append('user_id', user_id)
      formData.append('container_name', name)
      this.$axios({
        method: 'post',
        url: '/teacher/load_files/',
        data: formData,
      }).then(res => {
        console.log(res)
        this.uploaded_files = res.data.data
        this.listLoading = false
      })
      this.files = []
    },
    handleFileUpload() {
      this.listLoading = true
      let filesArray = Array.from(this.$refs.folderFiles.files);
      let filePromises = filesArray.map(file => {
        return new Promise((resolve, reject) => {
            let reader = new FileReader();
            reader.onload = () => {
            resolve({ name: file.webkitRelativePath, data: reader.result });
            };
            reader.onerror = reject;
            reader.readAsArrayBuffer(file);
        });
        });

      Promise.all(filePromises).then(fileDataArray => {
        let pack = tarStream.pack();

        for(let fileData of fileDataArray) {
            pack.entry({ name: fileData.name }, new Buffer(fileData.data));
        }

        pack.finalize();
        pack.pipe(bl((err, data) => {
            if (err) {
              console.error(err);
              return;
            }

            let blob = new Blob([data], { type: "application/x-tar" });
            let reader = new FileReader();
            reader.onloadend = () => {
              this.tarData = reader.result;
              // 在这里加入日志
            };
            reader.readAsArrayBuffer(blob);
            this.listLoading = false
          }));
        }).catch(error => {
          console.error(error);
        });
    },
    handleSingleFileUpload() {
        let filesArray = Array.from(this.$refs.singleFile.files);
        this.tarData = []; // Ensure it's set to array before usage
        let filePromises = filesArray.map(file => {
            return new Promise((resolve, reject) => {
                let reader = new FileReader();
                reader.onload = () => {
                    this.tarData.push({name: file.name, data: reader.result}); 
                    resolve();
                };
                reader.onerror = reject;
                reader.readAsArrayBuffer(file);
            });
        });

        Promise.all(filePromises).then(() => {
            console.log("All files have been read.");
        }).catch(error => {
            console.error(error);
        });
    },
    isSelectable(file) {
      // 这个函数决定哪些文件可以被选中
      // 不写代表允许所有文件被选中
      return true;
    },
    submitFile(){
        let formData = new FormData();
        let user_id = localStorage.getItem('user_id')
        let container_name = this.container_info.container_name
        let blob = new Blob([this.tarData], {type: "application/x-tar"}); 
        formData.append('tarFile', blob);
        formData.append('user_id', user_id);
        formData.append('container_name', container_name);
        formData.append('path', this.path);
        
        this.$axios({
          method: 'post',
          url: '/teacher/upload_file/',
          data: formData,
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        .then(response => {
          console.log(response);
          this.loadFiles(container_name);
          this.files = [];
          this.listLoading = false;
        })
        .catch(error => console.log(error));
    },

    submitSingleFile(){
        let formData = new FormData();
        let user_id = localStorage.getItem('user_id')
        let container_name = this.container_info.container_name
        for(let fileData of this.tarData) {
            let blob = new Blob([fileData], {type: "application/octet-stream"});  
            formData.append('files[]', blob, fileData.name);  
        }
        formData.append('user_id', user_id);
        formData.append('container_name', container_name);
        formData.append('path', this.path);

        this.$axios({
            method: 'post',
            url: '/teacher/upload_file/',
            data: formData,
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        })
        .then(response => {
          console.log(response);
          this.loadFiles(container_name);
          this.tarData = []; // Reset the tarData for next usage
          this.listLoading = false;
        })
        .catch(error => console.log(error));
    },
    onDelete(path){
      console.log(path)
      const formData = new FormData();
      let user_id = localStorage.getItem('user_id')
      let container_name = this.container_info.container_name
      formData.append('user_id', user_id)
      formData.append('container_name', container_name)
      formData.append('file_paths', JSON.stringify(path))
      this.$axios({
          method: 'post',
          url: '/teacher/delete_file/',
          data: formData,
        }).then(response => {
          console.log(response)
          this.loadFiles(container_name)
        })
          .catch(error => console.log(error));
    },
    onDeleteSelectedFiles(){
      console.log(this.selectedFiles)
      this.onDelete(this.selectedFiles); // Call onDelete with the paths of the selected files
    },
    search_container(){
      const formData = new FormData();
      let container_id = this.$route.query.container_id
      formData.append('container_id', container_id)
      this.$axios({
          method: 'post',
          url: '/teacher/search_container/',
          data: formData,
        }).then(response => {
          console.log(response)
          this.container_info = response.data.data
          this.loadFiles(response.data.data.container_name)
        })
          .catch(error => console.log(error));
    },
    handleEnter(){
      let url = this.container_info.container_url
      console.log(url)
      window.open(url, '_blank');
    },
    handleReturn(){
      this.$router.push('/manage/image')
    },
  },
  created(){
      this.search_container()
  },
}
</script>
  

<style lang="scss" scoped>
.detail {
  &-text {
    font-size: 20px;
    line-height: 36px;
    white-space: pre-wrap;
    display:flex;
  }
}
</style>