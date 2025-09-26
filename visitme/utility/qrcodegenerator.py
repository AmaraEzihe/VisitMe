import qrcode
from io import BytesIO

def generate_qrcode(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    #use if you want to save image to disk
    # img.save(filename)

    # Save image to memory (instead of file)
    buffer = BytesIO()
    img.save(buffer, format="PNG")  # Save as PNG
    qr_blob = buffer.getvalue()     # Raw bytes
    buffer.close()

    return qr_blob