from django.apps import AppConfig
from django.db.models.signals import post_delete


def recalculate_autonumbering_after_document_delete(sender, **kwargs):
    from autonumber.models import AutoNumber
    from documents.models import Document

    instance = kwargs['instance']
    if isinstance(instance, Document):
        AutoNumber.objects.recalculate_max_number(
            instance.selected_owner, type(instance)
        )


class DocumentsAppConfig(AppConfig):
    name = 'documents'

    def ready(self):
        post_delete.connect(
            recalculate_autonumbering_after_document_delete,
            dispatch_uid='recalculate_autonumbering_after_document_delete')
