from django.db import models

# Create your models here.
class BillType(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50)
    remark = models.TextField(blank=True, null=True)
    created_at=models.DateField(auto_now_add=True)
    updated_at=models.DateField(blank=True,null=True)

    def __str__(self):
        return self.name
    