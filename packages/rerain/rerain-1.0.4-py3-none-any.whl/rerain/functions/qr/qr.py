import os
import qrcode

def newqr(data, filename="newqr.png"):
    current_directory = os.path.dirname(os.path.realpath(__file__))
    filepath = os.path.join(current_directory, filename)

    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=0)
    qr.add_data(data)
    qr.make(fit=True)
    qr.make_image(fill='black', back_color='white').save(filepath)

    print(f"QR code saved as {filepath}")
