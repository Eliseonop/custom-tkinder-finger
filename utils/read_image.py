from PIL import ImageTk, Image,ImageMode


def leer_imagen(path, size=None):
    return ImageTk.PhotoImage(Image.open(path).resize(size))


