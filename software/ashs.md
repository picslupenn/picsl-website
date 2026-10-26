---
title: ASHS
redirect_from:
- /software/ashs/
---

# ASHS

{%
  include figure.html
  image="images/software/ashs.png"
  width="60%"
%}

ASHS stands for “Automatic Segmentation of Hippocampal Subfields.” Here is what it does:

- Automatically labels hippocampal subfields and medial temporal lobe cortices in MRI
- Uses T1-weighted and T2-weighted MRI to obtain optimal segmentation
  - New: ASHS-T1 extracts a subset of labels in only T1-weighted MRI
- Leverages latest label fusion approaches for multi-atlas segmentation
- Can be easily retrained to use your own segmentation protocol
- Free, open-source software
  - Can be executed directly from [ITK-SNAP 3.8](http://itksnap.org)

ASHS development is led by [Paul Yushkevich](/members/paul-yushkevich.html).

{% include button.html link="https://ashs.itksnap.org" text="Documentation" icon="fa-solid fa-book" %}
{% include button.html link="https://github.com/pyushkevich/ashs" text="Code" icon="fa-brands fa-github" %}
{% include button.html link="https://ashs.itksnap.org" text="Download" icon="fa-solid fa-download" %}
