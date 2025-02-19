from reportlab.pdfgen import canvas

c = canvas.Canvas("table_canvas.pdf", pagesize=(4768, 6741))

x_start, y_start = 100, 6741 - 700
header_cell_width, header_cell_height = 300, 40
for row in range(2):
    y = y_start - row * header_cell_height
    c.line(x_start, y, x_start + header_cell_width, y)
for col in range(2):
    x = x_start + col * header_cell_width
    c.line(x, y_start, x, y_start - header_cell_height)
x = x_start + 10
y = y_start - 25
c.drawString(x, y, "OFFICER'S NAME AND SIGNATURE")

y_start = y_start - header_cell_height
body_cell_width, body_cell_height = 300, 200
for row in range(2):
    y = y_start - row * body_cell_height
    c.line(x_start, y, x_start + body_cell_width, y)
for col in range(2):
    x = x_start + col * body_cell_width
    c.line(x, y_start, x, y_start - body_cell_height)
x = x_start + 10
y = y_start - 25
c.drawImage("tick.jpg", x, y-50, width=50, height=50, mask="auto")
y -= 55
text = ("Post verification will be carried out as per the provisions of the GHMC TG-bPASS Act and "
        "action will be initiated if any violation or misrepresentation of the facts is found.")
words = text.split(' ')
current_line = ''
line_height = 15
for word in words:
    test_line = current_line + ' ' + word if current_line else word
    test_width = c.stringWidth(test_line, "Helvetica", 12)
    if test_width > body_cell_width - 10:
        c.drawString(x, y, current_line)
        y -= line_height
        current_line = word
    elif test_width > body_cell_width - 10:
        c.drawString(x, y, current_line)
        y -= line_height
        current_line = word
    else:
        current_line = test_line
if current_line:
    c.drawString(x, y, current_line)
y -= 15
c.drawString(x, y, "Checking Officer")
y -= 15
c.drawString(x, y, "28/09/2002")

y_start = y_start - body_cell_height
header_cell_width, header_cell_height = 300, 40
for row in range(2):
    y = y_start - row * header_cell_height
    c.line(x_start, y, x_start + header_cell_width, y)
for col in range(2):
    x = x_start + col * header_cell_width
    c.line(x, y_start, x, y_start - header_cell_height)
x = x_start + 10
y = y_start - 25
c.drawString(x, y, "LTP'S NAME AND SIGNATURE")

y_start = y_start - header_cell_height
body_cell_width, body_cell_height = 300, 200
for row in range(2):
    y = y_start - row * body_cell_height
    c.line(x_start, y, x_start + body_cell_width, y)
for col in range(2):
    x = x_start + col * body_cell_width
    c.line(x, y_start, x, y_start - body_cell_height)
x = x_start + 10
y = y_start - 25
c.drawImage("tick.jpg", x, y-50, width=50, height=50, mask="auto")
y -= 55
text = ("Post verification will be carried out as per the provisions of the GHMC TG-bPASS Act and "
        "action will be initiated if any violation or misrepresentation of the facts is found.")
words = text.split(' ')
current_line = ''
line_height = 15
for word in words:
    test_line = current_line + ' ' + word if current_line else word
    test_width = c.stringWidth(test_line, "Helvetica", 12)
    if test_width > body_cell_width - 10:
        c.drawString(x, y, current_line)
        y -= line_height
        current_line = word
    elif test_width > body_cell_width - 10:
        c.drawString(x, y, current_line)
        y -= line_height
        current_line = word
    else:
        current_line = test_line
if current_line:
    c.drawString(x, y, current_line)
y -= 15
c.drawString(x, y, "0123456789")

c.save()
