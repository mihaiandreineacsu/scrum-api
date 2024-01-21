"""
Abstract Views for the position APIs.
"""
from position.position_exception import PositionException
from rest_framework import viewsets, status
from django.db.models import Max
from django.db import IntegrityError


class PositionViewSet(viewsets.ModelViewSet):
    """Abstract View for manage position APIs."""

    class Meta:
        abstract = True

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        new_position = request.data.pop("position", None)
        parent = getattr(instance, instance.parent_attribute)
        new_parent = request.data.pop(instance.parent_attribute, (parent.id if parent is not None else None))

        change_parent = new_parent != (parent.id if parent is not None else None)
        change_position = new_position is not None and new_position != instance.position

        try:
            if change_parent:
                # Using _meta to get the related model for instance parent_attribute
                parent_model = instance._meta.get_field(instance.parent_attribute).related_model
                max_position = type(instance).objects.filter(**{instance.parent_attribute: new_parent}).aggregate(Max("position"))["position__max"]
                max_position = (max_position or 0) + 1
                new_parent_instance = parent_model.objects.get(id=new_parent)
                type(instance).swap_parent(instance=instance, new_parent=new_parent_instance, new_position=max_position)

            if change_position:
                new_position = int(new_position)
                target_instance = type(instance).objects.get(**{instance.parent_attribute: new_parent}, position=new_position)
                type(instance).swap_positions(instance1=instance, instance2=target_instance)
        except ValueError as e:
            raise PositionException("Invalid value type", status.HTTP_400_BAD_REQUEST, e)
        except IntegrityError as e:
            raise PositionException("Request did not end successfully", status.HTTP_409_CONFLICT, e)
        except parent_model.DoesNotExist:
            type(instance).swap_parent(instance=instance, new_parent=None, new_position=max_position)
        except type(instance).DoesNotExist as e:
            raise PositionException("Bad Request", status.HTTP_404_NOT_FOUND, e)
        return super().update(request, *args, **kwargs)
