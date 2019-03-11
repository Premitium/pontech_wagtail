def grouped(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]

def chunks(l, n):
    n = max(1, n)
    return (l[i:i+n] for i in range(0, len(l), n))

ICON_CHOICES = (
    ('icon-science-1','Science one'),
    ('icon-science', 'Sciences'),
    ('icon-mathematics','Math'),
    ('icon-computer','Computer'),
    ('icon-left3', 'Left3'),
    ('icon-left', 'Left'),
    ('icon-left-arrow-angle', 'Left Arrow Angle'),
    ('icon-left-arrow-angle2', 'Left Arrow Angle 2'),
    ('icon-note', 'Note'),
    ('icon-note2', 'Note 2'),
    ('icon-arrows .path2', 'Arrows'),
    ('icon-arrows-1', 'Arrows-1'),
    ('icon-arrows-2', 'Arrows-2'),
    ('icon-book', 'Book'),
    ('icon-box', 'Box'),
    ('icon-business', 'Business'),
    ('icon-circle', 'Circle'),
    ('icon-clock', 'Clock'),
    ('icon-close', 'Close'),
    ('icon-cup', 'Cup'),
    ('icon-graphic', 'Graphic'),
    ('icon-graphic-1', 'Graphic 1'),
    ('icon-layers', 'Layers'),
    ('icon-left2', 'Left 2'),
    ('icon-man', 'Man'),
    ('icon-multimedia', 'Multimedia'),
    ('icon-office', 'Office'),
    ('icon-people', 'People'),
    ('icon-office-1', 'People 1'),
    ('icon-professor', 'Professor'),
    ('icon-signs', 'Signs'),
    ('icon-technology', 'Technology'),
    ('icon-technology-1', 'Technology 1'),
    ('icon-world','Globe'),
    ('icon-world2 .path1','Globe 1'),
    ('icon-world2 .path2','Globe 2'),
    ('icon-world2 .path3','Globe 3'),
    ('icon-world2 .path4','Globe 4'),
    ('icon-world2 .path5','Globe 5'),
    ('icon-world2 .path6','Globe 6'),
    ('icon-world2 .path7','Globe 7'),
    )
