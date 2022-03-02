.. list-table::
    :header-rows: 1

    *   - pretty_name
        - 2018 Datascience Bowl
    *   - annotations_creators
        -
    *   - language_creators
        -
    *   - languages
        - 
    *   - licenses
        - CC0
    *   - multilinguality
        -
    *   - size_categories
        - 1K<n<10K
    *   - source_datasets
        -
    *   - task_categories
        - 
    *   - task_ids
        - semantic-segmentation
    *   - paperswithcode_id
        - 2018-data-science-bowl
    

Dataset Description
###################

* Homepage: `DS Bowl on Kaggle <https://www.kaggle.com/c/data-science-bowl-2018/data>`_
* Licenses: CC0 (public domain)

Dataset Summary
***************

Segmentation of nuclei in cells.

Download and prepare data
*************************

Download the data directly from `kaggle <https://www.kaggle.com/c/data-science-bowl-2018/data>`_ and extract all zip files. 
Replace {PATH_TO_DATA} below with the location of the folder containing all data. Use the following code to load it:

.. code-block:: python

    from squirrel_datasets_core.datasets.ds_bowl_2018 import DataScienceBowl2018Driver
    iter_train = DataScienceBowl2018Driver("{PATH_TO_DATA}").get_iter("stage1_train")
    iter_test1 = DataScienceBowl2018Driver("{PATH_TO_DATA}").get_iter("stage1_test")
    iter_test2 = DataScienceBowl2018Driver("{PATH_TO_DATA}").get_iter("stage2_test_final")


Dataset Structure
###################

Data Instances
**************

A sample from the training set is provided below:

.. code-block::

    {
        'sample_url': '{PATH_TO_DATA}/stage1_train/3ebd...', 
        'split': 'stage1_train'
        'image': array(...)
        'masks': [array(...)]
    }

Dataset Schema
**************

- `img`: A numpy array containing an RGB image of varying size.
- `masks`: List of semantic segmentation maps for each nucleus. `True` if within area of nucleus and `False` if not.
 
Masks are not included for the test splits.

Data Splits
***********

+---------------------+------------+------------+-----------------+
|   name              |stage1_train|stage1_test |stage2_test_final|
+---------------------+------------+------------+-----------------+
|datascience-bowl-2018|670         |65          |3019             | 
+---------------------+------------+------------+-----------------+
