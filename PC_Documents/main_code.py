from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.pagesizes import letter
from pdf_flowable_blocks.pdf_flowable_blocks.paragraph_block import ParagraphBlockV2
from pdf_flowable_blocks.pdf_flowable_blocks.header_block import HeaderBlockV2
from pdf_flowable_blocks.pdf_flowable_blocks.generic_table_block import GenericTableBlockV2
from pdf_flowable_blocks.pdf_flowable_blocks.generic_table_block import CellConfig, RowConfig
#from pdf_flowable_blocks.pdf_flowable_blocks.grid_block import GridBlockV2

def generate_pdf_for_letter():
    doc = SimpleDocTemplate("pc_documents.pdf", pagesize=letter, leftMargin=48, \
                            rightMargin=48, topMargin=50, bottomMargin=50)
    story = []
    logo_url = "https://crm-backend-media-static.s3.ap-south-1.amazonaws.com/alpha/media/tgbpass_logo.png"
    header_text = "If “Title 1” has 2 lines height of the heading "
    sub_header_text = "If “Title 2” has long text of the heading be here"
    sub_sub_header_text = "If “Title 3” has long text of the heading be here"
    sub_sub_header_text = "If “Title 3” has long text of the heading be here"
    right_block_text = "BuildNow"

    heads = HeaderBlockV2().create_header_flowables(logo_url=logo_url, header_text=header_text, \
                                                    sub_header_text=sub_header_text,
                                                    sub_sub_header_text=sub_sub_header_text, \
                                                    right_block_text=right_block_text)
    for head in heads:
        story.append(head)
    heading = "Sir/Madam"
    lines = ["""Sub: Greater Hyderabad Municipal Corporation - Construction of Individual<br/>
                            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Residential Building consisting of Ground Floor to an extent of 267.56<br/>
                            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Sq.Meters (320.0 Sq.Yds)situated at Plot No: 23, Locality: 23, Survey No: 233,<br/> 
                            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Amberpet(V), Musheerabad Circle 15, Secunderabad Zone,
                            Amberpet(M),<br/> 
                            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;GHMC, Hyderabad(Dist) - Building Permission-Instant Approval
                            issued - Reg""", """Ref: 1. Your Application dated: 13-11-2024""",
             """&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2. G.O.Ms.No.168, MA&UD, dt.07-04-2012 and its time to time amendments."""]

    paragraphs = ParagraphBlockV2().create_flowables(heading=heading, lines=lines)
    for paragraph in paragraphs:
        story.append(paragraph)

    lines = ["""With reference to your application 1st cited, the Certificate of Registration for <br/>construction of
                Individual Residential Building is hereby issued based."""]
    paragraphs = ParagraphBlockV2().create_flowables(lines=lines)
    for paragraph in paragraphs:
        story.append(paragraph)

    row1_cells = [CellConfig(value="1", width=10),CellConfig(value="Name", width=30),\
                  CellConfig(value="Smt DEVULAPALLI PRASANNA KUMARI", width=60)]

    row2_cells = [CellConfig(value="2", width=10), CellConfig(value="Permit No", width=30),\
                  CellConfig(value="DEVULAPALLI UMA SHANKAR", width=60)]
    row3_cells = [CellConfig(value="3", width=10), CellConfig(value="Date", width=30), \
                 CellConfig(value="FLAT NO 201, MARUTHI KALYAN APT,<br/> NALLAKUNTA, HYDERABAD-44", width=60)]
    rows = [RowConfig(cells=row1_cells,height=36),RowConfig(cells=row2_cells,height=36),\
            RowConfig(cells=row3_cells, height=36)]
    heading = "Section Heading Title"
    table_values = GenericTableBlockV2().create_generic_table_flowables(heading=heading, \
                                                                        rows=rows)
    for value in table_values:
        story.append(value)
    doc.build(story)