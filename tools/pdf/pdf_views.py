import datetime
from django.conf import settings
from django.views.generic import TemplateView
from django.views.generic.detail import SingleObjectMixin
from wkhtmltopdf.views import PDFTemplateView

from customer_invoicing.models import CustInvoice


# Some testing objects
obj_internalize = {
    'receipt_id': 142861,
    'cooperant': 5590,
    'date': datetime.datetime.now(),
    'customer_name': "Stichting IAPC Intern",
    'customer_address': "Hallenweg 5",
    'customer_zipcode': "7522 NH",
    'customer_city': "Enschede",
    'type': "Internname",
    'is_receipt': True,
    'lines': [
        {'amount': 2, 'article': "TP-LINK TL-SG108E (8p, managed)", 'piece_price': 35.50, 'vat': 21, 'total_price': 71}
    ],
    'memo': "These are networking things for the syscom.",
    'totals': {
        'excl_vat': 58.68,
        'vat': 12.32,
        'total': 71
    }
}

obj_multipage_internalize_lotsofarticles = {
    'receipt_id': 142861,
    'cooperant': 5590,
    'date': datetime.datetime.now(),
    'customer_name': "Stichting IAPC Intern",
    'customer_address': "Hallenweg 5",
    'customer_zipcode': "7522 NH",
    'customer_city': "Enschede",
    'type': "Internname",
    'is_receipt': True,
    'lines': [
        {'amount': 2, 'article': "TP-LINK TL-SG108E (8p, managed)", 'piece_price': 35.50, 'vat': 21, 'total_price': 71},
        {'amount': 2, 'article': "TP-LINK TL-SG108E (8p, managed)", 'piece_price': 35.50, 'vat': 21, 'total_price': 71},
        {'amount': 2, 'article': "TP-LINK TL-SG108E (8p, managed)", 'piece_price': 35.50, 'vat': 21, 'total_price': 71},
        {'amount': 2, 'article': "TP-LINK TL-SG108E (8p, managed)", 'piece_price': 35.50, 'vat': 21, 'total_price': 71},
        {'amount': 2, 'article': "TP-LINK TL-SG108E (8p, managed)", 'piece_price': 35.50, 'vat': 21, 'total_price': 71},
        {'amount': 2, 'article': "TP-LINK TL-SG108E (8p, managed)", 'piece_price': 35.50, 'vat': 21, 'total_price': 71},
        {'amount': 2, 'article': "TP-LINK TL-SG108E (8p, managed)", 'piece_price': 35.50, 'vat': 21, 'total_price': 71},
        {'amount': 2, 'article': "TP-LINK TL-SG108E (8p, managed)", 'piece_price': 35.50, 'vat': 21, 'total_price': 71},
        {'amount': 2, 'article': "TP-LINK TL-SG108E (8p, managed)", 'piece_price': 35.50, 'vat': 21, 'total_price': 71},
        {'amount': 2, 'article': "TP-LINK TL-SG108E (8p, managed)", 'piece_price': 35.50, 'vat': 21, 'total_price': 71},
        {'amount': 2, 'article': "TP-LINK TL-SG108E (8p, managed)", 'piece_price': 35.50, 'vat': 21, 'total_price': 71},
        {'amount': 2, 'article': "TP-LINK TL-SG108E (8p, managed)", 'piece_price': 35.50, 'vat': 21, 'total_price': 71},
        {'amount': 2, 'article': "TP-LINK TL-SG108E (8p, managed)", 'piece_price': 35.50, 'vat': 21, 'total_price': 71},
        {'amount': 2, 'article': "TP-LINK TL-SG108E (8p, managed)", 'piece_price': 35.50, 'vat': 21, 'total_price': 71},
        {'amount': 2, 'article': "TP-LINK TL-SG108E (8p, managed)", 'piece_price': 35.50, 'vat': 21, 'total_price': 71},
        {'amount': 2, 'article': "TP-LINK TL-SG108E (8p, managed)", 'piece_price': 35.50, 'vat': 21, 'total_price': 71},
        {'amount': 2, 'article': "TP-LINK TL-SG108E (8p, managed)", 'piece_price': 35.50, 'vat': 21, 'total_price': 71},
        {'amount': 2, 'article': "TP-LINK TL-SG108E (8p, managed)", 'piece_price': 35.50, 'vat': 21, 'total_price': 71},
        {'amount': 2, 'article': "TP-LINK TL-SG108E (8p, managed)", 'piece_price': 35.50, 'vat': 21, 'total_price': 71},
        {'amount': 2, 'article': "TP-LINK TL-SG108E (8p, managed)", 'piece_price': 35.50, 'vat': 21, 'total_price': 71},
        {'amount': 2, 'article': "TP-LINK TL-SG108E (8p, managed)", 'piece_price': 35.50, 'vat': 21, 'total_price': 71},
        {'amount': 2, 'article': "TP-LINK TL-SG108E (8p, managed)", 'piece_price': 35.50, 'vat': 21, 'total_price': 71},
        {'amount': 2, 'article': "TP-LINK TL-SG108E (8p, managed)", 'piece_price': 35.50, 'vat': 21, 'total_price': 71},
        {'amount': 2, 'article': "TP-LINK TL-SG108E (8p, managed)", 'piece_price': 35.50, 'vat': 21, 'total_price': 71},
        {'amount': 2, 'article': "TP-LINK TL-SG108E (8p, managed)", 'piece_price': 35.50, 'vat': 21, 'total_price': 71},
        {'amount': 2, 'article': "TP-LINK TL-SG108E (8p, managed)", 'piece_price': 35.50, 'vat': 21, 'total_price': 71},
        {'amount': 2, 'article': "TP-LINK TL-SG108E (8p, managed)", 'piece_price': 35.50, 'vat': 21, 'total_price': 71},
        {'amount': 2, 'article': "TP-LINK TL-SG108E (8p, managed)", 'piece_price': 35.50, 'vat': 21, 'total_price': 71},
        {'amount': 2, 'article': "TP-LINK TL-SG108E (8p, managed)", 'piece_price': 35.50, 'vat': 21, 'total_price': 71},
        {'amount': 2, 'article': "TP-LINK TL-SG108E (8p, managed)", 'piece_price': 35.50, 'vat': 21, 'total_price': 71},
        {'amount': 2, 'article': "TP-LINK TL-SG108E (8p, managed)", 'piece_price': 35.50, 'vat': 21, 'total_price': 71},
        {'amount': 2, 'article': "TP-LINK TL-SG108E (8p, managed)", 'piece_price': 35.50, 'vat': 21, 'total_price': 71},
        {'amount': 2, 'article': "TP-LINK TL-SG108E (8p, managed)", 'piece_price': 35.50, 'vat': 21, 'total_price': 71},
        {'amount': 2, 'article': "TP-LINK TL-SG108E (8p, managed)", 'piece_price': 35.50, 'vat': 21, 'total_price': 71},
        {'amount': 2, 'article': "TP-LINK TL-SG108E (8p, managed)", 'piece_price': 35.50, 'vat': 21, 'total_price': 71},
        {'amount': 2, 'article': "TP-LINK TL-SG108E (8p, managed)", 'piece_price': 35.50, 'vat': 21, 'total_price': 71},
        {'amount': 2, 'article': "TP-LINK TL-SG108E (8p, managed)", 'piece_price': 35.50, 'vat': 21, 'total_price': 71},
        {'amount': 2, 'article': "TP-LINK TL-SG108E (8p, managed)", 'piece_price': 35.50, 'vat': 21, 'total_price': 71},
        {'amount': 2, 'article': "TP-LINK TL-SG108E (8p, managed)", 'piece_price': 35.50, 'vat': 21, 'total_price': 71},
        {'amount': 2, 'article': "TP-LINK TL-SG108E (8p, managed)", 'piece_price': 35.50, 'vat': 21, 'total_price': 71},
        {'amount': 2, 'article': "TP-LINK TL-SG108E (8p, managed)", 'piece_price': 35.50, 'vat': 21, 'total_price': 71}
    ],
    'memo': "These are networking things for the syscom.",
    'totals': {
        'excl_vat': 2288.43,
        'vat': 480.57,
        'total': 2769
    }
}

