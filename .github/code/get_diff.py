import sys
sys.path.insert(0, '.github/code/')

import json
import re
import sqlparse
from sqlparse import tokens
import script_writer as sw 

ADDED_FILES = []
DELETED_FILES = []
CHANGED_FILES = []
RENAMED_FILES = []
IGNORED_FILES = []


# get what changed
def get_what_changed_in_branch() -> None:
    with open('diff.json') as f:
        data = json.load(f)

        for file in data['files']:
            match file['type']: 
                case "AddedFile":
                    # print("File: {} | Type: {}".format(file['path'],file['type']))
                    ADDED_FILES.append(file['path'])
                
                case "DeletedFile":
                    # print("File: {} | Type: {}".format(file['path'],file['type']))
                    DELETED_FILES.append(file['path'])

                case "ChangedFile":
                    # print("File: {} | Type: {}".format(file['path'],file['type']))
                    CHANGED_FILES.append(file['path'])

                case "RenamedFile":
                    # print("File: {}->{} | Type: {}".format(file['pathBefore'],file['pathAfter'],file['type']))
                    RENAMED_FILES.append({file['pathBefore'],file['pathAfter']})
                    
                case _:
                    # print("File {} was ignored.".format(file['path]']))
                    IGNORED_FILES.append(file['path'])


def get_sql_object_type(content: str) -> str:
    line = content.strip().split("\n")[0]
    result = re.match("CREATE .*(TABLE|VIEW|PROCEDURE|TASK) .+ ?\(?", line)
    # print(result)
    if result is not None:
        return result.group(1)
    else:
        return "unknown"


def get_sql_object_type_and_name(content: str) -> tuple[str, str]:
    statements = sqlparse.split(content);
    print(sqlparse.format(statements[0], keyword_case='upper'))

    parsed = sqlparse.parse(statements[0])[0]
    # print(parsed.tokens)
    # print(parsed.get_type())            # CREATE
    # print("=====")

    obj_type = ""
    obj_name = ""
    for token in parsed.tokens:
        # sqlparse.sql.Token.is_group
        # print(token)
        # print(type(token))
        # print("[{}] - {} >> {}".format(token.ttype,type(token),str(token)))
        # print(type(token))
        # if token.match(sqlparse.sql.Token,[]):
        #     print("found identifier: {}".format(token))
        
        match type(token):
            case sqlparse.sql.Identifier:
                print("found identifier = {}".format(token))
                obj_name = str(token)
                break

            case sqlparse.sql.Token:
                # print("found token. token type is {}".format(token.ttype))
                # if token.ttype == tokens.Keyword.DDL:
                #     print("found token type is {}".format(token.ttype))

                if token.ttype == tokens.Keyword:
                    match str(token):
                        case "TABLE" | "VIEW" | "PROCEDURE":
                            obj_type = str(token)

    return obj_type, obj_name

def get_file_content(path: str) -> str:
    with open(path) as f:
        return f.read()

def process_sql_file(path: str) -> str:
    file_content = get_file_content(path)
    sql_object_type, object_name = get_sql_object_type_and_name(file_content)

    return sql_object_type,file_content, object_name


get_what_changed_in_branch()
print("\n\nadded:")
print(ADDED_FILES)
for file in ADDED_FILES:
    print(get_file_content(file))
    print('--')


print("\n\nchanged:")
print(CHANGED_FILES)
for file in CHANGED_FILES:
    print(get_file_content(file))
    print('--')


print("\n\ndeleted:")
print(DELETED_FILES)
# for file in DELETED_FILES:
    # retrieve content of file first
    
    
print("\n\nignored:")
print(IGNORED_FILES)

print("\n\nrenamed:")
print(RENAMED_FILES)



contents = {"table":[], "procedure": [], "view": [], "task": [], "unknown": []}
list_of_contents = {"created": [], "deleted": [], "modified": []}

for file in ADDED_FILES:
    if not file.endswith('.sql'):
        continue
    sql_object_type, content, object_name = process_sql_file(file)
    contents[sql_object_type.lower()].append(content)
    list_of_contents["created"].append(object_name)

template_content = sw.read_file('./resources/release-script-template.sql')
template_content = sw.modify_template(
                        template_content, 
                        list_of_contents["created"],
                        contents["table"]
                        )
print(template_content)
sw.write_to_file(template_content, "output-script.sql")

# print("Added content:\n")
# print(contents)


# changed_content = ''
# for file in CHANGED_FILES:
#     changed_content += process_sql_file(file) + '\n'

# print("Changed content:\n" + changed_content)


# for this we need to checkout the deleted path before processing
# deleted_content = ''
# for file in DELETED_FILES:
#     deleted_content += process_sql_file(file) + '\n'

# print("Deleted content:\n" + deleted_content)


# # for this we need to checkout the pathBefore before processing pathAfter
# renamed_content = ''
# for fileBefore, fileAfter in RENAMED_FILES:
#     renamed_content += process_sql_file(fileAfter) + '\n'

# print("Added content:\n" + renamed_content)

