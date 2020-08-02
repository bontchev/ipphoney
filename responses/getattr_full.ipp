GROUP Operation-Attributes-Tag
ATTR charset attributes-charset utf-8
ATTR language attributes-natural-language en
GROUP Printer-Attributes-Tag
ATTR charset charset-configured utf-8
ATTR charset charset-supported us-ascii,utf-8
ATTR boolean color-supported false
ATTR keyword compression-supported deflate,gzip,none
ATTR integer copies-default 1
ATTR rangeOfInteger copies-supported 1-999
ATTR keyword document-creation-attributes-supported document-access,document-charset,document-format,document-message,document-metadata,document-name,document-natural-language,ipp-attribute-fidelity,copies
ATTR mimeMediaType document-format-default application/pdf
ATTR mimeMediaType document-format-supported application/pdf,image/jpeg,image/pwg-raster
ATTR integer document-password-supported 127
ATTR keyword document-settable-attributes-supported document-metadata,document-name
ATTR enum finishings-default none
ATTR enum finishings-supported none
ATTR language generated-natural-language-supported en
ATTR keyword identify-actions-default sound
ATTR keyword identify-actions-supported display,sound
ATTR keyword ipp-features-supported document-object,ipp-everywhere,page-overrides,system-service
ATTR keyword ipp-versions-supported 1.0,1.1,2.0,2.1,2.2
ATTR integer ippget-event-life 300
ATTR nameWithoutLanguage job-account-id-default ''
ATTR boolean job-account-id-supported true
ATTR nameWithoutLanguage job-accounting-user-id-default ''
ATTR boolean job-accounting-user-id-supported true
ATTR keyword job-creation-attributes-supported document-access,document-charset,document-format,document-message,document-metadata,document-name,document-natural-language,ipp-attribute-fidelity,job-name,job-priority,copies,document-password,finishings,job-account-id,job-accounting-user-id
ATTR keyword job-hold-until-default no-hold
ATTR keyword job-hold-until-supported no-hold,indefinite,day-time,evening,night,second-shift,third-shift,weekend
ATTR rangeOfInteger job-hold-until-time-supported 0-2147483647
ATTR boolean job-ids-supported true
ATTR rangeOfInteger job-k-octets-supported 0-105998440
ATTR keyword job-password-encryption-supported none
ATTR integer job-password-supported 4
ATTR integer job-priority-default 50
ATTR integer job-priority-supported 100
ATTR keyword job-settable-attributes-supported document-metadata,document-name,job-hold-until,job-hold-until-time,job-name,job-priority
ATTR integer media-bottom-margin-supported 635
ATTR collection media-col-default {media-key=na_letter_8.5x11in_main_auto media-size={x-dimension=21590 y-dimension=27940} media-size-name=na_letter_8.5x11in media-bottom-margin=635 media-left-margin=635 media-right-margin=635 media-top-margin=635 media-source=main media-type=auto}
ATTR collection media-col-ready {media-key=na_letter_8.5x11in_main_auto media-size={x-dimension=21590 y-dimension=27940} media-size-name=na_letter_8.5x11in media-bottom-margin=635 media-left-margin=635 media-right-margin=635 media-top-margin=635 media-source=main media-type=auto}
ATTR keyword media-default na_letter_8.5x11in
ATTR integer media-left-margin-supported 635
ATTR keyword media-ready na_letter_8.5x11in
ATTR integer media-right-margin-supported 635
ATTR keyword media-supported na_letter_8.5x11in,na_legal_8.5x14in,iso_a4_210x297mm
ATTR collection media-size-supported {x-dimension=21590 y-dimension=27940},{x-dimension=21590 y-dimension=35560},{x-dimension=21000 y-dimension=29700}
ATTR keyword media-source-supported main
ATTR integer media-top-margin-supported 635
ATTR keyword media-type-supported auto
ATTR keyword media-col-supported media-bottom-margin,media-color,media-info,media-key,media-left-margin,media-right-margin,media-size,media-size-name,media-source,media-top-margin,media-type
ATTR keyword multiple-document-handling-supported separate-documents-uncollated-copies,separate-documents-collated-copies
ATTR boolean multiple-document-jobs-supported false
ATTR integer multiple-operation-time-out 60
ATTR keyword multiple-operation-time-out-action abort-job
ATTR language natural-language-configured en
ATTR keyword notify-attributes-supported printer-state-change-time,notify-lease-expiration-time,notify-subscriber-user-name
ATTR keyword notify-events-default job-completed
ATTR keyword notify-events-supported document-completed,document-config-changed,document-created,document-fetchable,document-state-changed,document-stopped,job-completed,job-config-changed,job-created,job-fetchable,job-progress,job-state-changed,job-stopped,none,printer-config-changed,printer-created,printer-deleted,printer-finishings-changed,printer-media-changed,printer-queue-order-changed,printer-restarted,printer-shutdown,printer-state-changed,printer-stopped,resource-canceled,resource-config-changed,resource-created,resource-installed,resource-changed,system-config-changed,system-state-changed,system-stopped
ATTR integer notify-lease-duration-default 86400
ATTR rangeOfInteger notify-lease-duration-supported 0-67108863
ATTR integer notify-max-events-supported 31
ATTR keyword notify-pull-method-supported ippget
ATTR integer number-up-default 1
ATTR integer number-up-supported 1
ATTR enum operations-supported Print-Job,Print-URI,Validate-Job,Create-Job,Send-Document,Send-URI,Cancel-Job,Get-Job-Attributes,Get-Jobs,Get-Printer-Attributes,Hold-Job,Release-Job,Pause-Printer,Resume-Printer,Set-Printer-Attributes,Set-Job-Attributes,Get-Printer-Supported-Values,Create-Printer-Subscriptions,Create-Job-Subscriptions,Get-Subscription-Attributes,Get-Subscriptions,Renew-Subscription,Cancel-Subscription,Get-Notifications,Enable-Printer,Disable-Printer,Pause-Printer-After-Current-Job,Hold-New-Jobs,Release-Held-New-Jobs,Restart-Printer,Shutdown-Printer,Startup-Printer,Cancel-Current-Job,Cancel-Document,Get-Document-Attributes,Get-Documents,Set-Document-Attributes,Cancel-Jobs,Cancel-My-Jobs,Close-Job,Identify-Printer,Validate-Document,Acknowledge-Document,Acknowledge-Identify-Printer,Acknowledge-Job,Fetch-Document,Fetch-Job,Get-Output-Device-Attributes,Update-Active-Jobs,Update-Document-Status,Update-Job-Status,Update-Output-Device-Attributes,Deregister-Output-Device
ATTR no-value orientation-requested-default no-value
ATTR enum orientation-requested-supported portrait,landscape,reverse-landscape,reverse-portrait
ATTR keyword output-bin-default face-down
ATTR keyword output-bin-supported face-down
ATTR keyword overrides-supported document-numbers,pages
ATTR boolean page-ranges-supported true
ATTR integer pages-per-minute 0
ATTR keyword pdl-override-supported attempted
ATTR boolean preferred-attributes-supported false
ATTR keyword print-color-mode-default auto
ATTR keyword print-color-mode-supported auto,color,monochrome
ATTR keyword print-content-optimize-default auto
ATTR keyword print-content-optimize-supported auto
ATTR keyword print-rendering-intent-default auto
ATTR keyword print-rendering-intent-supported auto
ATTR keyword print-scaling-default auto
ATTR keyword print-scaling-supported auto,auto-fit,fill,fit,none
ATTR enum print-quality-default normal
ATTR enum print-quality-supported draft,normal,high
ATTR textWithoutLanguage printer-device-id MFG:Test;MDL:Printer;CMD:PDF,JPEG,image/pwg-raster;
ATTR keyword printer-get-attributes-supported document-format
ATTR unknown printer-geo-location unknown
ATTR uri printer-icons http://$ip/ipp/print/icon.png
ATTR textWithoutLanguage printer-info PrintService
ATTR octetString printer-input-tray type=sheetFeedAutoRemovableTray;mediafeed=0;mediaxfeed=0;maxcapacity=250;level=100;status=0;name=main;
ATTR keyword printer-kind document
ATTR textWithoutLanguage printer-location ''
ATTR textWithoutLanguage printer-make-and-model TestPrinter
ATTR uri printer-more-info http://$ip/ipp/print
ATTR nameWithoutLanguage printer-name PrintService
ATTR textWithoutLanguage printer-organization IEEE-ISTO-Printer-Working-Group
ATTR textWithoutLanguage printer-organizational-unit IPP-Workgroup
ATTR resolution printer-resolution-default 600dpi
ATTR resolution printer-resolution-supported 600dpi
ATTR keyword printer-settable-attributes-supported job-constraints-supported,job-presets-suppored,job-resolvers-supported,job-triggers-supported,printer-contact-col,printer-dns-sd-name,printer-device-id,printer-geo-location,printer-icc-profiles,printer-info,printer-kind,printer-location,printer-make-and-model,printer-mandatory-job-attributes,printer-name,printer-organization,printer-organizational-unit,copies-default,copies-supported,document-password-supported,finishings-default,finishings-supported,job-account-id-default,job-accounting-user-id-default,job-hold-until-default,job-password-supported,job-password-encryption-supported,media-default,media-supported,media-ready,media-col-default,media-col-supported,media-col-ready,media-col-database,multiple-document-handling-supported,number-up-default,number-up-supported,orientation-requested-default,orientation-requested-supported,output-bin-default,output-bin-supported,overrides-supported,page-ranges-supported,print-color-mode-default,print-color-mode-supported,print-content-optimize-default,print-content-optimize-supported,print-quality-default,print-quality-supported,print-rendering-intent-default,print-rendering-intent-supported,print-scaling-default,print-scaling-supported,printer-resolution-default,printer-resolution-supported
ATTR octetString printer-supply index=1;class=receptacleThatIsFilled;type=wasteToner;unit=percent;maxcapacity=100;level=67;colorantname=unknown;,index=2;class=supplyThatIsConsumed;type=toner;unit=percent;maxcapacity=100;level=100;colorantname=black;
ATTR textWithoutLanguage printer-supply-description TonerWaste,BlackToner
ATTR uri printer-supply-info-uri http://$ip/ipp/print/supplies
ATTR uri printer-uri-supported ipp://$ip/ipp/print
ATTR uri printer-uuid urn:uuid:6797635e-74f5-3262-5006-bf530c347406
ATTR collection printer-xri-supported {xri-authentication=none xri-security=tls xri-uri=ipp://$ip/ipp/print}
ATTR resolution pwg-raster-document-resolution-supported 150dpi,300dpi
ATTR keyword pwg-raster-document-sheet-back normal
ATTR keyword pwg-raster-document-type-supported black_1,cmyk_8,sgray_8,srgb_8,srgb_16
ATTR uriScheme reference-uri-schemes-supported ftp,http,https
ATTR keyword sides-default one-sided
ATTR keyword sides-supported one-sided
ATTR keyword uri-authentication-supported none
ATTR keyword uri-security-supported tls
ATTR keyword which-jobs-supported aborted,all,canceled,completed,not-completed,pending,pending-held,processing,processing-stopped
ATTR keyword xri-authentication-supported none
ATTR keyword xri-security-supported tls
ATTR uriScheme xri-uri-scheme-supported ipps
ATTR keyword document-privacy-attributes none
ATTR keyword document-privacy-scope all
ATTR keyword job-privacy-attributes none
ATTR keyword job-privacy-scope all
ATTR keyword subscription-privacy-attributes none
ATTR keyword subscription-privacy-scope all
ATTR dateTime printer-config-change-date-time $old
ATTR integer printer-config-change-time 0
ATTR dateTime printer-current-time $now
ATTR nameWithoutLanguage printer-dns-sd-name PrintService
ATTR boolean printer-is-accepting-jobs true
ATTR enum printer-state idle
ATTR dateTime printer-state-change-date-time $old
ATTR integer printer-state-change-time 0
ATTR textWithoutLanguage printer-state-message Idle.
ATTR keyword printer-state-reasons paused
ATTR integer printer-up-time 514
ATTR integer queued-job-count 0
GROUP End-of-Attributes-Tag
