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

{% include button.html link="team/#faculty" text="Faculty" style="bare" %}
{% include button.html link="team/#staff-postdocs-and-students" text="Staff, Postdocs and Students" style="bare" %}
{% include button.html link="team/#alumni" text="Alumni" style="bare" %}
{% include button.html link="team/#collaborating-labs-and-centers" text="Collaborating Labs and Centers" style="bare" %}

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

{% include list.html component="portrait" data="collaborators" filter="group == 'penn'" %}

### Outside Penn

{% include list.html component="portrait" data="collaborators" filter="group == 'external'" %}
