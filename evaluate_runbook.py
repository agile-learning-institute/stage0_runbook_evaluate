from datetime import datetime
import os
import json
import yaml
import logging

CONFIG_FOLDER = os.getenv("CONFIG_FOLDER", "./config") 
INPUT_FOLDER = os.getenv("INPUT_FOLDER", "./input")
OUTPUT_FOLDER = os.getenv("OUTPUT_FOLDER", "./output")
LOGGING_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOGGING_LEVEL = getattr(logging, LOGGING_LEVEL, logging.INFO)

# Reset logging handlers
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

# Configure logging
logging.basicConfig(
    level=LOGGING_LEVEL,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger(__name__)

# Suppress noisy http loggers
logging.getLogger("httpcore").setLevel(logging.WARNING)  
logging.getLogger("httpx").setLevel(logging.WARNING)  

# Utils import
from stage0_py_utils import Evaluator, Loader

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
        os.makedirs(self.output_folder, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(output, file, indent=4) 
        logger.info(f"Evaluation saved to {file_path} ")
        pass
    
def main():
    start = datetime.now()
    logger.info(f"============================ Evaluation Pipeline Starting ==============================")
    logger.info(f"Initialized, Input: {INPUT_FOLDER}, Output: {OUTPUT_FOLDER}, Config: {CONFIG_FOLDER} Logging Level {LOGGING_LEVEL}")
    
    try:
        runner = Runbook(input_folder=INPUT_FOLDER, output_folder=OUTPUT_FOLDER, config_folder=CONFIG_FOLDER)
        runner.run()
    except Exception as e:
        logger.error(f"Error Reported {str(e)}", exc_info=True)
    end = datetime.now()
    logger.info(f"================ Evaluated {len(runner.configs)} configurations in {end-start} =====================")

if __name__ == "__main__":
    main()