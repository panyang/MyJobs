class BaseXError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class BaseX():
    """Encodes and Decodes integers using a supplied character set

    Attributes:
    number -- An integer
    encoded -- Encoded string
    character_set -- String containing character set used to encode
    """
    encoded = ""
    character_set = \
        "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    number = 0

    def _encode(self):
        """Encodes number using an arbitrary character set"""
        n = self.number
        if n == 0:
            self.encoded = self.character_set[0]
        # Quick base whatever encode algorithm
        array = []
        base = len(self.character_set)
        while n:
            remainder = n % base
            n = n // base
            array.append(self.character_set[remainder])
        array.reverse()
        self.encoded = ''.join(array)

    def _decode(self):
        """Decodes a string using an arbitrary character set"""
        base = len(self.character_set)
        strlen = len(self.encoded)
        num = 0
        i = 0
        for char in self.encoded:
            power = (strlen - (i + 1))
            num += self.character_set.index(char) * (base ** power)
            i += 1
        self.number = num

    def __str__(self):
        """Renders the encoded value as a string"""
        return self.encoded

    def __int__(self):
        """Renders the number as an integer"""
        return self.number

    def __unicode__(self):
        """Renders the encoded value as a unicode string"""
        return u'%s' % (self.encoded)

    def __init__(self, number=0, encoded="", character_set=""):
        """Create shorty object using a string or number & character set"""

        if character_set != "":
            self.character_set = character_set
        # Confirm we have a string or an integer
        if (encoded == "") and (number == 0):
            raise BaseXError('A num or string must be provided.')
        cset = set()
        # Cofirm character set contains only unique characters
        for c in character_set:
            if c in cset:
                raise BaseXError('Duplicate character in character set.')
            else:
                cset.add(c)
        # Encode or decode based on if we have a string to encode
        if encoded == "":
            self.number = number
            self._encode()
        else:
            self.encoded = encoded
            self._decode()
