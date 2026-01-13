class PrivateKey:
    def __init__(self, key: bytes):
        self._key: bytes = key
        # TODO set public key
        self.public_key: PublicKey = None

    def as_bytes(self) -> bytes:
        return self._key


class Point:
    def __init__(self, x, y):
        self.x = x % P
        self.y = y % P

    def __repr__(self):
        return f'Point({self.x},{self.y})'

    def __eq__(self, other: any) -> bool:
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        return False


class PublicKey(Point):
    def __init__(self, key: bytes):
        # TODO parse key in compressed (02,03) or uncompressed (04) format
        x, y = self._parse_key(key)
        super().__init__(x, y)

    def _parse_key(self, key: bytes):
        # TODO parse key in compressed (02,03) or uncompressed (04) format
        return None, None


# secp256k1: y^2 = x^3 + 7

# prime modulus
P = 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f

# order (number of points on curve)
N = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141

# generator point
G = Point(
    0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798,
    0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8,
)


def modinv(scalar: int, mod: int) -> int:
    # https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
    t = 0
    r = mod
    newt = 1
    newr = scalar

    while newr != 0:
        q = r // newr
        (t, newt) = (newt, t - q * newt)
        (r, newr) = (newr, r - q * newr)

    if r > 1:
        raise ValueError(f'{scalar} mod {mod} is not invertible')

    if t < 0:
        t += mod

    return t


def modinv_n(scalar: int) -> int:
    # scalars like private keys are chosen from [1, n-1], so we need to use mod N.
    return modinv(scalar, N)


def modinv_p(coordinate: int) -> int:
    # point coordinates use mod P
    return modinv(coordinate, P)


def ecdouble(p: Point) -> Point:
    # From a visual perspective, to "double" a point you draw a tangent to the
    # curve at the given point, then find the point on the curve this line
    # intersects (there will only be one), then take the reflection of this
    # point across the x-axis.
    s = 3*p.x**2 * modinv_p(2*p.y)
    x = s**2 - 2*p.x
    y = s*(p.x - x) - p.y
    return Point(x, y)


def ecadd(p1: Point, p2: Point) -> Point:
    # TODO implement
    pass


def ecmul(p: Point, scalar: int) -> Point:
    # TODO implement
    pass
