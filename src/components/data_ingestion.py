import os
import sys
from src.exception import CustomException # Calling from src folder
from src.logger import logging # Importing logging from src.logger
import pandas as pd

# Scikit-Learn's train_test_split module
from sklearn.model_selection import train_test_split


from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig

#from src.components.model_trainer import ModelTrainerConfig
#from src.components.model_trainer import ModelTrainer


# dataclasses from Python
from dataclasses import dataclass

# DataIngestConfig Class defining inputs eg. where I'm saving the data.
# That's the classes. You'll see with the artifacts.
# @dataclass decorator. inside a class you use init. 
# but if you use @dataclass you can directly define your class variable.
# alternative: create a folder 'config' in components folder.
# and then define the class over there. 
# but DataIngestion can refer to DataIngestionConfig here. 

@dataclass
class DataIngestionConfig:
    train_data_path: str=os.path.join('artifacts',"train.csv")
    test_data_path: str=os.path.join('artifacts',"test.csv")
    raw_data_path: str=os.path.join('artifacts',"data.csv")

# If we want to go beyond defining variables, but have functions:
# We'll have to use class, not dataclass.

class DataIngestion:
    def __init__(self):
        self.ingestion_config=DataIngestionConfig() # Will have the 3 values above.

    # Creating own function. 
    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion method or component")
        try:
            # Reading locally, but could be database.
            # eg. mongodb_client / sql_client in utils.py
            df=pd.read_csv('notebook/data/stud.csv')

            # Keep writing logs
            logging.info('Read the dataset as dataframe')

            # Inside ingestion_config dataclass, make dirs
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)

            # Export / Save to raw data path as 'data.csv'
            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)

            # Train Test Split
            logging.info("Train test split initiated")
            train_set,test_set=train_test_split(df,test_size=0.2,random_state=42)

            # Export 'train.csv'
            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
            # Export 'test.csv'
            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)

            logging.info("Ingestion of the data is completed")

            # Return 3 important things: It's important for data transformation.
            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path

            )
        except Exception as e:
            raise CustomException(e,sys)
        
if __name__=="__main__":
    obj=DataIngestion()
    # returning train and test data
    train_data,test_data=obj.initiate_data_ingestion()

    # let's do the data transformation
    data_transformation=DataTransformation()
    train_arr,test_arr,_ = data_transformation.initiate_data_transformation(train_data,test_data)

    #modeltrainer=ModelTrainer()
    #print(modeltrainer.initiate_model_trainer(train_arr,test_arr))