from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration:.3f} ч.; '
            f'Дистанция: {self.distance:.3f} км; '
            f'Ср. скорость: {self.speed:.3f} км/ч; '
            f'Потрачено ккал: {self.calories:.3f}.'
        )


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    M_IN_HR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""

    COEFF_CALORIE_1: float = 18
    COEFF_CALORIE_2: float = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        form_4 = (
            (self.COEFF_CALORIE_1 * self.get_mean_speed()
             - self.COEFF_CALORIE_2) * self.weight
        )
        return form_4 / self.M_IN_KM * self.duration * self.M_IN_HR


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    COEFF_CALORIE_1: float = 0.035
    COEFF_CALORIE_2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action,
                         duration,
                         weight,
                         )
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        form_3 = (
            (self.COEFF_CALORIE_1 * self.weight
             + (self.get_mean_speed() ** 2 // self.height)
             * self.COEFF_CALORIE_2 * self.weight)
        )
        return form_3 * self.duration * self.M_IN_HR


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    COEFF_CALORIE_1 = 1.1
    COEFF_CALORIE_2 = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float,
                 ) -> None:
        super().__init__(action,
                         duration,
                         weight,
                         )
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        form_1 = self.length_pool * self.count_pool
        return form_1 / self.M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        form_2 = self.get_mean_speed() + self.COEFF_CALORIE_1
        return form_2 * self.COEFF_CALORIE_2 * self.weight


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    dict_training = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking,
    }
    if workout_type in dict_training.keys():
        return dict_training[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
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
