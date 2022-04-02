<template>
  <div>
    <div style="display: flex;justify-content: center">
      <el-upload
        class="avatar-uploader"
        action="/axiosapi/original_image"
        name="img"
        :show-file-list="false"
        :on-success="handleAvatarSuccess1"
        :before-upload="beforeAvatarUpload">
        <img v-if="image1" :src="image1" class="avatar">
        <i v-else class="el-icon-plus avatar-uploader-icon"></i>
      </el-upload>
      <el-upload
        class="avatar-uploader"
        action="/axiosapi/original_image"
        name="img"
        :show-file-list="false"
        :on-success="handleAvatarSuccess2"
        :before-upload="beforeAvatarUpload">
        <img v-if="image2" :src="image2" class="avatar">
        <i v-else class="el-icon-plus avatar-uploader-icon"></i>
      </el-upload>
    </div>

    <el-dialog :visible.sync="dialogVisible">
      <img width="100%" :src="dialogImageUrl" alt="">
    </el-dialog>

    <el-dialog title="图片剪裁" :visible.sync="openCropper" append-to-body>
      <div class="cropperContent">
        <vueCropper
          ref="cropper"
          :img="option.img"
          :outputSize="option.size"
          :outputType="option.outputType"
          :autoCrop="option.autoCrop"
          :autoCropWidth="option.cropWidth"
          :autoCropHeight="option.cropHeight"
        ></vueCropper>
      </div>
      <div slot="footer">
        <el-button @click="openCropper = false">取消</el-button>
        <el-button type="primary" @click="finishCrop" :loading="loading">确认</el-button>
      </div>
    </el-dialog>

    <div>
      <el-button type="primary" @click="postPicture">开始检测</el-button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Home',
  components: {},
  data() {
    return {
      option: {
        img: '',
        size: 0.8,
        outputType: 'jpeg',
        autoCrop: true,
        cropWidth: 64,
        cropHeight: 64,
      },
      dialogImageUrl: '',
      dialogVisible: false,
      openCropper: false,
      loading: false,
      image1: '',
      image2: '',
      whichImage: 1,
      result: '',
      cs: 1,
    }
  },
  methods: {
    postPicture() {
      if(this.image1 === ''){
        this.$message.error("请传入图片1")
        return
      }
      if(this.image2 === ''){
        this.$message.error("请传入图片2")
        return
      }
      let data = new FormData();
      data.append('img1', this.image1);
      data.append('img2', this.image2);
      this.$axios.post('/axiosapi/cropped_image', data, {})
        .then((res) => {
          console.log(res)
          this.result=res.data['result']
          this.cs=res.data['cs']
          this.$message.success(this.cs)
        }).catch((err) => {
        console.log(err)
      })
    },
    handleAvatarSuccess1(res, file, fileList) {
      this.$nextTick(() => {
        console.log("res", res)
        console.log("file", file)
        this.option.img = URL.createObjectURL(file.raw)
        this.whichImage = 1
        this.openCropper = true
      })
    },
    handleAvatarSuccess2(res, file, fileList) {
      this.$nextTick(() => {
        console.log("res", res)
        console.log("file", file)
        this.option.img = URL.createObjectURL(file.raw)
        this.whichImage = 2
        this.openCropper = true
      })
    },
    beforeAvatarUpload(file) {
      const isJPG = file.type === 'image/jpeg' || file.type === 'image/png';
      const isLt2M = file.size / 1024 / 1024 < 2;

      if (!isJPG) {
        this.$message.error('上传头像图片只能是 JPG 格式!');
      }
      if (!isLt2M) {
        this.$message.error('上传头像图片大小不能超过 2MB!');
      }
      return isJPG && isLt2M;
    },
    finishCrop() {
      this.$refs.cropper.getCropData((data) => {
        console.log("crop data", data)
        if(this.whichImage === 1){
          this.image1 = data
        }
        else if(this.whichImage === 2){
          this.image2 = data
        }
      });
      this.openCropper = false
    },
    handleRemove(file, fileList) {
      console.log(file, fileList);
    },
    handlePictureCardPreview(file) {
      this.dialogImageUrl = file.url;
      this.dialogVisible = true;
    },
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
.cropperContent{
  text-align: center;
  width: 500px;
  height: 500px;
  background: pink;
}

.avatar-uploader .el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  margin: 20px;
  width: 128px;
  height: 128px;
}

.avatar-uploader .el-upload:hover {
  border-color: #409EFF;
}

.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 128px;
  height: 128px;
  line-height: 128px;
  text-align: center;
}

.avatar {
  width: 128px;
  height: 128px;
  display: block;
}
</style>
