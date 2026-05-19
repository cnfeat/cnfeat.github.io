---
layout: main
title: 博客
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