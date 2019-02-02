from fetch_urls import Fetcher

class CallBuilder:
    """Copied from:
    https://github.com/sybrenstuvel/flickrapi/blob/master/flickrapi/call_builder.py
    """

    def __init__(self, flickrapi_object, method_name='flickr'):
        self.flickrapi_object = flickrapi_object
        self.method_name = method_name
        self.__name__ = method_name.split('.')[-1]

    def __getattr__(self, name):
        if name.startswith('_'):
            raise AttributeError("No such attribute {}".format(name))

        return self.__class__(self.flickrapi_object,
                              self.method_name + '.' + name)

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.method_name)

    def __call__(self, **kwargs):
        return self.flickrapi_object.do_flickr_call(self.method_name, **kwargs)


def get_flickr_api_valid():

    class DummyFlickrAPI:

        def do_flickr_call(self, method_name, **kwargs):
            return {'photos': {'page': 1,
                    'pages': 3,
                    'perpage': 1,
                    'photo': [{'farm': 5,
                            'id': '46944690811',
                            'isfamily': 0,
                            'isfriend': 0,
                            'ispublic': 1,
                            'owner': '161920781@N04',
                            'secret': '3535fb688d',
                            'server': '4865',
                            'title': 'Weigh'},
                            {'farm': 5,
                            'id': '46025158395',
                            'isfamily': 0,
                            'isfriend': 0,
                            'ispublic': 1,
                            'owner': '23498592@N03',
                            'secret': 'c51c5d80e6',
                            'server': '4887',
                            'title': 'Goldbuntbarsch'},
                            {'farm': 8,
                            'id': '31997999617',
                            'isfamily': 0,
                            'isfriend': 0,
                            'ispublic': 1,
                            'owner': '23498592@N03',
                            'secret': '64de3b6600',
                            'server': '7845',
                            'title': 'Mittelmeermuräne (Mitte), Brauner Zackenbarsch (hinten)'}]
                               }
                    }

    return CallBuilder(DummyFlickrAPI())


def get_flickr_api_not_enough():

    class DummyFlickrAPI:

        def do_flickr_call(self, method_name, **kwargs):
            return {'photos': {'page': 1,
                    'pages': 1,
                    'perpage': 1,
                    'photo': [{'farm': 5,
                            'id': '46944690811',
                            'isfamily': 0,
                            'isfriend': 0,
                            'ispublic': 1,
                            'owner': '161920781@N04',
                            'secret': '3535fb688d',
                            'server': '4865',
                            'title': 'Weigh'}]
                               }
                    }

    return CallBuilder(DummyFlickrAPI())


def get_flickr_api_invalid():

    class DummyFlickrAPI:

        def do_flickr_call(self, method_name, **kwargs):
            return {'photos': {'page': 1,
                    'no_key_for_pages': 1,
                    'perpage': 1,
                    'photo': [{'farm': 5,
                            'id': '46944690811',
                            'isfamily': 0,
                            'isfriend': 0,
                            'ispublic': 1,
                            'owner': '161920781@N04',
                            'secret': '3535fb688d',
                            'server': '4865',
                            'title': 'Weigh'}]
                               }
                    }

    return CallBuilder(DummyFlickrAPI())


def get_flickr_api_invalid_data():

    class DummyFlickrAPI:

        def do_flickr_call(self, method_name, **kwargs):
            return {'photos': {'page': 1,
                    'pages': 1,
                    'perpage': 1,
                    'photo': [{'farm': 'wrong_type',
                            'id': '46944690811',
                            'isfamily': 0,
                            'isfriend': 0,
                            'ispublic': 1,
                            'owner': '161920781@N04',
                            'wrong_key_secret': '3535fb688d',
                            'server': '4865',
                            'title': 'Weigh'}]
                               }
                    }

    return CallBuilder(DummyFlickrAPI())


def test_fetch_valid():
    fetcher = Fetcher(get_flickr_api_valid())
    requested_class = 'dog'
    requested_count = 2
    fetched_urls = fetcher.fetch([{'name': requested_class,
                                   'count': requested_count}])

    assert type(fetched_urls) is dict
    assert requested_class in fetched_urls.keys()
    assert len(fetched_urls[requested_class]) == requested_count


def test_fetch_valid_not_enough():
    fetcher = Fetcher(get_flickr_api_not_enough())
    requested_class = 'dog'
    requested_count = 2
    fetched_urls = fetcher.fetch([{'name': requested_class,
                                   'count': requested_count}])

    assert type(fetched_urls) is dict
    assert requested_class in fetched_urls.keys()
    assert len(fetched_urls[requested_class]) < requested_count


def test_fetch_invalid():
    fetcher = Fetcher(get_flickr_api_invalid())
    requested_class = 'dog'
    requested_count = 2
    fetched_urls = fetcher.fetch([{'name': requested_class,
                                   'count': requested_count}])

    assert type(fetched_urls) is dict
    assert requested_class in fetched_urls.keys()
    assert fetched_urls[requested_class] is None


def test_fetch_invalid_data():
    fetcher = Fetcher(get_flickr_api_invalid_data())
    requested_class = 'dog'
    requested_count = 2
    fetched_urls = fetcher.fetch([{'name': requested_class,
                                   'count': requested_count}])

    assert type(fetched_urls) is dict
    assert requested_class in fetched_urls.keys()
    assert len(fetched_urls[requested_class]) == 1
    assert fetched_urls[requested_class][0] is None
