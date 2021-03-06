import pathlib
import json
from extract_ratings import get_aggregated_classification, create_binary_scale, is_harmless, get_avg_rating

db_files = [
    r"..\..\results_db\storage_yaara.db",
    r"..\..\results_db\storageAri.db",
    r"..\..\results_db\storageKadyn.db",
]

if __name__ == '__main__':
    import pprint

    current_dir = pathlib.Path(__file__).parent
    in_path = current_dir.joinpath('all_text')
    out_path = current_dir.parent.joinpath('rated_memes.json')

    image_to_text = dict()
    with open(in_path, 'rb') as in_file:
        for raw_image_data in in_file.readlines():
            image_data = json.loads(raw_image_data)
            image_to_text[image_data['img']] = image_data['text']

    image_to_agg_class = get_aggregated_classification(db_files)
    image_to_bin_scale = create_binary_scale(image_to_agg_class)

    image_to_full_data = dict()

    for image_path, text in image_to_text.items():
        image_file_name = image_path.split('img/')[-1]
        if image_file_name in image_to_agg_class:
            data = dict()
            data['text'] = text

            aggregated_ratings = image_to_agg_class[image_file_name]
            data['aggregated_ratings'] = aggregated_ratings
            data['target_avg'] = get_avg_rating(aggregated_ratings)

            binary_ratings = image_to_bin_scale[image_file_name]
            data['binary_ratings'] = binary_ratings
            data['target_harmful'] = not is_harmless(binary_ratings)

            image_to_full_data[image_file_name] = data

    with open(out_path, 'w') as out_file:
        json.dump(image_to_full_data, out_file)

    pprint.pprint(image_to_full_data)
    print(f'Extracted data for {len(image_to_full_data)} rated memes')
