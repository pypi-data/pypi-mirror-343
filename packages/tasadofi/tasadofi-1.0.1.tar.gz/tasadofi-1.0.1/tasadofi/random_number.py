import random
from abc import abstractmethod
from collections import deque
from typing import Callable, Union


class RndBase:
    """Base class for random number generation."""

    def __init__(self, sampler: Union[Callable, str], *sampler_args, **sampler_kwargs):
        self._sampler = sampler
        self._sampler_args = sampler_args
        self._sampler_kwargs = sampler_kwargs
        self._qlen = 10
        self._cache = deque(maxlen=self._qlen)

        if isinstance(sampler, str):
            self._sampler_fc = lambda: self.add_to_cache(
                RndBase._build_sampler(sampler, *sampler_args, **sampler_kwargs)
            )
        elif isinstance(sampler, Callable):
            self._sampler_fc = lambda: self.add_to_cache(sampler(*sampler_args, **sampler_kwargs))
        else:
            raise ValueError(f'{sampler} is not supported sampler')

        self._check_sampler()

    @abstractmethod
    def _check_sampler(self):
        raise NotImplementedError()

    def set_cache_size(self, size: int = 10):
        """
        Sets the maximum size of the cache for storing generated random numbers.

        Parameters
        ----------
        size : int, optional
            The maximum number of random numbers to store in the cache. Defaults to 10.

        Notes
        -----
        When the cache reaches its maximum size, the oldest entries are discarded
        as new random numbers are added.
        """
        self._qlen = size
        self._cache = deque(maxlen=size)

    @staticmethod
    def _build_sampler(sampler: str, *args, **kwargs) -> Callable:
        """Build sampler function from a string."""
        samplers = {
            'betavariate': random.betavariate,
            'expovariate': random.expovariate,
            'gammavariate': random.gammavariate,
            'gauss': random.gauss,
            'lognormvariate': random.lognormvariate,
            'paretovariate': random.paretovariate,
            'normalvariate': random.normalvariate,
            'randint': random.randint,
            'random': random.random,
            'sample': random.sample,
            'triangular': random.triangular,
            'uniform': random.uniform,
            'vonmisesvariate': random.vonmisesvariate,
            'weibullvariate': random.weibullvariate,
        }

        if sampler in samplers:
            return samplers[sampler](*args, **kwargs)
        else:
            raise ValueError(f'unknown sampler: {sampler}. Supported samplers are {list(samplers.keys())}')

    def add_to_cache(self, value):
        self._cache.append(value)
        return value

    def __abs__(self):
        return abs(self._sampler_fc())

    def __add__(self, value):
        return self._sampler_fc() + value

    def __bool__(self):
        return self._sampler_fc() != 0

    def __call__(self, *args, **kwds):
        raise NotImplementedError('cannot be called as a function')

    def __divmod__(self, value):
        return divmod(self._sampler_fc(), value)

    def __float__(self):
        return float(self._sampler_fc())

    def __eq__(self, value):
        return self._sampler_fc() == value

    def __floordiv__(self, value):
        return self._sampler_fc() // value

    def __ge__(self, value):
        return self._sampler_fc() >= value

    def __gt__(self, value):
        return self._sampler_fc() > value

    def __int__(self):
        return int(self._sampler_fc())

    def __le__(self, value):
        return self._sampler_fc() <= value

    def __lt__(self, value):
        return self._sampler_fc() < value

    def __mod__(self, value):
        return self._sampler_fc() % value

    def __mul__(self, value):
        return self._sampler_fc() * value

    def __ne__(self, value):
        return self._sampler_fc() != value

    def __neg__(self):
        return -self._sampler_fc()

    def __pos__(self):
        return +self._sampler_fc()

    def __radd__(self, value):
        return value + self._sampler_fc()

    def __rdivmod__(self, value):
        return value / self._sampler_fc()

    def __reduce__(self):
        raise not NotImplementedError('pickling is not supported yet')

    def __repr__(self):
        raise NotImplementedError('TODO: string rep')

    def __rfloordiv__(self, value):
        return value // self._sampler_fc()

    def __rmod__(self, value):
        return value % self._sampler_fc()

    def __rmul__(self, value):
        return value / self._sampler_fc()

    def __rsub__(self, value):
        return value - self

    def __rtruediv__(self, value):
        return value / self._sampler_fc()

    def __str__(self):
        if isinstance(self._sampler, Callable):
            sampler_name = self._sampler.__name__
        elif isinstance(self._sampler, str):
            sampler_name = self._sampler
        else:
            sampler_name = 'unknown'
        args = ', '.join([str(arg) for arg in self._sampler_args])
        kwargs = [f'{kwarg}={value}' for kwarg, value in self._sampler_kwargs.items()]
        kwargs = ', '.join(kwargs)

        if kwargs:
            kwargs = ', ' + kwargs
        else:
            kwargs = ''

        return f'sampler {sampler_name}({args}{kwargs})' f'\nlast {self._qlen} generated values {list(self._cache)}'

    def __sub__(self, value):
        return self._sampler_fc() - value

    def __truediv__(self, value):
        return self._sampler_fc() / value


