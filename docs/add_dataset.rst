Add a Dataset
===============================

Squirrel-datasets supports you with two tasks:

* Preprocessing data and registering the preprocessed dataset in the data mesh
* Loading data from the data mesh

Preprocessing
-------------
For the first task, i.e. preprocessing, we recommend using `Apache Spark`_. The scenario is that quite often you would
like to work with data stored in Google Cloud Storage and finish your batch processing job on a kubernetes cluser. We use
`PySpark`_ for defining the preprocessing logic in python. You can find a tutorial how to use spark for preprocessing under 
:code:`examples/08.Spark_Preprocessing.ipynb`.

Data Loading
------------
For the second task, i.e. data loading, we use the high level API from :py:mod:`squirrel`. The corresponding data loading logic
is defined through a :py:class:`Driver` class.

Add a New Dataset
------------------
After having understood the two above discussed main tasks and how we handle them, here is how it looks like when you
want to add a new dataset into :py:mod:`squirrel-datasets`: define your preprocessing logic; define your loading logic;
register the dataset into a catalog plugin.

#. Define your preprocessing logic.

   - Create a new directory under :code:`squirrel_datasets_core/datasets` named after your dataset, e.g. "example_dataset".
     Write your preprocessing scripts under a new ``preprocessing.py`` file in it if needed.

#. Define your loading logic.

   - After the preprocessing step, you want to make sure your preprocessed dataset is valid and readable. In that case,
     you need to define the loading logic. The driver defines how the dataset is read from the serialized file into your memory.

   - In :py:mod:`squirrel` there are already many built-in drivers for reading all kinds of datasets. There are
     :py:class:`~squirrel.driver.CsvDriver`, :py:class:`~squirrel.driver.JsonlDriver`, :py:class:`~squirrel.driver.MessagepackDriver`, 
     and many others. For details, please refer to :py:mod:`squirrel.driver`.

   - Select a suitable driver if one of them is applicable to your dataset's format and compression method.

   - If there is no driver suitable for your dataset, then you need to define a custom driver. The custom driver should
     have the same interface as :py:class:`squirrel.driver.IterDriver`. We recommend that you subclass from
     this class, then add the loading logic inside. This class should be saved under 
     :code:`squirrel_datasets_core/datasets/example_dataset/driver.py`

   .. note::

     This is not always the case that data loading occurs after the preprocessing steps. For image datasets, spark is
     not always the right tool to do it. In that case, you may want to load and process the data without it, and you
     need to define the loading logic for your raw data. In that case, you may swap the above steps or use them more
     flexibly. See :py:mod:`squirrel_datasets_core.datasets.imagenet` for an example.

.. _Apache Spark: https://spark.apache.org/docs/latest/
.. _PySpark: https://spark.apache.org/docs/latest/api/python/
.. _squirrel.driver: https://squirrel-core.readthedocs.io/
.. _squirrel_datasets_core.datasets.imagenet: https://squirrel-core.readthedocs.io/