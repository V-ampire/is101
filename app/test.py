from rest_framework.test import APIClient

from accounts.factories import CompanyUserAccountModelFactory

from companies.factories import EmployeeProfileFactory



def test_change_position_by_company_user():
    user = CompanyUserAccountModelFactory()
    employee = EmployeeProfileFactory()


tests_list = [
    test_change_position_by_company_user,
]


def run_tests():
    for test in tests_list:
        test()


if __name__ == "__main__":
    run_tests()