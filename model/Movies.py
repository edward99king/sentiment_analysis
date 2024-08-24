
class Movies(object):

    def __init__(self, _id=None
                 , _primary_title=None
                 , _original_title=None
                 , _is_adult=None
                 , _start_year=None
                 , _end_year=None
                 , _runtime_minutes=None
                 , _genres=None):
        self._id = _id
        self._primary_title = _primary_title
        self._original_title = _original_title
        self._is_adult = _is_adult
        self._start_year = _start_year
        self._end_year = _end_year
        self._runtime_minutes = _runtime_minutes
        self._genres = _genres

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, _new_value):
        self._id = _new_value

    @property
    def primary_title(self):
        return self._primary_title

    @primary_title.setter
    def primary_title(self, _new_value):
        self._primary_title = _new_value

    @property
    def original_title(self):
        return self._original_title

    @original_title.setter
    def original_title(self, _new_value):
        self._original_title = _new_value

    @property
    def is_adult(self):
        return self._is_adult

    @is_adult.setter
    def is_adult(self, _new_value):
        self._is_adult = _new_value

    @property
    def is_adult(self):
        return self._is_adult

    @is_adult.setter
    def is_adult(self, _new_value):
        self._is_adult = _new_value

    @property
    def start_year(self):
        return self._start_year

    @start_year.setter
    def start_year(self, _new_value):
        self._start_year = _new_value

    @property
    def end_year(self):
        return self._end_year

    @end_year.setter
    def end_year(self, _new_value):
        self._end_year = _new_value

    @property
    def runtime_minutes(self):
        return self._runtime_minutes

    @runtime_minutes.setter
    def runtime_minutes(self, _new_value):
        self._runtime_minutes = _new_value

    @property
    def genres(self):
        return self._genres

    @genres.setter
    def genres(self, _new_value):
        self._genres = _new_value

