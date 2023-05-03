from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    MESSAGE = ('Тип тренировки: {training_type}; '
               'Длительность: {duration:.3f} ч.; '
               'Дистанция: {distance:.3f} км; '
               'Ср. скорость: {speed:.3f} км/ч; '
               'Потрачено ккал: {calories:.3f}.')

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return self.MESSAGE.format(**asdict(self))


@dataclass
class Training:
    """Базовый класс тренировки."""
    M_IN_KM = 1_000
    LEN_STEP = 0.65
    H_IN_M = 60

    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Method has not been implemented yet.')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        spent_calories = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                          * self.get_mean_speed()
                          + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight
                          / self.M_IN_KM * (self.duration * self.H_IN_M))
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    WEIGHT_MULTIPLIER_1 = 0.035
    WEIGHT_MULTIPLIER_2 = 0.029
    CM_IN_M = 100
    KMPH_IN_MPS = 0.278

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        spent_calories = ((self.WEIGHT_MULTIPLIER_1 * self.weight
                          + ((self.get_mean_speed() * self.KMPH_IN_MPS)**2
                             / (self.height / self.CM_IN_M))
                          * self.WEIGHT_MULTIPLIER_2 * self.weight)
                          * (self.duration * self.H_IN_M))
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    MEAN_SPEED_SHIFT = 1.1
    MEAN_SPEED_MULTIPLIER = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = (self.length_pool * self.count_pool
                      / self.M_IN_KM / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        spent_calories = ((self.get_mean_speed() + self.MEAN_SPEED_SHIFT)
                          * self.MEAN_SPEED_MULTIPLIER * self.weight
                          * self.duration)
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_class_type: dict[str, type[Training]] = {'SWM': Swimming,
                                                     'RUN': Running,
                                                     'WLK': SportsWalking}
    if workout_type in workout_class_type:
        return workout_class_type[workout_type](*data)
    raise ValueError('There is no such workout_type.')


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
