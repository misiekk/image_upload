from collections import defaultdict


def statistics(func):
    u'''Decorator function which counts hits on pages according to the image name'''
    stats = defaultdict(int)

    def wrap(request, image_name):
        stats[image_name] += 1
        # after some time or after a specified number of hits update the statistics in database
        # and reset the defaultdict
        return func(request, image_name)
    return wrap
