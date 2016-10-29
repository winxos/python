import qrcode 
from PIL import Image
qr = qrcode.QRCode(     
    version=None,     
    error_correction=qrcode.constants.ERROR_CORRECT_H,     
    box_size=10,     
    border=2, 
) 
qr.add_data('http://www.aistlab.com:3000') 
qr.make(fit=True)  
img=qr.make_image()
icon=Image.open("logo.jpg")
iw,ih=icon.size
imw,imh=img.size
sw=int(imw/4)
sh=int(imh/4)
icon=icon.resize((sw,sh),Image.ANTIALIAS)
w=int((imw-sw)/2)
h=int((imh-sh)/2)
ti=Image.new("RGB",img.size)
ti.paste(img,(0,0))
ti.paste(icon,(w,h))
ti.save("p.png")
