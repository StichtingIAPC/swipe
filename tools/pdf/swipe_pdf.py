from django.conf import settings
from django.contrib.staticfiles import finders
from reportlab.graphics.barcode import createBarcodeDrawing
from reportlab.lib import enums
from reportlab.lib.units import cm
from reportlab.pdfgen.canvas import Canvas

from reportlab.platypus import Paragraph, Frame, FrameBreak, BaseDocTemplate
from svglib.svglib import svg2rlg

from tools.pdf.base_pdf import PdfView, PdfData, scale_svg_drawable, move_svg_drawable


class SwipePdfData(PdfData):
    current_page = None
    header_height = 6 * cm
    footer_height = 4 * cm
    logo_width = 7 * cm
    barcode_width = 5 * cm

    @staticmethod
    def render_header_footer(canvas, doc):
        SwipePdfData.render_header(canvas, doc)
        SwipePdfData.render_footer(canvas, doc)

    @staticmethod
    def render_header(canvas, doc):
        """
        Render the header of this page
        :type canvas: Canvas
        :type doc: BaseDocTemplate
        """
        # Load resources
        header_path = settings.PDF_HEADER_IMAGE_PATH
        logo_path = settings.PDF_LOGO_IMAGE_PATH

        header_drawable = svg2rlg(finders.find(header_path))
        if header_drawable is None:
            raise ValueError("File at '{}' does not exist.".format(finders.find(header_path)))

        logo_drawable = svg2rlg(finders.find(logo_path))
        if logo_drawable is None:
            raise ValueError("File at '{}' does not exist.".format(finders.find(logo_path)))

        # Save state of canvas so we can draw on it
        canvas.saveState()

        # Resize resources to fit properly on the page, and add padding
        logo_drawable = scale_svg_drawable(logo_drawable, height=SwipePdfData.header_height - doc.topMargin,
                                           width=SwipePdfData.logo_width - doc.rightMargin)
        logo_drawable = move_svg_drawable(logo_drawable, y=1 * cm)

        header_drawable = scale_svg_drawable(header_drawable, height=SwipePdfData.header_height - doc.topMargin,
                                             width=doc.width - logo_drawable.width - doc.leftMargin)
        header_drawable = move_svg_drawable(header_drawable, y=-5)

        # Add resources to the page
        header_drawable.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - header_drawable.height)
        logo_drawable.drawOn(canvas, doc.width + doc.leftMargin - logo_drawable.width,
                             doc.height + doc.topMargin - logo_drawable.height)

    @staticmethod
    def render_footer(canvas, doc):
        """
        Render the footer of this page
        :type canvas: Canvas
        :type doc: BaseDocTemplate
        """
        # Add content to footer
        p = SwipePdfData.stylesheet['Normal']
        p.alignment = enums.TA_LEFT
        para = Paragraph(
            "Alle prijzen zijn inclusief BTW tenzij anders vermeld. Alle prijzen zijn in euros.<br/>"
            "<br/>"
            "Deze kassabon is tevens uw garantiebewijs. Zonder kassabon geen garantie. Op deze "
            "overeenkomst en al onze leveringen zijn onze Algemene Voorwaarden van toepassing. Een "
            "exemplaar wordt u op eerste verzoek toegezonden en is tevens in te zien op onze website "
            "www.iapc.utwente.nl",
            p
        )
        w, h = para.wrap(doc.width - SwipePdfData.barcode_width, doc.bottomMargin)
        para.drawOn(canvas, doc.leftMargin, doc.bottomMargin)

        # Render barcode at bottom right corner
        # TODO: Move this to a separate, non-static function render_barcode so I can actually set the proper number
        d = createBarcodeDrawing('Code128', value="$W-O-123456", width=SwipePdfData.barcode_width, humanReadable=True,
                                 fontName="Helvetica", fontSize=6)
        vcenter_spacing = (h / 2) - (d.height / 2)  # Calculate vertical spacing needed to center barcode with text.
        d.drawOn(canvas, doc.leftMargin + w, doc.bottomMargin + vcenter_spacing)

    def render_contents(self):
        # Define frames for page
        margins = self.get_margins()
        content_frame = Frame(0, self.footer_height,
                              self.page_width, self.page_height - self.header_height - self.footer_height,
                              showBoundary=self.show_boundary, id="content",
                              leftPadding=margins[0], rightPadding=margins[1])

        # Add content to page
        p = self.stylesheet['Normal']
        p.alignment = enums.TA_CENTER
        self.page_contents.extend([Paragraph("<br /><br /><br /><br /><br />"
                                             "<i>Ceci n'est pas une PDF.</i>"
                                             "<br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br />"
                                             "Or is it?"
                                             "<br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br />"
                                             "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum elementum faucibus blandit. Fusce nibh tellus, posuere vitae dignissim eu, egestas id justo. Sed malesuada euismod fringilla. Pellentesque lobortis felis tellus, id blandit sapien sollicitudin in. Nam lobortis risus nunc, vel efficitur sem vestibulum quis. Vestibulum tempor risus at leo suscipit, at vulputate justo venenatis. Phasellus quis quam feugiat, sollicitudin arcu nec, pharetra felis. Morbi vitae libero tortor. Sed egestas elit sodales mi fermentum tincidunt."
                                             "<br /><br />"
                                             "Duis cursus nibh urna, et vehicula arcu pulvinar sit amet. In id dapibus mauris, ut sollicitudin leo. In commodo, elit vulputate condimentum tempor, dolor risus sodales mi, quis molestie lectus sapien non mi. In et ultricies dui. Aliquam molestie nibh ut eros congue, ac sagittis neque eleifend. Vivamus lacinia commodo elit vel euismod. Etiam ultricies leo ac tortor scelerisque dapibus. Fusce scelerisque, quam ac placerat congue, nulla metus cursus erat, et auctor dui ante non mauris. Cras tristique erat orci."
                                             "<br /><br />"
                                             "Vivamus quis lorem a nunc aliquet facilisis. Nam vehicula sollicitudin nisi, ac molestie diam. Donec id euismod quam. Praesent congue lacus ex, id placerat dui interdum eu. Quisque malesuada laoreet diam ut iaculis. Etiam ullamcorper nunc eu odio luctus volutpat. Nunc elementum blandit lacinia. Mauris pharetra eget lorem eget hendrerit."
                                             "<br /><br />"
                                             "Donec sit amet sagittis libero. Curabitur vitae ligula quam. In quis iaculis justo. Phasellus mollis imperdiet massa. Ut aliquam aliquam justo, pharetra pharetra lorem dictum in. Sed erat magna, auctor faucibus dui vel, dapibus dictum nisi. Duis at lorem eu erat imperdiet viverra. Proin non interdum diam. Vivamus fringilla pellentesque dui, dictum blandit felis placerat vel. Proin vitae finibus arcu, id aliquet eros. Sed ex felis, laoreet at quam nec, egestas ultrices mi. Cras eget mollis diam, sed lacinia nisi. Praesent at aliquam erat. Nulla facilisis mollis felis vel hendrerit."
                                             "<br /><br />"
                                             "In porta eget ipsum eu malesuada. Aliquam sapien nisl, venenatis quis aliquet sed, gravida at justo. Aenean dictum, justo eu aliquam tincidunt, mauris nunc semper magna, eget sollicitudin turpis arcu et neque. Integer orci purus, malesuada laoreet vulputate nec, tincidunt vitae dolor. Curabitur et enim ut lacus ornare sagittis a in metus. Interdum et malesuada fames ac ante ipsum primis in faucibus. Suspendisse dignissim congue leo sit amet auctor. In gravida neque odio, sed commodo justo condimentum quis. Suspendisse leo mi, dignissim at purus sit amet, vestibulum ultricies erat."
                                             , p),
                                   FrameBreak()
                                   ])

        # Add frame to page
        self.current_page['frames'].append(content_frame)

    def render_pdf(self):
        """
        Renders a header, the wanted PDF contents, and a footer into the Canvas at self.canvas.
        """
        # Define pages structure and first page
        self.pages = []
        self.current_page = {
            'id': 'swipe_page',
            'frames': [],
            'onPage': SwipePdfData.render_header_footer
        }

        # Render the necessary frames/pages for this page
        self.render_contents()

        # Add current page to pages list to finish the PDF.
        self.pages.append(self.current_page)


class SwipePdfView(PdfView):
    pdf_class = SwipePdfData
