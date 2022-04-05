<template>
  <div>
    <div class="header">
      <div style="cursor: pointer;display: flex;margin-left: 40px" @click="gotoHome">
        <div style="margin-top: 5px;">
          <el-image
            style="width: 40px; height: 40px"
            :src="require('../../static/logo.svg')"
            :fit="fit"></el-image>
        </div>
        <div style="font-size: 22px;font-weight: bold;margin-top: 13px;margin-left: 5px">细粒度人脸认证</div>
      </div>

      <div style="display: flex">
        <div style="display: flex;cursor: pointer" @click="gotoGit1">
          <div>
            <el-image
              style="width: 26px; height: 26px;margin-top: 18px"
              :src="require('../../static/github.svg')"
              :fit="fit"></el-image>
          </div>
          <div style="margin-top: 18px;margin-left: 5px">
            <el-link :underline="false"><span style="font-size: 18px">演示程序代码</span></el-link>
          </div>
        </div>
        <div style="margin-left: 35px;margin-right: 40px;display: flex;cursor:pointer" @click="gotoGit2">
          <div>
            <el-image
              style="width: 26px; height: 26px;margin-top: 18px"
              :src="require('../../static/github.svg')"
              :fit="fit"></el-image>
          </div>
          <div style="margin-top: 18px;margin-left: 5px">
            <el-link :underline="false"><span style="font-size: 18px">算法代码</span></el-link>
          </div>
        </div>
      </div>
    </div>
    <div class="main">
      <el-row>
        <el-col :span=12>
          <div class="leftContent">
            <el-carousel height="380px" style="margin-top: 15px" :autoplay="true" indicator-position="outside">
              <el-carousel-item>
                <div style="margin-top: 20px">
                  <el-image
                    style="width: 500px; height: 200px"
                    :src="require('../../static/show1.png')"
                    :fit="fit"></el-image>
                </div>
                <div style="font-size: 18px;margin-top: 50px;text-align: left;margin-left: 50px;margin-right: 50px">
                  本网站是基于余弦相似度学习的细粒度人脸认证的演示网站。在右侧上传两张人脸图像，点击开始检测即可得到两种图像为同一人还是双胞胎的预测结果。
                </div>
              </el-carousel-item>
              <el-carousel-item style="display: flex;justify-content: space-between">
                <div style="margin-top: 50px;margin-left: 50px">
                  <el-image
                    style="width: 200px; height: 200px"
                    :src="require('../../static/show_crop.jpg')"
                    :fit="fit"></el-image>
                </div>
                <div style="font-size: 18px;margin-left: 25px;margin-right: 50px;margin-top: 120px;text-align: left">
                  将上传的图片进行裁剪时，请参考左侧所示的截取方式，将人脸尽可能包括。
                </div>
              </el-carousel-item>
            </el-carousel>
          </div>
        </el-col>

        <el-col :span=12 style="text-align: left">
          <div class="rightContent">
            <div style="display: flex;">
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
                       style="color: white;font-size: 24px;margin-top: 77px"></i>
                    <i class="el-icon-delete" @click.stop="deleteImage(1)"
                       style="color: white;font-size: 24px;margin-top: 77px;margin-left: 15px"></i>
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
                       style="color: white;font-size: 24px;margin-top: 77px"></i>
                    <i class="el-icon-delete" @click.stop="deleteImage(2)"
                       style="color: white;font-size: 24px;margin-top: 77px;margin-left: 15px"></i>
                  </div>
                </div>
                <div v-else>
                  <i class="el-icon-plus avatar-uploader-icon"></i>
                  <div style="font-size: 12px;margin-top: 5px">点击上传图片2</div>
                </div>
              </el-upload>
            </div>

            <div v-show="!ifResult" class="showResult">
              <div>
                <span style="color:#606266;">result:&nbsp;</span>
                <span v-if="result==='same'" style="color: #67C23A">{{result}}</span>
                <span v-else style="color:#F56C6C;">{{result}}</span>
              </div>
              <div style="margin-top: 10px">
                <span style="color: #606266">cosine similarity:&nbsp;</span>
                <span>{{cs}}</span>
              </div>
            </div>
            <div v-show="ifResult" class="showResult"></div>

            <div>
              <el-button type="primary" style="margin-left: 170px" @click="postPicture">开始检测</el-button>
            </div>
          </div>
        </el-col>
      </el-row>
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
        result: 'same',
        cs: 1.0,
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
        this.ifResult = false
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
        this.ifResult = false
        if (k === 1) {
          this.image1 = ''
        } else {
          this.image2 = ''
        }
      },
      gotoHome(){
        this.$router.push({
          path:'/'
        })
      },
      gotoGit1(){
        window.open('https://github.com/youabcd/Fine-grained_Face_Verification_Demo')
      },
      gotoGit2(){
        window.open('https://github.com/youabcd/Face_Verification')
      },
    }
  }
</script>

<style>
  .header {
    width: 100%;
    height: 50px;
    background-color: white;
    display: flex;
    justify-content: space-between;
  }

  .main {
    margin-top: 120px;
  }

  .leftContent {
    width: 85%;
    margin-left: 10%;
  }

  .rightContent {
    padding: 20px;
    border-left: 1px solid #C0C4CC;
    height: 400px;
  }

  .cropperContent {
    margin-left: 100px;
    width: 350px;
    height: 350px;
    background: pink;
  }

  .avatar-uploader .el-upload {
    border: 1px dashed #d9d9d9;
    border-radius: 6px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
    margin: 20px;
    width: 178px;
    height: 178px;
  }

  .avatar-uploader .el-upload:hover {
    border-color: #409EFF;
  }

  .avatar-uploader-icon {
    font-size: 28px;
    color: #8c939d;
    margin-top: 74px;
    text-align: center;
  }

  .avatar {
    width: 178px;
    height: 178px;
    display: block;
    position: absolute;
  }

  .mask {
    position: absolute;
    height: 178px;
    width: 178px;
    background-color: black;
    opacity: 0;
  }

  .showImage:hover .mask {
    opacity: 0.5;
    transition: all .4s ease;
  }

  .showResult {
    height: 80px;
    text-align: left;
    margin-left: 150px;
    font-size: 22px;
  }

  /*.el-carousel__item:nth-child(2n) {*/
  /*  background-color: #99a9bf;*/
  /*}*/

  /*.el-carousel__item:nth-child(2n+1) {*/
  /*  background-color: #d3dce6;*/
  /*}*/
</style>
