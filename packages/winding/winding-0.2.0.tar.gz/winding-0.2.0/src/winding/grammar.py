import os

grammar = r"""start: (winding | markdown)+

winding: meta_winding | space_winding | inline_winding
meta_winding: "---\n" IDENTIFIER ":" attributes header_winding* "\n---\n" content? 
space_winding: "--\n" IDENTIFIER ":" attributes header_winding* "\n--\n" content?
header_winding: "\n" IDENTIFIER ":" attributes
inline_winding: "@" IDENTIFIER ":" attributes "\n" content?

content: (winding | markdown)+

markdown: (image | TEXT)+

attributes: (IDENTIFIER ("," IDENTIFIER)*)?

image: "![" CAPTION? "]" "(" URI? ")"

IDENTIFIER: /!?[A-Za-z][A-Za-z0-9_.-]*/
URI: /[^\)\n]+/
TEXT: /(?:(?!@\w+:|--|!\[).)*\n+/ 
CAPTION: /[^\]]+/
    
%ignore /[ \t]+/
%ignore "\r"  
"""