---
permalink: /sanft-sorgfältig/alle-episoden
layout: page
title: Alle Episoden
parent: Sanft und Sorgfältig
nav_order: 1
---

<table>
  {% for row in site.data.list_episodes_metadata_ss %}
    {% if forloop.first %}
    <tr>
        <th>Num.</th>
        <th>Titel</th>
        <th>Datum</th>
        <th>Länge in Minuten</th>
    </tr>
    {% endif %}
    <tr>
    <td markdown="span">{{ row['track'] }}</td>
    <td markdown="span">{{ row['name'] }}</td>
    <td markdown="span" style="white-space: nowrap;overflow: hidden;text-overflow:ellipsis;">
                  {{ row['release_date'] | date: "%-d." }}{% assign month = row['release_date'] | date: '%-m' %}
              {% case month %}
                {% when '1' %}Jan.
                {% when '2' %}Feb.
                {% when '3' %}März
                {% when '4' %}April
                {% when '5' %}Mai
                {% when '6' %}Juni
                {% when '7' %}Juli
                {% when '8' %}Aug.
                {% when '9' %}Sep.
                {% when '10' %}Okt.
                {% when '11' %}Nov.
                {% when '12' %}Dez.
              {% endcase %}{{ row['release_date'] | date: "%Y" }}
    </td>
    <td markdown="span">{{ row['duration_sec'] | divided_by: 60.00 | round }}</td>
    </tr>
  {% endfor %}
</table>