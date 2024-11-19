def appearance(intervals: dict[str, list[int]]) -> int:
    def merge_intervals(intervals):
        """
        Объединяет пересекающиеся интервалы в один.
        """
        merged = []
        for start, end in zip(intervals[::2], intervals[1::2]):
            if merged and merged[-1][1] >= start:
                merged[-1][1] = max(merged[-1][1], end)
            else:
                merged.append([start, end])
        return merged

    def intersect_intervals(intervals1, intervals2):
        """
        Возвращает пересечение двух списков интервалов.
        """
        result = []
        i, j = 0, 0
        while i < len(intervals1) and j < len(intervals2):
            start1, end1 = intervals1[i]
            start2, end2 = intervals2[j]
            # Найти пересечение интервалов
            start = max(start1, start2)
            end = min(end1, end2)
            if start < end:
                result.append([start, end])
            # Двигаем указатель в списке, где интервал закончился раньше
            if end1 < end2:
                i += 1
            else:
                j += 1
        return result

    # Извлекаем интервалы
    lesson = merge_intervals(intervals["lesson"])
    pupil = merge_intervals(intervals["pupil"])
    tutor = merge_intervals(intervals["tutor"])

    # Пересечение всех интервалов
    pupil_tutor = intersect_intervals(pupil, tutor)
    lesson_pupil_tutor = intersect_intervals(lesson, pupil_tutor)

    # Считаем общее время
    total_time = sum(end - start for start, end in lesson_pupil_tutor)
    return total_time


tests = [
    {
        "intervals": {
            "lesson": [1594663200, 1594666800],
            "pupil": [
                1594663340,
                1594663389,
                1594663390,
                1594663395,
                1594663396,
                1594666472,
            ],
            "tutor": [1594663290, 1594663430, 1594663443, 1594666473],
        },
        "answer": 3117,
    },
    {
        "intervals": {
            "lesson": [1594702800, 1594706400],
            "pupil": [
                1594702789,
                1594704500,
                1594702807,
                1594704542,
                1594704512,
                1594704513,
                1594704564,
                1594705150,
                1594704581,
                1594704582,
                1594704734,
                1594705009,
                1594705095,
                1594705096,
                1594705106,
                1594706480,
                1594705158,
                1594705773,
                1594705849,
                1594706480,
                1594706500,
                1594706875,
                1594706502,
                1594706503,
                1594706524,
                1594706524,
                1594706579,
                1594706641,
            ],
            "tutor": [
                1594700035,
                1594700364,
                1594702749,
                1594705148,
                1594705149,
                1594706463,
            ],
        },
        "answer": 3577,
    },
    {
        "intervals": {
            "lesson": [1594692000, 1594695600],
            "pupil": [1594692033, 1594696347],
            "tutor": [1594692017, 1594692066, 1594692068, 1594696341],
        },
        "answer": 3565,
    },
]

if __name__ == "__main__":
    for i, test in enumerate(tests):
        test_answer = appearance(test["intervals"])
        assert (
            test_answer == test["answer"]
        ), f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'