class RndFloat(RndBase, float):
    """
    A class that represents a random floating-point number.
    This class inherits from RndBase and the built-in float type to provide
    functionality for sampling random float values.

    Parameters
    ----------
    sampler : Union[Callable, str]
        A callable function or a string that identifies a predefined sampler.
        The sampler should return a float value when called.
    *sampler_args
        Positional arguments to pass to the sampler function.
    **sampler_kwargs
        Keyword arguments to pass to the sampler function.

    Raises
    ------
    AssertionError
        If the sampler function does not return a float value.

    Examples
    --------
    >>> from tasadofi.random_number import RndFloat
    >>> import random
    >>> # Using a callable
    >>> rand_float = RndFloat(random.uniform, 0, 1)
    >>> float(rand_float)  # Get a random float between 0 and 1
    0.7239...
    >>> # Using a predefined sampler string
    >>> rand_std_normal = RndFloat("normal", 0, 1)
    >>> float(rand_std_normal)  # Get a random float from normal distribution
    -0.2314...
    """

    def __new__(cls, sampler: Union[Callable, str], *sampler_args, **sampler_kwargs):
        instance = super().__new__(cls, 0.0)
        return instance

    def _check_sampler(self):
        assert isinstance(self._sampler_fc(), float), 'sampler function did not return float'
        self._cache.clear()


class RndInt(RndBase, int):
    """
    A class that represents a random integer number.
    This class inherits from RndBase and the built-in integer type to provide
    functionality for sampling random integer values.

    Parameters
    ----------
    sampler : Union[Callable, str]
        A callable function or a string that identifies a predefined sampler.
        The sampler should return a integer value when called.
    *sampler_args
        Positional arguments to pass to the sampler function.
    **sampler_kwargs
        Keyword arguments to pass to the sampler function.

    Raises
    ------
    AssertionError
        If the sampler function does not return a integer value.

    Examples
    --------
    >>> from tasadofi.random_number import RndInt
    >>> import random
    >>> # Using a callable
    >>> rand_integer = RndInt(random.randint, 0, 10)
    >>> int(rand_integer)  # Get a random integer between 0 and 10
    7...
    >>> # Using a predefined sampler string
    >>> rand_integer = RndInt("randint", 0, 10)
    >>> float(rand_integer)  # Get a random integer from uniform distribution
    3...
    """

    def __new__(cls, sampler: Union[Callable, str], *sampler_args, **sampler_kwargs):
        instance = super().__new__(cls, 0)
        return instance

    def _check_sampler(self):
        assert isinstance(self._sampler_fc(), int), 'sampler function did not return int'
        self._cache.clear()
