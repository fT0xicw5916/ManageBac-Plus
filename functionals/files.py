ALLOWED_EXTENSIONS = {"mochi", "pdf"}

def allowed_file(filename):
    """
    Double-checks whether the file is allowed to be uploaded.

    :param filename: The full name of the file to check for, including its file extension. NOT the path of the file
    :return: True if the file is allowed to be uploaded, else False
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
