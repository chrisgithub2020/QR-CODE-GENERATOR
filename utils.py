import qrcode
from PIL import Image, ImageDraw
from qrcode.image.styledpil import StyledPilImage
import uuid


def generate_qr_code(link: str):
    f_name = uuid.uuid4().__str__()
    print(link)
    qr = qrcode.QRCode(
        version=5,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
    )
    qr.add_data(link)

    logo = Image.open("./resources/revna_logo.png").convert("RGBA").resize((95,95), Image.LANCZOS)


    qr.make(fit=True)
    qr_image = qr.make_image(back_color="white", fill_color=(3, 66, 112, 1))
    
    ## set position of the logo
    pos_x = (qr_image.size[0]-logo.width)//2
    pos_y = (qr_image.size[1]-logo.height)//2

    ## create padding illusion around image
    draw = ImageDraw.Draw(qr_image)
    draw.rectangle((pos_x, pos_y, pos_x+100, pos_y+90), fill="white")

    # put image in the code
    qr_image.paste(logo, (pos_x+5,pos_y), logo)
    
    qr_image.save(f"./images/{f_name}.png")
    return f_name