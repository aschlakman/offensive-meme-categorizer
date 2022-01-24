import sqlite3
from typing import Set, List, Dict
from collections import defaultdict


def _get_image_to_category(db_file: str):
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    image_to_category = dict()

    for image_name, category_name in cur.execute('''
select images.imageName, categories.categoryName from categories 
join labels on categories.id = labels.category_id
join images on images.id = labels.image_id
join dataSets on dataSets.id = images.dataSet_id
where dataSets.dataSetName != 'ds\sampleSetOne'
    '''):
        image_to_category[image_name] = category_name
    return image_to_category


def _get_categories(db_file: str):
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    categories = []
    for row in cur.execute('''
select categories.categoryName from categories 
join labels on categories.id = labels.category_id
join images on images.id = labels.image_id
join dataSets on dataSets.id = images.dataSet_id
where dataSets.dataSetName != 'ds\sampleSetOne'
group by categories.categoryName
    '''):
        categories.append(row[0])
    return categories


def _get_indexed_categories(categories: Set[str]):
    ordered_categories = list(categories)
    ordered_categories.sort()

    category_to_index = dict()
    for i, category in enumerate(ordered_categories):
        category_to_index[category] = i
    return category_to_index


def get_aggregated_classification(db_file_names: List[str]) -> Dict[str, List[int]]:
    """
    Get a list of the amount of scores given for each meme,
    i.e. [[2,1,0],[...]] -> For the first meme, a score of 1 was given by 2 raters, and a score of 2 was given by 1 rater.
    :param db_file_names: Names of the db files.
    :return: A list of the amount of scores given by the raters for each meme.
    """
    file_to_categorized_images = dict()
    categories = set()

    for db_file_path in db_file_names:
        categories.update(_get_categories(db_file_path))
        image_to_category = _get_image_to_category(db_file_path)
        file_to_categorized_images[db_file_path] = image_to_category

    category_to_index = _get_indexed_categories(categories)

    image_to_classifications = defaultdict(list)
    for db_file, categorized_images in file_to_categorized_images.items():
        for image_name, category_name in categorized_images.items():
            image_to_classifications[image_name].append(category_name)

    classification_matrix: Dict[str, List[int]] = dict()
    for image, classifications in image_to_classifications.items():

        aggregated_classifications = [0 for _ in category_to_index]
        for classification in classifications:
            index = category_to_index[classification]
            aggregated_classifications[index] += 1
        classification_matrix[image] = aggregated_classifications

    return classification_matrix


def get_rater_classifications(db_file_names: List[str]) -> List[List[int]]:
    """
    Get a list of the all the scores that each rater gave.
    :param db_file_names: Names of the db files
    :return: All scores given by each rater.
    """
    file_to_categorized_images = dict()
    categories = set()

    for db_file_path in db_file_names:
        categories.update(_get_categories(db_file_path))
        image_to_category = _get_image_to_category(db_file_path)
        file_to_categorized_images[db_file_path] = image_to_category

    category_to_index = _get_indexed_categories(categories)

    all_raters_classifications: List[List[int]] = []
    for db_file, categorized_images in file_to_categorized_images.items():

        rater_classifications: List[int] = []

        for image_name, category_name in categorized_images.items():
            rater_classifications.append(category_to_index[category_name])

        all_raters_classifications.append(rater_classifications)

    return all_raters_classifications


def is_harmless(binary_classification: List[int]) -> bool:
    """
    Check if individual binary classification counts as harmful / harmless
    :param binary_classification:  binary meme classification
    :return: True for harmless meme, False otherwise
    """
    return binary_classification[0] >= binary_classification[1]


def get_avg_rating(meme_rating: List[int]) -> float:
    """
    Get the average rating, based on raters overall score
    :param meme_rating: rating, in format returned by `get_aggregated_classification`
    :return: Average rater score
    """
    raters_count = 0
    rating_sum = 0
    for i, val in enumerate(meme_rating):
        rating_sum += i * val
        raters_count += val
    return rating_sum / raters_count


def create_binary_scale(classification_matrix: Dict[str, List[int]]) -> Dict[str, List[int]]:
    """
    Create a binary scale for rater scores (i.e. convert numeric scores to boolean scores)
    :param classification_matrix: Mapping between image name and classifications.
    :return: Image name to the raters binary score
    """
    binary_classification_matrix:Dict[str, List[int]] = dict()

    harmless_count = 0
    offensive_count = 0

    for image_name, discrete_classification in classification_matrix.items():
        binary_classification = [0, 0]
        for i, value in enumerate(discrete_classification):
            if i + 1 <= len(discrete_classification) / 2:
                binary_classification[0] += value
            else:
                binary_classification[1] += value

        if is_harmless(binary_classification):
            harmless_count += 1
        else:
            offensive_count += 1
        binary_classification_matrix[image_name] = binary_classification

    print(f"Harmless: {harmless_count} Offensive: {offensive_count} "
          f"Percent Offensive: {offensive_count / (offensive_count + harmless_count)}")
    return binary_classification_matrix


if __name__ == '__main__':
    db_files = [
        r"C:\Code\seminar\results_db\storage_yaara.db",
        r"C:\Code\seminar\results_db\storageMerav.db",
        r"C:\Code\seminar\results_db\storageAri.db"
                ]
    image_to_aggregated_classification = get_aggregated_classification(db_files)
    print(image_to_aggregated_classification)
