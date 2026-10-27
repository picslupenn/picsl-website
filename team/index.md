---
title: Team
nav:
  order: 5
  tooltip: About our team
redirect_from:
  - /people/
  - /people/faculty-staff/
  - /people/post-docs/
  - /people/students/
  - /people/alumni/
  - /people/administrators/
---

# {% include icon.html icon="fa-solid fa-users" %}Team

{% include section.html %}

## Faculty

{% include list.html data="members" component="portrait" filter="role == 'principal-investigator' and group != 'alum'" %}
{% include list.html data="members" component="portrait" filter="role == 'faculty' and group != 'alum'" %}

{% include section.html %}

## Staff, Postdocs and Students

{% include list.html data="members" component="portrait" filter="role != 'principal-investigator' and role != 'faculty' and group != 'alum'" %}

{% include section.html %}

## Alumni

{% include list.html data="members" component="portrait" filter="group == 'alum'" style="small" %}

{% include section.html %}

## Collaborating Labs and Centers

Labs and centers whose investigators frequently co-author papers with PICSL.

### At Penn

<div class="collaborators">
{% for c in site.data.collaborators %}{% if c.group == "penn" %}
  <div class="collaborator">
    <strong>{% if c.link %}<a href="{{ c.link }}">{{ c.name }}</a>{% else %}{{ c.name }}{% endif %}</strong>
    <span>{{ c.institution }}</span>
    <p>{{ c.description }}</p>
  </div>
{% endif %}{% endfor %}
</div>

### Outside Penn

<div class="collaborators">
{% for c in site.data.collaborators %}{% if c.group == "external" %}
  <div class="collaborator">
    <strong>{% if c.link %}<a href="{{ c.link }}">{{ c.name }}</a>{% else %}{{ c.name }}{% endif %}</strong>
    <span>{{ c.institution }}</span>
    <p>{{ c.description }}</p>
  </div>
{% endif %}{% endfor %}
</div>

<style>
.collaborators { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 20px; margin: 20px 0; }
.collaborator { border: 1px solid #ddd; border-radius: 5px; padding: 15px; }
.collaborator strong a { color: #16567a; }
.collaborator span { display: block; color: #00a8d8; font-size: 0.9em; }
.collaborator p { margin: 8px 0 0; }
</style>
