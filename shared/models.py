class ImageData:
    def __init__(self, image_id, imageName, file_size_bytes, width, height, file_format, path, text):
        self.image_id = image_id
        self.imageName = imageName
        self.file_size_bytes = file_size_bytes
        self.width = width
        self.height = height
        self.file_format = file_format
        self.path = path
        self.text = text
        


class CleanedData(ImageData):
    def __init__(self,image_id, imageName, file_size_bytes, width, height, file_format, path, text, cleaned_text):
        super().__init__(image_id, imageName, file_size_bytes, width, height, file_format, path, text)
        self.cleaned_text = cleaned_text = None