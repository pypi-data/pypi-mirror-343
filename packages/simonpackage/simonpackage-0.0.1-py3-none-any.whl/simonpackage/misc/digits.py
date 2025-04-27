import datetime
import math

__all__ = ["len_digit", "factors", "fullFactors", "twoFactors", "isPrime", "primeFactors",
                                                                           "P", "C"]


def len_digit(n: int, base: int = 10):
    """
    to count the length of an integer
    :param n: a digit number, positive or negative or zero
    :param base: the base of the number, default to 10
    :return: the length of the integer
    """
    an = abs(n)
    quotient = an // base
    length = 1
    while quotient != 0:
        length += 1
        quotient //= base
    return length


def isPrime(num: int) -> bool:
    """
    to deicide if a number is a prime number
    :param num:
    :return:
    """
    return not bool(factors(num))


def primeFactors(num: int) -> list:
    """
    to find all the prime factors of a number
    :param num:
    :return:
    """
    return [factor for factor in factors(num) if isPrime(factor)]


def factors(num: int) -> list:
    """
    求一个整数的所有因数
    :param num:
    :return:
    """
    factors = []
    for i in range(2, (num // 2) + 1):
        if num % i == 0:
            factors.append(i)
    return factors


def twoFactors(num: int) -> list:
    """
    将一个整数分解为两个因数的方法，返回一个元组的列表
    :param num:
    :return:
    """
    facs = factors(num)
    two_factors = []
    if facs:
        for i in range(len(facs) // 2):
            first = 0 + i
            second = -1 - i
            two_factors.append((facs[first], facs[second]))
    return two_factors


def fullFactors(num: int) -> list:
    """
    get the full factorization of a number
    :param num:
    :return:
    """
    total_factors = primeFactors(num)
    product = math.prod(total_factors)
    res = num // product
    if isPrime(res):  # walrus operator
        if res != 1:
            total_factors.append(res)
        return sorted(total_factors)
    else:
        total_factors.extend(fullFactors(res))  # recursion
        return sorted(total_factors)


def P(m: int, n: int) -> int:
    """
    the number of permutations without replacement
    :param m:
    :param n:
    :return:
    """
    if n < 1:
        raise ValueError('n must be positive')
    else:
        return math.prod(range(1, m + 1)[-1 * n:])


def C(m, n) -> int:
    if n < 1:
        raise ValueError('n must be positive')
    else:
        numerator = math.prod(range(1, m + 1)[-1 * n:])
        denominator = math.prod(range(1, n + 1))
        return numerator // denominator


class GetIdCardInformation:
    def __init__(self, id: str):
        self.id = id
        self.birth_year = int(self.id[6:10])
        self.birth_month = int(self.id[10:12])
        self.birth_day = int(self.id[12:14])

    def get_birthday(self):
        # 通过身份证号获取出生日期
        birthday = "{0}-{1}-{2}".format(self.birth_year, self.birth_month, self.birth_day)
        return birthday

    def get_sex(self):
        # 男生：1 女生：0
        num = int(self.id[16:17])
        if num % 2 == 0:
            return "女"
        else:
            return "男"

    def get_age(self):
        # 获取年龄
        now = (datetime.datetime.now() + datetime.timedelta(days=1))
        year = now.year
        month = now.month
        day = now.day

        if year == self.birth_year:
            return 0
        else:
            if self.birth_month > month or (self.birth_month == month and self.birth_day > day):
                return year - self.birth_year - 1
            else:
                return year - self.birth_year


if __name__ == '__main__':
    # print(fullFactors(123456780))
    # print(primeFactors(123456780))
    print(P(6, 2))
    # print(C(6, 2))
    print(factors(240))
