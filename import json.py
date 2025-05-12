import json

def save_tutorials_to_file(self, filename: str = "tutorials.json") -> None:
    """
    Save tutorials to a JSON file.
    """
    with open(filename, "w") as file:
        json.dump(self.tutorials, file)
    print("Tutorials saved to file.")