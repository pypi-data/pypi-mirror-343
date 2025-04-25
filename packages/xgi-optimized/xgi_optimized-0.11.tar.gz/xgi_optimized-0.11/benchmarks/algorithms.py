import xgi_optimized

rounds = 10
fname = "benchmarks/email-enron.json"


def test_connected(benchmark):
    def setup():
        H = xgi_optimized.read_hif(fname)
        return (H,), {}

    benchmark.pedantic(xgi_optimized.is_connected, setup=setup, rounds=rounds)


def test_clustering_coefficient(benchmark):
    def setup():
        H = xgi_optimized.read_hif(fname)
        return (H,), {}

    benchmark.pedantic(xgi_optimized.clustering_coefficient, setup=setup, rounds=rounds)
