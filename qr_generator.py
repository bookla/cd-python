import qrcode


def get_qr(uuid):
    base_url = "https://his-christmas-dinner.web.app/session.html?sessionID="
    target = base_url + str(uuid)
    img = qrcode.make(target)
    return img
