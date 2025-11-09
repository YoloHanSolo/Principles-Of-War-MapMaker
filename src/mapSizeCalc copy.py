from inquirer import Text, prompt

if __name__ == "__main__":
    values = prompt([
        Text(
            "size_x",
            "size_x",
        ),
        Text(
            "size_y",
            "size_y",
        ),
        Text(
            "scale",
            "scale",
        )
    ])

    size_x = int(values["size_x"])
    size_y = int(values["size_y"])
    scale = float(values["scale"])

    x = (size_x - 60) / 120
    y = (size_y - 33) / 107

    print(f"INFO: x={x}; y={y}")

    tiles_x = int(x * scale)
    tiles_y = int(y * scale)

    print(f"INFO: tiles_x={tiles_x}; tiles_y={tiles_y}")

    pixels_x = tiles_x * 120 + 60
    pixels_y = tiles_y * 107 + 33

    print(f"INFO: pixels_x={pixels_x}; pixels_y={pixels_y}")

