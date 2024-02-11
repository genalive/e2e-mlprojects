# tracking errors and exception into txt
import logging
import os
from datetime import datetime


# f string for filename with timestamp
LOG_FILE=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
# Create pathname
logs_path=os.path.join(os.getcwd(),"logs",LOG_FILE)
# Make directory if doesn't exist
os.makedirs(logs_path,exist_ok=True)

# Create the filepath for the file
LOG_FILE_PATH=os.path.join(logs_path,LOG_FILE)


# Generate the log file
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO, # This is the level
)

# quick_test
if __name__=="__main__":
#    logging.info("Logging has started")
    try: 
        a=1/0
    except Exception as e:
        logging.info("Dividing by zero.")
        raise CustomException(e,sys)