# stage0_runbook_evaluate

# Evaluation Runbook
This runbook reads a [configuration.yaml](./test_data/configuration/configuration.yaml) file, loads the referenced data files from the [input](./test_data/input/) folder, and then evaluates a model's responses to each assistant reply in the specified test conversations. Grades are assigned by a separate grading prompt that specializes in comparing given and expected values. Grades are written to the [output](./test_data/output/) folder as yyyy.mm.ddThh:mm:ss-output.json

## Expected Directory Structure
When you run the utility you will specify folders to mount for ``/config``, ``/input`` and ``/output``
```text
/📁 config
├── 📝 configuration.yaml               # Evaluation Pipeline Configuration
/📁 input
│── 📁 conversations                    # Conversations that are used to test the model
│   ├── 💬 test_conversation1.csv       
│   ├── 💬 test_conversation2.csv       
│── 📁 grader                           # Simple LLM message list with grading prompts
│   ├── ✏️ grader1.csv       
│   ├── ✏️ grader2.csv       
│── 📁 prompts                          # Formatted Echo messages with your bot prompts
│   ├── 🧑‍🏫 your_base.csv                    # A base prompt that establishes a name (Fran, Json, Ivan, etc.)
│   ├── 🧑‍🏫 echo.csv                         # Group chat and echo formatted message comprehension
│   ├── 🧑‍🏫 tool.csv                         # How to use agent/action commands
│   ├── 🧑‍🏫 you.csv                          # Your custom prompt, specific agent/actions or processes
/📁 output
│   ├── 📀 yyyy-mm-ddThh:mm:ss-output.json  # Grades from running the evaluation
```

## Using this in your project. 
Adjust the command below to use appropriate values for your Echo Bot project, and add it to your pipenv scripts. See the [test_data] folder for sample files. Grades will be written to a file called ``{datetime}-output.json`` in the output folder when you run the tool. 

```bash
docker run --rm /
    -v ./bot_name:/input
    -v ./bot_name/config:/config
    -v ./bot_name/output:/output
    ghcr.io/agile-learning-institute/stage0-echo-evaluate:latest
```

# Contributing

## Prerequisites

Ensure the following tools are installed:
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Python](https://www.python.org/downloads/)
- [Pipenv](https://pipenv.pypa.io/en/latest/installation.html)

## Testing
All testing uses config/input/output folders in ./test_data.

## Install Dependencies
```bash
pipenv install
```

### Run Evaluate Runbook locally.
```bash
pipenv run evaluate
```

### Debug Evaluate Runbook locally
```bash
pipenv run debug
```
Runs locally with logging level set to DEBUG

### Build the Evaluate Runbook container
```bash
pipenv run build
```

### Build, and run the Evaluate Runbook container
```bash
pipenv run container
```

