from inquirer import List, prompt
from src.map_compile import run as map_compile
from src.map_size_calc import run as map_size_calc
from src.map_landmarks_template_generator import run as map_landmarks_template_generator
from src.map_upload import run as map_upload
from src.map_new import run as map_new

commands = {
    "Compile Map": map_compile,
    "Calculate Map Size": map_size_calc,
    "Generate Map Landmarks Template": map_landmarks_template_generator,
    "Upload Map To Server": map_upload,
    "Create new Map": map_new,
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
