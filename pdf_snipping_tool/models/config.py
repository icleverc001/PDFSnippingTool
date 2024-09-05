from pathlib import Path
from page_data import PageData
from definitions import Definitions
import yaml
import pprint

class Config:
    def __init__(self, config_path: str) -> None:
        self.__path: str = ''
        self.__pdf_path: str = ''
        self.__page_data: PageData = None
        self.__definitions: Definitions = None
        
        self.load(config_path)
        
    def load(self, config_path: str):
        self.__clear()
        
        self.__path: str = config_path
        file: Path = Path(config_path)
        if not file.exists():
            return
        with file.open(mode='r', encoding='utf-8') as yml:
            config: dict[str, object] = yaml.safe_load(yml)
            self.__pdf_path = config['pdf_path']
            self.__page_data = config['page_data']
            self.__definitions = config['definitions']

    def __clear(self):
        self.__path = ''
        self.__pdf_path = ''
        self.__page_data = None
        self.__definitions = None
        
    @property
    def config_path(self) -> str:
        return self.__path
    @property
    def pdf_path(self) -> str:
        return self.__pdf_path
    @property
    def data(self) -> PageData:
        return self.__page_data
    @property
    def definitions(self) -> Definitions:
        return self.__definitions
    