class PageRange:
    def __init__(self) -> None:
        self.__id: str = ''
        self.__range: dict[str, int] = {}
    
    def set_yaml_data(self, yaml: dict[str, object]) -> None:
        self.clear()
        
        self.__id = yaml['id']
        self.__range = yaml['range']
    
    def clear(self):
        self.__id = ''
        self.__range.clear()

    @property
    def id(self) -> str:
        return self.__id
    @property
    def range(self) -> dict[str, int]:
        return self.__range