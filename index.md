---
layout: main
description: "卡片创作实验室 - cnfeat的个人网站。专注卡片创作、写作系统、生产力提升，提供《笨方法文化手册》《卡片创作100讲》等课程与手册。"
---

<div class="intro-section">
  <img src="{{ site.baseurl }}/images/Avatar.png" alt="cnfeat头像" class="avatar-img" />
  <div class="intro-text">
    <h2>我是 <strong>cnfeat</strong></h2>
    <p>📍 <a href="https://hardwaylab.com">笨方法实验室</a>创始人，日课一卡 10 年，写过 50000+ 张纸质卡片。</p>
    <p>📝 持续创作手册与课程，构建长期主义者的人生成长系统。</p>
    <p>✍️ 纸笔创作 · 效率系统 · 人生发展</p>
    <p>🧪 这里是<strong>卡片创作实验室</strong>，是我试验卡片写作的地方，记录的每一篇都是我写过的卡片合集。</p>
  </div>
</div>

---

## 最近更新

<ul class="related-posts">
{% for post in site.posts limit:7 %}
    <li class="main-page-list">
        <h4>
            <small>{{ post.date | date: "%Y-%m-%d" }}</small>
            <span><a class="una" href="{{ site.baseurl }}{{ post.url }}">{{ post.title }}</a></span>
        </h4>
    </li>
{% endfor %}
</ul>

## 我的作品

我写作最重要的一件事，就是持续生产各种手册。我不是在写手册，就是在更新手册的路上，直到我拥有很多本有趣、简洁、有效的手册。

<div class="works-grid">

<div class="work-card">
<a href="https://mp.weixin.qq.com/s/KVO_rI6ZiYGO1clk6y6YBg"><img src="{{ site.baseurl }}/images/hardwaybook.png" alt="笨方法文化手册4.0" /></a>
<h4><a href="https://mp.weixin.qq.com/s/KVO_rI6ZiYGO1clk6y6YBg">《笨方法文化手册4.0》</a></h4>
<p class="work-desc">历时6年沉淀，27万字536页，助你从0到1构建长期主义者的人生成长系统。2020年起每年更新，新增13万字真实世界高手实践案例。</p>
</div>

<div class="work-card">
<a href="https://www.yuque.com/hardwaylab/zzybgv/luvhdr"><img src="{{ site.baseurl }}/images/card100.png" alt="卡片创作100讲" /></a>
<h4><a href="https://www.yuque.com/hardwaylab/zzybgv/luvhdr">《卡片创作100讲》</a></h4>
<p class="work-desc">100天构建你的卡片创作系统。从灵感唤醒到结构梳理，从卡片构建到批量输出，全流程实战方法，8大模块100+讲内容。</p>
</div>

<div class="work-card">
<a href="https://xiaobot.net/p/productivity"><img src="{{ site.baseurl }}/images/productbook.png" alt="个人生产力发展指南" /></a>
<h4><a href="https://xiaobot.net/p/productivity">《个人生产力发展指南》</a></h4>
<p class="work-desc">8年生产力实战经验，11万+字精炼内容，帮你构建真正适合自己的个人生产力系统，实现高效、专注、身心富足。</p>
</div>

<div class="work-card">
<a href="https://chromewebstore.google.com/detail/%E6%97%A5%E8%AF%BE%E4%B8%80%E9%97%AE-%E6%AF%8F%E6%97%A5%E4%B8%80%E9%97%AE%EF%BC%8C%E7%A0%B4%E5%B1%80%E4%BA%BA%E7%94%9F/lmjibmhpjhcjlkbceenghmfjpibdjinp?hl=zh-CN"><img src="{{ site.baseurl }}/images/dailyQ.png" alt="日课一问" /></a>
<h4><a href="https://chromewebstore.google.com/detail/%E6%97%A5%E8%AF%BE%E4%B8%80%E9%97%AE-%E6%AF%8F%E6%97%A5%E4%B8%80%E9%97%AE%EF%BC%8C%E7%A0%B4%E5%B1%80%E4%BA%BA%E7%94%9F/lmjibmhpjhcjlkbceenghmfjpibdjinp?hl=zh-CN">《日课一问》</a></h4>
<p class="work-desc">极简自省卡片系统，内置400+灵魂拷问。每日随机3张问题卡片，刺破日常惯性，重构自我认知。Chrome浏览器插件，免费下载。</p>
</div>

</div>

更多产品介绍，详细见[笨方法产品货架](https://www.yuque.com/hardwaylab/zzybgv)