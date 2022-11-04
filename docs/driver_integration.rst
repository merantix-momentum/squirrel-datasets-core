Huggingface, Hub, Torchvision
=============================

Ever wondered how you can tap into common databases like `Huggingface <https://huggingface.co/>`_, `Activeloop Hub <https://www.activeloop.ai/>`_ and `Torchvision <https://pytorch.org/vision/stable/datasets.html>`_ with Squirrel? Squirrel creates lightweight wrappers around these libraries' APIs, which means you can quickly and easily load data from the mentioned servers. The benefit is that you get Squirrel's stream manipulation functionality on-top. Say you want to pre-process a Huggingface dataset with a Squirrel multi-processing :code:`async_map` that is easily achievable with the :py:class:`HuggingfaceDriver`. 

The below examples show how to instantiate the three drivers and shows what they output. Note that we simply “forward” the output of these libraries, so the format of whatever they output may differ. For example, in the below code we take the first item of the pipeline with :code:`.take(1)` and we map a :code:`print` function over this pipeline, which outputs something different for each backend. The images coming from the Huggingface servers are :py:class:`PIL` images, while for Hub they are in their custom :py:class:`Tensor` format. The user should write corresponding pre-processing functions that suit their use-case.

.. literalinclude:: code/all_drivers.py
    :language: python

What does this look like in a realistic scenario? Let's say you want to train a classifier on the CIFAR-100 dataset and you need a torch :py:class:`Dataloader` to train the model. 
Simply create the :py:class:`HuggingfaceDriver` as shown below and use it as a data source. 
A cool side-effect of using the :py:class:`HuggingfaceDriver` is that you won't need to download the data locally - but it can be streamed directly from the Huggingface servers. 
Beware that your machine's internet connection may become a bottleneck here. 
Also note that you can pass any arguments and keyword arguments to the respective drivers to influence their internals. 
For example for Huggingface, you can set :py:class:`HuggingfaceDriver(url, streaming=False)` to download the data locally before starting to iterate.

.. literalinclude:: code/real_scenario.py
    :language: python

Please take note of the original dataset license from the dataset provider.