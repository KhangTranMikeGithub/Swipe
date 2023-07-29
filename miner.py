import fitz
from tkinter import PhotoImage
class PDFMiner:
    def __init__(self, filepath):
        self.filepath = filepath
        self.pdf = fitz.open(self.filepath)
        self.first_page = self.pdf.load_page(0)
        self.width, self.height = self.first_page.rect.width, self.first_page.rect.height
        res = self.getZoom(self.width)
        self.zoom = res
    def getDimensions(self):
        return [self.width, self.height]
    def getZoom(self, width):
        return float(500 / width)
    def get_metadata(self):
        metadata = self.pdf.metadata
        numPages = self.pdf.page_count
        return metadata, numPages
    def get_page(self, page_num, z):
        page = self.pdf.load_page(page_num)
        if self.zoom and z == True:
            mat = fitz.Matrix(self.zoom, self.zoom)
            pix = page.get_pixmap(matrix=mat)
        else:
            pix = page.get_pixmap()
        px1 = fitz.Pixmap(pix, 0) if pix.alpha else pix
        imgdata = px1.tobytes("ppm")
        return PhotoImage(data=imgdata)