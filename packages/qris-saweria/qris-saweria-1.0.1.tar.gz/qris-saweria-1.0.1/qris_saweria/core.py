import random
import string
import json
from typing import Tuple, Optional
import qrcode
from PIL import Image, ImageDraw, ImageFont
import os
from bs4 import BeautifulSoup
import requests

BACKEND = 'https://backend.saweria.co'
FRONTEND = 'https://saweria.co'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
}

RANDOM_MESSAGES = [
    "Semangat kak!",
    "Terima kasih atas kontennya",
    "Lanjutkan karya baiknya",
    "Support terus",
    "Keep up the good work!",
    "Sukses selalu",
    "Tetap semangat"
]

def random_sender() -> str:
    names = ['Budi', 'Ani', 'Dedi', 'Rina', 'Joko', 'Siti', 'Ahmad', 'Dewi', 'Agus', 'Linda', 'Rudi', 'Maya', 'Fajar', 'Nina', 'Hendra', 'Lina', 'Yanto', 'Rina', 'Bayu', 'Dina', 'Rizky', 'Sari', 'Aji', 'Rita', 'Doni', 'Wati', 'Irfan', 'Yuni', 'Rama', 'Dewi']
    return random.choice(names)

def random_message() -> str:
    return random.choice(RANDOM_MESSAGES)

def insert_plus_in_email(email, insert_str):
    return email.replace("@", f"+{insert_str}@", 1)

def create_payment_qr(
    saweria_username: str,
    amount: int,
    email: str,
    output_path: str = 'qris.png',
    use_template: bool = True
) -> Tuple[str, str, str]:
    """
    Create a QRIS payment for Saweria and generate QR image.
    Returns (qr_string, transaction_id, output_path)
    """
    if not saweria_username or not amount or not email:
        raise ValueError("Parameter is missing!")
    if amount < 1000:
        raise ValueError("Minimum amount is 1000 ya ajg")

    sender = random_sender()
    pesan = random_message()
    email_plus = insert_plus_in_email(email, sender)

    # Get userId from saweria username
    response = requests.get(f'{FRONTEND}/{saweria_username}', headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    next_data_script = soup.find(id='__NEXT_DATA__')
    if not next_data_script:
        raise Exception('Saweria account not found')
    data = json.loads(next_data_script.text)
    user_id = data.get("props", {}).get("pageProps", {}).get("data", {}).get("id")
    if not user_id:
        raise Exception('Saweria account not found')

    payload = {
        "agree": True,
        "notUnderage": True,
        "message": pesan,
        "amount": int(amount),
        "payment_type": "qris",
        "vote": "",
        "currency": "IDR",
        "customer_info": {
            "first_name": sender,
            "email": email_plus,
            "phone": ""
        }
    }
    ps = requests.post(f"{BACKEND}/donations/{user_id}", json=payload, headers=HEADERS)
    if not ps.ok:
        raise Exception(f'Failed to create payment: {ps.text}')
    pc = ps.json()["data"]
    qr_string = pc["qr_string"]
    transaction_id = pc["id"]

    # Generate QR image
    if use_template:
        template_path = os.path.join(os.path.dirname(__file__), 'template.png')
        generate_qr_image(qr_string, output_path, template_path, saweria_username)
    else:
        generate_qr_image(qr_string, output_path, None, None)

    return qr_string, transaction_id, output_path

def check_paid_status(transaction_id: str) -> bool:
    """
    Check if a Saweria QRIS payment is paid.
    Returns True if paid, False otherwise.
    """
    url = f'{BACKEND}/donations/qris/{transaction_id}'
    r = requests.get(url, headers=HEADERS)
    if not r.ok:
        raise Exception('Transaction ID not found')
    data = r.json()['data']
    return data['qr_string'] == ''

def generate_qr_image(qr_string: str, output_path: str = 'qris.png', template_path: Optional[str] = None, saweria_username: Optional[str] = None) -> str:
    """
    Generate QR image (with/without template DANA)
    """
    qr_img = qrcode.make(qr_string)
    if template_path and os.path.exists(template_path):
        template = Image.open(template_path).convert('RGBA')
        qr_img = qr_img.resize((380, 380))
        # Paste QR to center
        x = (template.width - 380) // 2
        y = (template.height - 380) // 2 + 20
        template.paste(qr_img, (x, y))
        # Draw username if provided
        if saweria_username:
            draw = ImageDraw.Draw(template)
            try:
                font = ImageFont.truetype('arial.ttf', 32)
            except:
                font = ImageFont.load_default()
            draw.text((template.width // 2, 160), saweria_username, fill='black', anchor='mm', font=font)
        template.save(output_path)
    else:
        qr_img.save(output_path)
    return output_path 