from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.styles import  ParagraphStyle
from pdf_flowable_blocks.pdf_flowable_blocks.paragraph_block import ParagraphBlockV2
from pdf_flowable_blocks.pdf_flowable_blocks.header_block import HeaderBlockV2
from pdf_flowable_blocks.pdf_flowable_blocks.generic_table_block import GenericTableBlockV2
from pdf_flowable_blocks.pdf_flowable_blocks.generic_table_block import CellConfig, RowConfig
from reportlab.lib.enums import TA_CENTER
from pdf_flowable_blocks.pdf_flowable_blocks.grid_block import GridBlockV2
from pdf_flowable_blocks.pdf_flowable_blocks.list_block import ListBlockV2

regular_font_path = "pdf_letter_generator/fonts/Inter-4.1/extras/ttf/Inter-Regular.ttf"
medium_font_path = "pdf_letter_generator/fonts/Inter-4.1/extras/ttf/Inter-Medium.ttf"
bold_font_path = "pdf_letter_generator/fonts/Inter-4.1/extras/ttf/Inter-Bold.ttf"
italic_font_path = "pdf_letter_generator/fonts/Inter-4.1/extras/ttf/Inter-Italic.ttf"
bolditalic_font_path = "pdf_letter_generator/fonts/Inter-4.1/extras/ttf/Inter-BoldItalic.ttf"

# Register fonts
pdfmetrics.registerFont(TTFont("Inter", regular_font_path))
pdfmetrics.registerFont(TTFont("Inter-Medium", medium_font_path))
pdfmetrics.registerFont(TTFont("Inter-Bold", bold_font_path))
pdfmetrics.registerFont(TTFont("Inter-Italic", italic_font_path))
pdfmetrics.registerFont(TTFont("Inter-BoldItalic", bolditalic_font_path))

pdfmetrics.registerFontFamily(
    "Inter",
    normal="Inter",
    bold="Inter-Bold",
    italic="Inter-Italic",
    boldItalic="Inter-BoldItalic"
)

