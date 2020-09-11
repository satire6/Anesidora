"""
Constants file that contains XML and misc. codes for RAT responses
"""

# --- Begin XML message constants ---


getToonListSuccessXML = """
<getToonListResponse>
 <success>true</success>
 <toonList>
%s
 </toonList>
</getToonListResponse>
\r\n"""

getToonListFailureXML = """
<getToonListResponse>
 <success>false</success>
 <error>%s</error>
</getToonListResponse>
\r\n"""

giveToonBeansCSSuccessXML = """
<giveToonBeansCSResponse>
 <success>true</success>
</giveToonBeansCSResponse>
\r\n"""

giveToonBeansCSFailureXML = """
<giveToonBeansCSResponse>
 <success>false</success>
 <error>%s</error>
</giveToonBeansCSResponse>
\r\n"""

giveToonBeansRATSuccessXML = """
<giveToonBeansRATResponse>
 <success>true</success>
</giveToonBeansRATResponse>
\r\n"""

giveToonBeansRATFailureXML = """
<giveToonBeansRATResponse>
 <success>false</success>
 <error>%s</error>
</giveToonBeansRATResponse>
\r\n"""

getToonPicIdSuccessXML = """
<getToonPicIdResponse>
 <success>true</success>
 <picId>%s</picId>
</getToonPicIdResponse>
\r\n"""

getToonPicIdFailureXML = """
<getToonPicIdResponse>
 <success>false</success>
 <error>%s</error>
</getToonPicIdResponse>
\r\n"""

getToonDNASuccessXML = """
<getToonDNAResponse>
 <success>true</success>
 <dna>%s</dna>
</getToonDNAResponse>
\r\n"""

getToonDNAFailureXML = """
<getToonDNAResponse>
 <success>false</success>
 <error>%s</error>
</getToonDNAResponse>
\r\n"""
