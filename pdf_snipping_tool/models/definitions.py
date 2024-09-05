class Definitions:
    def __init__(self) -> None:
        self.__rectangles: dict[str, object] = []
        self.__options: dict[str, object] = []
    
    def set_yaml_data(self, yaml: dict[str, object]) -> None:
        self.clear()
        
        self.__rectangles = yaml['rectangles']
        self.__options = yaml['options']
    
    def clear(self) -> None:
        self.__rectangles.clear()
        self.__options.clear()
    
    @property
    def rectangles(self) -> dict[str, object]:
        return self.__rectangles
    @property
    def options(self) -> dict[str, object]:
        return self.__options