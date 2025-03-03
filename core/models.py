from django.db import models
from django.contrib.auth.models import User

class Publication(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Edition(models.Model):
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.publication.name} - {self.name}"

class Rate(models.Model):
    edition = models.ForeignKey(Edition, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=[("color", "Color"), ("bw", "Black & White")])
    position = models.CharField(max_length=20, choices=[("inside", "Inside"), ("front_page", "Front Page"), ("back_page", "Back Page")])
    rate_per_sq_cm = models.DecimalField(max_digits=10, decimal_places=2)
    effective_from = models.DateField()

    def __str__(self):
        return f"{self.edition} ({self.type}, {self.position}) - {self.rate_per_sq_cm}"

class Client(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Campaign(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name

class Coverage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField()
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    edition = models.ForeignKey(Edition, on_delete=models.CASCADE)
    headline = models.TextField()
    page = models.IntegerField()
    size_sq_cm = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    type = models.CharField(max_length=20, choices=[("color", "Color"), ("bw", "Black & White")], blank=True)
    position = models.CharField(max_length=20, choices=[("inside", "Inside"), ("front_page", "Front Page"), ("back_page", "Back Page")], blank=True)
    ave = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    is_online = models.BooleanField(default=False)

    def calculate_ave(self):
        if self.is_online:
            return self.ave
        rate = Rate.objects.filter(
            edition=self.edition, type=self.type, position=self.position,
            effective_from__lte=self.date
        ).order_by('-effective_from').first()
        if rate and self.size_sq_cm:
            return rate.rate_per_sq_cm * self.size_sq_cm
        return None

    def save(self, *args, **kwargs):
        if not self.is_online or not self.ave:
            self.ave = self.calculate_ave()
        super().save(*args, **kwargs)

class CustomFormula(models.Model):
    name = models.CharField(max_length=100)
    formula = models.TextField(help_text="Use 'ave' as variable, e.g., 'ave * 1.5'")
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name