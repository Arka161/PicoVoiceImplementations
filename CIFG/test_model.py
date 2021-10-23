import unittest
import numpy as np
from modelCIFG import LSTM

# Set up constructor for LSTM, copied from logger during debugging.
char_to_idx = {
    "l": 0,
    "\n": 1,
    "k": 2,
    "s": 3,
    "o": 4,
    "c": 5,
    ";": 6,
    "-": 7,
    "d": 8,
    "y": 9,
    "'": 10,
    ")": 11,
    "j": 12,
    "u": 13,
    "z": 14,
    "i": 15,
    "n": 16,
    "b": 17,
    "v": 18,
    ",": 19,
    "p": 20,
    "h": 21,
    "q": 22,
    "r": 23,
    "e": 24,
    "x": 25,
    ".": 26,
    "g": 27,
    "t": 28,
    "(": 29,
    "w": 30,
    "f": 31,
    ":": 32,
    "?": 33,
    "a": 34,
    "!": 35,
    "m": 36,
    " ": 37,
}
idx_to_char = dict(map(reversed, char_to_idx.items()))

# Unit tests

# Tests for forward propagation, backward propagation, softmax (numerically stable), tanh


class unitRead(unittest.TestCase):
    def setUp(self) -> None:
        self.basics = LSTM(
            char_to_idx=char_to_idx, idx_to_char=idx_to_char, vocab_size=38
        )

    def test_forward(self) -> None:
        # 38 is the vocab size given the test vocab given above
        # 100 is the hidden units
        # Shapes must match for this unit test to pass

        test_x = np.random.randn(38, 1)
        test_h_p = np.random.randn(100, 1)
        test_c_p = np.random.randn(100, 1)

        test_z = np.random.randn(test_c_p.shape[0] + test_x.shape[0], 1)
        out, v, h, o, c, c_bar, i, f, z = self.basics.forward_step(
            test_x, test_h_p, test_c_p
        )
        self.assertEqual(out.shape, test_x.shape, "Test forward failed for y_hat")
        self.assertEqual(v.shape, test_x.shape, "Test forward failed for v")
        self.assertEqual(h.shape, test_h_p.shape, "Test forward failed for h")
        self.assertEqual(o.shape, test_h_p.shape, "Test forward failed for o")
        self.assertEqual(c.shape, test_h_p.shape, "Test forward failed for c")
        self.assertEqual(c_bar.shape, test_h_p.shape, "Test forward failed for c_bar")
        self.assertEqual(i.shape, test_h_p.shape, "Test forward failed for i")
        self.assertEqual(f.shape, test_h_p.shape, "Test forward failed for f")
        self.assertEqual(z.shape, test_z.shape, "Test forward failed for z")

    def test_tanh(self) -> None:
        test_vec = np.array([1, 2, 3, 4, 5])
        test_vec_2 = np.array([1, 1, 0, -4, 5])
        same = False

        # We obv do not want equal equal, so we check for close proximity
        if np.allclose(self.basics.tanh(test_vec), np.tanh(test_vec)) and np.allclose(
            self.basics.tanh(test_vec_2), np.tanh(test_vec_2)
        ):
            same = True
        self.assertEqual(same, True, "Test failed for tanh")

    def test_softmax(self) -> None:
        test_vec = np.array([-1, 0, 3, 5])
        same = False

        # We obv do not want equal equal, so we check for close proximity, value calculated by hand for the unit test
        if np.allclose(
            self.basics.softmax(test_vec),
            np.array([0.0021657, 0.00588697, 0.11824302, 0.87370431]),
        ):
            same = True
        self.assertEqual(same, True, "Test failed for tanh")

    def test_backward(self):
        y_hat = np.random.randn(38, 1)

        # Mock shape items
        dh_next = dc_next = c_prev = f = i = c_bar = c = i = h = o = np.random.randn(
            100, 1
        )
        test_z = np.random.randn(y_hat.shape[0] + dh_next.shape[0], 1)

        dh_prev, dc_prev = self.basics.backward_step(
            3, y_hat, dh_next, dc_next, c_prev, test_z, f, i, c_bar, c, o, h
        )
        self.assertEqual(
            dc_prev.shape, dc_next.shape, "Test backpropagation failed for dc_prev"
        )
        self.assertEqual(
            dh_prev.shape, dh_next.shape, "Test backpropagation failed for dh_next"
        )

    if __name__ == "__main__":
        unittest.main()
