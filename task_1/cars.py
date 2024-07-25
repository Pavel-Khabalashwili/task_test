def arrange_cars(car_red, car_white):
    answer = ""
    
    if (car_red > 2 * car_white) or (car_white > 2 * car_red):
        return "Нет решения"
    
    elif car_red >= car_white:
        difference = car_red - car_white
        for _ in range(difference):
            answer += "RWR"
        for _ in range(car_white- difference):
            answer += "RW"
    else:
        difference = car_white - car_red
        for _ in range(difference):
            answer += "WRW"
        for _ in range(car_red - difference):
            answer += "WR"
    
    return answer

car_red = int(input("Введите количество красных машин: "))
car_white = int(input("Введите количество белых машин: "))

print(arrange_cars(car_red, car_white))
