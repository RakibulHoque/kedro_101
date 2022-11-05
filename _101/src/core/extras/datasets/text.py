from kedro.extras.datasets.text import TextDataSet
from kedro.io.core import (
    get_filepath_str
)

class FOPathTextDataSet(TextDataSet):
    def _load(self) -> str:
        load_path = get_filepath_str(self._get_load_path(), self._protocol)
        return load_path
