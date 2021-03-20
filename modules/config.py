# PiQRAP Copyright (C) 2021 Andy Jones - teardrop@zen.co.uk
#!/usr/bin/env python3
import os.path
import yaml

class YamlReaderError(Exception):
    pass

class Singleton(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):

        if Singleton._instances.get(cls, None) is None:
            Singleton._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return Singleton._instances[cls]

class Configuration(dict, metaclass=Singleton):

    def __init__(self):

        super(Configuration, self).__init__({})

    def loadConfig(self, configPath=None):

        if configPath is not None:

            if os.path.exists(os.path.join(configPath)):

                with open(configPath) as file:

                    settings = yaml.full_load(file)

                    self.__dict__.update(settings)

        return self

    def mergeConfig(self, configPath=None):

        if configPath is not None:

            if os.path.exists(os.path.join(configPath)):

                with open(configPath) as file:

                    settings = yaml.full_load(file)

                    self.__dict__ = self._merge(self.__dict__, settings)

        return self

    def _merge(self, a, b):

        key = None
        # ## debug output
        # sys.stderr.write("DEBUG: %s to %s\n" %(b,a))
        try:
            if a is None or isinstance(a, str) or isinstance(a, int) or isinstance(a, float):
                # border case for first run or if a is a primitive
                a = b
            elif isinstance(a, list):
                # lists can be only appended
                if isinstance(b, list):
                    # merge lists
                    a.extend(b)
                else:
                    # append to list
                    a.append(b)
            elif isinstance(a, dict):
                # dicts must be merged
                if isinstance(b, dict):
                    for key in b:
                        if key in a:
                            a[key] = self._merge(a[key], b[key])
                        else:
                            a[key] = b[key]
                else:
                    raise YamlReaderError('Cannot merge non-dict "%s" into dict "%s"' % (b, a))
            else:
                raise YamlReaderError('NOT IMPLEMENTED "%s" into "%s"' % (b, a))
        except TypeError as  e:
            raise YamlReaderError('TypeError "%s" in key "%s" when merging "%s" into "%s"' % (e, key, b, a))
        return a

    def __getattr__(self, key):

        try:
            return self[key]
        except KeyError:
            return None

    def __setattr__(self, key, value):

        self[key] = value

    def get(self, key, default = None):

        try:
            return self[key]
        except KeyError:
            return default
