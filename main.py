from inquirer import List, prompt
from src.scenario_compile import run as scenario_compile
from src.scenario_size_calc import run as scenario_size_calc
from src.scenario_landmarks_template_generator import (
    run as scenario_landmarks_template_generator,
)
from src.scenario_upload import run as scenario_upload
from src.scenario_new import run as scenario_new
from src.scenario_generate_preview import run as scenario_generate_preview
from src.scenario_upload_preview import run as scenario_upload_preview

commands = {
    "Compile Scenario": scenario_compile,
    "Calculate Scenario Size": scenario_size_calc,
    "Generate Scenario Landmarks Template": scenario_landmarks_template_generator,
    "Upload Scenario To Server": scenario_upload,
    "Create New Scenario": scenario_new,
    "Generate Scenario Preview": scenario_generate_preview,
    "Upload Scenario Preview": scenario_upload_preview,
}

if __name__ == "__main__":

    values = prompt(
        [
            List(
                "command",
                "command",
                choices=[cmd for cmd in commands.keys()],
            ),
        ]
    )

    commands[values["command"]]()
