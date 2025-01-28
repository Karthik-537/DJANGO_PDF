from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.graphics.shapes import Drawing, Line
from reportlab.lib.colors import Color

def get_paragraph_style(font_size=None, text_color=None, font_name=None):
    style = ParagraphStyle(name='Custom')
    if font_size:
        style.fontSize = font_size
    if text_color:
        style.textColor = text_color
    if font_name:
        style.fontName = font_name
    return style

doc = SimpleDocTemplate(
    "data_analysis_project_assignment.pdf",
    pagesize=letter,
    rightMargin=inch,
    leftMargin=inch,
    topMargin=inch,
    bottomMargin=inch,
)

story = []

story.append(Paragraph('Data Analysis Project Assignment', get_paragraph_style(font_size=20, text_color='blue', font_name='Helvetica-Bold')))
story.append(Spacer(0, 0.5 * inch))

line = Drawing(500, 1)
line_shape = Line(0, 0, 450, 0)
line_shape.strokeColor = Color(0, 0, 0)
line.add(line_shape)
story.append(line)
story.append(Spacer(0, 0.5 * inch))

story.append(Paragraph('Project Description', get_paragraph_style(font_size=18, text_color='blue', font_name='Helvetica-Bold')))
story.append(Spacer(0, 0.2 * inch))
story.append(Paragraph("""
You will analyze our e-commerce platform's customer behavior data. This analysis aims to identify key purchasing patterns and customer segments driving business growth. The project involves working with real transaction data from the past 12 months.
""", get_paragraph_style(font_size=15, text_color='black', font_name='Helvetica')))
story.append(Spacer(0, 0.2*inch))

story.append(Paragraph('Technical Requirements', get_paragraph_style(font_size=18, text_color='blue', font_name='Helvetica-Bold')))
story.append(Spacer(0, 0.2 * inch))
story.append(Paragraph("""
The analysis requires proficiency in Python, particularly with pandas and scikit-learn libraries. You will need to perform data cleaning, exploratory data analysis, and create meaningful visualizations of key insights. The project emphasizes efficient handling of large datasets while maintaining data integrity throughout the analysis process.
""", get_paragraph_style(font_size=15, text_color='black', font_name='Helvetica')))
story.append(Spacer(0, 0.2*inch))

story.append(Paragraph('Expected Deliverables', get_paragraph_style(font_size=18, text_color='blue', font_name='Helvetica-Bold')))
story.append(Spacer(0, 0.2 * inch))
story.append(Paragraph("""
Prepare a comprehensive analysis report covering customer segmentation, purchase frequency patterns, and revenue trends. Your submission must include both technical documentation of the analysis process and business-oriented presentations of your findings. Ensure all code is properly documented and version controlled.
""", get_paragraph_style(font_size=15, text_color='black', font_name='Helvetica')))
story.append(Spacer(0, 0.2*inch))

line = Drawing(500, 1)
line_shape = Line(0, 0, 450, 0)
line_shape.strokeColor = Color(0, 0, 0)
line.add(line_shape)
story.append(line)
story.append(Spacer(0, 0.5 * inch))

story.append(Paragraph('Timeline', get_paragraph_style(font_size=18, text_color='blue', font_name='Helvetica-Bold')))
story.append(Spacer(0, 0.2 * inch))
story.append(Paragraph("""
The project spans two weeks. Dedicate the first week to data cleaning and exploratory analysis. Focus the second week on in-depth analysis and preparation of final deliverables. Regular check-ins will be scheduled to monitor progress and provide guidance as needed.
""", get_paragraph_style(font_size=15, text_color='black', font_name='Helvetica')))
story.append(Spacer(0, 0.2*inch))

story.append(Paragraph('Available Resources', get_paragraph_style(font_size=18, text_color='blue', font_name='Helvetica-Bold')))
story.append(Spacer(0, 0.2*inch))
story.append(Paragraph("""
You will have access to our internal data warehouse, documentation of previous analyses, and technical mentorship from the data science team. Support will be provided through weekly team meetings and code review sessions.
""", get_paragraph_style(font_size=15, text_color='black', font_name='Helvetica')))

doc.build(story)