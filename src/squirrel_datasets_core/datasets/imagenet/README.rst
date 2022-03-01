.. list-table::
    :header-rows: 1

    *   - pretty_name
        - Imagenet Dataset
    *   - annotations_creators
        -
    *   - language_creators
        -
    *   - languages
        - 
    *   - licenses
        - custom
    *   - multilinguality
        -
    *   - size_categories
        - 1M<n<10M
    *   - source_datasets
        -
    *   - task_categories
        - image-classification
    *   - task_ids
        -
    *   - paperswithcode_id
        - imagenet
    

Dataset Description
###################

* Homepage: `Imagenet <https://image-net.org/index.php>`_
* Licenses: non-commercial use

Dataset Summary
***************

General image classification.

Download and prepare data
*************************

Download the data directly from `kaggle <https://www.kaggle.com/c/imagenet-object-localization-challenge/data>`_ and extract it. 
Replace {PATH_TO_DATA} below with the location of the folder containing the data. Use the following code to load it:

.. code-block:: python

    from squirrel_datasets_core.datasets.imagenet import RawImageNetDriver
    iter_train = RawImageNetDriver("{PATH_TO_DATA}").get_iter("train")
    iter_val = RawImageNetDriver("{PATH_TO_DATA}").get_iter("val")
    iter_test = RawImageNetDriver("{PATH_TO_DATA}").get_iter("test")


Data Splits
***********

+--------------+-----+----+-----+
|   name       |train|val |test |
+--------------+-----+----+-----+
|imagenet      |1,2M |50K |100K | 
+--------------+-----+----+-----+
