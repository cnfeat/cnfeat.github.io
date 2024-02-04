## 更新说明

插入图片

![](images/favicon.png)

css 无内容

site 自动生成不用修改

_sass

typography 改字体

背景：color: #ffffff

字体颜色：color: #102a43;

链接文字颜色：color: #00a67d; 

日期颜色：#9fb3c8


_layouts\default.html 
- 修订 footer 课程图片文字
- 文章标题
- 发布日期


footer_url: "http://www.HardWayLab.com"
footer_text: "笨方法实验室：世上无难事，只怕笨方法"

在 _layouts\default.html 以下修改

 <p style="text-align: center; margin-bottom: 10px">
                    <a class="una" href="{{ site.footer_url }}" style="color: black"><small>{{ site.footer_text
                            }}</small></a>
                </p>


## Changelog

- 2024-01-01 初稿完成
- 2023-12-30 迁移文章成功，从21点折腾到凌晨6点
- 2023-12-29 本地部署成功，继续修改
- 2023-12-29 开始选择新模板，利用ChatGPT更新修改