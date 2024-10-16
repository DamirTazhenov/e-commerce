from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Product

import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Product)
def clear_product_cache_on_save(sender, instance, **kwargs):
    logger.info(f'Product cache invalidated for {instance}')
    cache.delete('product_list')


@receiver(post_delete, sender=Product)
def clear_product_cache_on_delete(sender, instance, **kwargs):
    logger.info(f'Product cache invalidated on delete for {instance}')
    cache.delete('product_list')
