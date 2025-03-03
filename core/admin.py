from django.contrib import admin
import pandas as pd
from .models import Publication, Edition, Rate, Client, Campaign, Coverage, CustomFormula

@admin.register(Rate)
class RateAdmin(admin.ModelAdmin):
    list_display = ('edition', 'type', 'position', 'rate_per_sq_cm', 'effective_from')

def upload_rate_sheet(modeladmin, request, queryset):
    if 'file' in request.FILES:
        file = request.FILES['file']
        df = pd.read_excel(file)
        for _, row in df.iterrows():
            publication, _ = Publication.objects.get_or_create(name=row['Publication'])
            edition, _ = Edition.objects.get_or_create(publication=publication, name=row['Edition'])
            Rate.objects.update_or_create(
                edition=edition, type=row['Type'], position=row['Position'],
                effective_from=row['Effective From'],
                defaults={'rate_per_sq_cm': row['Rate']}
            )
        modeladmin.message_user(request, "Rate sheet uploaded successfully.")

upload_rate_sheet.short_description = "Upload Rate Sheet"
admin.site.add_action(upload_rate_sheet)
admin.site.register(Publication)
admin.site.register(Edition)
admin.site.register(Client)
admin.site.register(Campaign)
admin.site.register(Coverage)
admin.site.register(CustomFormula)