.. list-table::
    :header-rows: 1

    *   - pretty_name
        - CamVid Dataset
    *   - annotations_creators
        -
    *   - language_creators
        -
    *   - languages
        - 
    *   - licenses
        - CC BY-NC-ND 4.0
    *   - multilinguality
        -
    *   - size_categories
        - 100<n<1K
    *   - source_datasets
        -
    *   - task_categories
        - semantic-segmentation
    *   - task_ids
        -
    *   - paperswithcode_id
        - camvid
    

Dataset Description
###################

* Homepage: `CamVid <http://mi.eng.cam.ac.uk/research/projects/VideoRec/CamVid/>`_
* Licenses: `Attribution-NonCommercial-NoDerivatives 4.0 International <https://creativecommons.org/licenses/by-nc-sa/4.0/>`_
 
Dataset Summary
***************

Cambridge-driving Labeled Video Database: Road/driving scene understanding database.

Download and prepare data
*************************

Download the data from this `github repository <https://github.com/alexgkendall/SegNet-Tutorial>`_ and extract it. 
Replace {PATH_TO_DATA} below with the location of the CamVid folder. Use the following code to load it:

.. code-block:: python

    from squirrel_datasets_core.datasets.camvid import CamvidDriver
    iter_train = CamvidDriver("{PATH_TO_DATA}").get_iter("train")
    iter_val = CamvidDriver("{PATH_TO_DATA}").get_iter("val")
    iter_test = CamvidDriver("{PATH_TO_DATA}").get_iter("test")


Dataset Structure
###################

Data Instances
**************

A sample from the training set is provided below:

.. code-block::

    {
        'image_url': '{PATH_TO_DATA}/train/0016E5_07920.png', 
        'label_url': '{PATH_TO_DATA}/trainannot/0016E5_07920.png', 
        'split': 'train'
        'image': array(...)
        'label': array(...)
    }

Dataset Schema
**************

- `img`: A numpy array containing the 480x360 RGB image.
- `label`: semantic segmentation map - sky (0), building (1), pole (2), road (3), pavement (4), tree (5), sign/symbol (6), fence (7), car (8), pedestrian (9), bicyclist (10), unlabelled (11)
 
Data Splits
***********

+--------------+-----+----+----+
|   name       |train|val |test|
+--------------+-----+----+----+
|camvid        |367  |101 |233 | 
+--------------+-----+----+----+
