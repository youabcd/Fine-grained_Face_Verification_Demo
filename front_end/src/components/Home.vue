<template>
  <div>
    <div></div>
    <div style="display: flex;justify-content: center">
      <el-upload
        class="avatar-uploader"
        action="/axiosapi/original_image"
        name="img"
        :show-file-list="false"
        :on-success="handleAvatarSuccess1"
        :before-upload="beforeAvatarUpload">
        <div v-if="image1" class="showImage">
          <img :src="image1" class="avatar">
          <div class="mask">
            <i class="el-icon-edit" @click.stop="changeImage(1)"
               style="color: white;font-size: 24px;margin-top: 52px"></i>
            <i class="el-icon-delete" @click.stop="deleteImage(1)"
               style="color: white;font-size: 24px;margin-top: 52px;margin-left: 15px"></i>
          </div>
        </div>
        <div v-else>
          <i class="el-icon-plus avatar-uploader-icon"></i>
          <div style="font-size: 12px;margin-top: 5px">点击上传图片1</div>
        </div>
      </el-upload>
      <el-upload
        class="avatar-uploader"
        action="/axiosapi/original_image"
        name="img"
        :show-file-list="false"
        :on-success="handleAvatarSuccess2"
        :before-upload="beforeAvatarUpload">
        <div v-if="image2" class="showImage">
          <img :src="image2" class="avatar">
          <div class="mask">
            <i class="el-icon-edit" @click.stop="changeImage(2)"
               style="color: white;font-size: 24px;margin-top: 52px"></i>
            <i class="el-icon-delete" @click.stop="deleteImage(2)"
               style="color: white;font-size: 24px;margin-top: 52px;margin-left: 15px"></i>
          </div>
        </div>
        <div v-else>
          <i class="el-icon-plus avatar-uploader-icon"></i>
          <div style="font-size: 12px;margin-top: 5px">点击上传图片2</div>
        </div>
      </el-upload>
    </div>

    <el-dialog title="图片剪裁" :visible.sync="openCropper" width="600px" center style="text-align: center">
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

    <div v-show="ifResult" class="showResult">
      <div>
        <span>result: </span>{{result}}
      </div>
      <div>
        <span>cosine similarity: </span>{{cs}}
      </div>
    </div>
    <div v-show="!ifResult" class="showResult"></div>

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
      openCropper: false,
      loading: false,
      image1: '',
      image2: '',
      whichImage: 1,
      result: '',
      cs: 1,
      ifResult: false,
      origin1: '',
      origin2: '',
    }
  },
  methods: {
    postPicture() {
      if (this.image1 === '') {
        this.$message.error("请传入图片1")
        return
      }
      if (this.image2 === '') {
        this.$message.error("请传入图片2")
        return
      }
      let data = new FormData();
      data.append('img1', this.image1);
      data.append('img2', this.image2);
      this.$axios.post('/axiosapi/cropped_image', data, {})
        .then((res) => {
          console.log(res)
          this.result = res.data['result']
          this.cs = res.data['cs']
          this.ifResult = true
          // this.$message.success(this.cs)
        }).catch((err) => {
        console.log(err)
      })
    },
    handleAvatarSuccess1(res, file, fileList) {
      this.$nextTick(() => {
        this.origin1 = URL.createObjectURL(file.raw)
        this.option.img = URL.createObjectURL(file.raw)
        this.whichImage = 1
        this.openCropper = true
      })
    },
    handleAvatarSuccess2(res, file, fileList) {
      this.$nextTick(() => {
        this.origin2 = URL.createObjectURL(file.raw)
        this.option.img = URL.createObjectURL(file.raw)
        this.whichImage = 2
        this.openCropper = true
      })
    },
    beforeAvatarUpload(file) {
      this.ifResult = false
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
        if (this.whichImage === 1) {
          this.image1 = data
        } else if (this.whichImage === 2) {
          this.image2 = data
        }
      });
      this.openCropper = false
    },
    changeImage(k) {
      if (k === 1) {
        this.whichImage = 1
        this.option.img = this.origin1
        this.openCropper = true
      } else {
        this.whichImage = 2
        this.option.img = this.origin2
        this.openCropper = true
      }
    },
    deleteImage(k) {
      if (k === 1) {
        this.image1 = ''
      } else {
        this.image2 = ''
      }
    },
  }
}
</script>

<style>
.cropperContent {
  margin-left: 25px;
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
  /*width: 128px;*/
  /*height: 128px;*/
  /*line-height: 128px;*/
  margin-top: 50px;
  text-align: center;
}

.avatar {
  width: 128px;
  height: 128px;
  display: block;
  position: absolute;
}

.mask {
  position: absolute;
  height: 128px;
  width: 128px;
  background-color: black;
  opacity: 0;
}

.showImage:hover .mask {
  opacity: 0.6;
  transition: all .4s ease;
}

.showResult {
  height: 5vh;
  text-align: center;
}
</style>
