<template>
  <div>
    <div :class="{'hhh':synClass.pid=='0','sss':true,'ddd':synClass.pid !='0'}">
      <div class="row">
        <div class="col-md-1">
          <span style>
            <img :src="synClass.img" alt style="border-radius:50%;width:50px;height:50px" />
          </span>
        </div>
        <div class="col-md-1" style="line-height: 50px;">{{synClass.username}}</div>
      </div>
      <p style="text-indent: 2em;margin-top:20px;font-size:16px;color:#000">{{synClass.content}}</p>
      <div class="row">
        <div>
          <div class="col-md-10">{{synClass.create_time}}&nbsp;&nbsp;&nbsp;来自:</div>
          <div class="col-md-2">
            <a>
              <span @click="show(synClass)">回复</span>
            </a>
          </div>
        </div>
      </div>
    </div>
    <template v-if="synClass.children">
      <comments v-for="i in synClass.children" :synClass="i" :key="i"></comments>
    </template>
          <!-- 评论回复 -->
      <div class="modal fade askquestion-modal" id="coummm" tabindex="-1" role="dialog">
        <div class="modal-dialog" role="document">
          <div class="modal-content">
            <div class="modal-header">
              <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                <span aria-hidden="true">&times;</span>
              </button>
              <h4 class="modal-title">回复</h4>
            </div>
            <div class="modal-body words-ctrl">
              <form class="form-horizontal" action="/questions/">
                <input
                  name="_csrf_token"
                  type="hidden"
                  value="1483794941##be4fb68b276c5f7cb970936cb25985cd53b943d1"
                />

                <div class="form-group">
                  <label class="col-md-2 control-label">描述</label>
                  <div class="col-md-10">
                    <div class="tabpanel mkeditor">
                      <ul class="nav nav-tabs" role="tablist">
                        <li role="presentation" class="active">
                          <a href="#mkeditor-editor" role="tab" data-toggle="tab">编辑</a>
                        </li>
                        <li role="presentation">
                          <a
                            class="mkeditor-btn-view"
                            href="#mkeditor-viewer"
                            role="tab"
                            data-toggle="tab"
                          >预览</a>
                        </li>
                      </ul>
                      <div class="tab-content">
                        <div
                          class="tab-pane active mkeditor-editor"
                          id="mkeditor-editor"
                          role="tabpanel"
                        >
                          <div class="btn-group" role="group">
                            <button type="button" class="btn btn-default mkeditor-btn-bold">
                              <i class="fa fa-bold"></i>
                            </button>
                            <button type="button" class="btn btn-default mkeditor-btn-italic">
                              <i class="fa fa-italic"></i>
                            </button>
                            <button type="button" class="btn btn-default mkeditor-btn-link">
                              <i class="fa fa-link"></i>
                            </button>
                            <button type="button" class="btn btn-default mkeditor-btn-quote">
                              <i class="fa fa-quote-left"></i>
                            </button>
                            <button type="button" class="btn btn-default mkeditor-btn-code">
                              <i class="fa fa-code"></i>
                            </button>
                            <button
                              id="mkeditor-pickfile"
                              type="button"
                              class="btn btn-default mkeditor-btn-img"
                            >
                              <i class="fa fa-image"></i>
                            </button>

                            <button type="button" class="btn btn-default mkeditor-btn-listol">
                              <i class="fa fa-list-ol"></i>
                            </button>
                            <button type="button" class="btn btn-default mkeditor-btn-listul">
                              <i class="fa fa-list-ul"></i>
                            </button>
                          </div>
                          <div class="btn-group pull-right" role="group">
                            <a
                              style="font-size:12px; color:#666; text-decoration:underline;"
                              href="/questions/764"
                              target="_blank"
                            >
                              <i class="fa fa-question-circle"></i>Markdown 语法
                            </a>
                          </div>
                          <textarea
                            name="content"
                            class="content"
                            min="0"
                            max="20000"
                            placeholder="推荐使用 Markdown 语法，至少输入 5 个字"
                            v-model="content"
                          ></textarea>
                          <div class="help-block"></div>
                        </div>
                        <div
                          class="tab-pane mkeditor-viewer markdown-body"
                          id="mkeditor-viewer"
                          role="tabpanel"
                        >
                          <div></div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </form>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-default" data-dismiss="modal">取消</button>
              <button
                type="button"
                class="submit-question btn btn-primary"
                data-dismiss="modal"
                @click="backWrite"
              >提交</button>
            </div>
          </div>
        </div>
      </div>
  </div>
</template>

<script>
export default {
  name: "comments",
  props: {
    synClass: {
      type: Object,
      default: function() {
        return {};
      }
    }
  },
  data() {
    return {
       user_id:localStorage.getItem("user_id"),
        course_id:'',
        content:'',
        pid:'',
        conmmitdict:''
    };
  },
  methods: {
    show: function(i) {
      var user_id = localStorage.getItem("user_id");
      if (user_id) {
        $("#coummm").modal("show");
        this.conmmitdict = i.id;
        this.course_id = i.course_id;
        console.log(this.conmmitdict)
      } else {
        $("#sign-modal").modal("show");
      }
    },

    backWrite: function() {
      this.axios
        .post("/api/comment/", {
          pid: this.conmmitdict,
          content: this.content,
          user_id: this.user_id,
          course_id: this.course_id
        })
        .then(res => {
          alert("评论成功");
        });
    },
  }
};
</script>

<style scoped>
.hhh {
  background-color: #f2f2f2;
}
.sss {
  padding: 25px;
  border-bottom: 1px solid #ccc;
}
.ddd {
  margin-left: 10px;
}
</style>