from __future__ import annotations

import sys
from abc import ABC
from typing import Any, Dict
from typing import Generator as Gen
from typing import Generic, Sequence, TypeVar

from numpy.random import PCG64, Generator, SeedSequence

if sys.version_info >= (3, 11):  # pragma: nocover
    from typing import Self
else:
    from typing_extensions import Self


class IGenerator(ABC):
    """This generic class describes a typical generator.

    Such generators can use random methods from :mod:`numpy` and/or
    :mod:`scipy`. The following examples show how to do it in both cases:

    .. code-block:: python

        from scipy.stats import beta

        gen = IGenerator()
        gen.rng.uniform(0, 1)  # Call numpy.random.uniform method using gen rng
        beta.rvs(a=1, b=3, random_state=gen.rng)  # Call scipy.stats.beta.rvs method using gen rng

    :param seed:
    """  # noqa: E501

    def __init__(self, seed: Any = None):
        self.seed = seed

    def configure_seed(self, seed: Any):
        """Set :attr`seed` and :attr`rng`.

        :param seed:
        :return: instance generator

        .. note::
            necessary to easily override it while being able to call it
        """
        if seed is None:
            self._seed = SeedSequence()
        elif isinstance(seed, SeedSequence):
            self._seed = seed
        else:
            self._seed = SeedSequence(seed)
        self._rng = Generator(PCG64(self.seed))
        return self

    @property
    def seed(self) -> SeedSequence:
        """Seed of the generator"""
        return self._seed

    @seed.setter
    def seed(self, seed: Any):
        """Set :attr`seed` and :attr`rng`.

        :param seed:
        """
        self.configure_seed(seed)

    @property
    def rng(self) -> Generator:
        """Random number generator of the generator"""
        return self._rng

    def _copy_kwargs(self) -> Dict:
        """Return kwargs for constructing a copy.

        :return:
        """
        return {
            "seed": SeedSequence(
                entropy=self.seed.entropy,
                spawn_key=self.seed.spawn_key,
                pool_size=self.seed.pool_size,
                n_children_spawned=self.seed.n_children_spawned,
            )
        }

    def copy(self) -> Self:
        """Return a copy of generator.

        :return:
        """
        return self.__class__(**self._copy_kwargs())

    def spawn(self, n_children: int = 1) -> Sequence[Self] | Self:
        """Spawn a copy of the generated with a child seed.

        :return: new generator
        """
        res = [
            self.copy().configure_seed(seed)
            for seed in self.seed.spawn(n_children)
        ]
        if n_children == 1:
            return res[0]
        return res


T = TypeVar("T")


class GeneratorLen(Generic[T]):
    """This class defines a generator of objects with expected length.

    :param generator: source generator of objects
    :param length: expected number of generated objects
    """

    def __init__(self, generator: Gen[T], length: int = None):
        self.generator = generator
        self.length = length

    def __len__(self):
        """Return expected number of objects to generate.

        :return:
        """
        return self.length

    def __iter__(self) -> Gen[T]:
        """Return generator to iterate on.

        :return:
        """
        return self.generator
