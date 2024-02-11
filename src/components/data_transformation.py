import sys
from dataclasses import dataclass

import numpy as np 
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler

from src.exception import CustomException
from src.logger import logging
import os

from src.utils import save_object

# Any inputs/outputs - saving into Pickle file
@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path=os.path.join('artifacts',"proprocessor.pkl")


class DataTransformation:
    # Starting with init
    def __init__(self):
        #class(self) is initialised to above
        self.data_transformation_config=DataTransformationConfig()

    # function here 'get_data_transformer_object', using 'self':
    def get_data_transformer_object(self):
        '''
        This function is responsible for data transformation based on different types of data
        
        '''
        try:
            
            # defining the numerical columns
            numerical_columns = ["writing_score", "reading_score"]
            
            # defining the categorical columns (will need OHE)
            categorical_columns = [
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course",
            ]

            # Note use the EDA on the Jupyter Notebooks to help design these pipelines.

            # Creating pipeline (with missing value handling)
            num_pipeline= Pipeline(
                steps=[
                ("imputer",SimpleImputer(strategy="median")),
                ("scaler",StandardScaler())

                ]
            )

            # Creating pipeline (with missing value handling)
            cat_pipeline=Pipeline(

                steps=[
                ("imputer",SimpleImputer(strategy="most_frequent")),
                ("one_hot_encoder",OneHotEncoder()),
                ("scaler",StandardScaler(with_mean=False))
                ]

            )

            logging.info(f"Categorical columns: {categorical_columns}")
            logging.info(f"Numerical columns: {numerical_columns}")

            # 'preprocessor' = Combining the two Pipelines above: name - pipelines - appropriate columns
            
            preprocessor=ColumnTransformer(
                [
                ("num_pipeline",num_pipeline,numerical_columns),
                ("cat_pipelines",cat_pipeline,categorical_columns)

                ]


            )

            # return as preprocessor
            return preprocessor
        
        except Exception as e:
            raise CustomException(e,sys)


    # starting data transformation: 
    def initiate_data_transformation(self,train_path,test_path):

        try:
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)

            logging.info("Read train and test data completed")

            logging.info("Obtaining preprocessing object")

            # Use the above function of the above class(self.)
            # Return to 'preprocessing_obj'
            # NB. this will eventually be converted to a pickle file.
            preprocessing_obj=self.get_data_transformer_object()

            # this is the column we are trying to predict
            target_column_name="math_score"

            # same as the numerical columns in the previous function
            numerical_columns = ["writing_score", "reading_score"]

            # dropping target column 'math score' to input - train
            # keeping target column to target - train
            input_feature_train_df=train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df=train_df[target_column_name]

            # dropping target column 'math score' to input - test
            # keeping target column to target - test
            input_feature_test_df=test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df=test_df[target_column_name]

            # logging output
            logging.info(
                f"Applying preprocessing object on training dataframe and testing dataframe."
            )

            # Applying the logic of preprocessing_obj to SKlearn's fit_transform
            # eg. scaler = StandardScaler()
            # X_train_scaled = scaler.fit_transform(X_train)
            # X_test_scaled = scaler.transform(X_test)
            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df) #fit_transform(input_df)
            input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df) #transform(test-df)

            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            logging.info(f"Saved preprocessing object.")

            # saving as pickle file, remember:
            # class DataTransformationConfig:
                # preprocessor_obj_file_path=os.path.join('artifacts',"proprocessor.pkl")
            save_object(

                # getting file_path
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                # this is the object we want to save
                obj=preprocessing_obj

                # we're going to use utils.py to have the save_object function

            )

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )
        except Exception as e:
            raise CustomException(e,sys)
