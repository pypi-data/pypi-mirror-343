from interface.hyoml import Hyoml

hy = Hyoml()
text = """
title: Hyoml
description: A universal parser
<important />
<directive=clean>
"""

data = hy.parse(text)

print(hy.asYAML(data, quotes_required=True))
print(hy.asTOML(data))
print(hy.toTXT(data))  # alias for asString/toString
