from scipy.stats import kendalltau

from FleissKappa.fleiss import fleissKappa
from extract_results import get_aggregated_classification, get_rater_classifications, create_binary_scale

if __name__ == '__main__':
    db_files = [
        r"C:\Code\seminar\offensive-meme-categorizer\results_db\storage_yaara.db",
        r"C:\Code\seminar\offensive-meme-categorizer\results_db\storageAri.db",
        r"C:\Code\seminar\offensive-meme-categorizer\results_db\storageKadyn.db",
    ]
    classification_matrix = get_aggregated_classification(db_files)
    print(classification_matrix)
    binary_matrix = create_binary_scale(classification_matrix)
    print(binary_matrix)

    f = fleissKappa(classification_matrix, len(db_files))

    f_bin = fleissKappa(binary_matrix, len(db_files))

    print('#######################\nComputing Kendall Tau:')
    flat_raters_classifications = get_rater_classifications(db_files)
    for i, classification_matrix_first in enumerate(flat_raters_classifications[:-1]):
        for j, classification_matrix_second in enumerate(flat_raters_classifications[i + 1:]):
            j += i + 1
            print(f'i: {i}, j: {j}')
            print(classification_matrix_first)
            print(classification_matrix_second)
            correlation, pvalue = kendalltau(classification_matrix_first, classification_matrix_second, nan_policy='raise')
            print(f'files {db_files[i]} <--> {db_files[j]}: Kendall Tau: {correlation}, pvalue: {pvalue}')
