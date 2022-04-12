# Routine for JWT Authentication
from ringcentral import SDK
import os,sys

rcsdk = SDK( os.environ.get('RC_CLIENT_ID'),
             os.environ.get('RC_CLIENT_SECRET'),
             os.environ.get('RC_SERVER_URL'))
platform = rcsdk.platform()

try:
  platform.login( jwt=os.environ.get('RC_JWT'))
except Exception as e:
  print(e)
  sys.exit("Unable to authenticate to platform. Check credentials." + str(e))

print(f'Login with JWT successful.')