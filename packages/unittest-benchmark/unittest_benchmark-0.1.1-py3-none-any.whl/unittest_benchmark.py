import time
from typing import Callable, Any
from scipy.stats import mannwhitneyu
import unittest


class BenchmarkMixin:
    """
    Example usage:
    ```
    class MyTestCase(unittest.TestCase, unittest_benchmark.BenchmarkMixin):
        def test_my_function_is_faster(self):
            self.assertIsFaster(fast_function, benchmark_function)
    ```
    """

    @staticmethod
    def _timeit(callable):
        start = time.perf_counter()
        callable()
        end = time.perf_counter()
        return end - start

    def assertIsFaster(
        self,
        faster: Callable[[], Any],
        benchmark: Callable[[], Any],
        samples: int = 20,
        p_value: float = 0.001,
        msg: Any = None,
    ) -> None:
        """
        Assert that `faster` has a faster runtime than `benchmark`

        Fails if `faster` is not significantly faster than `benchmark`
        at the `p-value` significance level
        """
        faster_samples = [self._timeit(faster) for _ in range(samples)]
        benchmark_samples = [self._timeit(benchmark) for _ in range(samples)]

        result = mannwhitneyu(faster_samples, benchmark_samples, alternative="less")
        test_p_value = result.pvalue

        if test_p_value >= p_value:
            standardMsg = (
                f"{unittest.util.safe_repr(faster)} is not "
                f"significantly faster than {unittest.util.safe_repr(benchmark)}"
            )
            msg = self._formatMessage(msg, standardMsg)
            raise self.failureException(msg)
