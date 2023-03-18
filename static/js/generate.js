$(function () {

    // 大纲生成的检索大纲
    $("#outline_outline_select").change(function() {
        if($(this).val() == 1 ) {
            $(function (){
                // 发送Ajax请求
                var title = $("#outline_title").val()
                var keywords = $("#outline_keywords").val()
                $.ajax({
                  url:"/get_outline/",
                  type:"post",
                  data:{'title': title, 'keywords': keywords},
                  dataType: 'json',
                  success:function (data) {
                      $("#outline_outline").val(data.outline)
                  },
                  error: function () {
                      $("#outline_outline").val("好像出问题了，请再试一次或联系管理员：bryanwang0702@163.com")
                  }
                })
            })
        }
        else if($(this).val() == 2 ) {
            $("#outline_outline").val("")
        }
    })

    // 摘要生成页面的检索摘要
    $("#abstract_select").change(function() {
        if($(this).val() == 1 ) {
            $(function (){
                // 发送Ajax请求
                var title = $("#abstract_title").val()
                var keywords = $("#abstract_keywords").val()
                $.ajax({
                    url:"/get_abstract/",
                    type:"post",
                    data:{'title': title, 'keywords': keywords},
                    dataType: 'json',
                    success:function (data) {
                        $("#abstract_abstract").val(data.abstract)
                    },
                    error: function () {
                        $("#abstract_abstract").val("好像出问题了，请再试一次或联系管理员：bryanwang0702@163.com")
                    }
                })
            })
        }
        else if($(this).val() == 2 ) {
            $("#abstract_abstract").val("")
        }
    })

    // 大纲生成的摘要检索
    $("#outline_abstract_div").hide();
    //给div添加change事件
    $("#outline_abstract_select").change(function() {
        if($(this).val() == 0 ) {
            $("#outline_abstract_div").hide();
            $("#outline_abstract").val("")
        } else if($(this).val() == 1 ) {
            $(function (){
                // 发送Ajax请求
                const title = $("#outline_title").val();
                const keywords = $("#outline_keywords").val();
                $.ajax({
                    url:"/get_abstract/",
                    type:"post",
                    data:{'title': title, 'keywords': keywords},
                    dataType: 'json',
                    success:function (data) {
                        $("#outline_abstract").val(data.abstract)
                    },
                    error: function () {
                        $("#outline_abstract").val("好像出问题了，请再试一次或联系管理员：bryanwang0702@163.com")
                    }
                })
            })
            $("#outline_abstract_div").show();
        }
        else if($(this).val() == 2 ) {
            $("#outline_abstract_div").show();
            $("#outline_abstract").val("");
        }
    })

    $("#title_submit").click(function () {
        // 发送Ajax请求
        var title = $("#title_title").val();
        var keywords = $("#title_keywords").val();
        const bt = document.getElementById("title_submit");
        bt.disabled = true;
        bt.innerText = "正在生成中...";
        $.ajax({
            url:"/titleGenerate/generate/",
            type:"post",
            data:{'title': title, 'keywords': keywords},
            dataType: 'json',
            success:function (data) {
                $("#title_output").val(data.article);
                // 加载完成后解除按钮的禁用
                bt.disabled = false;
                bt.innerText = "一键生成文章";
            },
            error:function () {
                $("#title_output").val("好像出问题了，请再试一次或联系管理员：bryanwang0702@163.com")
                // 加载完成后解除按钮的禁用
                bt.disabled = false;
                bt.innerText = "一键生成文章";
            }
        })

    })

    $("#abstract_submit").click(function () {
        // 发送Ajax请求
        var title = $("#abstract_title").val();
        var keywords = $("#abstract_keywords").val();
        var abstract = $("#abstract_abstract").val();
        const bt = document.getElementById("abstract_submit");
        bt.disabled = true;
        bt.innerText = "正在生成中...";
        $.ajax({
            url:"/abstractGenerate/generate/",
            type:"post",
            data:{'title': title, 'keywords': keywords, 'abstract': abstract},
            dataType: 'json',
            success:function (data) {
                $("#abstract_output").val(data.article);
                // 加载完成后解除按钮的禁用
                bt.disabled = false;
                bt.innerText = "一键生成文章";
            },
            error:function () {
                $("#abstract_output").val("好像出问题了，请再试一次或联系管理员：bryanwang0702@163.com")
                // 加载完成后解除按钮的禁用
                bt.disabled = false;
                bt.innerText = "一键生成文章";
            }
        })

    })

    $("#outline_submit").click(function () {
        // 发送Ajax请求
        var title = $("#outline_title").val()
        var keywords = $("#outline_keywords").val();
        var abstract = $("#outline_abstract").val();
        var outline = $("#outline_outline").val();
        const bt = document.getElementById("outline_submit");
        bt.disabled = true;
        bt.innerText = "正在生成中...";
        $.ajax({
            url:"/outlineGenerate/generate/",
            type:"post",
            data:{'title': title, 'keywords': keywords, 'abstract': abstract, 'outline': outline},
            dataType: 'json',
            success:function (data) {
                //将返回的值放到大纲生成的输出中
                $("#outline_output").val(data.article);
                // 加载完成后解除按钮的禁用
                bt.disabled = false;
                bt.innerText = "一键生成文章";
            },
            error:function () {
                $("#outline_output").val("好像出问题了，请再试一次或联系管理员：bryanwang0702@163.com")
                // 加载完成后解除按钮的禁用
                bt.disabled = false;
                bt.innerText = "一键生成文章";
            }
        })

    })
})

