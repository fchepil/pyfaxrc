import os
import pathlib
import logging
from logging.handlers import RotatingFileHandler
import datetime
from dotenv import load_dotenv


load_dotenv()

# Check initial Application environment and create if missing directories
basedir = os.path.abspath(str(os.getenv('BASE_DIR')))
print (basedir)
obdir = os.getenv('OB_DIR')
obdir = str(basedir) + '\\' + str(obdir)
print(obdir)
respdir = os.getenv('RESP_DIR')
respdir =str(basedir) + '\\' + str(respdir)
print(respdir)
logdir = os.getenv('LOGS_DIR')
logdir = str(basedir) + '\\' + str(logdir)
print(logdir)

for xdir in [obdir, respdir, logdir]:
    if not os.path.exists(xdir):
        os.mkdir(xdir)



# Setup error log creation

logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
logger = logging.getLogger(__name__)
f_handler = RotatingFileHandler(logdir + 'faxservice.log', maxBytes=20480, backupCount=10)
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
f_handler.setFormatter(f_format)
logger.addHandler(f_handler)


# Setup RingCentral Fax Transmission logging

rc_logger = logging.getLogger()
rc_handler = RotatingFileHandler(respdir + 'RC_Transmission.log', maxBytes=20480, backupCount=30)
rc_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
rc_handler.setFormatter(f_format)
rc_logger.addHandler(rc_handler)


# Setup directory Path for Outbound Faxes
def rc_outbound(faxdoc):
    obfax = obdir + str(faxdoc)
    return obfax


# Setup directory path for json response's from Ring Central
def rc_confirm(response):
    f_json = str(datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '_' + response)
    f_w_response = respdir + f_json
    return f_w_response


class FaxValidate:
    # Create Class to manage validation of parameters passed for faxing
    # Validate the fax numbers passed to RingCentral function

    def valid_num(fx_to, fx_from):

        for fx_num in [fx_to, fx_from]:
            if len(fx_num) < 12:
                return False
            elif len(fx_num) > 12:
                return False
            else:
                return True

    # Validate fax document is correct file type
    def valid_doc(faxdoc):
        fx_doctype = faxdoc.suffix
        if str(faxdoc) == '':
            if fx_doctype == ".pdf":
                return True
            else:
                logger.error("Document Passed is not a PDF")
                return False
        else:
            logger.error("Document not found " + str(faxdoc))
            return False


# Make Methods Static
FaxValidate.valid_num = staticmethod(FaxValidate.valid_num)
FaxValidate.valid_doc = staticmethod(FaxValidate.valid_doc)


# if __name__ == '__main__':
#    app.run()
