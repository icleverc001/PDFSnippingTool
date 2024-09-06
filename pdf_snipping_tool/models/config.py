from pathlib import Path
from page_data import PageData
from definitions import Definitions
import yaml
import pprint

class Config:
    def __init__(self) -> None:
        # self.__config = {}
        self.__path: str = ''
        self.__pdf_path: str = ''
        self.__outputfile: dict[str, bool] = {}
        self.__page_data: PageData = PageData()
        self.__definitions: Definitions = Definitions()
        self.__colors: dict[str, object] = {}
        
    def load(self, config_path: str):
        self.clear()
        
        self.__path: str = config_path
        file: Path = Path(config_path)
        if not file.is_file():
            return
        with file.open(mode='r', encoding='utf-8') as yml:
            config: dict[str, object] = yaml.safe_load(yml)
            self.__pdf_path = config['pdf_path']
            self.__outputfile = config['outputfile']
            self.__page_data.set_yaml_data(config['page_data'])
            self.__definitions.set_yaml_data(config['definitions'])
            self.__colors = config['colors']

    def clear(self):
        self.__path = ''
        self.__pdf_path = ''
        self.__outputfile.clear()
        self.__page_data.clear()
        self.__definitions.clear()
        self.__colors.clear()
        
    @property
    def config_path(self) -> str:
        return self.__path
    @property
    def pdf_path(self) -> str:
        return self.__pdf_path
    @property
    def outputfile(self) -> dict[str, bool]:
        return self.__outputfile
    @property
    def data(self) -> PageData:
        return self.__page_data
    @property
    def definitions(self) -> Definitions:
        return self.__definitions
    @property
    def colors(self) -> dict[str, object]:
        return self.__colors
    