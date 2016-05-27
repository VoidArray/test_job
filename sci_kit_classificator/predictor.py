import os
import re
import math

from sklearn.linear_model import LogisticRegression

class Predictor():

    def __init__(self, learn_dir_path, test_dir_path):
        self._learn_dataset, self._learn_dataset_marks = \
            self._dir_seeker(learn_dir_path, w_class_mark=True)
        self._test_dataset, _ = self._dir_seeker(test_dir_path, w_class_mark=False)

    def _dir_seeker(self, dir_path, w_class_mark):
        files_list = os.listdir(dir_path)
        test_values = []
        classes_marks = []
        for filename in files_list:
            full_path = os.path.join(dir_path, filename)
            values, marks = self._read_file(full_path, w_class_mark)
            test_values.extend(values)
            classes_marks.extend(marks)
        return test_values, classes_marks

    def _read_file(self, file_path, w_class_mark):
        """
        File parser.

        w_class_mark - try read mark of class or not
        """
        test_values = []
        classes_marks = []
        inputs_count = 7
        with open(file_path, 'r') as file_handler:
            for line in file_handler:
                if '@' in line:
                    if '@inputs' in line:
                        inputs_count = len(re.findall(r'[\w|\d]+', line)) - 1
                else:
                    splited_line = line.strip().replace(' ', '').split(',')
                    # Here we round float values
                    test_value = list([math.floor(float(x)) for x in splited_line[:inputs_count]])
                    test_values.append(test_value)
                    if w_class_mark:
                        class_mark = splited_line[-1]
                        classes_marks.append(class_mark)
        return test_values, classes_marks

    def estimate(self):
        logistic_regression = LogisticRegression()
        # calc accuracy
        count_80percent = len(self._learn_dataset) // 5 * 4
        train_x = self._learn_dataset[:count_80percent]
        train_y = self._learn_dataset_marks[:count_80percent]
        estimate_x = self._learn_dataset[count_80percent:]
        estimate_y = self._learn_dataset_marks[count_80percent:]
        logistic_regression.fit(train_x, train_y)
        accuracy = logistic_regression.score(estimate_x, estimate_y)
        # train on full learn_dataset
        logistic_regression.fit(self._learn_dataset, self._learn_dataset_marks)
        predict_result = logistic_regression.predict(self._test_dataset)
        predict_probability = logistic_regression.predict_proba(self._test_dataset)
        # gen output result
        result = []
        for i in range(len(self._test_dataset)):
            list_str_from_test_value = [str(x) for x in self._test_dataset[i]]
            str_test_value = ', '.join(list_str_from_test_value)
            predicted_mark = int(predict_result[i])
            confidence_mark = predict_probability[i][predicted_mark]
            confidence_mark_percent = round(confidence_mark * 100, 2)
            result_value = (str_test_value, str(predicted_mark), confidence_mark_percent)
            result.append(result_value)
        return accuracy, result
