def recommend_tshirt_size(profile):
    """
    Функция для рекомендации размера футболок.
    """
    # Используем обхват талии вместо длины рукава
    chest_circumference = profile.chest_circumference
    waist_circumference = profile.waist_circumference
    height = profile.height

    # Определяем размер футболки на основе нескольких измерений
    if height < 160:
        if chest_circumference < 90 and waist_circumference < 70:
            return "XS"
        elif chest_circumference < 100 and waist_circumference < 80:
            return "S"
        elif chest_circumference < 110 and waist_circumference < 90:
            return "M"
        elif chest_circumference < 120 and waist_circumference < 100:
            return "L"
        else:
            return "XL"
    elif 160 <= height < 170:
        if chest_circumference < 90 and waist_circumference < 72:
            return "XS"
        elif chest_circumference < 100 and waist_circumference < 82:
            return "S"
        elif chest_circumference < 110 and waist_circumference < 92:
            return "M"
        elif chest_circumference < 120 and waist_circumference < 102:
            return "L"
        else:
            return "XL"
    else:
        if chest_circumference < 100 and waist_circumference < 84:
            return "S"
        elif chest_circumference < 110 and waist_circumference < 94:
            return "M"
        elif chest_circumference < 120 and waist_circumference < 104:
            return "L"
        else:
            return "XL"

def recommend_sweatshirt_size(profile):
    """
    Функция для рекомендации размера толстовки или верхней одежды.
    """
    chest_circumference = profile.chest_circumference
    waist_circumference = profile.waist_circumference
    hip_girth = profile.hip_girth
    shoulder_width = profile.shoulder_width
    height = profile.height

    # Определяем размер толстовки на основе измерений
    if height < 160:
        if chest_circumference < 90 and waist_circumference < 70 and hip_girth < 90 and shoulder_width < 40:
            return "XS"
        elif chest_circumference < 100 and waist_circumference < 80 and hip_girth < 100 and shoulder_width < 42:
            return "S"
        elif chest_circumference < 110 and waist_circumference < 90 and hip_girth < 110 and shoulder_width < 44:
            return "M"
        elif chest_circumference < 120 and waist_circumference < 100 and hip_girth < 120 and shoulder_width < 46:
            return "L"
        else:
            return "XL"
    elif 160 <= height < 170:
        if chest_circumference < 90 and waist_circumference < 72 and hip_girth < 92 and shoulder_width < 42:
            return "XS"
        elif chest_circumference < 100 and waist_circumference < 82 and hip_girth < 102 and shoulder_width < 44:
            return "S"
        elif chest_circumference < 110 and waist_circumference < 92 and hip_girth < 112 and shoulder_width < 46:
            return "M"
        elif chest_circumference < 120 and waist_circumference < 102 and hip_girth < 122 and shoulder_width < 48:
            return "L"
        else:
            return "XL"
    else:
        if chest_circumference < 100 and waist_circumference < 84 and hip_girth < 104 and shoulder_width < 46:
            return "S"
        elif chest_circumference < 110 and waist_circumference < 94 and hip_girth < 114 and shoulder_width < 48:
            return "M"
        elif chest_circumference < 120 and waist_circumference < 104 and hip_girth < 124 and shoulder_width < 50:
            return "L"
        else:
            return "XL"

def recommend_pants_size(profile):
    """
    Функция для рекомендации размера штанов.
    """
    waist_circumference = profile.waist_circumference
    hip_girth = profile.hip_girth
    pants_length = profile.pants_length

    # Определяем размер штанов на основе измерений
    if waist_circumference < 70 and hip_girth < 90 and pants_length < 100:
        return "XS"
    elif waist_circumference < 80 and hip_girth < 100 and pants_length < 105:
        return "S"
    elif waist_circumference < 90 and hip_girth < 110 and pants_length < 110:
        return "M"
    elif waist_circumference < 100 and hip_girth < 120 and pants_length < 115:
        return "L"
    else:
        return "XL"
