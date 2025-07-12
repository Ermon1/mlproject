import sys

def error_message_details(error: Exception) -> str:
    _, _, exc_tb = sys.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename if exc_tb else "Unknown"
    line_no = exc_tb.tb_lineno if exc_tb else "Unknown"

    return "Error occurred in python script name [{}] at line number: [{}], error message: [{}]".format(
        file_name, line_no, str(error)
    )
    
class CustomException(Exception):
    def __init__(self, error: Exception):
        message = error_message_details(error)
        super().__init__(message)
        self.error_message = message

    def __str__(self):
        return self.error_message

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.error_message)})"
