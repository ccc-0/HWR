<template>
  <div id="app">
    <div class="top-left">
      <div class="paint">手写板</div>
      <canvas
        id="canvas"
        ref="canvas"
        class="canvas"
        width="400"
        height="400"
        @mousedown="penMouseDown"
        @mouseup="penMouseUp"
        @mouseleave="penMouseLeave"
        @mousemove="penMouseMove"
      >您的浏览器不支持canvas技术,请升级浏览器!</canvas>
    </div>
    <div class="top-right">
      <div class="display-result">识别结果</div>
      <div class="display">
        <h1>{{result}}</h1>
      </div>
      <div class="buttons">
        <span id="clear" @click="canvasClear">清空</span>
        <span id="save" @click="saveAsImg">识别</span>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
// axios.defaults.baseURL = "http://127.0.0.1:8000";
axios.defaults.baseURL = "http://127.0.0.1:11000";
// axios.defaults.baseURL = "http://192.168.1.71:11000";
export default {
  name: "App",
  components: {},
  data() {
    return {
      canvas: null,
      obj: {},
      emptyCanvas: null,
      result: "",
      compositeOperation:null,
    };
  },
  created() {},
  mounted() {
    this.init();
    this.canvasInit();
    this.canvasClear();
    this.initPen();
  },
  methods: {
    init() {
      this.canvas = this.$refs.canvas;
      this.obj = {
        canvas: this.canvas,
        context: this.canvas.getContext("2d"),
        isWrite: false, //是否开始
        lastWriteTime: -1,
        lastWriteSpeed: 0,
        lastWriteWidth: 0,
        canvasWidth: 400, //canvas宽高
        canvasHeight: 400,
        isShowBorder: false, //是否显示网格
        bgColor: "#fff", //背景色
        borderWidth: 2, //	网格线宽度
        borderColor: "#fff", //网格颜色
        lastPoint: {}, //
        writeWidth: 2, //基础轨迹宽度
        maxWriteWidth: 30, // 写字模式最大线宽
        minWriteWidth: 1, // 写字模式最小线宽
        writeColor: "#000", //	轨迹颜色
        isWriteName: false //签名模式
      };
    },
    // 初始化画笔
    initPen() {
      this.obj.borderWidth = 10;
      this.obj.writeWidth = 20;
      this.obj.borderColor = "#ff6666";
      this.obj.isWriteName = true; //签名模式
      
    },
    // 初始化画板
    canvasInit() {
      this.canvas.width = this.obj.canvasWidth;
      this.canvas.height = this.obj.canvasHeight;
      this.emptyCanvas = this.canvas.toDataURL("image/png");
    },
    // 保存图片
    saveAsImg() {
      let image = new Image();
      //add background-color
      this.compositeOperation = this.obj.context.globalCompositeOperation;
      this.obj.context.globalCompositeOperation = "destination-over";
      this.obj.context.fillStyle = this.obj.bgColor;
      this.obj.context.fillRect(0,0,this.obj.canvasWidth,this.obj.canvasHeight);

      image.src = this.canvas.toDataURL("image/png");

      if (image.src == this.emptyCanvas) {
        alert("请先书写");
      } else {
        //add background-color
        
        // this.obj.context.clearRect(0,0,this.obj.canvasWidth,this.obj.canvasHeight);
        this.obj.context.putImageData(this.obj.context.getImageData(0, 0,this.obj.canvasWidth,this.obj.canvasHeight), 0,0);
        this.obj.context.globalCompositeOperation = this.compositeOperation;
        
        console.log("提交的内容===>", image.src);
        let blob = this.dataURItoBlob(image.src);
        let fd = new FormData();
        fd.append("file", blob); //fileData为自定义
        fd.append("fileName", "123png"); //fileName为自定义，名字随机生成或者写死，看需求
        let options = {
          url: "/HRI/hri/",
          data: fd,
          method: "post",
          contentType: false,
          headers: { "Content-Type": "multipart/form-data" }
        };
        axios(options)
          .then(result => {
            // console.log('result:',result);

            this.result = result.data.result;
          })
          .catch(error => {
            this.$notify.error({
              title: "网络错误",
              message: "请求数据失败"
            });
          });
      }
    },
    // dataURItoBlob
    dataURItoBlob(base64Data) {
      let byteString;
      if (base64Data.split(",")[0].indexOf("base64") >= 0)
        byteString = atob(base64Data.split(",")[1]);
      else byteString = unescape(base64Data.split(",")[1]);
      let mimeString = base64Data
        .split(",")[0]
        .split(":")[1]
        .split(";")[0];
      let ia = new Uint8Array(byteString.length);
      for (let i = 0; i < byteString.length; i++) {
        ia[i] = byteString.charCodeAt(i);
      }
      return new Blob([ia], { type: mimeString });
    },
    // 清空画板
    canvasClear() {
      // console.log('canvasClear');

      this.result = "";

      this.obj.context.save();
      this.obj.context.strokeStyle = "#fff";
      this.obj.context.clearRect(
        0,
        0,
        this.obj.canvasWidth,
        this.obj.canvasHeight
      );
      if (this.obj.isShowBorder && !this.obj.isWriteName) {
        this.obj.context.beginPath();
        let size = this.obj.borderWidth / 2;
        //画外面的框
        this.obj.context.moveTo(size, size);
        this.obj.context.lineTo(this.obj.canvasWidth - size, size);
        this.obj.context.lineTo(
          this.obj.canvasWidth - size,
          this.obj.canvasHeight - size
        );
        this.obj.context.lineTo(size, this.obj.canvasHeight - size);
        this.obj.context.closePath();
        this.obj.context.lineWidth = this.obj.borderWidth;
        this.obj.context.strokeStyle = this.obj.borderColor;
        this.obj.context.stroke();
        //画里面的框
        this.obj.context.moveTo(0, 0);
        this.obj.context.lineTo(this.obj.canvasWidth, this.obj.canvasHeight);
        this.obj.context.lineTo(
          this.obj.canvasWidth,
          this.obj.canvasHeight / 2
        );
        this.obj.context.lineTo(
          this.obj.canvasWidth,
          this.obj.canvasHeight / 2
        );
        this.obj.context.lineTo(0, this.obj.canvasHeight / 2);
        this.obj.context.lineTo(0, this.obj.canvasHeight);
        this.obj.context.lineTo(this.obj.canvasWidth, 0);
        this.obj.context.lineTo(this.obj.canvasWidth / 2, 0);
        this.obj.context.lineTo(
          this.obj.canvasWidth / 2,
          this.obj.canvasHeight
        );
        this.obj.context.stroke();
      }
      this.obj.context.restore();
    },
    // 轨迹样式
    writeContextStyle() {
      this.obj.context.beginPath();
      this.obj.context.strokeStyle = this.obj.writeColor;
      this.obj.context.lineCap = "round";
      this.obj.context.lineJoin = "round";
    },
    // 轨迹宽度
    setLineWidth() {
      let nowTime = new Date().getTime();
      let diffTime = nowTime - this.obj.lastWriteTime;
      this.obj.lastWriteTime = nowTime;
      let returnNum =
        this.obj.minWriteWidth +
        ((this.obj.maxWriteWidth - this.obj.minWriteWidth) * diffTime) / 30;
      if (returnNum < this.obj.minWriteWidth) {
        returnNum = this.obj.minWriteWidth;
      } else if (returnNum > this.obj.maxWriteWidth) {
        returnNum = this.obj.maxWriteWidth;
      }

      returnNum = returnNum.toFixed(2);
      //写字模式和签名模式
      if (this.obj.isWriteName) {
        this.obj.context.lineWidth = this.obj.writeWidth;
      } else {
        this.obj.context.lineWidth = this.obj.lastWriteWidth =
          (this.obj.lastWriteWidth / 4) * 3 + returnNum / 4;
      }
    },
    // 写开始
    writeBegin(point) {
      this.obj.isWrite = true;
      this.obj.lastWriteTime = new Date().getTime();
      this.obj.lastPoint = point;
      this.writeContextStyle();
    },
    // 绘制轨迹
    writing(point) {
      this.obj.context.beginPath();
      this.obj.context.moveTo(this.obj.lastPoint.x, this.obj.lastPoint.y);
      this.obj.context.lineTo(point.x, point.y);
      this.setLineWidth();
      this.obj.context.stroke();
      this.obj.lastPoint = point;
      this.obj.context.closePath();
    },
    // 写结束
    writeEnd() {
      this.obj.isWrite = false;
    },
    //事件监听
    penMouseDown(e) {
      console.log("penMouseDown:", e);

      let point = {
        x: e.offsetX || e.clientX,
        y: e.offsetY || e.clientY
      };
      this.writeBegin(point);
    },
    penMouseUp(e) {
      console.log("penMouseUp:", e);
      let point = {
        x: e.offsetX,
        y: e.offsetY
      };
      this.writeEnd(point);
    },
    penMouseLeave(e) {
      let point = {
        x: e.offsetX,
        y: e.offsetY
      };
      this.writeEnd(point);
    },
    penMouseMove(e) {
      if (this.obj.isWrite) {
        let point = {
          x: e.offsetX,
          y: e.offsetY
        };

        this.writing(point);
      }
    }
  }
};
</script>

