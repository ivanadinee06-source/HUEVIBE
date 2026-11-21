
class SearchSortEngine:

    @staticmethod
    def linear_search(data, keyword, key):
        keyword = str(keyword).lower()

        for index, item in enumerate(data):
            value = str(item.get(key, "")).lower()

            if keyword in value:
                return item

        return None

    @staticmethod
    def binary_search(data, target, key):
        left = 0
        right = len(data) - 1

        while left <= right:
            mid = (left + right) // 2
            value = str(data[mid].get(key, ""))

            if value == str(target):
                return data[mid]

            elif value < str(target):
                left = mid + 1

            else:
                right = mid - 1

        return None

    @staticmethod
    def merge_sort(data, key, reverse=False):
        if len(data) <= 1:
            return data

        mid = len(data) // 2

        left = SearchSortEngine.merge_sort(
            data[:mid], key, reverse
        )

        right = SearchSortEngine.merge_sort(
            data[mid:], key, reverse
        )

        return SearchSortEngine._merge(
            left, right, key, reverse
        )

    @staticmethod
    def _merge(left, right, key, reverse):
        result = []
        i = 0
        j = 0

        while i < len(left) and j < len(right):
            left_value = left[i][key]
            right_value = right[j][key]

            if isinstance(left_value, str):
                left_value = left_value.lower()

            if isinstance(right_value, str):
                right_value = right_value.lower()

            if reverse:
                condition = left_value >= right_value
            else:
                condition = left_value <= right_value

            if condition:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        result.extend(left[i:])
        result.extend(right[j:])

        return result

    @staticmethod
    def insertion_sort(data, key, reverse=False):
        result = data.copy()

        for i in range(1, len(result)):
            current = result[i]
            current_value = current[key]

            if isinstance(current_value, str):
                current_value = current_value.lower()

            j = i - 1

            while j >= 0:
                previous_value = result[j][key]

                if isinstance(previous_value, str):
                    previous_value = previous_value.lower()

                if reverse:
                    condition = previous_value < current_value
                else:
                    condition = previous_value > current_value

                if condition:
                    result[j + 1] = result[j]
                    j -= 1
                else:
                    break

            result[j + 1] = current

        return result
