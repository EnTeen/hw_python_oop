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
        """Возвращает строку сообщения."""

        return (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration:.3f} ч.; '
            f'Дистанция: {self.distance:.3f} км; '
            f'Ср. скорость: {self.speed:.3f} км/ч; '
            f'Потрачено ккал: {self.calories:.3f}.'
        )


@dataclass
class Training:
    """Базовый класс тренировки."""
    MIN_COEFF = 60
    M_IN_KM = 1000
    LEN_STEP = 0.65

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

        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories(),
        )


class Running(Training):
    """Тренировка: бег."""
    coeff_calorie_1 = 18
    coeff_calorie_2 = 20

    def get_spent_calories(self) -> float:
        return ((self.coeff_calorie_1 * self.get_mean_speed()
                 - self.coeff_calorie_2) * self.weight / self.M_IN_KM
                * (self.duration * self.MIN_COEFF)
                )


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    coeff_calorie_3 = 0.035
    coeff_calorie_4 = 0.029

    action: int
    duration: float
    weight: float
    height: float

    def get_spent_calories(self):
        return ((self.coeff_calorie_3 * self.weight
                 + (self.get_mean_speed() ** 2 // self.height)
                 * self.coeff_calorie_4 * self.weight)
                * (self.duration * self.MIN_COEFF)
                )


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    coeff_calorie_5 = 1.1
    coeff_calorie_6 = 2

    action: int
    duration: float
    weight: float
    count_pool: float
    length_pool: float

    def get_mean_speed(self):
        return (
            (self.length_pool * self.count_pool
             / self.M_IN_KM / self.duration)
        )

    def get_spent_calories(self):
        return ((self.get_mean_speed() + self.coeff_calorie_5)
                * self.coeff_calorie_6 * self.weight
                )


def read_package(workout_type: str, data: list):
    """Прочитать данные полученные от датчиков."""

    if workout_type not in ('SWM', 'RUN', 'WLK'):
        raise ValueError('Не верный тип тренировки')
    else:
        read = {
            'SWM': Swimming,
            'RUN': Running,
            'WLK': SportsWalking,
        }
        return read[workout_type](*data)


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
