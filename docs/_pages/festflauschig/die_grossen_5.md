---
permalink: /fest-flauschig/die-grossen-5
layout: single
sidebar:
  nav: "sidebar"
---

<table style="display: table;">
{% assign items_grouped = site.data.timestamps_diegrossen5 | group_by: 'track' %}
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
        <td markdown="span"  style="word-wrap: break-word;max-width: 100px;"><a href="https://open.spotify.com/episode/{{ row['id'] }}?t={{ row['duration_total_min'] | round }}">{{ row['name']| slice: 0,30  }}</a></td>
        {% endif %}
      {% endfor %}
      <td markdown="span">
      {% for row in row.items %}
        {{ row['duration_min'] }} Minuten / {{ row['duration_sec'] }} Sekunden
      {% endfor %}
      </td>
  </tr>
  {% endfor %}
</table>