# jubilant_adapters

[![PyPI version](https://badge.fury.io/py/jubilant-adapters.svg)](https://pypi.org/project/jubilant-adapters/) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


**Jubilant Adapters** is a *back-to-basics* effort to facilitate migration of charm repositories using `pytest-operator` as their integration testing library, to the newer and better `jubilant` library. By *back-to-basics*, I mean pure Gang of Four design patterns, instead of blindly throwing in developers, LLMs and/or agents and burning token, CI and developer budget for something that could be achieved much simpler, with a software engineering mindset.

The way it works is to add `jubilant_adpaters` as a test dependency, use the `JujuFixture` provided by that lib as the pivot fixture instead of `OpsTest`, and simply replace all `ops_test` calls with `juju.ext`. I have also included a utility script which does that for you, but it is opinionated and may not work optimally in your particular case. But the general flow remains the same regardless of whether or not you use the utility script.

## More on `JujuFixture`

`JujuFixture` inherits from `jubilant.Juju`, and adds an extension layer via the `ext` property, which provides familiar libjuju-style API on the surface, but uses `jubilant` on the backend.

So instead of calling `ops_test.model.deploy(...)`, you can call `juju.ext.model.deploy(...)`, and so on.

The adapters may not cover 100% of the libjuju API, and I followed the Pareto rule, coupled with my own experience and judgement to provide adpaters for the most widely used APIs. But feel free to contribute and extend the adapters if you feel something is missing, and I would highly appreciate that!
