import json
template1 = """
<html>
<head>
title
</head>
<body>
body
</body>
</html>
"""
template2 = """
<html>
<link rel="stylesheet" type="text/css" href="style.css">
<head>
<title>
Title Goes Here
</title>
</head>
<body>
<table id="body" style="font-family: Calibri; font-size: 12pt; height: 100%; width: 100%;">

<tr>

<td id="header" colspan=2 style="font-size: 25pt; font-family: Calibri;">
Page Header Goes Here
</td>

</tr>

<tr>

<td colspan=2 style="background-color: #71ff74; text-align: center; height: 40px">
<b>
Navigational Links here
</b>
</td>

</tr>

<tr>

<td id="addcolumn" style="background-color: #00dd5e; height: 90%; width: 25%;">
Adds Here
</td>

<td id="bodycolumn" style="vertical-align: top; background-color: #b8ffb4; height: 90%; width: 75%;">

Body goes here

</td>

</tr>

</table>
</body>
</html>
"""
templatelist = []
templatelist.append(["basic html", template1])
templatelist.append(["basic page", template2])
with open("templates.json", "w") as fobj:
    json.dump(templatelist, fobj)