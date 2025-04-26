from typing import Optional, Any
from .model import modelsData

class AudioCategoryList:
    def __init__(self):
        self.Default = "Default"
        self.Music = "Music"
        self.Sound="Sound"
        self.Ambient="Ambient"
        self.Footsteps="Footsteps"

class AudioChangesData(modelsData):
    """
Category: Values in the class AudioCategoryList
    """
    def __init__(self,
        key:str,
        ID:str,
        FilePaths:list[str],
        Category: str,
        StreamVorbis: bool, Loomped: bool,
        UseReverb:bool,
        CustomFields: Optional[dict[str,str]] = None
    ):
        super().__init__(key)
        self.ID = ID
        self.FilePaths = FilePaths
        self.Category = Category
        self.StreamVorbis = StreamVorbis
        self.Loomped = Loomped
        self.UseReverb = UseReverb
        self.CustomFields = CustomFields