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

{% include list.html component="card" data="collaborators" filter="group == 'penn'" style="small" %}

### Outside Penn

{% include list.html component="card" data="collaborators" filter="group == 'external'" style="small" %}
