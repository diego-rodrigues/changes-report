

def read_file(template_path: str) -> str:
    with open(template_path, "r") as template_file:
        template_text = template_file.read()
        return template_text


def write_to_file(content: str, file_name: str):
    with open(file_name, "w") as f:
        f.write(content)


def modify_template(template_content: str, 
                    # creation_date: str,
                    # branch_tag: str,
                    list_added_objects: list[str],
                    # list_removed_objects: list[str],
                    # list_changed_objects: list[str],
                    # extra_in_commands: str,
                    list_added_contents: list[str]
                    ) -> str:
    template_content = template_content.replace("<list_added_objects>", "-- "+"\n\n".join(list_added_objects))
    template_content = template_content.replace("<tables_commands>", "\n\n".join(list_added_contents))
    return template_content

