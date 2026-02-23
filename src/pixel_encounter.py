from os import getcwd
from pathlib import Path
from random import randint
from requests import Session

class PixelEncounter:
    def __init__(self) -> None:
        self.api = "https://app.pixelencounter.com/api"
        self.second_api = "https://app.pixelencounter.com/api/v2"
        self.data_api = " https://app.pixelencounter.com/odata"
        self.session = Session()
        self.session.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
        }

    def save_file(self, content: bytes, location: str = getcwd()) -> bool:
        with open(Path(location).joinpath(f"{randint(0, 86400)}.png"), "wb+",) as file:
            file.write(content)
        return True

    def get_monster(self, monster_id: int, size: int = 512) -> bool:
        response = self.session.get(
            f"{self.api}/basic/monsters/{monster_id}/png?size={size}").content
        return self.save_file(response)

    def get_random_monster(self, size: int = 512) -> bool:
        response = self.session.get(
            f"{self.api}/basic/monsters/random/png?size={size}").content
        return self.save_file(response)

    def get_monsters_list(self) -> bool:
        return self.session.get(f"{self.api}/basic/monsters").json()

    def get_monster_info(self, monster_id: int) -> dict:
        return self.session.get(
            f"{self.api}/basic/monsterdetails/{monster_id}").json()

    def get_monsters_list_info(
            self,
            rows: int = 10,
            order: str = "Id&desc",
            skip: int = 0,
            count: bool = True) -> dict:
        params = {
            "orderby": order,
            "skip": skip,
            "count": count
        }
        filtered_params = {
            key: value for key, value in params.items() if value is not None
        }
        return self.session.get(
            f"{self.data_api}/basic/monsterdetails?top={rows}",
            params=filtered_params).json()

    def get_monster_svg(
            self,
            size: int = 512,
            background_color: str = None,
            edge_brightness: int = 0,
            brightness_noise: int = 0,
            colored: bool = True,
            color_variations: int = 1,
            saturation: int = 1) -> bool:
        params = {
            "backgroundColor": background_color,
            "edgeBrightness": edge_brightness,
            "brightnessNoise": brightness_noise,
            "colorVariations": color_variations,
            "saturation": saturation
        }
        filtered_params = {
            key: value for key, value in params.items() if value is not None
        }
        response = self.session.get(
            f"{self.second_api}/basic/svgmonsters/image/png?colored={colored}&size={size}",
            params=params).content
        return self.save_file(response)

    def get_random_planet(
            self,
            width: int = 1080,
            height: int = 1080,
            frame: int = None) -> bool:
        params = {"frame": frame} if frame else {}
        response = self.session.get(
            f"{self.api}/basic/planets?width={width}&height={height}",
            params=params).content
        return self.save_file(response)

    def get_planet(self, seed_id: int) -> bool:
        response = self.session.get(
            f"{self.api}/basic/planets/{seed_id}").content
        return self.save_file(response)
