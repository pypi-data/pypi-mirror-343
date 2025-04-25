"""
A Python library for generating ZATCA-compliant QR codes for Saudi Arabia invoices.
"""

import base64
import qrcode


def tlv_encode(tag, value):
    """
    Encodes a tag-length-value (TLV) element.

    Args:
        tag (int): The tag identifier (1 byte).
        value (str): The value corresponding to the tag.

    Returns:
        bytes: Encoded TLV element.
    """
    tag_bytes = tag.to_bytes(1, byteorder='big')
    length_bytes = len(value).to_bytes(1, byteorder='big')
    value_bytes = value.encode('utf-8')
    return tag_bytes + length_bytes + value_bytes


def generate_zatca_qr(seller_name, vat_number, timestamp, total_amount, vat_amount):
    """
    Generates base64-encoded TLV data for ZATCA-compliant QR codes.

    Args:
        seller_name (str): Seller name.
        vat_number (str): VAT registration number.
        timestamp (str): Invoice timestamp.
        total_amount (str): Invoice total amount.
        vat_amount (str): VAT amount.

    Returns:
        str: Base64-encoded TLV data.
    """
    tlv_data = b""
    tlv_data += tlv_encode(1, seller_name)  # Seller Name
    tlv_data += tlv_encode(2, vat_number)   # VAT Registration Number
    tlv_data += tlv_encode(3, timestamp)    # Timestamp of the Invoice
    tlv_data += tlv_encode(4, total_amount) # Invoice Total Amount
    tlv_data += tlv_encode(5, vat_amount)   # VAT Amount
    return base64.b64encode(tlv_data).decode('utf-8')


def create_zatca_qr(seller_name, tax_number, invoice_time, total_amount, tax_amount):
    """
    Creates a ZATCA-compliant QR code image.

    Args:
        seller_name (str): Seller name.
        tax_number (str): Tax number.
        invoice_time (str): Invoice time.
        total_amount (float): Total amount.
        tax_amount (float): Tax amount.

    Returns:
        PIL.Image.Image: QR code image.
    """
    qr_data = generate_zatca_qr(
        seller_name=seller_name,
        vat_number=tax_number,
        timestamp=invoice_time,
        total_amount=str(total_amount),
        vat_amount=str(tax_amount)
    )
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    return qr.make_image(fill='black', back_color='white')
