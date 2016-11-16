import inspect

class Analysis:
    @staticmethod
    def analyse(result, para1=1, para2=2):
        # Cache kwargs parameters
        local = locals().copy()
        argspec = inspect.getfullargspec(Analysis.analyse)
        kwargs = {name:local[name] for name in argspec.args[-len(argspec.defaults):]}
        result.parameters = kwargs