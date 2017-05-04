from django.conf import settings
from django.http import HttpResponse
from django.views.generic import View

from io import BytesIO

from reportlab.graphics.shapes import Drawing
from reportlab.lib import styles, enums
from reportlab.lib.units import cm
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph, PageBreak


class PdfData:
    document = None
    stylesheet = styles.getSampleStyleSheet()
    pages = []
    page_contents = []
    page_width = 0
    page_height = 0

    def __init__(self, show_boundary=False):
        self._filename = "swipe.pdf"
        self.show_boundary = show_boundary

    def get_filename(self):
        return self._filename

    def set_filename(self, filename):
        self._filename = filename

    filename = property(get_filename, set_filename)

    def get_title(self):
        """
        :return: The title of the PDF
        :rtype: str
        """
        return ""

    def get_author(self):
        """
        :return: The author of the PDF
        :rtype: str
        """
        return ""

    def get_subject(self):
        """
        :return: The subject of the PDF
        :rtype: str
        """
        return ""

    def get_creator(self):
        """
        :return: The creator of the PDF
        :rtype: str
        """
        return ""

    def get_show_boundary(self):
        """
        :return: If the boundary of the page should be shown on the rendered PDF
        :rtype: bool
        """
        return self.show_boundary

    def get_margins(self):
        """
        :return: Tuple of page margins, in the order (left, right, top, bottom) 
        :rtype: tuple
        """
        return cm, cm, cm, cm

    def get_allow_splitting(self):
        """
        :return: If the splitting of objects across pages is allowed. 
        :rtype: bool
        """
        return True

    # noinspection PyMethodMayBeStatic
    def render_pdf(self):
        """
        Renders the wanted PDF contents into the Canvas at self.canvas.
        Override this method with your own implementation.
        """
        # Define pages
        self.pages = [
            {
                'id': 'blank_page',
                'frames': [Frame(0, 0, self.page_width, self.page_height, showBoundary=self.get_show_boundary())]
            }
        ]

        # Set default content.
        p = self.stylesheet['Italic']
        p.alignment = enums.TA_CENTER
        self.page_contents.extend([Paragraph("Ceci n'est pas une PDF.", p)])

    def get_pdf_bytes(self):
        """
        Renders the PDF object with the wanted contents and returns the bytes of the PDF file.
        :return: The filled-in PDF object.
        :rtype: bytes
        """
        # Create buffer for quicker PDF generation
        _buffer = BytesIO()

        # Create document
        margins = self.get_margins()
        self.document = BaseDocTemplate(_buffer,
                                        showBoundary=self.get_show_boundary(),
                                        leftMargin=margins[0],
                                        rightMargin=margins[1],
                                        topMargin=margins[2],
                                        bottomMargin=margins[3],
                                        allowSplitting=self.get_allow_splitting(),
                                        title=self.get_title(),
                                        author=self.get_author(),
                                        subject=self.get_subject(),
                                        creator=self.get_creator(),
                                        )

        # Set page width and height
        # noinspection PyUnresolvedReferences
        self.page_width, self.page_height = self.document.pagesize

        # Generate contents
        self.render_pdf()

        # Generate page templates
        page_templates = [PageTemplate(**page) for page in self.pages]

        # Add templates to document
        self.document.addPageTemplates(page_templates)

        # Build the PDF
        self.document.build(self.page_contents)

        # Return the generated PDF data
        final_pdf = _buffer.getvalue()
        _buffer.close()

        return final_pdf


class PdfBehaviour:
    BEHAVIOUR_SHOW = 1
    BEHAVIOUR_DOWNLOAD = 2


class PdfView(View):
    pdf_class = PdfData
    _pdf = None  # The PDF object

    behaviour = PdfBehaviour.BEHAVIOUR_SHOW

    def get_pdf_object(self):
        show_boundary = settings.PDF_SHOW_BOUNDARIES if hasattr(settings, "PDF_SHOW_BOUNDARIES") else False
        self._pdf = self.pdf_class(show_boundary=show_boundary)
        return self._pdf

    def get(self, request, *args, **kwargs):
        # Get the PDF object
        pdf = self.get_pdf_object()

        # Create response object for PDF
        response = HttpResponse(content_type='application/pdf')
        if self.behaviour == PdfBehaviour.BEHAVIOUR_SHOW:
            response['Content-Disposition'] = 'filename="{}"'.format(pdf.get_filename())
        elif self.behaviour == PdfBehaviour.BEHAVIOUR_DOWNLOAD:
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(pdf.get_filename())
        else:
            # No special options by default.
            response['Content-Disposition'] = 'filename="{}"'.format(pdf.get_filename())

        # Render the PDF
        p = pdf.get_pdf_bytes()

        # Write the PDF to the response
        response.write(p)
        return response


def scale_svg_drawable(drawing, height=-1, width=-1, factor=-1):
    """
    Scale an SVG drawable loaded by svglib to a given height and/or width, or by a given factor.
    Height and width take priority over the factor if given.
    :param drawing: The Drawing to be scaled.
    :type drawing: Drawing
    :param height: The height to limit the drawable to.
    :type height: float
    :param width: The width to limit the drawable to.
    :type width: float
    :param factor: The factor to scale the drawable by.
    :type factor: float
    :return The resized Drawing
    :rtype Drawing
    """
    if height != -1 or width != -1:
        factor = 1
        if height != -1 and width != -1:
            factor = min((height / drawing.height), (width / drawing.width))
        elif height != -1:
            factor = height / drawing.height
        elif width != -1:
            factor = width / drawing.width

    if factor != -1:
        drawing.scale(factor, factor)
        drawing.height *= factor
        drawing.width *= factor

    return drawing


def move_svg_drawable(drawing, x=0, y=0):
    """
    Pad an SVG drawable with whitespace by the amounts on the given sides.
    :param drawing: The Drawing to be scaled.
    :type drawing: Drawing
    :param x: Amount to move drawing on the X-axis.
    :type x: float
    :param y: Amount to move drawing on the Y-axis.
    :type y: float
    :return The moved Drawing
    :rtype Drawing
    """
    drawing.translate(x, y)
    return drawing
