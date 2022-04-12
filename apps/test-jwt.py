from ringcentral import SDK


RINGCENTRAL_CLIENTID = 'NXdwJSgYRhmmGQz6Jf62xA'
RINGCENTRAL_CLIENTSECRET = 'mNGVhRY7QF23Jh7pODoaFgiAQoEVEWTx-GgvTZXZV2mQ'
RINGCENTRAL_SERVER = 'https://platform.devtest.ringcentral.com'

JWT_TOKEN = 'eyJraWQiOiI4NzYyZjU5OGQwNTk0NGRiODZiZjVjYTk3ODA0NzYwOCIsInR5cCI6IkpXVCIsImFsZyI6IlJTMjU2In0.eyJhdWQiOiJodHRwczpcL1wvcGxhdGZvcm0uZGV2dGVzdC5yaW5nY2VudHJhbC5jb21cL3Jlc3RhcGlcL29hdXRoXC90b2tlbiIsInN1YiI6IjcxNTU0MDAwNSIsImlzcyI6Imh0dHBzOlwvXC9wbGF0Zm9ybS5kZXZ0ZXN0LnJpbmdjZW50cmFsLmNvbSIsImV4cCI6Mzc5Njg1NDgyNCwiaWF0IjoxNjQ5MzcxMTc2LCJqdGkiOiJLV0gwX21rOVJvaThHZlg1NFVxRGNBIn0.B-5rhWzrP_hTXKorMFNEb1L5vlxSpWHd-VA6t10GLfBNBcd1LiqjpaiNW01nNEIlK_YTck25jN37Cfv66vAc0Gy3_Js1VA7PVJocdbYzVTun8nH9GrYSPoseEv86i5TFAwYe2RQiGxRLaH_jTbh0nvxdCKMjU2i6VlkyGvZRoJbPOFzZKdpK4MYWrp6winqTsZpbsRWfGS7rj_KKVmqozrXUQJelKOb6gpojHjD9FbPq8GEjbZE3YJAsJDZ220Qq9c5r9gta-JhwzDkNh_RBU96utlEGln5XnXeBXUzDQLJaBWZva7PZq4WLw9zAgmDIyiNyc3qn83skYDY7ftqjqg'

rcsdk = SDK(RINGCENTRAL_CLIENTID, RINGCENTRAL_CLIENTSECRET, RINGCENTRAL_SERVER)
platform = rcsdk.platform()

try:
    platform.login(jwt=JWT_TOKEN)
    params = {
        'dateFrom': "2012-01-01T00:00:00.000Z"
    }
    resp = platform.get('/restapi/v1.0/account/~/extension/~/call-log', params)
    # for record in resp.json().records:
    #     print("Call type: " + record.type)

except Exception as e:
    print("Unable to authenticate to platform. Check credentials." + str(e))