obj_multipage_internalize_longmemo = {
    'receipt_id': 142861,
    'cooperant': 5590,
    'date': datetime.datetime.now(),
    'customer_name': "Stichting IAPC Intern",
    'customer_address': "Hallenweg 5",
    'customer_zipcode': "7522 NH",
    'customer_city': "Enschede",
    'type': "Internname",
    'is_receipt': True,
    'lines': [
        {'amount': 2, 'article': "TP-LINK TL-SG108E (8p, managed)", 'piece_price': 35.50, 'vat': 21, 'total_price': 71},
        {'amount': 2, 'article': "TP-LINK TL-SG108E (8p, managed)", 'piece_price': 35.50, 'vat': 21, 'total_price': 71},
        {'amount': 2, 'article': "TP-LINK TL-SG108E (8p, managed)", 'piece_price': 35.50, 'vat': 21, 'total_price': 71},
        {'amount': 2, 'article': "TP-LINK TL-SG108E (8p, managed)", 'piece_price': 35.50, 'vat': 21, 'total_price': 71},
        {'amount': 2, 'article': "TP-LINK TL-SG108E (8p, managed)", 'piece_price': 35.50, 'vat': 21, 'total_price': 71},
        {'amount': 2, 'article': "TP-LINK TL-SG108E (8p, managed)", 'piece_price': 35.50, 'vat': 21, 'total_price': 71},
        {'amount': 2, 'article': "TP-LINK TL-SG108E (8p, managed)", 'piece_price': 35.50, 'vat': 21, 'total_price': 71},
        {'amount': 2, 'article': "TP-LINK TL-SG108E (8p, managed)", 'piece_price': 35.50, 'vat': 21, 'total_price': 71},
        {'amount': 2, 'article': "TP-LINK TL-SG108E (8p, managed)", 'piece_price': 35.50, 'vat': 21, 'total_price': 71},
        {'amount': 2, 'article': "TP-LINK TL-SG108E (8p, managed)", 'piece_price': 35.50, 'vat': 21, 'total_price': 71},
        {'amount': 2, 'article': "TP-LINK TL-SG108E (8p, managed)", 'piece_price': 35.50, 'vat': 21, 'total_price': 71},
        {'amount': 2, 'article': "TP-LINK TL-SG108E (8p, managed)", 'piece_price': 35.50, 'vat': 21, 'total_price': 71},
        {'amount': 2, 'article': "TP-LINK TL-SG108E (8p, managed)", 'piece_price': 35.50, 'vat': 21, 'total_price': 71},
        {'amount': 2, 'article': "TP-LINK TL-SG108E (8p, managed)", 'piece_price': 35.50, 'vat': 21, 'total_price': 71},
        {'amount': 2, 'article': "TP-LINK TL-SG108E (8p, managed)", 'piece_price': 35.50, 'vat': 21, 'total_price': 71}
    ],
    'memo': "These are networking things for the syscom. Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
            "Nullam iaculis quam eros, quis varius purus ultrices ac. Nulla et diam elit. Maecenas ullamcorper ac "
            "purus nec ultrices. Aliquam aliquam neque lacus, ut facilisis eros accumsan ut. Donec volutpat sed orci "
            "id maximus. Proin consequat eros lectus, in iaculis felis faucibus vel. Aenean pharetra egestas "
            "vulputate. Nam vitae tempus nunc. Integer imperdiet pretium elit eget finibus. Cras felis arcu, luctus "
            "eget justo id, faucibus pellentesque odio.",
    'totals': {
        'excl_vat': 938.84,
        'vat': 197.16,
        'total': 1136
    }
}

