from io_handler.load_images import ImageLoader
from io_handler.load_labels import Labelloader
from io_handler.save_labels import LabelSaver, BoundingBox, Segmentation, obbox
from collections import UserList

class BoundingBoxList(UserList):
    def append(self, item):
        if not isinstance(item, BoundingBox):
            raise TypeError("Solo se permiten objetos BoundingBox")
        super().append(item)

class SegmentationList(UserList):
    def append(self, item):
        if not isinstance(item, Segmentation):
            raise TypeError("Solo se permiten objetos Segmentation")
        super().append(item)

class ObboxList(UserList):
    def append(self, item):
        if not isinstance(item, obbox):
            raise TypeError("Solo se permiten objetos obbox")
        super().append(item)


class data_io_handler:
    def __init__(self, save_directory: str = None, file_format: str = 'txt', encoding: str = 'utf-8', format_label: str = 'yolo'):
        self.image_loader = ImageLoader()
        self.label_loader = Labelloader()
        self.label_saver = LabelSaver(save_directory,file_format,encoding,format_label)  # Se inicializa cuando se configura el guardado
        self.bbox_labels = BoundingBoxList()
        self.segmentation_labels = SegmentationList()
        self.obbox_labels = ObboxList()

        