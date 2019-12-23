import os

from compare_directories import compare_directories


def test_compare():

    compare_directories('srcdir', 'dstdir')


def test_compare_and_copy():

    assert not os.path.exists('dstdir/file_2.bin')
    assert not os.path.exists('dstdir/file_3.wav')

    compare_directories('srcdir', 'dstdir', copy_source=True)

    assert os.path.exists('dstdir/file_2.bin')
    assert os.path.exists('dstdir/file_3.wav')

    os.remove('dstdir/file_2.bin')
    os.remove('dstdir/file_3.wav')

    compare_directories('srcdir', 'dstdir', copy_dest=True)

    assert os.path.exists('srcdir/file_1.txt')

    os.remove('srcdir/file_1.txt')