obj_receipt = {
    'receipt_id': 142861,
    'cooperant': 5590,
    'date': datetime.datetime.now(),
    'customer_name': "I.C. Weiner",
    'customer_address': "Hallenweg 5",
    'customer_zipcode': "7522 NH",
    'customer_city': "Enschede",
    'type': "Kassabon",
    'is_receipt': True,
    'lines': [
        {'amount': 2, 'article': "TP-LINK TL-SG108E (8p, managed)", 'piece_price': 35.50, 'vat': 21, 'total_price': 71}
    ],
    'memo': "",
    'totals': {
        'excl_vat': 58.68,
        'vat': 12.32,
        'total': 71
    }
}

obj_invoice = {
    'receipt_id': 142861,
    'cooperant': 5590,
    'date': datetime.datetime.now(),
    'customer_name': "I.C. Weiner",
    'customer_address': "Hallenweg 5",
    'customer_zipcode': "7522 NH",
    'customer_city': "Enschede",
    'type': "Factuur",
    'is_invoice': True,
    'lines': [
        {'amount': 2, 'article': "TP-LINK TL-SG108E (8p, managed)", 'piece_price': 35.50, 'vat': 21, 'total_price': 71}
    ],
    'memo': "",
    'totals': {
        'excl_vat': 58.68,
        'vat': 12.32,
        'total': 71
    }
}


