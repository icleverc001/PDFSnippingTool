
class PageData:
    def __init__(self, yaml: dict[str, object]) -> None:
        self.__pages: list[dict[str, object]] = []
        self.__options: list[dict[str, object]] = []
        self.set_yaml_data(yaml)
    
    def set_yaml_data(self, yaml: dict[str, object]) -> None:
        self.__clear()

        self.__pages = yaml['pages']
        self.__options = yaml['options']
    
    def __clear(self) -> None:
        self.__pages.clear()
        self.__options.clear()

    @property
    def pages(self):
        return self.__pages
    @property
    def options(self):
        return self.__options