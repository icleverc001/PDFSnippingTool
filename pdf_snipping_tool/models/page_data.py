
class PageData:
    def __init__(self) -> None:
        self.__pages: list[dict[str, object]] = []
        self.__options: list[dict[str, object]] = []
    
    def set_yaml_data(self, yaml: dict[str, object]) -> None:
        self.clear()

        self.__pages = yaml['pages']
        self.__options = yaml['options']
    
    def clear(self) -> None:
        self.__pages.clear()
        self.__options.clear()

    @property
    def pages(self) -> list[dict[str, object]]:
        return self.__pages
    @property
    def options(self) -> list[dict[str, object]]:
        return self.__options