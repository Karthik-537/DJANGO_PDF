from reportlab.platypus import SimpleDocTemplate, Spacer
from pdf_flowable_blocks.pdf_flowable_blocks.extra_feature_paragraph_block import ExtraFeatureParagraph
from reportlab.lib.pagesizes import letter

extra_paragraph = ExtraFeatureParagraph()

doc = SimpleDocTemplate("paragraph.pdf", pagesize=letter, leftMargin=48, \
                            rightMargin=48, topMargin=50, bottomMargin=50)
story = []

all_flowables = []
# lines = ["""The applicant has mortgaged 6.67% of Villas area i.e. Plot Nos. 30,42,46,47,48,86 & 103 to an extent of 2848.95 Sqm of
#                     Sy.No.87/P,88/P & 89/P situated at Mankhal Village, Maheswaram Mandal, Ranga Reddy District, Mortgaged in favour
#                     of The Metropolitan Commissioner, Hyderabad Metropolitan Development Authority, Swarna jayanthi complex,
#                     Ameerpet Hyderabad, Vide Document No. 14678/2024, Dt: 06.09.2024.<br/><br/>
#                      Applicant has submitted NALA conversation Certificate<br/><br/>
#                      Accordingly added proceedings condition"""]
grid_units = [
    {
        "text_lines": ["<b>SUNKARA SRI VEERA VIJAYA MANI DHANARAJU[Planning Ofcr]</b>"],  # Name
        "unit_width": 70,  # Column width (example)
        "alignment": "LEFT",  # Align name to the left
    },
    {
        "text_lines": ["19/9/2024 5:11:05 PM"],  # Date and Time
        "unit_width": 32,  # Column width (example)
        "alignment": "RIGHT",  # Align date and time to the center
    },
]
flowables = create_feature_paragraph_flowables(grid_units=grid_units)

all_flowables.extend(flowables)
all_flowables.extend([Spacer(1, 24)])
# lines = ["""The applicant has mortgaged 6.67% of Villas area i.e. Plot Nos. 30,42,46,47,48,86 & 103 to an extent of 2848.95 Sqm
#                     of Sy.No.87/P,88/P & 89/P situated at Mankhal Village, Maheswaram Mandal, Ranga Reddy District, Mortgaged in
#                     favour of The Metropolitan Commissioner, Hyderabad Metropolitan Development Authority, Swarna jayanthi complex,
#                     Ameerpet Hyderabad, Vide Document No. 14678/2024, Dt: 06.09.2024.
#                     The applicant has submitted NALA conversion certificate
#                     Hence proceeding conditions and drawing conditions were added for further process
#                     Submitted for kind perusal"""]
grid_units = [
    {
        "text_lines": ["<b>SHASHIKALA jpo R</b>[Junior Planning Officer ]"],  # Name
        "unit_width": 70,  # Column width (example)
        "alignment": "LEFT",  # Align name to the left
    },
    {
        "text_lines": ["18/9/2024 6:18:03 PM"],  # Date and Time
        "unit_width": 32,  # Column width (example)
        "alignment": "RIGHT",  # Align date and time to the center
    },
]
flowables = create_feature_paragraph_flowables(grid_units=grid_units)
all_flowables.extend(flowables)
for flowable in all_flowables:
    story.append(flowable)

doc.build(story)