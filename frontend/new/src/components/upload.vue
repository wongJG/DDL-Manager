<template>
  <div id="app" align='center'>
    
    <!-- Load the avatar if exist -->
     <b-img-lazy width="120px" v-if="imageUrl" rounded="circle"
      :src="imageUrl"
      alt="" />
      <br><br>
    
    <!-- Upload bottom -->
    <el-upload ref="upload"
      action="#"
      :show-file-list="false"
      :http-request="uploadFile">
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
    // Send uploaded file to back-end
    async uploadFile(params) {
      const form = new FormData();
      form.append('file', params.file);                // Avatar file
      form.append('id', this.$session.get('userid'));  // Uploaded user
      const res = await axios.post('api/upload', form);
      console.log(res);
      this.imageUrl = res.data;
      this.$router.go(0);
    },
  },
  // try to get the user avatar from backend when loading the page
  created() {
    const url = `api/uploads/${this.$session.get('userid')}`;
    this.imageUrl = url;
  },
};
</script>
