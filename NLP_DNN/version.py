from pkg_resources import get_distribution, DistributionNotFound

def da_version():
    try:
        __version__ = get_distribution('quantext').version
        return __version__
    except DistributionNotFound:
        # package is not installed
        pass
