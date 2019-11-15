<template>
    <div id="wangeditor">
      <div ref="editorElem" style="text-align:left;"></div>
      <button style="text-align:right;"  @click="sendMesToParent">提交</button>
  </div>
</template>
<script>
import E from "wangeditor";
export default {
  name: "Editor",
  data() {
    return {
      editor: null,
      editorContent: ""
    };
  },
  // catchData是一个类似回调函数，来自父组件，当然也可以自己写一个函数，主要是用来获取富文本编辑器中的html内容用来传递给服务端
  props: ["catchData"], // 接收父组件的方法
  mounted() {
    this.editor = new E(this.$refs.editorElem);
    // 编辑器的事件，每次改变会获取其html内容
    this.editor.customConfig.onchange = html => {
      this.editorContent = html;
    //   this.catchDatas(this.editorContent); // 把这个html通过catchData的方法传入父组件
    };
    this.editor.customConfig.menus = [
      // 菜单配置
      "head", // 标题
      "bold", // 粗体
      "fontSize", // 字号
      "fontName", // 字体
      "italic", // 斜体
      "underline", // 下划线
      "strikeThrough", // 删除线
      "foreColor", // 文字颜色
      "backColor", // 背景颜色
      "link", // 插入链接
      "list", // 列表
      "justify", // 对齐方式
      "quote", // 引用
      "emoticon", // 表情
      "image", // 插入图片
      "table", // 表格
      "code", // 插入代码
      "undo", // 撤销
      "redo" // 重复
    ];
     // 上传图片 配置服务器端地址
    this.editor.customConfig.uploadImgServer = '/api/img_upload'
    this.editor.customConfig.withCredentials = true
    // 关闭粘贴内容中的样式
    this.editor.customConfig.pasteFilterStyle = false
    // 忽略粘贴内容中的图片
    this.editor.customConfig.pasteIgnoreImg = true

    this.editor.customConfig.debug = true

    this.editor.customConfig.uploadImgMaxSize = 3 * 1024 * 1024; // 将图片大小限制为 3M
    //上传图片时，可自定义filename，即在使用formdata.append(name, file)添加图片文件时，自定义第一个参数。
    this.editor.customConfig.uploadFileName = 'yourFileName'
    //自定义上传图片事件
    this.editor.customConfig.uploadImgHooks = {
		before : function(xhr, editor, files) {
			
		},
		success : function(xhr, editor, result) {
			console.log("上传成功");
		},
		fail : function(xhr, editor, result) {
			console.log("上传失败,原因是"+result);
		},
		error : function(xhr, editor) {
			console.log("上传出错");
		},
		timeout : function(xhr, editor) {
			console.log("上传超时");
		}}
    this.editor.create(); // 创建富文本实例

  },
  methods: {
      sendMesToParent(){
          console.log('传递前',this.editorContent)
          this.$emit('listentochildevents',this.editorContent)
      },
      sss(){
        // 读取 html
        console.log(this.editorContent)
      }
      
  },
};
</script>
<style scoped>
.w-e-text-container{
    background-color: #fff;
}

.w-e-text{
    background-color: #fff;
}
</style>