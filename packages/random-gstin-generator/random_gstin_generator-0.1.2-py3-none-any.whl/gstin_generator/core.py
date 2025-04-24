from ._internal import generate_gstin

class GSTINGenerator:
    def __init__(self, num_gstins: int = 1):
        self.num_gstins = num_gstins

    def generate(self):
        return generate_gstin(self.num_gstins)