import labels
from reportlab.graphics import shapes

# Create an A4 portrait (210mm x 297mm) sheets with 2 columns and 8 rows of
# labels. Each label is 90mm x 25mm with a 2mm rounded corner. The margins are
# automatically calculated.
specs = labels.Specification(210, 297, 2, 8, 90, 25, corner_radius=2)


def draw_label(label, width, height, obj):
    # Just convert the object to a string and print this at the bottom left of
    # the label.
    label.add(shapes.String(2, 2, str(obj), fontName="Helvetica", fontSize=12))


# Create the sheet.
sheet = labels.Sheet(specs, draw_label)

# Add a couple of labels.
sheet.add_label("Hello"+"\n"+"Workd")
sheet.add_label("World")

# We can also add each item from an iterable.
sheet.add_labels(range(3, 22))

# Note that any oversize label is automatically trimmed to prevent messing up
# other labels.
sheet.add_label("Oversized label here")

# Save the file and we are done.
sheet.save('basic.pdf')
