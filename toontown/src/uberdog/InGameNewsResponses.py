"""
Constants file that contains XML and misc. codes for award responses
"""

# --- Begin XML message constants ---


setLatestIssueFailureXML = """
<setLatestIssueResponse>
 <success>false</success>
 <error>%s</error>
</setLatestIssueResponse>
\r\n"""

setLatestIssueSuccessXML = """
<setLatestIssueResponse>
 <success>true</success>
 <info>%s</info>
</setLatestIssueResponse>
\r\n"""
