class BaseAdapter:
    def connect(self, endpoint):
        raise NotImplementedError("Subclasses must implement connect()")
