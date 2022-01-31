from pathlib import Path
from scipy.stats import kendalltau

from FleissKappa.fleiss import fleissKappa
from extract_ratings import get_aggregated_classification, get_rater_classifications, create_binary_scale

if __name__ == '__main__':
    db_files = [
        r"..\results_db\storage_yaara.db",
        r"..\results_db\storageAri.db",
        r"..\results_db\storageKadyn.db",
    ]
    image_to_agg_classification = get_aggregated_classification(db_files)
    classification_matrix = list(image_to_agg_classification.values())
    print(classification_matrix)
    binary_matrix = create_binary_scale(image_to_agg_classification)
    binary_matrix_values = list(binary_matrix.values())
    print(binary_matrix_values)

    print('################### FleissKappa, discrete categories:')

    f = fleissKappa(classification_matrix, len(db_files))

    print('################### FleissKappa, binary categories:')

    f_bin = fleissKappa(binary_matrix_values, len(db_files))

    print('#######################\nComparing overall scores:')
    flat_raters_classifications = get_rater_classifications(db_files)
    for i, flat_classification_matrix in enumerate(flat_raters_classifications):
        rater_sum = 0
        for score in flat_classification_matrix:
            rater_sum += score
        print(f'file {Path(db_files[i]).name} overall score: {rater_sum}')

    print('#######################\nComputing Kendall Tau:')

    for i, classification_matrix_first in enumerate(flat_raters_classifications[:-1]):
        for j, classification_matrix_second in enumerate(flat_raters_classifications[i + 1:]):
            j += i + 1
            print(f'i: {i}, j: {j}')
            # print(classification_matrix_first)
            # print(classification_matrix_second)
            correlation, pvalue = kendalltau(classification_matrix_first, classification_matrix_second, nan_policy='raise')
            print(f'files {Path(db_files[i]).name} <--> {Path(db_files[j]).name}: Kendall Tau: {correlation}, pvalue: {pvalue}')
