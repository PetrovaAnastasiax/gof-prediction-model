import os
import shutil
from openai import OpenAI

client = OpenAI(api_key='') #insert api_key

source_directory = "" #insert source directory
destination_directory = "" #insert destination directory
prompt = ("I need to distinguish between Java classes that represent GoF patterns - ABSTRACT FACTORY, BUILDER, "
          "FACTORY METHOD, PROTOTYPE, SINGLETON, ADAPTER, BRIDGE, COMPOSITE, DECORATOR, FACADE, FLYWEIGHT, PROXY, "
          "CHAIN OF RESPONSIBILITY, COMMAND, INTERPRETER, ITERATOR, MEDIATOR, MEMENTO, OBSERVER, STATE, STRATEGY, "
          "TEMPLATE METHOD, VISITOR - and classes that represent no GoF pattern. I would like to mark other classes "
          "as NONE. If the class represents one of the aforementioned patterns, reply with only one uppercase word of "
          "the pattern name, if it does not represent any aforementioned pattern, reply with word NONE. Mark this "
          "class: ")


def find_java_files(directory):
    java_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".java"):
                java_files.append(os.path.join(root, file))
    return java_files


def read_java_file(file_path):
    with open(file_path, "r") as file:
        java_code = file.read()
    return java_code


def get_response(class_code):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt + class_code}
        ]
    )
    return completion.choices[0].message.content


java_files = find_java_files(source_directory)

for java_file in java_files:
    file_name = os.path.basename(java_file)
    java_code = read_java_file(java_file)

    destination_folder = ""
    response = get_response(java_code)
    if response == 'ABSTRACT FACTORY':
        destination_folder = "/abstract_factory/"
    elif response == 'BUILDER':
        destination_folder = "/builder/"
    elif response == 'FACTORY METHOD':
        destination_folder = "/factory_method/"
    elif response == 'PROTOTYPE':
        destination_folder = "/prototype/"
    elif response == 'SINGLETON':
        destination_folder = "/singleton/"
    elif response == 'ADAPTER':
        destination_folder = "/adapter/"
    elif response == 'BRIDGE':
        destination_folder = "/bridge/"
    elif response == 'COMPOSITE':
        destination_folder = "/composite/"
    elif response == 'DECORATOR':
        destination_folder = "/decorator/"
    elif response == 'FACADE':
        destination_folder = "/facade/"
    elif response == 'FLYWEIGHT':
        destination_folder = "/flyweight/"
    elif response == 'PROXY':
        destination_folder = "/proxy/"
    elif response == 'CHAIN OF RESPONSIBILITY':
        destination_folder = "/chain_of_responsibility/"
    elif response == 'COMMAND':
        destination_folder = "/command/"
    elif response == 'INTERPRETER':
        destination_folder = "/interpreter/"
    elif response == 'ITERATOR':
        destination_folder = "/iterator/"
    elif response == 'MEDIATOR':
        destination_folder = "/mediator/"
    elif response == 'MEMENTO':
        destination_folder = "/memento/"
    elif response == 'OBSERVER':
        destination_folder = "/observer/"
    elif response == 'STATE':
        destination_folder = "/state/"
    elif response == 'STRATEGY':
        destination_folder = "/strategy/"
    elif response == 'TEMPLATE_METHOD':
        destination_folder = "/template_method/"
    elif response == 'VISITOR':
        destination_folder = "/visitor/"
    elif response == 'NONE':
        destination_folder = "/none/"
    else:
        print(file_name + " ERROR")

    destination_file_path = destination_directory + destination_folder
    destination_file = os.path.join(destination_file_path, file_name)
    shutil.copyfile(java_file, destination_file)

    print("Copied file " + file_name + " to dir " + destination_file)
