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
    page = models.IntegerField(null=True, blank=True)
    size = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Size (sq cms)")
    rate_per_sq_cm = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    type = models.CharField(max_length=20, choices=[
        ("Print", "Print"), 
        ("Online", "Online"),
        ("color", "Color"), 
        ("bw", "Black & White")
    ], default="Print")
    position = models.CharField(max_length=20, choices=[
        ("inside", "Inside"), 
        ("front_page", "Front Page"), 
        ("back_page", "Back Page")
    ], blank=True)
    ave = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    is_online = models.BooleanField(default=False)

    def calculate_ave(self):
        # For online coverage, return the existing AVE value if set
        if self.type == 'Online' or self.is_online:
            return self.ave
            
        # For print coverage, try to find a matching rate from the Rate model
        rate = Rate.objects.filter(
            edition=self.edition, 
            type=self.type if self.type in ['color', 'bw'] else 'color',
            position=self.position,
            effective_from__lte=self.date
        ).order_by('-effective_from').first()
        
        if rate and self.size:
            return rate.rate_per_sq_cm * self.size
        return None

    def save(self, *args, **kwargs):
        # Set is_online based on type for backward compatibility
        if self.type == 'Online':
            self.is_online = True
        
        # Calculate AVE if needed
        if not self.ave and (self.size and self.rate_per_sq_cm):
            # For print coverage, calculate AVE if size and rate are provided
            if not self.is_online and self.type != 'Online':
                self.ave = self.size * self.rate_per_sq_cm
            # For online coverage, AVE is required but we'll set it to 0 if not provided
            elif (self.is_online or self.type == 'Online') and not self.ave:
                # We don't auto-calculate for online, but we ensure it's not None
                pass
        
        # If AVE is still None, try to calculate from rates table
        if not self.ave:
            calculated_ave = self.calculate_ave()
            if calculated_ave is not None:
                self.ave = calculated_ave
            
        super().save(*args, **kwargs)

class CustomFormula(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    formula = models.TextField(help_text="Use variables like 'ave', 'size', 'rate', etc. Example: 'ave * 1.5' or 'size * rate * 2'")
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    AVAILABLE_VARIABLES = [
        ('ave', 'AVE (Advertising Value Equivalent)'),
        ('size', 'Size in sq cm'),
        ('rate', 'Rate per sq cm'),
        ('count', 'Number of coverages'),
        ('print_count', 'Number of print coverages'),
        ('online_count', 'Number of online coverages'),
    ]
    
    def calculate(self, coverage_data):
        """
        Calculate the result using the formula and provided coverage data
        
        Args:
            coverage_data: A dictionary containing values for variables used in the formula
            
        Returns:
            The calculated result
        """
        try:
            # Create a safe local environment with only the variables we allow
            safe_env = {}
            for var, _ in self.AVAILABLE_VARIABLES:
                if var in coverage_data:
                    safe_env[var] = coverage_data[var]
            
            # Add basic math functions
            import math
            safe_env.update({
                'sum': sum,
                'min': min,
                'max': max,
                'avg': lambda x: sum(x) / len(x) if x else 0,
                'round': round,
                'abs': abs,
                'sqrt': math.sqrt,
            })
            
            # Evaluate the formula in the safe environment
            result = eval(self.formula, {"__builtins__": {}}, safe_env)
            return result
        except Exception as e:
            return f"Error: {str(e)}"

    def __str__(self):
        return self.name

# Report Template Models
class ReportTemplate(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    template_file = models.FileField(upload_to='report_templates/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    # Field mappings stored as JSON
    field_mappings = models.JSONField(default=dict)
    
    def __str__(self):
        return self.name

class GeneratedReport(models.Model):
    template = models.ForeignKey(ReportTemplate, on_delete=models.CASCADE)
    report_file = models.FileField(upload_to='generated_reports/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    
    # Filter criteria used to generate the report
    filter_criteria = models.JSONField(default=dict)
    
    # Status of report generation
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    error_message = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Report from {self.template.name} - {self.created_at.strftime('%Y-%m-%d')}"