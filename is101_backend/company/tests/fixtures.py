from company.factories import CompanyFactory

import pytest


@pytest.fixture
def create_companies(db):
    def generate_companies(n):
        return CompanyFactory.create_batch(n)
    return generate_companies