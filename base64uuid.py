#coding:utf-8
#python create uuid and convert to base64 for shorter.
#winxos 2016-09-10

import uuid
import base64
uid=uuid.uuid3(uuid.NAMESPACE_DNS,'winxos')
suid=base64.b64encode(uid.bytes)[:-2]
print len(suid),suid