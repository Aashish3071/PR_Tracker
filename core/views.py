from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
import csv
import pandas as pd
from .forms import CoverageForm
from .models import Coverage, Publication, Edition, Rate, Client, Campaign

def add_coverage(request):
    if request.method == 'POST':
        form = CoverageForm(request.POST)
        if form.is_valid():
            coverage = form.save(commit=False)
            coverage.user = request.user
            coverage.save()
            messages.success(request, "Coverage added successfully.")
            return redirect('coverage_list')
    else:
        form = CoverageForm()
    return render(request, 'core/add_coverage.html', {'form': form})

def coverage_list(request):
    coverages = Coverage.objects.filter(user=request.user)
    return render(request, 'core/coverage_list.html', {'coverages': coverages})

def upload_coverage(request):
    if request.method == 'POST' and 'file' in request.FILES:
        file = request.FILES['file']
        try:
            df = pd.read_excel(file)
            for _, row in df.iterrows():
                publication = Publication.objects.get_or_create(name=row['Publication'])[0]
                edition = Edition.objects.get_or_create(publication=publication, name=row['Editions'])[0]
                client = Client.objects.get_or_create(name="Sony Sports")[0]
                campaign_name = row.get('Campaign', 'Weekly Coverage')
                campaign = Campaign.objects.filter(name=campaign_name).first()
                Coverage.objects.create(
                    user=request.user,
                    client=client,
                    campaign=campaign,
                    date=row['Date'],
                    publication=publication,
                    edition=edition,
                    headline=row['Headline'],
                    page=row['Page'],
                    size_sq_cm=row.get('Size (sq cms)'),
                    type=row.get('Type', 'bw'),
                    position=row.get('Position', 'inside'),
                    is_online=row.get('Type', '').lower() == 'online',
                    ave=row.get('AVE') if row.get('Type', '').lower() == 'online' else None
                )
            messages.success(request, "Coverage data uploaded successfully.")
        except Exception as e:
            messages.error(request, f"Error uploading file: {str(e)}")
        return redirect('coverage_list')
    return render(request, 'core/upload_coverage.html')

def coverage_report(request):
    coverages = Coverage.objects.filter(user=request.user)
    if 'start_date' in request.GET:
        coverages = coverages.filter(date__gte=request.GET['start_date'])
    if 'end_date' in request.GET:
        coverages = coverages.filter(date__lte=request.GET['end_date'])

    print_coverages = coverages.filter(is_online=False)
    online_coverages = coverages.filter(is_online=True)

    if 'export' in request.GET and request.GET['export'] == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="coverage_report.csv"'
        writer = csv.writer(response)
        writer.writerow(['Sr. No.', 'Date', 'Publication', 'Edition', 'Headline', 'Page', 'Size', 'Rate', 'AVE'])
        for i, cov in enumerate(print_coverages, 1):
            rate = Rate.objects.filter(
                edition=cov.edition, type=cov.type, position=cov.position,
                effective_from__lte=cov.date
            ).order_by('-effective_from').first()
            writer.writerow([
                i, cov.date, cov.publication.name, cov.edition.name, cov.headline,
                cov.page, cov.size_sq_cm, rate.rate_per_sq_cm if rate else '', cov.ave
            ])
        writer.writerow([])
        writer.writerow(['Online Coverages'])
        writer.writerow(['Sr. No.', 'Date', 'Publication', 'Headline', 'AVE'])
        for i, cov in enumerate(online_coverages, 1):
            writer.writerow([i, cov.date, cov.publication.name, cov.headline, cov.ave])
        return response

    return render(request, 'core/report.html', {
        'print_coverages': print_coverages,
        'online_coverages': online_coverages,
        'total_ave': coverages.aggregate(models.Sum('ave'))['ave__sum'] or 0
    })