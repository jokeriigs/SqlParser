class SqlStruct:
    oid = -1
    group = ""
    part = ""
    keyword = ""
    line = -1
    depth = -1
    no = -1
    pos = -1
    filename = ""
    isComment = False

    def __init__(self, oid, group, part, keyword, line, depth, no, pos, isComment, filename):
        self.oid = oid
        self.group = group
        self.part = part
        self.keyword = keyword
        self.line = line
        self.depth = depth
        self.no = no
        self.pos = pos
        self.isComment = isComment
        self.filename = filename