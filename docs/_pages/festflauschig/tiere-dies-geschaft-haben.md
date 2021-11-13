---
permalink: /fest-flauschig/tiere-dies-geschaft-haben
layout: single
sidebar:
  nav: "sidebar"
---

<table style="display: table;">
{% assign items_grouped = site.data.timestamps_tiere_dies_geschafft_haben | group_by: 'track' %}
  {% for row in items_grouped %}
    {% if forloop.first %}
    <tr>
        <th>Num.</th>
        <th>Titel</th>
        <th style="word-wrap: break-word;max-width: 100px;">Timestamps</th>
    </tr>
    {% endif %}
    <tr>
    <td markdown="span">{{ row['name'] }}</td>
      {% for row in row.items %}
        {% if forloop.first %}
        <td markdown="span"  style="word-wrap: break-word;max-width: 100px;">{{ row['name']| slice: 0,30  }}</td>
        {% endif %}
      {% endfor %}
      <td markdown="span">
      {% for row in row.items %}
      <a href="https://open.spotify.com/episode/{{ row['id'] }}?t={{ row['duration_total_min'] | round }}">{{ row['duration_min'] }} Minuten / {{ row['duration_sec'] }} Sekunden</a>
      {% endfor %}
      </td>
  </tr>
  {% endfor %}
</table>