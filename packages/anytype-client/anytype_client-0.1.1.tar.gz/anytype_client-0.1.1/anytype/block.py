class Block:
    def __init__(self, **kwargs):
        self.type = ""

    def __repr__(self):
        return f"<Block(type={self.type})>"
