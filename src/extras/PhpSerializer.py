import logging

logger = logging.getLogger(__name__)


class PhpSerializer:
    @classmethod
    def loads(cls, s: str, custom_char_lengths: dict = None):
        """
        Декодирует строку, закодированную в формате PHP-сериализации, в питоновские структуры.

        Параметры:
          s: Входная строка в формате PHP-сериализации.
          custom_char_lengths: Словарь, в котором ключ – символ, а значение – его "длина" (в байтах),
                               например, {'\n': 2}. Если символа нет в словаре, его длина определяется как
                               len(ch.encode('utf-8')).

        Возвращает:
          Разобранное значение (int, str, bool, list или dict).

        Генерирует:
          ValueError с подробным сообщением, если обнаружена ошибка синтаксиса.
        """
        if custom_char_lengths is None:
            custom_char_lengths = {}
        value, idx = cls._parse(s, 0, custom_char_lengths)
        idx = cls._skip_whitespace(s, idx)
        if idx != len(s):
            raise ValueError(f"Лишние символы после разбора на позиции {idx}: {s[idx:]}")
        return value

    @classmethod
    def dumps(cls, obj, custom_char_lengths: dict = None) -> str:
        """
        Кодирует питоновские структуры (bool, int, str, list, dict) в строку формата PHP-сериализации.

        Параметры:
          obj: Значение для сериализации.
          custom_char_lengths: Словарь, в котором ключ – символ, а значение – его "длина" (в байтах).

        Для строк вычисляется длина как сумма «байтовых длин» каждого символа с учетом custom_char_lengths.

        Возвращает:
          Строку, представляющую PHP-сериализацию объекта.

        Генерирует:
          ValueError, если тип значения не поддерживается.
        """
        if custom_char_lengths is None:
            custom_char_lengths = {}
        if isinstance(obj, bool):
            return f"b:{1 if obj else 0};"
        elif isinstance(obj, int):
            return f"i:{obj};"
        elif isinstance(obj, str):
            length = sum(cls._custom_char_length(ch, custom_char_lengths) for ch in obj)
            return f's:{length}:"{obj}";'
        elif isinstance(obj, list):
            result = f"a:{len(obj)}:{{"
            for i, value in enumerate(obj):
                result += cls.dumps(i, custom_char_lengths) + cls.dumps(value, custom_char_lengths)
            result += "}"
            return result
        elif isinstance(obj, dict):
            result = f"a:{len(obj)}:{{"
            for key, value in obj.items():
                if not isinstance(key, (int, str)):
                    raise ValueError(f"Ключи должны быть int или str, найден {type(key)} (значение: {key})")
                result += cls.dumps(key, custom_char_lengths) + cls.dumps(value, custom_char_lengths)
            result += "}"
            return result
        else:
            raise ValueError(f"Неподдерживаемый тип для сериализации: {type(obj)}")

    @staticmethod
    def _custom_char_length(ch: str, custom_char_lengths: dict) -> int:
        """
        Возвращает «длину» символа ch в байтах.

        Параметры:
          ch: Символ, для которого вычисляется длина.
          custom_char_lengths: Словарь с кастомными значениями длин.

        Если ch присутствует в custom_char_lengths, возвращается указанное значение, иначе
        возвращается len(ch.encode('utf-8')).
        """
        return custom_char_lengths.get(ch, len(ch.encode('utf-8')))

    @classmethod
    def _skip_whitespace(cls, s: str, idx: int) -> int:
        """
        Пропускает пробельные символы в строке s, начиная с позиции idx.

        Возвращает индекс первого непробельного символа.
        """
        while idx < len(s) and s[idx] in " \n\r\t":
            idx += 1
        return idx

    @classmethod
    def _parse(cls, s: str, idx: int, custom_char_lengths: dict):
        """
        Рекурсивно разбирает строку s, начиная с позиции idx, с учетом custom_char_lengths.

        Определяет тип следующего значения по первой букве ('s', 'i', 'a', 'b')
        и вызывает соответствующий парсер.

        Возвращает кортеж (разобранное значение, новый индекс).

        Генерирует ValueError, если обнаружен неожиданный символ или ошибка синтаксиса.
        """
        idx = cls._skip_whitespace(s, idx)
        if idx >= len(s):
            raise ValueError("Неожиданный конец строки при разборе данных.")
        type_char = s[idx]
        if type_char == 's':
            return cls._parse_string(s, idx, custom_char_lengths)
        elif type_char == 'i':
            return cls._parse_int(s, idx)
        elif type_char == 'a':
            return cls._parse_array(s, idx, custom_char_lengths)
        elif type_char == 'b':
            return cls._parse_bool(s, idx)
        else:
            raise ValueError(f"Неизвестный тип данных '{type_char}' на позиции {idx}. Ожидались 's', 'i', 'a' или 'b'.")

    @classmethod
    def _parse_string(cls, s: str, idx: int, custom_char_lengths: dict):
        """
        Разбирает строку в формате:
          s:<длина>:"<значение>";

        Длина определяется как сумма «байтовых длин» символов с учетом custom_char_lengths.

        Параметры:
          s: Полная строка.
          idx: Текущая позиция в строке s, с которой начинается строка.
          custom_char_lengths: Словарь с кастомными значениями длин для символов.

        Возвращает кортеж (строка, новый индекс).

        Генерирует ValueError, если формат строки нарушен или данные заканчиваются неожиданно.
        """
        start_idx = idx
        if s[idx] != 's':
            raise ValueError(f"Ожидалась метка 's' для строки на позиции {idx}, получено '{s[idx]}'.")
        idx += 1
        if idx >= len(s) or s[idx] != ':':
            raise ValueError(f"Ожидался символ ':' после 's' на позиции {idx} (начало: {start_idx}).")
        idx += 1

        # Читаем числовое значение длины до следующего ':'.
        length_start = idx
        while idx < len(s) and s[idx] != ':':
            idx += 1
        if idx >= len(s):
            raise ValueError(f"Не найден разделитель ':' для длины строки, начиная с позиции {length_start}.")
        length_str = s[length_start:idx]
        try:
            length = int(length_str)
        except Exception as e:
            raise ValueError(
                f"Неверное числовое значение длины строки '{length_str}' на позициях {length_start}-{idx}: {e}")
        idx += 1  # пропускаем ':'.
        if idx >= len(s) or s[idx] != '"':
            raise ValueError(f"Ожидалась открывающая кавычка '\"' для строкового значения на позиции {idx}.")
        idx += 1  # пропускаем открывающую кавычку.

        # Читаем символы до тех пор, пока накопленная длина (с учетом custom_char_lengths) не достигнет указанной.
        result = ""
        current_length = 0
        while current_length < length:
            if idx >= len(s):
                raise ValueError(
                    f"Неожиданный конец строки при чтении строкового значения, начиная с позиции {idx}. "
                    f"Ожидалась суммарная длина {length} байт, текущая длина {current_length}."
                )
            ch = s[idx]
            ch_len = cls._custom_char_length(ch, custom_char_lengths)
            if current_length + ch_len > length:
                raise ValueError(
                    f"Длина строки не соответствует заданной длине. На позиции {idx} символ '{ch}' с длиной {ch_len} "
                    f"приводит к превышению: {current_length} + {ch_len} > {length}."
                )
            result += ch
            current_length += ch_len
            idx += 1

        if idx >= len(s) or s[idx] != '"':
            raise ValueError(f"Ожидалась закрывающая кавычка '\"' после строкового значения на позиции {idx}.")
        idx += 1  # пропускаем закрывающую кавычку.
        if idx >= len(s) or s[idx] != ';':
            raise ValueError(f"Ожидался символ ';' после строкового значения на позиции {idx}.")
        idx += 1  # пропускаем ';'.
        return result, idx

    @classmethod
    def _parse_int(cls, s: str, idx: int):
        """
        Разбирает целое число в формате:
          i:<значение>;

        Параметры:
          s: Полная строка.
          idx: Текущая позиция, с которой начинается число.

        Возвращает кортеж (целое число, новый индекс).

        Генерирует ValueError, если формат числа нарушен.
        """
        start_idx = idx
        if s[idx] != 'i':
            raise ValueError(f"Ожидалась метка 'i' для целого числа на позиции {idx}, получено '{s[idx]}'.")
        idx += 1
        if idx >= len(s) or s[idx] != ':':
            raise ValueError(f"Ожидался символ ':' после 'i' на позиции {idx} (начало: {start_idx}).")
        idx += 1

        num_start = idx
        if idx < len(s) and s[idx] == '-':
            idx += 1
        while idx < len(s) and s[idx].isdigit():
            idx += 1
        num_str = s[num_start:idx]
        if not num_str:
            raise ValueError(f"Не найдено числовое значение для целого числа на позиции {num_start}.")
        try:
            number = int(num_str)
        except Exception as e:
            raise ValueError(f"Ошибка преобразования '{num_str}' в целое число на позициях {num_start}-{idx}: {e}")
        if idx >= len(s) or s[idx] != ';':
            raise ValueError(
                f"Ожидался символ ';' после целого числа на позиции {idx}, получено '{s[idx] if idx < len(s) else 'EOF'}'.")
        idx += 1  # пропускаем ';'.
        return number, idx

    @classmethod
    def _parse_bool(cls, s: str, idx: int):
        """
        Разбирает булево значение в формате:
          b:0; или b:1;

        Параметры:
          s: Полная строка.
          idx: Текущая позиция, с которой начинается булево значение.

        Возвращает кортеж (булево значение, новый индекс).

        Генерирует ValueError, если значение не равно '0' или '1', или если формат нарушен.
        """
        start_idx = idx
        if s[idx] != 'b':
            raise ValueError(f"Ожидалась метка 'b' для булевого значения на позиции {idx}, получено '{s[idx]}'.")
        idx += 1
        if idx >= len(s) or s[idx] != ':':
            raise ValueError(f"Ожидался символ ':' после 'b' на позиции {idx} (начало: {start_idx}).")
        idx += 1

        bool_start = idx
        while idx < len(s) and s[idx] != ';':
            idx += 1
        if idx >= len(s):
            raise ValueError(f"Не найден символ ';' для булевого значения, начиная с позиции {bool_start}.")
        bool_str = s[bool_start:idx]
        if bool_str == '1':
            value = True
        elif bool_str == '0':
            value = False
        else:
            raise ValueError(
                f"Неверное булево значение '{bool_str}' на позициях {bool_start}-{idx}. Ожидалось '0' или '1'.")
        idx += 1  # пропускаем ';'.
        return value, idx

    @classmethod
    def _parse_array(cls, s: str, idx: int, custom_char_lengths: dict):
        """
        Разбирает массив в формате:
          a:<количество элементов>:{ <ключ><значение> ... }

        Если ключи являются последовательными целыми числами (0, 1, 2, ...), возвращается список,
        иначе – словарь.

        Параметры:
          s: Полная строка.
          idx: Текущая позиция, с которой начинается массив.
          custom_char_lengths: Словарь с кастомными значениями длин для символов.

        Возвращает кортеж (массив (list или dict), новый индекс).

        Генерирует ValueError, если формат массива нарушен.
        """
        start_idx = idx
        if s[idx] != 'a':
            raise ValueError(f"Ожидалась метка 'a' для массива на позиции {idx}, получено '{s[idx]}'.")
        idx += 1
        if idx >= len(s) or s[idx] != ':':
            raise ValueError(f"Ожидался символ ':' после 'a' на позиции {idx} (начало: {start_idx}).")
        idx += 1

        count_start = idx
        while idx < len(s) and s[idx] != ':':
            idx += 1
        if idx >= len(s):
            raise ValueError(
                f"Не найден разделитель ':' после количества элементов массива, начиная с позиции {count_start}.")
        count_str = s[count_start:idx]
        try:
            count = int(count_str)
        except Exception as e:
            raise ValueError(
                f"Неверное значение количества элементов массива '{count_str}' на позициях {count_start}-{idx}: {e}")
        idx += 1  # пропускаем ':'.
        if idx >= len(s) or s[idx] != '{':
            raise ValueError(
                f"Ожидалась открывающая фигурная скобка '{{' после количества элементов массива на позиции {idx}.")
        idx += 1  # пропускаем '{'.

        items = []
        for i in range(count):
            key, idx = cls._parse(s, idx, custom_char_lengths)
            value, idx = cls._parse(s, idx, custom_char_lengths)
            items.append((key, value))

        if idx >= len(s) or s[idx] != '}':
            raise ValueError(f"Ожидалась закрывающая фигурная скобка '}}' для массива на позиции {idx}.")
        idx += 1  # пропускаем '}'.

        # Если все ключи – последовательные целые числа (0, 1, 2, ...), возвращаем список.
        if all(isinstance(key, int) for key, _ in items):
            keys = [key for key, _ in items]
            if sorted(keys) == list(range(len(items))):
                lst = [None] * len(items)
                for key, value in items:
                    lst[key] = value
                return lst, idx

        # Иначе – возвращаем словарь.
        d = {}
        for key, value in items:
            d[key] = value
        return d, idx


