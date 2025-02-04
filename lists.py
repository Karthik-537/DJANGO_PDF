from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, ListFlowable, ListItem, Spacer, Paragraph
from reportlab.lib.styles import ParagraphStyle, ListStyle

lists_dict = {
    "Project Planning": ["Define project scope", "Set timeline", " Allocate resources"],
    "Implementation Phase": ["Development", "Testing", "Deployment"],
    "Project Review": [" Performance analysis", "Documentation", "Feedback collection"]
}
style = ParagraphStyle(
        name="lists",
        fontName="Helvetica",
        fontSize=12,
        fontColor="black"
        )
list_style = ListStyle(
                name="lists",
                bulletColor="black",
                bulletFontSize=12
             )
doc = SimpleDocTemplate("lists.pdf", pagesize=letter, leftMargin=48,
                            rightMargin=48, topMargin=50, bottomMargin=50)

story = []
main_list_items = []
for list_header, list_values in lists_dict.items():
    list_items = []
    for value in list_values:
        list_item = ListItem([Paragraph(value, style=style), Spacer(1,10)])
        list_items.append(list_item)
    sublist_flowable = ListFlowable(list_items, bulletType='1')
    header_paragraph = Paragraph(list_header, style=style)
    main_list_items.append(ListItem([header_paragraph, Spacer(1,10), sublist_flowable]))

main_list_flowable = ListFlowable(main_list_items, bulletType="bullet", style=list_style)

story.append(main_list_flowable)

doc.build(story)

