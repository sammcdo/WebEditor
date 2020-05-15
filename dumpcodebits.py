import json
template1 = """
<ul>

<li>
</li>

<li>
</li>

</ul>
"""
template2 = """
<ol>

<li>
</li>

<li>
</li>

</ol>
"""
template3 = """
<video src="path" controls width="75%", height="50%">
  Your browser does not support the <code>video</code> element.
</video>
"""
template4 = """
<img src="path" alt="alternate text" />
"""
template5 = """
<link rel="" type="" href="">
"""
template6 = """
<script>
<!-- hide frm browser
script
// no more hiding -->
</script>
<noscript>
What to show w/o script
</nosript>
"""
template7 = """
<table style="border: 1px solid blue;">
<thead>
Header
</thead>
<tr>
<td>data1 row1</td>
<td>data2 row1</td>
</tr>
<tr>
<td>data1 row2</td>
<td>data2 row2</td>
</tr>
</table>
"""
templatelist = []
templatelist.append(["unordered list", template1])
templatelist.append(["ordered list", template2])
templatelist.append(["html5 vid", template3])
templatelist.append(["image", template4])
templatelist.append(["style link", template5])
templatelist.append(["javascript", template6])
templatelist.append(["table", template7])
with open("codebits.json", "w") as fobj:
    json.dump(templatelist, fobj)