def decode_php_serialized(s: str):
    """
    Пробует декодировать PHP-сериализованную строку сначала с дефолтными
    настройками (newline = 1 байт), а при ошибке — повторяет с подсчётом
    newline за 2 байта.

    :param s: входная строка в формате PHP-сериализации
    :return: разобранная питоновская структура (int, str, bool, list, dict)
    :raises: Exception, если оба варианта загрузки не сработали
    """
    try:
        # Первый проход — считаем '\n' за 1 байт
        return PhpSerializer.loads(s)
    except Exception as error:
        logger.warning("PhpSerializer.loads failed with default lengths: %s. Retrying with newline=2", error)
        try:
            # Второй проход — считаем '\n' за 2 байта
            return PhpSerializer.loads(s, custom_char_lengths={'\n': 2})
        except Exception as error2:
            logger.error("PhpSerializer.loads failed again with custom newline=2: %s", error2)
            # Если нужно, можно здесь возвращать None или пустую структуру,
            # но правильнее — дать упасть вверх, чтобы ошибка не замалчивалась.
            raise


# Пример использования:
if __name__ == '__main__':
    serialized = (
        r'''a:62:{s:5:"align";s:5:"block";s:11:"form_select";s:0:"";s:9:"show_hide";s:4:"show";s:7:"any_all";s:3:"any";s:10:"hide_field";a:0:{}s:15:"hide_field_cond";a:1:{i:0;s:2:"==";}s:8:"hide_opt";a:0:{}s:10:"post_field";s:0:"";s:12:"custom_field";s:0:"";s:8:"taxonomy";s:8:"category";s:11:"exclude_cat";i:0;s:9:"read_only";i:0;s:12:"autocomplete";s:0:"";s:10:"admin_only";a:1:{i:0;s:0:"";}s:6:"unique";s:1:"1";s:10:"unique_msg";s:67:"Это значение должно быть уникальным.";s:4:"calc";s:0:"";s:8:"calc_dec";s:0:"";s:9:"calc_type";s:0:"";s:11:"is_currency";i:0;s:15:"custom_currency";i:0;s:25:"custom_thousand_separator";s:1:",";s:24:"custom_decimal_separator";s:1:".";s:15:"custom_decimals";i:2;s:18:"custom_symbol_left";s:0:"";s:19:"custom_symbol_right";s:0:"";s:17:"dyn_default_value";s:0:"";s:8:"multiple";i:0;s:7:"autocom";i:0;s:10:"conf_field";s:0:"";s:10:"conf_input";s:0:"";s:9:"conf_desc";s:0:"";s:8:"conf_msg";s:59:"Введенные значения не совпадают";s:5:"other";i:0;s:10:"in_section";s:1:"6";s:7:"prepend";s:0:"";s:6:"append";s:0:"";s:9:"auto_grow";i:0;s:9:"max_limit";i:0;s:14:"max_limit_type";s:4:"char";s:8:"min_size";s:0:"";s:15:"get_values_form";s:0:"";s:16:"get_values_field";s:0:"";s:12:"watch_lookup";a:0:{}s:21:"get_most_recent_value";s:0:"";s:26:"lookup_filter_current_user";b:0;s:4:"size";s:0:"";s:3:"max";s:0:"";s:5:"label";s:0:"";s:5:"blank";s:54:"Это поле не может быть пустым.";s:18:"required_indicator";s:1:"*";s:7:"invalid";s:43:"Телефон недействителен";s:14:"separate_value";i:0;s:14:"clear_on_focus";i:0;s:7:"classes";s:14:"frm6 frm_first";s:11:"custom_html";s:521:"<div id="frm_field_[id]_container" class="frm_form_field form-field [required_class][error_class]">
    <label for="field_[key]" id="field_[key]_label" class="frm_primary_label">[field_name]
        <span class="frm_required" aria-hidden="true">[required_label]</span>
    </label>
    [input]
    [if description]<div class="frm_description" id="frm_desc_field_[key]">[description]</div>[/if description]
    [if error]<div class="frm_error" role="alert" id="frm_error_field_[key]">[error]</div>[/if error]
</div>";s:6:"minnum";i:1;s:6:"maxnum";i:10;s:4:"step";i:1;s:6:"format";s:0:"";s:11:"placeholder";s:12:"+79008007060";s:5:"draft";i:0;}'''
    )

    # from collections import Counter
    #
    # print(Counter(serialized))

    # Вывод разобранной структуры (для наглядности используем pprint)
    import pprint

    print("Исходная строка:")
    print(serialized)
    data = PhpSerializer.loads(serialized, custom_char_lengths={'\n': 2})
    print("\nДекодированная структура:")
    pprint.pprint(data)

    # Кодирование структуры обратно в строку
    encoded = PhpSerializer.dumps(data, custom_char_lengths={'\n': 2})
    print("\nЗакодированная строка:")
    print(encoded)

    print("\nПоверка на совпадение:")
    print(serialized == encoded)