<style>
* {
  margin: 0;
  padding: 0;
}
#app {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  height: 100%;
}

/* top-left start*/
.top-left {
  position: absolute;
  right: 0;
}
.paint {
  color: #3a3b67;
  background-color: rgba(218, 223, 247, 0.795);
  margin-top: 10%;
  height: 30px;
  line-height: 30px;
  width: 80px;
  text-align: center;
  border-radius: 5px 5px 0 0;
}
.canvas {
  /*width: 100%;*/
  display: block;
  /* border: 1px solid lightblue; */
  background-color: #fff;
  box-shadow: 2px 2px 5px #464545;
  margin: 0 5px 0 0;
}
/* top-left end*/

/* top-right start */
.top-right {
  position: absolute;
  left: 0;
}
.display-result {
  color: #3a3b67;
  background-color: rgba(218, 223, 247, 0.795);
  margin-top: 10%;
  height: 30px;
  line-height: 30px;
  width: 80px;
  text-align: center;
  border-radius: 5px 5px 0 0;
}
.display {
  width: 400px;
  height: 400px;
  text-align: center;
  line-height: 400px;
  /* float: right; */
  /* position: absolute; */
  left: 450px;
  top: 21px;
  /* border: 1px solid red; */
  background-color: rgb(245, 243, 243);
  box-shadow: 2px 2px 5px #464545;
  margin: 0 0 0 0;
  font-size: 180px;
  color: #413e3e;
}
/* top-right end */

.buttons {
  position: absolute;
  width: 150px;
  left: 250px;
  /* right: 0; */
  right: 0;
  /* margin-right: 0; */
}
#clear,
#save {
  display: inline-block;
  padding: 5px 10px;
  width: 50px;
  height: 15px;
  line-height: 15px;
  border: 1px solid #eee;
  background: #ebedee;
  background: #fff;
  color: #3a3b67;
  border-radius: 10px;
  text-align: center;
  margin: 10px auto;
  cursor: pointer;
}
</style>
