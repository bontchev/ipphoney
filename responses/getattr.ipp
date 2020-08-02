GROUP Operation-Attributes-Tag

ATTR charset attributes-charset utf-8
ATTR language attributes-natural-language en

GROUP Printer-Attributes-Tag

# Required attributes:

ATTR charset charset-configured utf-8
ATTR charset charset-supported us-ascii,utf-8
ATTR keyword compression-supported deflate,gzip,none
ATTR mimeMediaType document-format-default application/pdf
ATTR mimeMediaType document-format-supported text/plain,application/pdf,image/jpeg
ATTR language generated-natural-language-supported en
ATTR keyword ipp-versions-supported 1.0,1.1,2.0,2.1,2.2
ATTR language natural-language-configured en

# Required operations:
#ATTR enum operations-supported Print-Job,Validate-Job,Get-Printer-Attributes,Get-Jobs,Cancel-Job,Get-Job-Attributes
# Recommended operations:
#ATTR enum operations-supported Create-Job,Send-Document,Send-URI
# Optional operations:
#ATTR enum operations-supported Print-URI,Pause-Printer,Resume-Printer,Hold-Job,Release-Job

ATTR enum operations-supported Print-Job,Validate-Job,Get-Printer-Attributes,Get-Jobs,Cancel-Job,Get-Job-Attributes,Create-Job,Send-Document,Send-URI,Print-URI,Pause-Printer,Resume-Printer,Hold-Job,Release-Job

ATTR keyword pdl-override-supported attempted
ATTR nameWithoutLanguage printer-name PrintService
ATTR boolean printer-is-accepting-jobs true
ATTR enum printer-state idle
ATTR keyword printer-state-reasons paused
ATTR integer printer-up-time 514
ATTR uri printer-uri-supported ipp://$ip/ipp/print
ATTR integer queued-job-count 0
ATTR keyword uri-authentication-supported none
ATTR keyword uri-security-supported none

# Recommended attributes:

ATTR boolean color-supported false
ATTR rangeOfInteger job-impressions-supported 1-255
ATTR boolean multiple-document-jobs-supported false
ATTR integer multiple-operation-time-out 60
ATTR textWithoutLanguage printer-info PrintService
ATTR textWithoutLanguage printer-location ''
ATTR textWithoutLanguage printer-make-and-model Test Printer
ATTR integer pages-per-minute 0
ATTR dateTime printer-current-time $now
ATTR uri printer-more-info https://$ip/ipp/print
ATTR textWithoutLanguage printer-state-message Idle.

GROUP End-of-Attributes-Tag

