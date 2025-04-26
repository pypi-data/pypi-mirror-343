# ZATCA QR

A Python library for generating ZATCA-compliant QR codes for Saudi Arabian e-invoices.

[![PyPI version](https://badge.fury.io/py/qrzatca.svg)](https://badge.fury.io/py/qrzatca)

---

## 📋 Description

**qrzatca** is a lightweight and developer-friendly Python package designed to help businesses in Saudi Arabia comply with ZATCA (Zakat, Tax, and Customs Authority) e-invoicing regulations.

This library encodes invoice information using TLV (Tag-Length-Value) format and generates QR codes containing:

- Seller name  
- VAT registration number  
- Invoice timestamp  
- Invoice total amount  
- VAT amount  

These QR codes can be used in invoice PDFs, printed receipts, and digital documents to meet ZATCA Phase I & II compliance.

---

## ✅ Key Features

- 🔒 ZATCA-compliant QR code generation  
- 📦 Encodes seller, VAT, timestamp, amount, and tax  
- 🖼️ Returns image as a Pillow object (customizable or savable)  
- 🧩 Easy integration into Django, Flask, or standalone Python apps  
- ⚙️ Minimal dependencies (`qrcode`, `Pillow`)

---
## 🧾 Usage Example
```python

from qrzatca import create_zatca_qr

# Input invoice data
seller_name = "ABC Trading Co."
vat_number = "123456789012345"
invoice_time = "2025-04-25T12:30:00Z"
total_amount = 2500.00
vat_amount = 375.00

# Generate the ZATCA-compliant QR code
qr_image = create_zatca_qr(
    seller_name=seller_name,
    tax_number=vat_number,
    invoice_time=invoice_time,
    total_amount=total_amount,
    tax_amount=vat_amount
)

# Save the image to a file
qr_image.save("zatca_invoice_qr.png")

# Or display it directly (if using Jupyter or a GUI app)
qr_image.show()



```



## 📦 Installation

Install directly from PyPI:

```bash
pip install qrzatca



