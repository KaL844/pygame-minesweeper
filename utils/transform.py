from utils.enum_types import AlignType


class TransformUtils:
    
    @staticmethod
    def alignAnchor(type: AlignType, x: int, y: int, width: int, height: int) -> tuple[int, int]:
        posX = x
        posY = y
        if type == AlignType.MID_CENTER: 
            posX = x - width // 2
            posY = y - height // 2
        elif type == AlignType.MID_RIGHT:
            posX = x - width
            posY = y - height // 2
        elif type == AlignType.MID_LEFT:
            posY = y - height // 2
        elif type == AlignType.TOP_CENTER:
            posX = x - width // 2
        elif type == AlignType.TOP_RIGHT:
            posX = x - width
        elif type == AlignType.BOTTOM_CENTER:
            posX = x - width // 2
            posY = y - height
        elif type == AlignType.BOTTOM_LEFT:
            posY = y - height
        elif type == AlignType.BOTTOM_RIGHT:
            posX = x - width
            posY = y - height
        return (posX, posY)

    @staticmethod
    def alignContent(type: AlignType, containerX: int, containerY: int, containerWidth: int, containerHeight: int) -> tuple[int, int]: 
        """
        Container must have TOP_LEFT anchor
        """
        posX = containerX
        posY = containerY
        if type == AlignType.MID_CENTER: 
            posX += containerWidth // 2
            posY += containerHeight // 2
        elif type == AlignType.MID_RIGHT:
            posX += containerWidth
            posY += containerHeight // 2
        elif type == AlignType.MID_LEFT:
            posY += containerHeight // 2
        elif type == AlignType.TOP_CENTER:
            posX += containerWidth // 2
        elif type == AlignType.TOP_RIGHT:
            posX += containerWidth
        elif type == AlignType.BOTTOM_CENTER:
            posX += containerWidth // 2
            posY += containerHeight
        elif type == AlignType.BOTTOM_LEFT:
            posY += containerHeight
        elif type == AlignType.BOTTOM_RIGHT:
            posX += containerWidth
            posY += containerHeight
        return (posX, posY)