from pathlib import Path
import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

from src.exception import CustomException
from src.logger import get_logger

from src.components.data_transformation import DataTransformation


logger = get_logger(__name__)

@dataclass
class DataIngestionConfig:
    # Absolute path to the current file (e.g., src/components/data_ingestion.py)
    CURRENT_FILE: Path = Path(__file__).resolve()

    # Root directory: go up two levels to reach mlproject/
    ROOT_DIR: Path = CURRENT_FILE.parent.parent.parent

    # Define paths relative to ROOT_DIR
    train_data_path: Path = ROOT_DIR / "artifacts" / "train.csv"
    test_data_path: Path = ROOT_DIR / "artifacts" / "test.csv"
    raw_data_path: Path = ROOT_DIR / "artifacts" / "raw.csv"
    source_data_path: Path = ROOT_DIR / "notebook" / "data" / "stud.csv"


class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()
        
    def initiate_data_ingestion(self):
        logger.info("Data Ingestion started")
        try:
            df = pd.read_csv(self.ingestion_config.source_data_path)

            if df.empty:
                raise CustomException("The dataset is empty. Please check the data source.")
            
            logger.info("Dataset read as pandas dataframe")
            
            # Create the artifacts directory if it doesn't exist
            self.ingestion_config.train_data_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Save raw data
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)
            logger.info("Raw data saved to artifacts folder")
            
            # Split data
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)
            logger.info("Train and test sets created")
            
            # Save splits
            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)
            
            logger.info("Train and test sets saved to artifacts folder")
            return self.ingestion_config
        
        except Exception as e:
            raise CustomException(e)


if __name__ == "__main__":
    try:
        data_ingestion = DataIngestion()
        config = data_ingestion.initiate_data_ingestion()  # returns ONE object

        data_transformation = DataTransformation()
        data_transformation.initiate_data_transformation(
            train_path=config.train_data_path, 
            test_path=config.test_data_path
        )
        logger.info("Data ingestion and transformation completed successfully")
        
    except Exception as e:
        logger.error(f"Error during data ingestion: {e}")
        sys.exit(1)
