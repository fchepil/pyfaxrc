# Ring Central Fax Bridge for MaxFax -push to Github

import os.path
import sys
from ringcentral import SDK
import main
from main import FaxValidate, logger, rc_logger, rc_outbound

# Receive Parameters from MaxFax
recipient = str(sys.argv[1])
faxdoc = str(sys.argv[2])
sender = str(sys.argv[3])

# Track Fax Transmissions
logger.info(recipient + " " + faxdoc + " " + sender)

# Verify phone numbers and fax document format
if FaxValidate.valid_num(recipient, sender):
    if FaxValidate.valid_doc(faxdoc):
        # Append Outbound Path to document
        faxdoc = rc_outbound(faxdoc)

        try:
            # --------------------RingCentral Fax Send Logic----------------------------------
            RINGCENTRAL_CLIENTID = 'NXdwJSgYRhmmGQz6Jf62xA'
            RINGCENTRAL_CLIENTSECRET = 'mNGVhRY7QF23Jh7pODoaFgiAQoEVEWTx-GgvTZXZV2mQ'
            RINGCENTRAL_SERVER = 'https://platform.devtest.ringcentral.com'
            RINGCENTRAL_USERNAME = '14705020103'
            # RINGCENTRAL_USERNAME = '15054880453'
            RINGCENTRAL_PASSWORD = 'Q1w2e3r4t5y$$'
            RINGCENTRAL_EXTENSION = '101'
            JWT_TOKEN = 'eyJraWQiOiI4NzYyZjU5OGQwNTk0NGRiODZiZjVjYTk3ODA0NzYwOCIsInR5cCI6IkpXVCIsImFsZyI6IlJTMjU2In0.eyJhdWQiOiJodHRwczpcL1wvcGxhdGZvcm0uZGV2dGVzdC5yaW5nY2VudHJhbC5jb21cL3Jlc3RhcGlcL29hdXRoXC90b2tlbiIsInN1YiI6IjcxNTU0MDAwNSIsImlzcyI6Imh0dHBzOlwvXC9wbGF0Zm9ybS5kZXZ0ZXN0LnJpbmdjZW50cmFsLmNvbSIsImV4cCI6Mzc5Njg1NDgyNCwiaWF0IjoxNjQ5MzcxMTc2LCJqdGkiOiJLV0gwX21rOVJvaThHZlg1NFVxRGNBIn0.B-5rhWzrP_hTXKorMFNEb1L5vlxSpWHd-VA6t10GLfBNBcd1LiqjpaiNW01nNEIlK_YTck25jN37Cfv66vAc0Gy3_Js1VA7PVJocdbYzVTun8nH9GrYSPoseEv86i5TFAwYe2RQiGxRLaH_jTbh0nvxdCKMjU2i6VlkyGvZRoJbPOFzZKdpK4MYWrp6winqTsZpbsRWfGS7rj_KKVmqozrXUQJelKOb6gpojHjD9FbPq8GEjbZE3YJAsJDZ220Qq9c5r9gta-JhwzDkNh_RBU96utlEGln5XnXeBXUzDQLJaBWZva7PZq4WLw9zAgmDIyiNyc3qn83skYDY7ftqjqg'
            rcsdk = SDK(RINGCENTRAL_CLIENTID, RINGCENTRAL_CLIENTSECRET, RINGCENTRAL_SERVER)

            platform = rcsdk.platform()
            # platform.login(RINGCENTRAL_USERNAME, RINGCENTRAL_EXTENSION, RINGCENTRAL_PASSWORD)
            platform.login(jwt=JWT_TOKEN)
            builder = rcsdk.create_multipart_builder()
            builder.set_body({
                'to': [{'phoneNumber': recipient}],
                'faxResolution': "High",
                'coverPageText': "Clinic Name \n" + str(sender)
            })

            with open(faxdoc, encoding="utf8", errors='ignore') as f:
                content = f.read()
                attachment = (faxdoc, content)

            builder.add(attachment)

            # request = builder.request('/account/~/extension/~/fax')

            # resp = platform.send_request(request)

            # Write Response to Response Directory
            j_resp = '_' + recipient + '_' + os.path.basename(faxdoc) + '_' + resp.json().messageStatus

            full_jsonpath = main.rc_confirm(j_resp)

            with open(full_jsonpath, 'w+') as f_resp:
                f_resp.write(recipient + '_' + os.path.basename(faxdoc))
                f_resp.close()

                # Write Transmission Events in Ring Central log file
                rc_logger.info('__' + recipient + '__' + os.path.basename(faxdoc))

        except Exception as e:
            logger.critical("Ring Central Exception occurred", exc_info=True)
    else:
        logger.error("Fax document has invalid extension", exc_info=True)
else:
    logger.error("Phone Number is invalid", exc_info=True)