def generate_pdf_for_letter():
    doc = SimpleDocTemplate("pc_documents.pdf", pagesize=letter, leftMargin=48,
                            rightMargin=48, topMargin=50, bottomMargin=50)
    story = []
    logo_url = "https://crm-backend-media-static.s3.ap-south-1.amazonaws.com/alpha/media/tgbpass_logo.png"
    header_text = "If “Title 1” has 2 lines height of the heading"
    sub_header_text = "If “Title 2” has long text of the heading be here"
    sub_sub_header_text = "<b>If “Title 3”</b> has long text of the heading be here"
    right_block_text = "BuildNow"

    heads = HeaderBlockV2().create_header_flowables(logo_url=logo_url, header_text=header_text, \
                                                    sub_header_text=sub_header_text,
                                                    sub_sub_header_text=sub_sub_header_text, \
                                                    right_block_text=right_block_text)
    for head in heads:
        story.append(head)
    grid_block = GridBlockV2()
    heading = "To,"
    grid_units = [
        {
            "text_lines":["""1. Smt. DEVULAPALLI PRASANNA KUMARI<br/>
                            &nbsp;&nbsp;&nbsp;W/o DEVULAPALLI UMA SHANKAR<br/>
                            &nbsp;&nbsp;&nbsp;FLAT NO 201, MARUTHI KALYAN APT,<br/>
                            &nbsp;&nbsp;&nbsp;NALLAKUNTA, HYDERABAD-44"""],
            "unit_width": 49.00
        },
        {
            "text_lines":["""Application No/ Permit No:<br/>Permit No.<br/>Date"""],
            "unit_width": 20.70
        },
        {
            "text_lines":["""128907/GHMC/0128/2024<br/><br/>128907/GHMC/0128/2024<br/>13-11-2024"""],
            "unit_width": 30.30
        }
    ]
    grid_values = grid_block.create_grid_flowables(heading=heading, grid_units=grid_units)
    for value in grid_values:
        story.append(value)

    heading = "Sir/Madam"
    lines = ["""Sub: Greater Hyderabad Municipal Corporation - Construction of Individual<br/>
                            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Residential Building consisting of Ground Floor to an extent of 267.56<br/>
                            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Sq.Meters (320.0 Sq.Yds)situated at Plot No: 23, Locality: 23, Survey No: 233,<br/> 
                            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Amberpet(V), Musheerabad Circle 15, Secunderabad Zone,
                            Amberpet(M),<br/> 
                            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;GHMC, Hyderabad(Dist) - Building Permission-Instant Approval
                            issued - Reg<br/><br/>Ref: 1. Your Application dated: 13-11-2024<br/>
                            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2. G.O.Ms.No.168, MA&UD, dt.07-04-2012 and its time to time amendments."""]

    paragraphs = ParagraphBlockV2().create_flowables(heading=heading, lines=lines)
    for paragraph in paragraphs:
        story.append(paragraph)

    lines = ["""With reference to your application 1st cited, the Certificate of Registration for <br/>construction of
                Individual Residential Building is hereby issued based."""]
    paragraphs = ParagraphBlockV2().create_flowables(lines=lines)
    for paragraph in paragraphs:
        story.append(paragraph)

    row1_cells = [CellConfig(value="1", width=10),CellConfig(value="Name", width=30),
                  CellConfig(value="Smt DEVULAPALLI PRASANNA KUMARI", width=60)]

    row2_cells = [CellConfig(value="2", width=10), CellConfig(value="Permit No.", width=30),
                  CellConfig(value="DEVULAPALLI UMA SHANKAR", width=60)]
    row3_cells = [CellConfig(value="3", width=10), CellConfig(value="Date", width=30),
                 CellConfig(value="FLAT NO 201, MARUTHI KALYAN APT,<br/> NALLAKUNTA, HYDERABAD-44", width=60)]
    rows = [RowConfig(cells=row1_cells,height=30),RowConfig(cells=row2_cells,height=30),
            RowConfig(cells=row3_cells, height=36)]
    heading = "Section Heading Title"
    table_values = GenericTableBlockV2().create_generic_table_flowables(heading=heading,
                                                                        rows=rows)
    for value in table_values:
        story.append(value)

    row1_cells = [CellConfig(value="1", width=10), CellConfig(value="Extent of the Plot", width=30),
                  CellConfig(value="30.1 Sq.Mtrs (36.0 Sq.Yds)", width=60)]

    row2_cells = [CellConfig(value="2", width=10), CellConfig(value="Permit No.", width=30),
                  CellConfig(value="DEVULAPALLI UMA SHANKAR", width=60)]
    row3_cells = [CellConfig(value="3", width=10), CellConfig(value="Date", width=30),
                  CellConfig(value="FLAT NO 201, MARUTHI KALYAN APT,<br/> NALLAKUNTA, HYDERABAD-44", width=60)]
    rows = [RowConfig(cells=row1_cells, height=30), RowConfig(cells=row2_cells, height=30),
            RowConfig(cells=row3_cells, height=36)]

    heading = "Plot Details"
    table_values = GenericTableBlockV2().create_generic_table_flowables(heading=heading,
                                                                        rows=rows)
    for value in table_values:
        story.append(value)

    list_block = ListBlockV2()
    list_values = list_block.create_list_flowables(
                    heading="""The Building permission is sanctioned subject to following conditions
                               The applicant should follow the clause 5.f (i) (ii) (iii) (iv) (v)( vii) (xi)&(xiv) of
                               G.O.Ms.No.168, MA&UD, dt:07.04.2012.
                            """,
                    lines=["""Post verification will be carried out as per the provisions of the GHMC TG-bPASS Act and
                              action will be initiated if any violation or misrepresentation of the facts is found.
                           """,
                           """In case of false declaration, the applicant is personally held responsible as per the
                              provisions of the GHMC TG-bPASS Act.
                           """,
                           """The applicant or owner is personally held responsible and accountable in case of false or
                              incorrect Self-Declaration if any found and shall be liable for punishment as per the
                              provisions of the GHMC TG-bPASS Act.
                           """,
                           """If the plot under reference is falling in any prohibited lands / Govt. lands / Municipal lands /
                              layout open space, earmarked parks and playground as per Master plan / Water bodies, the
                              Certificate of Registration will be revoked and structure there upon will be demolished as
                              per the provisions of the GHMC TG-bPASS Act.
                           """],
                    presentation_type="ordered_list")
    for value in list_values:
        story.append(value)

    list_values = list_block.create_list_flowables(
        heading="""The Building permission is sanctioned subject to following conditions
                   The applicant should follow the clause 5.f (i) (ii) (iii) (iv) (v)( vii)
                   (xi)&(xiv) of G.O.Ms.No.168, MA&UD, dt:07.04.2012.
                """,
        lines=["""Post verification will be carried out as per the provisions of the GHMC TG-bPASS Act and
                  action will be initiated if any violation or misrepresentation of the facts is found.
               """,
               """In case of false declaration, the applicant is personally held responsible as per the
                  provisions of the GHMC TG-bPASS Act.
               """],
        presentation_type="unordered_list")
    for value in list_values:
        story.append(value)

    grid_units = [
        {
            "text_lines": ["""NOTE: This is a computer-generated letter and does not require any manual signatures."""],
            "unit_width": 100,
            "alignment": "CENTER"
        }
    ]
    grid_values = grid_block.create_grid_flowables(grid_units=grid_units)
    for value in grid_values:
        story.append(value)

    def add_watermark(canvas, doc):

        image_path = "https://crm-backend-media-static.s3.ap-south-1.amazonaws.com/alpha/media/tgbpass_logo.png"

        img_width = 400
        img_height = 400

        page_width, page_height = letter
        x_position = (page_width - img_width) / 2
        y_position = (page_height - img_height) / 2

        canvas.setFillAlpha(0.2)

        canvas.drawImage(image_path, x_position, y_position, width=img_width, height=img_height, mask='auto')

    doc.build(story, onFirstPage=add_watermark, onLaterPages=add_watermark)