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
