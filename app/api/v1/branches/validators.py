from rest_framework.serializers import ValidationError

from company.models import Branch, Employee


def validate_branch_to_archivate(branch_uuid):
    """
    В филиале не должно числится активных работников.
    """
    try:
        branch = Branch.objects.get(uuid=branch_uuid)
        if branch.employees.filter(status=Employee.ACTIVE).exists():
            raise ValidationError(
                'Невозможно архивировать филиал в котором числятся активные работники.'
            )
    except AttributeError: # Случай когда нет связанных работников
        pass
    except Branch.DoesNotExist:
        raise ValidationError('Филиала не существует.')
    return branch_uuid