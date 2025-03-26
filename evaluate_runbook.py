from datetime import datetime
import os
import json
import yaml

import logging
logger = logging.getLogger(__name__)

# Utils import
from stage0_py_utils import Evaluator, Loader, Config
config = Config()

class Runbook:
    """
    Processor class for evaluating a Echo LLM Configuration (Models and Prompts)
    """
    def __init__(self):
        self.config_folder = config.CONFIG_FOLDER
        self.input_folder = config.INPUT_FOLDER
        self.output_folder = config.OUTPUT_FOLDER
        
        # Load configurations.yaml
        with open(os.path.join(self.config_folder, "configuration.yaml"), "r", encoding="utf-8") as file:
            self.configs = yaml.safe_load(file) or []
            
    def run(self):
        """Process Evaluation Configuration"""
        start = datetime.now()
        logger.info(f"Starting {len(self.configs)} configurations at {str(start)}")
        output = {}
        for config in self.configs:
            # Load Input data
            loader = Loader(input_folder=self.input_folder)
            grade_prompt = loader.load_messages(files=config["grade_by"])
            prompt = loader.load_formatted_messages(files=config["prompts"]) 
            conversations=loader.load_formatted_conversations(files=config["conversations"])

            # Setup Output base
            output[config["name"]] = config
            output[config["name"]]["grades"] = "Preparing to Test"
            
            # Setup Evaluator
            evaluator = Evaluator(
                name=config["name"], 
                model=config["model"], 
                grade_model=config["grade_model"],
                grade_prompt_files=config["grade_by"],
                prompt_files=config["prompts"],
                grade_prompt=grade_prompt, 
                prompt=prompt,
                conversations=conversations
            )

            # Evaluate the configured conversations
            output[config["name"]]["grades"] = evaluator.evaluate()
            
        # Write output
        timestamp = datetime.now().strftime("%Y.%m.%dT%H:%M:%S")  
        filename = f"{timestamp}-evaluation.json"
        file_path = os.path.join(self.output_folder, filename)
        os.makedirs(self.output_folder, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(output, file, indent=4) 
            
        end = datetime.now()
        logger.info(f"Evaluation saved to {file_path} in {end-start}")
        pass
    
def main():
    start = datetime.now()
    logger.info(f"============================ Evaluation Pipeline Starting ==============================")
    
    try:
        runner = Runbook()
        runner.run()
    except Exception as e:
        logger.error(f"Error Reported {str(e)}")

    logger.info(f"============================ Evaluation Pipeline Completed =====================")

if __name__ == "__main__":
    main()