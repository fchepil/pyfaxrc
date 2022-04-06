# Ring Central Fax Bridge for MaxFax -push to Github
import os.path
import sys
import main
from ringcentral import SDK
from main import FaxValidate, logger

# Receive Parameters from MaxFax
recipient = str(sys.argv[1])
faxdoc = str(sys.argv[2])
sender = str(sys.argv[3])

logger.info(recipient + " " + faxdoc + " " + sender)

# Verify phone numbers and fax document format
if FaxValidate.valid_num(recipient, sender):
    if FaxValidate.valid_doc(faxdoc):
        try:
            # --------------------RingCentral Fax Send Logic----------------------------------
            RINGCENTRAL_CLIENTID = 'NXdwJSgYRhmmGQz6Jf62xA'
            RINGCENTRAL_CLIENTSECRET = 'mNGVhRY7QF23Jh7pODoaFgiAQoEVEWTx-GgvTZXZV2mQ'
            RINGCENTRAL_SERVER = 'https://platform.devtest.ringcentral.com'
            RINGCENTRAL_USERNAME = '14705020103'
            # RINGCENTRAL_USERNAME = '15054880453'
            RINGCENTRAL_PASSWORD = 'Q1w2e3r4t5y$$'
            RINGCENTRAL_EXTENSION = '101'

            rcsdk = SDK(RINGCENTRAL_CLIENTID, RINGCENTRAL_CLIENTSECRET, RINGCENTRAL_SERVER)

            platform = rcsdk.platform()
            platform.login(RINGCENTRAL_USERNAME, RINGCENTRAL_EXTENSION, RINGCENTRAL_PASSWORD)

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

            # full_jsonpath = main.rc_confirm(resp.json().messageStatus)
            resp = '_TestFax'
            full_jsonpath = main.rc_confirm(resp)

            with open(full_jsonpath, 'w+') as f_resp:
                f_resp.write(recipient+'_'+os.path.basename(faxdoc)+'_'+full_jsonpath)
                f_resp.close()
            # logger.info('Fax sent. Message status: ' + resp.json().messageStatus)
            logger.info('Fax sent. Message status: '+full_jsonpath)

        except Exception as e:
            logger.critical("Ring Central Exception occurred", exc_info=True)
    else:
        logger.error("Fax document has invalid extension", exc_info=True)
else:
    logger.error("Phone Number is invalid", exc_info=True)
