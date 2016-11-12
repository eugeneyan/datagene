#!/usr/bin/env bash
python -m data_prep.prep_title_category metadata_categories_only title_category
python -m data_prep.clean_titles title_category
python -m categorize.create_dict title_category_keep categorization_dicts
python run.py 127.0.0.1 6688
