import os
import json
import yaml
from datetime import datetime
from stage0_py_utils import Evaluator, Loader

import logging
logger = logging.getLogger(__name__)

class Runbook:
    """
    Processor class for evaluating a Echo LLM Configuration (Models and Prompts)
    """
    def __init__(self, config_folder="./config", input_folder="./input", output_folder="./output"):
        self.config_folder = config_folder
        self.input_folder = input_folder
        self.output_folder = output_folder
        
        # Load configurations.yaml
        with open(os.path.join(config_folder, "configuration.yaml"), "r", encoding="utf-8") as file:
            self.configs = yaml.safe_load(file) or []
            
    def run(self):
        """Process Evaluation Configuration"""
        output = {}
        for config in self.configs:
            try:
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
            except Exception as e:
                output[config["name"]]["grades"] = f"An Exception Occurred {e}"
                break
            
        # Write output
        timestamp = datetime.now().strftime("%Y.%m.%dT%H:%M:%S")  
        filename = f"{timestamp}-evaluation.json"
        file_path = os.path.join(self.output_folder, filename)
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(output, file, indent=4) 
        logger.info(f"Evaluation saved to {file_path} ")
        pass
    
def main():
    input_folder = os.getenv("INPUT_FOLDER", "/input")
    output_folder = os.getenv("OUTPUT_FOLDER", "/output")
    config_folder = os.getenv("CONFIG_FOLDER", "/config")
    logging_level = os.getenv("LOG_LEVEL", logging.INFO)

    # Suppress excessive DEBUG logs from `httpcore`
    logging.basicConfig(level=logging_level)
    logging.getLogger("httpcore").setLevel(logging_level)  
    logging.getLogger("httpx").setLevel(logging.WARNING)  # suppress `httpx` logs
    logging.getLogger("stage0_py_utils.evaluator").setLevel(logging_level)

    logger.info(f"============================ Evaluation Pipeline Starting ==============================")
    logger.info(f"Initialized, Input: {input_folder}, Output: {output_folder}, Config: {config_folder} Logging Level {logging_level}")
    
    try:
        runner = Runbook(config_folder=config_folder, input_folder=input_folder, output_folder=output_folder)
        runner.run()
    except Exception as e:
        logger.error(f"Error Reported {str(e)}", exc_info=True)
    logger.info(f"===================== Evaluation Pipeline Completed Successfully =======================")

if __name__ == "__main__":
    main()