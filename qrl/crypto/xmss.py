# coding=utf-8
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.
from pyqrllib import pyqrllib
from pyqrllib.pyqrllib import bin2hstr, getRandomSeed, str2bin, bin2mnemonic, mnemonic2bin  # noqa
from pyqrllib.pyqrllib import XmssFast, QRLDescriptor


class XMSS(object):
    @staticmethod
    def from_extended_seed(extended_seed: bytes):
        if len(extended_seed) != 51:
            raise Exception('Extended seed should be 50 bytes long')

        descr = QRLDescriptor.fromBytes(extended_seed[0], extended_seed[1])
        if descr.getSignatureType() != pyqrllib.XMSS:
            raise Exception('Signature type nor supported')

        height = descr.getHeight()
        hash_function = descr.getHashFunction()
        tmp = XmssFast(extended_seed[2:], height, hash_function)
        return XMSS(tmp)

    @staticmethod
    def from_height(tree_height: int):
        seed = getRandomSeed(48, '')
        return XMSS(XmssFast(seed, tree_height, pyqrllib.SHAKE_128))

    def __init__(self, _xmssfast):
        """
        :param
        tree_height: height of the tree to generate. number of OTS keypairs=2**tree_height
        :param _xmssfast:

        >>> from qrl.crypto.doctest_data import *
        >>> tmp = XMSS.from_extended_seed(xmss_test_eseed1)
        >>> tmp.height
        4

        >>> from qrl.crypto.doctest_data import *
        >>> tmp = XMSS.from_extended_seed(xmss_test_eseed1)
        >>> tmp._xmss.getSignatureSize()
        2308

        >>> from qrl.crypto.doctest_data import *
        >>> tmp = XMSS.from_extended_seed(xmss_test_eseed1)
        >>> bin2hstr( tmp._xmss.getPK() )
        '0002eb0372d56b886645e7c036b480be95ed97bc431b4e828befd4162bf432858df83191da3442686282b3d5160f25cf162a517fd2131f83fbf2698a58f9c46afc5d'

        >>> from qrl.crypto.doctest_data import *
        >>> tmp = XMSS.from_extended_seed(xmss_test_eseed1)
        >>> len( tmp._xmss.getPK() )
        66

        >>> from qrl.crypto.doctest_data import *
        >>> tmp = XMSS.from_extended_seed(xmss_test_eseed1)
        >>> bin2hstr( tmp._xmss.getSK() ) == xmss_sk_expected1
        True

        >>> from qrl.crypto.doctest_data import *
        >>> tmp = XMSS.from_extended_seed(xmss_test_eseed1)
        >>> bin2hstr( tmp._xmss.getRoot() )
        'eb0372d56b886645e7c036b480be95ed97bc431b4e828befd4162bf432858df8'

        >>> from qrl.crypto.doctest_data import *
        >>> tmp = XMSS.from_extended_seed(xmss_test_eseed1)
        >>> bin2hstr( tmp._xmss.getPKSeed() )
        '3191da3442686282b3d5160f25cf162a517fd2131f83fbf2698a58f9c46afc5d'

        >>> from qrl.crypto.doctest_data import *
        >>> tmp = XMSS.from_extended_seed(xmss_test_eseed1)
        >>> tmp._xmss.getIndex()
        0

        >>> from qrl.crypto.doctest_data import *
        >>> tmp = XMSS.from_extended_seed(xmss_test_eseed1)
        >>> bin2hstr( tmp._xmss.getSKSeed() )
        'eda313c95591a023a5b37f361c07a5753a92d3d0427459f34c7895d727d62816'

        >>> from qrl.crypto.doctest_data import *
        >>> tmp = XMSS.from_extended_seed(xmss_test_eseed1)
        >>> bin2hstr( tmp._xmss.getSKPRF() )
        'b3aa2224eb9d823127d4f9f8a30fd7a1a02c6483d9c0f1fd41957b9ae4dfc63a'

        >>> from qrl.crypto.doctest_data import *
        >>> tmp = XMSS.from_extended_seed(xmss_test_eseed1)
        >>> bin2hstr(tmp._xmss.getAddress())
        '0002e4b1da78e5bc64632506135301f67b22bebeea46f74c37eb5379bd7602a8e0d1b53ff966'
        """
        self._xmss = _xmssfast

    @property
    def height(self):
        return self._xmss.getHeight()

    @property
    def _sk(self):
        """
        >>> from qrl.crypto.doctest_data import *
        >>> tmp = XMSS.from_extended_seed(xmss_test_eseed1)
        >>> len(tmp._sk)
        132

        >>> from qrl.crypto.doctest_data import *
        >>> tmp = XMSS.from_extended_seed(xmss_test_eseed1)
        >>> bin2hstr(tmp._sk) == xmss_sk_expected1
        True

        >>> from qrl.crypto.doctest_data import *
        >>> tmp = XMSS.from_extended_seed(xmss_test_eseed2)
        >>> bin2hstr(tmp._sk) == xmss_sk_expected2
        True
        """
        return bytes(self._xmss.getSK())

    @property
    def pk(self):
        """
        >>> from qrl.crypto.doctest_data import *
        >>> tmp = XMSS.from_extended_seed(xmss_test_eseed1)
        >>> bin2hstr(tmp.pk) == xmss_pk_expected1
        True
        >>> from qrl.crypto.doctest_data import *
        >>> tmp = XMSS.from_extended_seed(xmss_test_eseed1)
        >>> bin2hstr(tmp.pk) == xmss_pk_expected2
        True
        """
        return bytes(self._xmss.getPK())

    @property
    def number_signatures(self) -> int:
        """
        Returns the number of signatures in the XMSS tree
        :return:
        :rtype:

        >>> from qrl.crypto.doctest_data import *
        >>> tmp = XMSS.from_extended_seed(xmss_test_eseed1)
        >>> tmp.number_signatures
        16
        >>> from qrl.crypto.doctest_data import *
        >>> tmp = XMSS.from_extended_seed(xmss_test_eseed1)
        >>> tmp.number_signatures
        16
        """
        return self._xmss.getNumberSignatures()

    @property
    def remaining_signatures(self):
        """
        Returns the number of remaining signatures in the XMSS tree
        :return:
        :rtype:

        >>> from qrl.crypto.doctest_data import *
        >>> tmp = XMSS.from_extended_seed(xmss_test_eseed1)
        >>> tmp.remaining_signatures
        16
        >>> from qrl.crypto.doctest_data import *
        >>> tmp = XMSS.from_extended_seed(xmss_test_eseed1)
        >>> tmp.remaining_signatures
        16
        """
        return self._xmss.getRemainingSignatures()

    @property
    def mnemonic(self) -> str:
        """
        :return:
        :rtype:

        >>> from qrl.crypto.doctest_data import *
        >>> tmp = XMSS.from_extended_seed(hstr2bin(xmss_mnemonic_seed1))
        >>> tmp.mnemonic == xmss_mnemonic_test1
        True
        >>> from qrl.crypto.doctest_data import *
        >>> tmp = XMSS.from_extended_seed(hstr2bin(xmss_mnemonic_seed2))
        >>> tmp.mnemonic == xmss_mnemonic_test2
        True
        >>> from qrl.crypto.doctest_data import *
        >>> tmp = XMSS.from_extended_seed(mnemonic2bin(xmss_mnemonic_test1))
        >>> tmp.mnemonic == xmss_mnemonic_test1
        True
        >>> from qrl.crypto.doctest_data import *
        >>> tmp = XMSS.from_extended_seed(mnemonic2bin(xmss_mnemonic_test2))
        >>> tmp.mnemonic == xmss_mnemonic_test2
        True
        """
        return bin2mnemonic(self._xmss.getExtendedSeed())

    @property
    def address(self) -> bytes:
        return bytes(self._xmss.getAddress())

    @property
    def ots_index(self) -> int:
        """
        :return:
        :rtype:

        >>> from qrl.crypto.doctest_data import *
        >>> tmp = XMSS.from_extended_seed(xmss_test_eseed1)
        >>> tmp.ots_index
        0
        >>> from qrl.crypto.doctest_data import *
        >>> tmp = XMSS.from_extended_seed(xmss_test_eseed1)
        >>> tmp.ots_index
        0
        >>> from qrl.crypto.doctest_data import *
        >>> tmp = XMSS.from_extended_seed(xmss_test_eseed1)
        >>> s = tmp.sign(str2bin("test"))
        >>> tmp.ots_index
        1
        """
        return self._xmss.getIndex()

    def set_ots_index(self, new_index):
        """
        :return:
        :rtype:

        >>> from qrl.crypto.doctest_data import *
        >>> xmss = XMSS.from_extended_seed(xmss_test_eseed1)
        >>> xmss.set_ots_index(1)
        >>> xmss.ots_index
        1
        >>> from qrl.crypto.doctest_data import *
        >>> xmss = XMSS.from_extended_seed(xmss_test_eseed1)
        >>> xmss.set_ots_index(10)
        >>> xmss.ots_index
        10
        """
        self._xmss.setIndex(new_index)

    @property
    def hexseed(self) -> str:
        """
        :return:
        :rtype:

        >>> from qrl.crypto.doctest_data import *
        >>> tmp = XMSS.from_extended_seed(xmss_test_eseed1)
        >>> tmp.hexseed
        '0002000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'

        >>> tmp = XMSS.from_extended_seed(xmss_test_eseed2)
        >>> tmp.hexseed
        '0002010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101'
        """
        return bin2hstr(self._xmss.getExtendedSeed())

    @property
    def seed(self):
        """
        :return:
        :rtype:

        >>> from qrl.crypto.doctest_data import *
        >>> tmp = XMSS.from_extended_seed(xmss_test_eseed1)
        >>> bin2hstr( tmp.seed )
        '000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'

        >>> from qrl.crypto.doctest_data import *
        >>> tmp = XMSS.from_extended_seed(xmss_test_eseed2)
        >>> bin2hstr( tmp.seed )
        '010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101'
        """
        return self._xmss.getSeed()

    def sign(self, message: bytes) -> bytes:
        """
        :param message:
        :return:

        >>> from qrl.crypto.doctest_data import *
        >>> tmp = XMSS.from_extended_seed(xmss_test_eseed1)
        >>> bin2hstr(tmp.sign(str2bin("test_message"))) == xmss_sign_expected1
        True
        >>> from qrl.crypto.doctest_data import *
        >>> tmp = XMSS.from_extended_seed(xmss_test_eseed2)
        >>> bin2hstr(tmp.sign(str2bin("test_message"))) == xmss_sign_expected2
        True
        """
        return bytes(self._xmss.sign(message))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
