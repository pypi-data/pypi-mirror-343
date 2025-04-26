from typing import Optional, List
from .model import modelsData

class ObjectsBuffsData(modelsData):
    def __init__(self,
            Id:str,
            Duration: Optional[int]=0,
            BuffId: Optional[int]=None,
            IsDebuff: Optional[bool]=False,
            IconTexture: Optional[str]=None,
            IconSpriteIndex: Optional[int]=0,
            GlowColor: Optional[str]=None,
            CustomAttributes: Optional[dict[str, str]]=None,
            CustomFields: Optional[dict[str, str]]=None

        ):
        super().__init__(None)
        self.Id=Id
        self.BuffId=BuffId
        self.IconTexture=IconTexture
        self.IconSpriteIndex=IconSpriteIndex
        self.Duration=Duration
        self.IsDebuff=IsDebuff
        self.GlowColor=GlowColor
        self.CustomAttributes=CustomAttributes
        self.CustomFields=CustomFields


class ObjectsData(modelsData):
    def __init__(
            self,
            key: str,
            Name: str,
            DisplayName: str,
            Description: str,
            Type: str,
            Category: int,
            Price: Optional[int]=0, 
            Texture: Optional[str] = None,
            SpriteIndex: int = 0,
            ColorOverlayFromNextIndex: Optional[bool] = False, 
            Edibility: Optional[int] = -300,
            IsDrink: Optional[bool] = False,
            Buffs: Optional[List[ObjectsBuffsData]] = None, 
            GeodeDropsDefaultItems: bool = False,
            GeodeDrops: Optional[List[str]] = None, 
            ArtifactSpotChances: Optional[str] = None,
            CanBeGivenAsGift: bool = True, 
            CanBeTrashed: bool = True,
            ExcludeFromFishingCollection: bool = False, 
            ExcludeFromShippingCollection: bool = False,
            ExcludeFromRandomSale: bool = False, 
            ContextTags: Optional[List[str]] = None,
            CustomFields: Optional[str] = None
        ):
        
        super().__init__(key)
        # Atribuindo valores padrão para listas e outros mutáveis
        self.Name = Name
        self.DisplayName = DisplayName
        self.Description = Description
        self.Type = Type
        self.Category = Category
        self.Price = Price
        self.Texture = Texture
        self.SpriteIndex = SpriteIndex
        self.ColorOverlayFromNextIndex = ColorOverlayFromNextIndex
        self.Edibility = Edibility
        self.IsDrink = IsDrink
        self.Buffs = Buffs  # Se None, usa lista vazia
        self.GeodeDropsDefaultItems = GeodeDropsDefaultItems
        self.GeodeDrops = GeodeDrops if GeodeDrops is not None else []  # Se None, usa lista vazia
        self.ArtifactSpotChances = ArtifactSpotChances
        self.CanBeGivenAsGift = CanBeGivenAsGift
        self.CanBeTrashed = CanBeTrashed
        self.ExcludeFromFishingCollection = ExcludeFromFishingCollection
        self.ExcludeFromShippingCollection = ExcludeFromShippingCollection
        self.ExcludeFromRandomSale = ExcludeFromRandomSale
        self.ContextTags = ContextTags if ContextTags is not None else []  # Se None, usa lista vazia
        self.CustomFields = CustomFields