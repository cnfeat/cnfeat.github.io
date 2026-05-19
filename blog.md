---
layout: main
title: 博客
description: "卡片创作实验室博客文章列表，涵盖卡片创作、写作技巧、认知科学、读书笔记、生产力系统等内容。"
---

## 文章列表

<ul class="related-posts">
{% for post in site.posts %}
    <li class="main-page-list">
        <h4>
            <small>{{ post.date | date: "%Y-%m-%d" }}</small>
            <span><a class="una" href="{{ site.baseurl }}{{ post.url }}">{{ post.title }}</a></span>
        </h4>
    </li>
{% endfor %}
</ul>