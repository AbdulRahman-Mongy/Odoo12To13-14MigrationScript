import os, re


def file_read_lines(file_name):
    try:
        file = open(file_name, "r")
        string = file.readlines()
        file.close()
        return string
    except Exception:
        raise Exception("Can't read {}".format(file_name))


def file_write_lines(file_name, string):
    try:
        file = open(file_name, "w")
        file.writelines(string)
        file.close()
    except Exception:
        raise Exception("Can't write to {}".format(file_name))


def handel_py_files(file_name):
    lines_to_delete = ["@api.multi", "@api.returns", "@api.one", "@api.cr", "@api.model_cr"]
    string = file_read_lines(file_name)
    computed_string = remove_models_lines(lines_to_delete, string)
    file_write_lines(file_name, computed_string)


def remove_models_lines(lines_to_delete, string):
    for i in range(len(string)):
        try:
            b = string[i].strip()
            if b in lines_to_delete:
                string[i] = ""
            # remove oldname attr
            if re.match(".*oldname=[\'\"].*[\'\"].*", string[i]):
                start = string[i].find("oldname=")
                end = string[i][start:].find(",")
                if end == -1:
                    end = string[i][start:].find(")")
                    temp = string[i][start:start + end]
                    string[i] = string[i].replace(temp, "")

                else:
                    temp = string[i][start:start + end + 1]
                    string[i] = string[i].replace(temp, "")
            # remove old_name attr
            if re.match(".*old_name=[\'\"].*[\'\"].*", string[i]):
                start = string[i].find("old_name=")
                end = string[i][start:].find(",")
                if end == -1:
                    end = string[i][start:].find(")")
                    temp = string[i][start:start + end]
                    string[i] = string[i].replace(temp, "")

                else:
                    temp = string[i][start:start + end + 1]
                    string[i] = string[i].replace(temp, "")

            # remove subtype attr
            if re.match(".*subtype=[\'\"].*[\'\"].*", string[i]):
                start = string[i].find("subtype=")
                end = string[i][start:].find(",")
                if end == -1:
                    end = string[i][start:].find(")")
                    temp = string[i][start:start + end]
                    string[i] = string[i].replace(temp, "")

                else:
                    temp = string[i][start:start + end + 1]
                    string[i] = string[i].replace(temp, "")




        except Exception:
            raise Exception("Can't compute this line {}".format(string[i]))
    return string


def handel_XML(file_name):
    string = file_read_lines(file_name)
    computed_string = remove_xml_unnecessary(string)
    computed_string = update_filters(computed_string)
    file_write_lines(file_name, computed_string)


def remove_xml_unnecessary(string):
    lines_to_delete = ['name="view_type"']
    for i in range(len(string)):
        for j in range(len(lines_to_delete)):
            if lines_to_delete[j] in string[i]:
                string[i] = ""
                continue
    return string


def update_filters(string):
    for i in range(len(string)):
        temp = string[i].strip()
        if temp.startswith("<filter "):
            if 'name="' not in temp:
                # get the name
                start = temp.find('string="')
                if start != -1:
                    end = temp.find('"', start + 8)
                    name = temp[start + 8:end]
                    place = string[i].find("<filter ") + 8
                    string[i] = string[i][:place] + 'name="' + name + '" ' + string[i][place:]

    return string


def traversing_files():
    for dirpath, d, files in os.walk(os.path.abspath("./modules")):
        path = dirpath
        for file in files:
            if file.endswith(".xml"):
                file_name = os.path.join(path, file)
                handel_XML(file_name)
            if file.endswith(".py"):
                file_name = os.path.join(path, file)
                handel_py_files(file_name)


traversing_files()
