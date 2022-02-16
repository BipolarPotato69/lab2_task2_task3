import argparse
import json
import sys

def parcing():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type = str)
    args = parser.parse_args()
    return args


def read_json(path):
    with open(path, "r") as json_file:
        data = json.load(json_file)
    return data


def main_loop(data):
    while True:
        try:
            keys = list_keys(data)

            if keys[-1] == list or keys[-1] == tuple:
                print("The value in this key is " + str(keys[-1]))
                print("Avalible keys: 0-" + str(len(keys[0])))
            elif keys[-1] == dict:
                print("The value in this key is " + str(keys[-1]))
                print("Avalible keys: ")
                print(keys[0])
            else:
                print("The value in this key is " + str(keys[-1]))
                print(keys[0])
                print("Press Enter to come back")
                answer = input(">>> ")

                if answer == "":
                    return
                else:
                    sys.exit()

            answer = input(">>> ")
            if answer.isdigit():
                answer = int(answer)
            elif answer == "":
                return
            elif answer == "exit":
                sys.exit()

            main_loop(data[answer])

        except KeyError:
            print("Wrong key")
            main_loop(data)
        except IndexError:
            print("Wrong key")
            main_loop(data)


def list_keys(json_file):
    if type(json_file) == dict:
        return (json_file.keys(), type(json_file))
    elif type(json_file) == list or type(json_file) == tuple:
        return (json_file, type(json_file))
    else:
        return (json_file, type(json_file))
    

path = parcing().path
main_loop(read_json(path))