class SwipePdfView(PDFTemplateView):
    filename = "swipe.pdf"
    show_content_in_browser = settings.PDF_SHOW_IN_BROWSER

    header_template = "pdf/base/swipe_header.html"
    template_name = "pdf/base/swipe_content.html"
    footer_template = "pdf/base/swipe_footer.html"

    cmd_options = {
        'enable-javascript': True
    }

    def get_context_data(self, **kwargs):
        context = super(SwipePdfView, self).get_context_data(**kwargs)

        if self.request.GET.get('as', '') == 'html':
            context['render_headers'] = True
            context['base_path'] = ""
        else:
            context['base_path'] = "/home/kevin/IAPC/swipe/tools"
        context['show_borders'] = settings.PDF_SHOW_BORDERS
        context['pdf_title'] = "Swipe PDF"
        context['footer_text'] = "Ceci n'est pas une footeur."
        context['document_id'] = '$W-d-123456'
        return context


class ReceiptPdfTest(SingleObjectMixin, SwipePdfView):
    filename = "receipt.pdf"
    template_name = 'pdf/swipe_invoice.html'
    model = CustInvoice
    object = None
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(ReceiptPdfTest, self).get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        obj = obj_multipage_internalize_longmemo
        self.object = obj
        return obj

    def get_context_data(self, **kwargs):
        context = super(ReceiptPdfTest, self).get_context_data(**kwargs)

        context['object'] = self.get_object()

        type = context['object']['type']
        if type == "Kassabon":
            ftext = """Alle prijzen zijn inclusief BTW tenzij anders vermeld. 
            Alle prijzen zijn in euros.<br/><br/>
            Deze kassabon is tevens uw garantiebewijs. Zonder kassabon geen garantie. Op deze 
            overeenkomst en al onze leveringen zijn onze Algemene Voorwaarden van toepassing. Een 
            exemplaar wordt u op eerste verzoek toegezonden en is tevens in te zien op onze website 
            www.iapc.utwente.nl"""
        elif type == "Internname":
            ftext = "Alle prijzen zijn inclusief BTW tenzij anders vermeld. Alle prijzen zijn in euros."
        elif type == "Factuur":
            ftext = ""
        else:
            ftext = "Alle prijzen zijn inclusief BTW tenzij anders vermeld. Alle prijzen zijn in euros."

        context['footer_text'] = ftext
        context['pdf_title'] = context['object']['type']
        context['document_id'] = '$W-{}-{}'.format(context['object']['type'][0], context['object']['receipt_id'])
        return context


class HeaderTest(TemplateView):
    template_name = 'pdf/base/swipe_header.html'

    def get_context_data(self, **kwargs):
        return {
            'show_borders': settings.PDF_SHOW_BORDERS,
            'pdf_title': "Swipe PDF",
            'footer_text': "Ceci n'est pas une footeur",
            'document_id': '$W-d-123456',
        }


class FooterTest(TemplateView):
    template_name = 'pdf/base/swipe_footer.html'

    def get_context_data(self, **kwargs):
        return {
            'show_borders': settings.PDF_SHOW_BORDERS,
            'pdf_title': "Swipe PDF",
            'footer_text': "Ceci n'est pas une footeur",
            'document_id': '$W-d-123456',
        }
