class InfoMessage():
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Получить строку сообщения с данными о тренировке."""
        text: str = (f'Тип тренировки: {self.training_type}; '
                     f'Длительность: {self.duration:.3f} ч.; '
                     f'Дистанция: {self.distance:.3f} км; '
                     f'Ср. скорость: {self.speed:.3f} км/ч; '
                     f'Потрачено ккал: {self.calories:.3f}.'
                     )
        return text


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65  # расстояние одного шага в метрах
    M_IN_KM: float = 1000   # константа для перевода значений из м в км
    H_IN_MIN: float = 60    # константа для перевода значений из ч в мин

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action        # число действий за троенировку
        self.duration = duration    # длительность тренировки
        self.weight = weight        # вес спортсмена

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed: float = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        msg = InfoMessage(self.__class__.__name__,
                          self.duration,
                          self.get_distance(),
                          self.get_mean_speed(),
                          self.get_spent_calories())
        return msg


class Running(Training):
    """Тренировка: бег."""
    cof_cal_1: float = 18  # коэффициент 1 для формулы
    cof_cal_2: float = 20  # коэффициент 2 для формулы

    def get_spent_calories(self) -> float:
        spent_calories: float = (Running.cof_cal_1
                                 * self.get_mean_speed()
                                 - Running.cof_cal_2) \
            * self.weight / self.M_IN_KM \
            * self.duration * self.H_IN_MIN
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    cof_cal_1: float = 0.035  # коэффициент 1 для формулы
    cof_cal_2: float = 0.029  # коэффициент 2 для формулы

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        spent_calories: float = (SportsWalking.cof_cal_1 * self.weight
                                 + (self.get_mean_speed() ** 2 // self.height)
                                 * SportsWalking.cof_cal_2
                                 * self.weight) * self.duration * self.H_IN_MIN
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38         # расстояние одного гребка в метрах
    cof_cal_1: float = 1.1  # коэффициент 1 для формулы
    cof_cal_2: float = 2    # коэффициент 2 для формулы

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,  # длина бассейна
                 count_pool: float    # количество переплытых бассейнов
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        self.mean_speed: float = self.length_pool * \
            self.count_pool / self.M_IN_KM / self.duration
        return self.mean_speed

    def get_spent_calories(self) -> float:
        self.spent_calories: float = (self.get_mean_speed(
        ) + Swimming.cof_cal_1) * Swimming.cof_cal_2 * self.weight
        return self.spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_dict = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    training = training_dict[workout_type](*data)
    return training


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    msg = info.get_message()
    print(msg)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180])
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
