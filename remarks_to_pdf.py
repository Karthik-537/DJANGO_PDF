from convert_remarks_to_pdf import ConvertRemarksToPDFInteractor
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.pagesizes import letter

doc = SimpleDocTemplate("remarks_to_pdf.pdf", pagesize=letter, leftMargin=48, \
                            rightMargin=48, topMargin=50, bottomMargin=50)

convert_remarks_to_pdf = ConvertRemarksToPDFInteractor()

story = convert_remarks_to_pdf.convert_remarks_to_pdf()

doc.build(story)
