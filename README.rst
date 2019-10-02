.. image:: https://github.com/Cheukting/picknmix/raw/master/logo/picknmix_logo.png

==========
Pick n Mix
==========


.. image:: https://img.shields.io/pypi/v/picknmix.svg
        :target: https://pypi.python.org/pypi/picknmix

.. image:: https://img.shields.io/travis/picknmix/picknmix.svg
        :target: https://travis-ci.org/picknmix/picknmix

.. image:: https://readthedocs.org/projects/picknmix/badge/?version=latest
        :target: https://picknmix.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
        :target: https://opensource.org/licenses/MIT
        :alt: License badge




A simple tool to help building stacking models.


* Free software: MIT license
* Documentation: https://picknmix.readthedocs.io.


Features
--------

Pick n Mix is a simple stacking tool for stacking Sci-Kit learn models of your picks.
It provided 2 classes: Layer and Stack. Layer is a parallel combination of models,
while Stack combine Layers to create a stacking model.

How to Install
--------------

Stable Release
~~~~~~~~~~~~~~
To install Pick n Mix, run this command in your terminal:

::

    $ pip install picknmix
    
This is the **preferred** method to install Pick n Mix, as it will always install the most recent **stable** release.

If you don’t have `pip <https://pip.pypa.io/en/stable/>`_ installed, this `Python <http://docs.python-guide.org/en/latest/starting/installation/>`_ installation guide can guide you through the process.

From sources
~~~~~~~~~~~~
+ You can either clone the public repository:

::

    $ git clone git://github.com/Cheukting/picknmix

+ Or download the `tarball <https://github.com/Cheukting/picknmix/tarball/master>`_:      

::

    $ curl  -OL https://github.com/Cheukting/picknmix/tarball/master

+ Once you have a copy of the source, you can install it with:

::

    $ python setup.py install
    
Usage
-----
Use Pick n Mix to create a regression model:

::

    from picknmix import Layer, Stack

    import numpy as np
    from sklearn.linear_model import LinearRegression
    from sklearn.linear_model import Ridge

    first_layer = Layer([LinearRegression(), Ridge()])
    second_layer = Layer([LinearRegression()])
    model = Stack([first_layer, second_layer])

    X = np.array([[1, 1], [1, 2], [2, 2], [2, 3]])
    y = np.dot(X, np.array([1, 2])) + 3
    model.fit(X, y)
    model.predict(np.array([[3, 5]]))
    
You can also use preprocessing in a Layer:

::

    from sklearn.linear_model import MinMaxScaler

    first_layer = Layer([LinearRegression(), Ridge()],
                        preprocessors = [MinMaxScaler(), None])
                        
For more examples for usage, please refer to the _`documentation < https://picknmix.readthedocs.io>`_.

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

Thanks Agathe_ for the logo.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _Agathe: https://www.agathests.com/
