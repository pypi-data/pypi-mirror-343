from .model import modelsData

class AnimationDescriptionsData(modelsData):
    def __init__(
        self,
        key: str,
        animation: list[list[int]]
    ):
        super().__init__(key)
        self.animation = animation

    def getJson(self) -> str:
        return "/".join(" ".join(map(str, sublista)) for sublista in self.animation)
