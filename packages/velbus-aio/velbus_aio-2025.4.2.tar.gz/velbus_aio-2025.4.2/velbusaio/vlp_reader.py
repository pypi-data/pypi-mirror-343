from bs4 import BeautifulSoup


class vlpFile:

    def __init__(self, file_path) -> None:
        self._file_path = file_path
        self._soup = None
        self._modules = {}
        self._read()
        self._parse()
        print(self._modules)

    def _read(self) -> None:
        with open(self._file_path) as file:
            xml_content = file.read()
        self._soup = BeautifulSoup(xml_content, "xml")

    def _parse(self) -> None:
        for module in self._soup.find_all("Module"):
            self._parse_module(module)

    def _parse_module(self, module) -> None:
        mod_info = {}
        mod_info["name"] = module.find("Caption").get_text()
        mod_info["addresses"] = module["address"]
        mod_info["build"] = module["build"]
        mod_info["serial"] = module["serial"]
        mod_info["build"] = module["build"]
        mod_info["type"] = module["type"]
        memory = module.find("Memory")
        mod_info["memory"] = memory.get_text()
        self._modules[mod_info["addresses"]] = mod_info
