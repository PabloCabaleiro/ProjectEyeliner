import unittest
from Validation.validate_configuration import ValidateConfiguration
from Objects.ResultClass import ResultClass


class ValidationTest(unittest.TestCase):
    image_list = None;
    names_list = None;

    def test_get_error(self):

        top1 = top2 = [(i,5) for i in range(30,80)]
        bot1 = bot2 = [(i,5) for i in range(30,80)]
        result1 = ResultClass(top1,bot1,3)
        mse, mae = ValidateConfiguration()._get_error(result1, top2, bot2)

        self.assertEqual(mse,0)
        self.assertEqual(mae,0)

        bot1 = top1 = [(i,10) for i in range(30,80)]
        bot2 = [(i,15) for i in range(30,80,5)]
        top2 = [(i,5) for i in range(30,80,5)]
        result1 = ResultClass(top1, bot1, 3)
        mse, mae = ValidateConfiguration()._get_error(result1, top2, bot2)

        self.assertEqual(mse,25)
        self.assertEqual(mae,5)


if __name__ == '__main__':
    unittest.main()