import sys
sys.path.append('./pdf_snipping_tool/models')
from pdf_snipping_tool.models.config import Config

if __name__ == '__main__':
    path: str = './config.yaml'
    config: Config = Config(path)
    print(config)
    