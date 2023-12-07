import pandas as pd
import sqlite3
import pickle
import os
import re
import sys
from pathlib import Path


path = Path(os.path.dirname(__file__))
sys.path.append(str(path.parent.parent.absolute()))


def extract_sql_content(text):
    pattern = r"<SQL>(.*?)</SQL>"
    matches = re.findall(pattern, text, re.DOTALL)
    return matches[0]


def clean_results(answerlist: list, return_failed: bool):
    if return_failed:
        failed_dict = {}

    # Clean the list of strings
    clean_list = []
    for idx, item in enumerate(answerlist):
        # extracting the SQL statement from the <SQL> tags
        try:
            item = extract_sql_content(item)
        except Exception as e:
            failed_dict[idx] = {"model_output": item}

        # Remove any leading or trailing whitespace
        item = item.strip()
        # Remove any trailing double quotes
        if item.startswith('"') and item.endswith('"'):
            item = item.rstrip('"')
            item = item.lstrip('"')
        # Remove any newlines
        item = item.replace("\n", " ")
        # Add the cleaned item to the clean_list
        clean_list.append(item)
    return clean_list, failed_dict


def run_exact_match_bench(
    df,
    model,
):
    results = []

    counter = 0

    for idx in range(0, df.shape[0]):
        sql_query = df.iloc[idx]["query"]
        prediction_query = df.iloc[idx][model]

        db_id = df.iloc[idx]["db_id"]

        db_file_path = (
            f"{path.parent.absolute()}/spider/spider/database/{db_id}/{db_id}.sqlite"
        )
        conn = sqlite3.connect(db_file_path)
        cursor = conn.cursor()
        try:
            # Fetching the gold standard
            cursor.execute(sql_query)
            result_gold = cursor.fetchall()
            gold_query = f"gold Query: {sql_query}\n"
            gold_result = f"gold result: {result_gold}\n"

            try:
                # Fetching prediction results
                cursor.execute(prediction_query)
                result_preds = cursor.fetchall()
                pred_query = f"prediction Query: {prediction_query}\n"
                pred_result = f"prediction: {result_preds}\n"
            except Exception as e:
                pred_query = f"prediction Query: {prediction_query}\n"
                pred_result = f"error: {e}\n"
                results.append(gold_query + gold_result + pred_query + pred_result)
                continue

            # Comparing the results
            if result_gold == result_preds:
                match = "match\n"
                counter += 1
            else:
                match = "no match\n"
            results.append(gold_query + gold_result + pred_query + pred_result + match)
        except:
            error = "General error\n"
            results.append(error)

    exact_execution_match_accuracy = counter / df.shape[0]
    print(f"Accuracy: {exact_execution_match_accuracy}")
    return exact_execution_match_accuracy


def orchestrate_bench(df_eval, model_id: str, model_id_answers):
    model_id_answers_cleaned, queries_cleaning_failed = clean_results(
        model_id_answers, return_failed=True
    )

    df_eval[model_id] = model_id_answers_cleaned

    exact_match_accuracy = run_exact_match_bench(df_eval, model_id)

    return exact_match_accuracy, df_eval


# def run_bench_on_folder(df_eval, results_folderpath):
#     results_dir = {}

#     # copy over the df to not alter it
#     df = df_eval.copy()

#     result_files = os.walk(results_folderpath)

#     for result_file_name in result_files:
#         filepath = os.path.join(results_folderpath, result_file_name)
#         with open(filepath, "rb") as fp:  # Unpickling
#             model_id_answers = pickle.load(fp)
#         exact_match_accuracy = orchestrate_bench(df, result_file_name, model_id_answers)
#         results_dir[result_file_name], df = exact_match_accuracy

#     return results_dir


def run_bench_on_folder(df_eval, results_folderpath):
    results_dir = {}

    # copy over the df to not alter it
    df = df_eval.copy()

    for root, dirs, files in os.walk(results_folderpath):
        for result_file_name in files:
            filepath = os.path.join(root, result_file_name)
            if result_file_name.startswith("answers"):
                print(f"working on {filepath}")
                with open(filepath, "rb") as fp:  # Unpickling
                    model_id_answers = pickle.load(fp)
                exact_match_accuracy = orchestrate_bench(
                    df, result_file_name, model_id_answers
                )
                results_dir[result_file_name], df = exact_match_accuracy

    return results_dir


# df_eval = pd.read_feather
df_eval = pd.read_feather(f"{path.parent.absolute()}/data/dev_df.feather")
path_to_results_folder = f"{path.parent.absolute()}/results/"

results_dir = run_bench_on_folder(df_eval, path_to_results_folder)

print(results_dir)
