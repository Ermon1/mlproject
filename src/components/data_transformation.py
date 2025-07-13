import sys
from dataclasses import dataclass
import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

from src.exception import CustomException
from src.logger import get_logger
from pathlib import Path
from src.utility import save_object


logger = get_logger(__name__)

@dataclass
class DataTransformationConfig:
    """Configuration for data transformation."""
    
    CURRENT_FILE: Path = Path(__file__).resolve()
    ROOT_DIR: Path = CURRENT_FILE.parent.parent.parent
    preprocessor_obj_file_path: Path = ROOT_DIR / "artifacts" / "preprocessor.pkl"

class DataTransformation:
    def __init__(self):
        """Initializes the DataTransformation class with configuration."""
        self.transformation_config = DataTransformationConfig()
        
    def get_data_transformer_object(self):
        """Creates a data transformation pipeline with preprocessing steps."""
        try:
            numerical_features = ['reading_score', 'writing_score']
            categorical_features = ['gender', 
                                    'race_ethnicity', 
                                    'parental_level_of_education', 
                                    'lunch', 
                                    'test_preparation_course']
            
            # logger.info("Numerical features: %s", numerical_features)
            # logger.info("Categorical features: %s", categorical_features)
            num_pipeline = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='median')),
                ('scaler', StandardScaler())        
            ])
            
            # Categorical pipeline
            # logger.info("Creating categorical pipeline with OneHotEncoder")
            cat_pipeline = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='most_frequent')),
                ('onehot', OneHotEncoder(handle_unknown='ignore')),
                ('scaler', StandardScaler(with_mean=False))  # Use with_mean=False for sparse output
            ])
            
            logger.info("Creating preprocessor with ColumnTransformer")
            # Combine numerical and categorical pipelines
            logger.info("Combining numerical and categorical pipelines into ColumnTransformer")
            
            
            
            preprocessor = ColumnTransformer(
                transformers=[
                    ('num', num_pipeline, numerical_features),
                    ('cat', cat_pipeline, categorical_features)
                    
                ]
            )
            return preprocessor
        
        except Exception as e:
            raise CustomException(e)

    def initiate_data_transformation(self, train_path: Path, test_path: Path):
        """Initiates the data transformation process."""
        try:
            logger.info("Data Transformation started")
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            logger.info("Train and test datasets read successfully")

            preprocessor_obj = self.get_data_transformer_object()
            logger.info("Preprocessor object created") 
            
            target_column_name = 'math_score'
            numerical_features = ['reading_score', 'writing_score']
            
            input_features_train = train_df.drop(columns=[target_column_name], axis=1)
            input_features_test = test_df.drop(columns=[target_column_name], axis=1)
            
            target_feature_train = train_df[target_column_name]
            target_feature_test = test_df[target_column_name]  
             
            logger.info("Input features and target feature separated")

            input_features_train_arr = preprocessor_obj.fit_transform(input_features_train)
            input_features_test_arr = preprocessor_obj.transform(input_features_test)
            
            train_arr = np.c_[input_features_train_arr, np.array(target_feature_train)]
            test_arr = np.c_[input_features_test_arr, np.array(target_feature_test)]
            logger.info("Data transformation completed successfully")
            save_object(
                        file_path=self.transformation_config.preprocessor_obj_file_path,
                        obj=preprocessor_obj
                )  # Save the preprocessor object   

            # Save the preprocessor object
            return train_arr, test_arr


        except FileNotFoundError as e:
            raise CustomException(f"File not found: {e.filename}")
        except pd.errors.EmptyDataError:
            raise CustomException("The dataset is empty. Please check the data source.")
        except Exception as e:
            raise CustomException(f"An error occurred while reading the dataset: {str(e)}")
        
