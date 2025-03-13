# Stage0 Evaluation Pipeline

# Evaluation Runbook
This runbook reads a [configuration.yaml](./test/configuration/configuration.yaml) file, and loads the referenced evaluation data files, and then evaluates the model's responses to each assistant reply in a set of test conversations. Grades are assigned by a separate grading prompt that specializes in comparing given and expected values. 

## Using this in your project. 
Adjust this command to use appropriate values for your Echo Bot project. Your input folder should contain ``conversations``, ``grader``, and ``prompts`` folders with the csv files with your grader, prompts, and testing conversations. Your config folder should contain a ``configurations.yaml`` file. There is a [sample file](./test/configuration/configuration.yaml) in the ``test/configuration`` folder. A single output file called ``grades.json`` will be written to the output folder. There is a [sample](./test/output/expected_grades.json) grades file in the ``test/output`` folder. Any existing ``grades.json`` file will be over-written.
```bash
docker run --rm /
    -v ./bot_name:/opt/input
    -v ./bot_name/config:/opt/config
    -v ./bot_name/output:/opt/output
    ghcr.io/agile-learning-institute/stage0-echo-evaluate:latest
```

# Contributing

## Prerequisites

Ensure the following tools are installed:
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Python](https://www.python.org/downloads/)
- [Pipenv](https://pipenv.pypa.io/en/latest/installation.html)

## Testing

## Install Dependencies
```bash
pipenv install
```

### Clear out the ./test/output folder
```bash
pipenv run clean
```

### Run Evaluate Runbook locally.
```bash
pipenv run evaluate
```
Note: This does clean then runs the code locally

### Debug Evaluate Runbook locally
```bash
pipenv run debug_evaluate
```
Runs locally with logging level set to DEBUG

### Build the Evaluate Runbook container
```bash
pipenv run build_evaluate
```

### Build, and run the Evaluate Runbook container
```bash
pipenv run evaluate_container
```
Note: Will use ./test folders

