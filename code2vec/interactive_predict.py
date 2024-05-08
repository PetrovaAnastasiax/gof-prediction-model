from common import common
from extractor import Extractor
import os
import numpy as np
import pandas as pd

SHOW_TOP_CONTEXTS = 10
MAX_PATH_LENGTH = 8
MAX_PATH_WIDTH = 2
JAR_PATH = 'JavaExtractor/JPredict/target/JavaExtractor-0.0.1-SNAPSHOT.jar'


class InteractivePredictor:
    java_patterns = {
        'adapter': 'JavaPatterns/adapter/',
        'builder': 'JavaPatterns/builder/',
        'prototype': 'JavaPatterns/prototype/',
        'singleton': 'JavaPatterns/singleton/',
        'none': 'JavaPatterns/none/',
    }

    def __init__(self, config, model):
        model.predict([])
        self.model = model
        self.config = config
        self.path_extractor = Extractor(config,
                                        jar_path=JAR_PATH,
                                        max_path_length=MAX_PATH_LENGTH,
                                        max_path_width=MAX_PATH_WIDTH)

    def read_file(self, input_filename):
        with open(input_filename, 'r') as file:
            return file.readlines()

    def predict(self):
        mean_vectors = []

        for pattern, base_dir in self.java_patterns.items():
            relative_paths = []
            for root, dirs, files in os.walk(base_dir):
                for file in files:
                    relative_path = os.path.relpath(os.path.join(root, file), base_dir)
                    relative_path = base_dir + relative_path
                    relative_paths.append(relative_path)

            for input_filename in relative_paths:
                # Split the string by '/'
                split_file_name = input_filename.split('/')

                # Select the portion after the second '/'
                java_class_name = "/".join(split_file_name[2:])

                code_vectors = []
                try:
                    predict_lines, hash_to_string_dict = self.path_extractor.extract_paths(input_filename)
                    raw_prediction_results = self.model.predict(predict_lines)

                    for raw_prediction in raw_prediction_results:
                        code_vectors.append(raw_prediction.code_vector)

                    mean_vector = np.mean(code_vectors, axis=0)
                    mean_vector = np.concatenate(([java_class_name, pattern], mean_vector))
                    mean_vectors.append(mean_vector)
                except ValueError as e:
                    print(java_class_name)
                    print(e)
            if self.config.EXPORT_CODE_VECTORS:
                df = pd.DataFrame(mean_vectors)
                file_path = "marked_up_embeddings.csv"
                df.to_csv(file_path, index=False)
