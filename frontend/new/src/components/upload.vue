<template>
  <div id="app" align='center'>
     <b-img width="120px" v-if="imageUrl" rounded="circle"
      :src="imageUrl"
      alt="" />
      <br><br>
    <el-upload ref="upload"
      action="#"
      :show-file-list="false"
      :http-request="uploadFile">
      <!-- <el-button>Upload</el-button> -->
    </el-upload>
    <hr><br><br>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'app',

  data() {
    return {
      imageUrl: '',
    };
  },

  methods: {
    async uploadFile(params) {
      const form = new FormData();
      form.append('file', params.file);
      form.append('id', this.$session.get('userid'));
      const res = await axios.post('api/upload', form);
      console.log(res);
      this.imageUrl = res.data;
    },
  },
  created() {
    const url = `api/uploads/${this.$session.get('userid')}`;
    this.imageUrl = url;
  },
};
</script>
