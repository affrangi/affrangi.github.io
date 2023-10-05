---
layout: page
title: Publications
permalink: /pubs/
description: 
nav: true
nav_order: 7
display_categories: [work, fun]
---

{%- assign categs = site.publications_categories  -%}
{%- assign sorted_publications = site.publications | sort: "year" | reverse -%}
{%- assign counter = 0 -%}

<!-- Display projects without categories -->
  <!-- Generate accordeons for each category -->
  <div class="accordion" id="PubsAccordion">
  {%- for categ in  categs -%}
    {%- assign counter = counter | plus: 1 -%}
    {%- assign INDX = counter -%}
	
     <div class="accordion-item">
       <h2 class="accordion-header" id={{ "heading" | append: INDX }}>
         <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="{{ "#collapse" | append: INDX }}" aria-expanded="false" aria-controls="{{ "collapse" | append: INDX }}">
		   {%- assign total_items_in_category = 0 -%}
		   {%- assign total_items_in_category = site.publications | where: "plural_category", categ | size -%}
           {{ categ }} <span class="category-items-count">({{ total_items_in_category }})</span>
         </button>
       </h2>
       <div id={{ "collapse" | append: INDX }} class="accordion-collapse collapse" aria-labelledby="{{ "heading" | append: INDX }}" data-bs-parent="#PubsAccordion">
         <div class="accordion-body">
              {%- assign year = 0 -%}
              {%- assign previous_year = 0 -%}
              {%- for publication in sorted_publications -%}
              {%-   if publication.plural_category == categ -%}
              {%-     assign year = publication.year -%}
              {%-       if year  <> previous_year  -%}
              {%-          assign previous_year = year  -%}
                           <div class="year_divider">{{ year }}</div>
              {%-       endif  -%}
                  {% include publications.html %}
             {%-   endif %}
             {%- endfor %}
         </div>
       </div>
     </div>
 
  {%- endfor -%}




