import sys

# Uses logging function from logger.py
from src.logger import logging

# whenever exception gets raised, push a custom message
def error_message_detail(error, error_detail:sys): #error detail comes from sys
    _,_,exc_tb=error_detail.exc_info() 
    # shows error and which line it occurred

    #exc_tb feeds into the next section
    file_name=exc_tb.tb_frame.f_code.co_filename

    # Filename, line number, error
    error_message="Error occurred in python script name [{0}] line numbers [{1}] error message [{2}]".format(
        file_name, exc_tb.tb_lineno, str(error))

    return error_message


#Custom Exception Class
class CustomException(Exception):

    def __init__(self, error_message, error_detail:sys):
        # we are inheriting from the exception above
        # Overwrite init function
        super().__init__(error_message)
        # getting populated from the function
        self.error_message=error_message_detail(error_message, error_detail=error_detail)

    # Every time we print it, we'll get string of the error message
    def __str__(self):
        return self.error_message
    
# For try catching
    
# quick_test
#if __name__=="__main__":
#    try: 
#        a=1/0
#    except Exception as e:
#        logging.info("Dividing by zero.")
#        raise CustomException(e,sys)