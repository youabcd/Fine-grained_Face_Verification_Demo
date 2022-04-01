<template>
  <div>
    <el-upload
      action="/axiosapi/"
      name="img1"
      list-type="picture-card"
      :on-success="handleAvatarSuccess"
      :before-upload="beforeAvatarUpload"
      :on-preview="handlePictureCardPreview"
      :on-remove="handleRemove">
      <i class="el-icon-plus"></i>
    </el-upload>
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
  name: 'HelloWorld',
  components: {},
  data() {
    return {
      imageUrl: '',
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
      fileInfo: [],
      image1: '',
      image2: '',
    }
  },
  methods: {
    postPicture() {
      let data = new FormData();
      data.append('img1', '123');
      data.append('img2', '456');
      this.$axios.post('/axiosapi/', data, {})
        .then((res) => {
          console.log(res)
        }).catch((err) => {
        console.log(err)
      })
    },
    getBase64(img, callback){
      const reader = new FileReader()
      reader.addEventListener("load", ()=>callback(reader.result))
      reader.readAsDataURL(img)
    },
    handleAvatarSuccess(res, file, fileList) {
      this.$nextTick(() => {
        console.log("res", res)
        console.log("file", file)
        this.option.img = URL.createObjectURL(file.raw)
        this.fileInfo = res
        this.imageUrl = this.option.img
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
      this.$refs.cropper.getCropBlob((data) => {
        let fileName = 'goods' + this.fileInfo.uid
        // this.loading = true
        this.imageUrl = data
        this.openCropper = false
      })
    },
    handleRemove(file, fileList) {
      console.log(file, fileList);
    },
    handlePictureCardPreview(file) {
      this.dialogImageUrl = file.url;
      this.dialogVisible = true;
    },
    getCropData() {
      this.$refs.cropper.getCropData(data => {
        console.log(data)
      })
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
}

.avatar-uploader .el-upload:hover {
  border-color: #409EFF;
}

.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  line-height: 178px;
  text-align: center;
}

.avatar {
  width: 178px;
  height: 178px;
  display: block;
}
</style>
