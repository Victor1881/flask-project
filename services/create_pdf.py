from datetime import datetime
from pyinvoice.models import InvoiceInfo, ServiceProviderInfo, ClientInfo, Transaction
from pyinvoice.templates import SimpleInvoice
from pyinvoice.components import SimpleTable


def create_transaction_pdf(amount, user_email, transaction):
    doc = SimpleInvoice('invoice.pdf')

    # Paid stamp, optional
    doc.is_paid = False

    doc.invoice_info = InvoiceInfo(1023, datetime.now(), datetime.now())  # Invoice info, optional

    # Service Provider Info, optional
    doc.service_provider_info = ServiceProviderInfo(
        name='PyInvoice',
        city='My City',
        country='My Country',
        post_code='222222',
    )

    # Client info, optional
    doc.client_info = ClientInfo(email=user_email)

    # Tax rate, optional
    doc.set_item_tax_rate(20)  # 20%

    # Transactions detail, optional
    doc.add_transaction(Transaction('Wise', transaction, datetime.now(), amount))
    # Optional
    doc.set_bottom_tip("Email: example@example.com<br />Don't hesitate to contact us for any questions.")

    doc.finish()


