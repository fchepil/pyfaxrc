# Ring Central Fax Bridge for MaxFax -push to Github
from dotenv import load_dotenv
import os
import sys
from ringcentral import SDK
import main
from main import valid_doc, valid_num, logger, rc_logger, rc_outbound


# Receive Parameters from MaxFax
recipient = str(sys.argv[1])
faxdoc = str(sys.argv[2])
sender = str(sys.argv[3])

load_dotenv()

# Track Fax Transmissions
logger.info(recipient + " " + faxdoc + " " + sender)

# Verify phone numbers and fax document format
if valid_num(recipient, sender):
    if valid_doc(faxdoc):
        # Append Outbound Path to document
        faxdoc = rc_outbound(faxdoc)
        try:
            # --------------------RingCentral Fax Send Logic----------------------------------
            RINGCENTRAL_CLIENTID = os.getenv('RC_CLIENT_ID')
            RINGCENTRAL_CLIENTSECRET = os.getenv('RC_CLIENT_SECRET')
            RINGCENTRAL_SERVER = os.getenv('RC_SERVER_URL')
            RINGCENTRAL_USERNAME = os.getenv('RC_USERNAME')
            RINGCENTRAL_PASSWORD = os.getenv('RC_PASSWORD')
            RINGCENTRAL_EXTENSION = os.getenv('101')
            JWT_TOKEN = os.getenv('RC_JWT')
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

            request = builder.request('/account/~/extension/~/fax')

            resp = platform.send_request(request)

            # Write Response to Response Directory
            j_resp = '_' + recipient + '_' + os.path.basename(faxdoc) + '_' + resp.json().messageStatus

            full_jsonpath = main.rc_confirm(j_resp)

            with open(full_jsonpath, 'w+') as f_resp:
                f_resp.write(recipient + '_' + os.path.basename(faxdoc))
                f_resp.close()

                # Write Transmission Events in Ring Central log file
                rc_logger.info(os.path.join(main.basedir, main.respdir, recipient + '__' + os.path.basename(faxdoc))
                               
        except Exception as e:
            logger.critical("Ring Central Exception occurred", exc_info=True)
    else:
        logger.error("Fax document has invalid extension", exc_info=True)
else:
    logger.error("Phone Number is invalid", exc_info=True)
