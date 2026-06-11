import json
import random
from datetime import datetime
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from .models import PlasticType, CollectionCenter, WasteSubmission, RecyclingData, DataMiningReport
from django.db.models import Sum, Count

def index(request):
    """Main dashboard"""
    total_submissions = WasteSubmission.objects.count()
    total_weight = sum(s.weight_kg for s in WasteSubmission.objects.all()) or 0
    recycled_count = WasteSubmission.objects.filter(status='recycled').count()
    co2_saved = total_weight * 2.5
    centers = CollectionCenter.objects.filter(is_active=True).count()
    context = {
        'total_submissions': total_submissions,
        'total_weight': round(total_weight, 2),
        'recycled_count': recycled_count,
        'co2_saved': round(co2_saved, 2),
        'active_centers': centers,
    }
    return render(request, 'index.html', context)


def submit_waste(request):
   from django.shortcuts import render, redirect
from django.contrib import messages
from .models import PlasticType, CollectionCenter, WasteSubmission


def submit_waste(request):
    # Auto-populate Plastic Types
    if not PlasticType.objects.exists():
        PlasticType.objects.get_or_create(
            id=1,
            defaults={
                "code": "PET",
                "name": "water bottle",
                "description": "Polyethylene Terephthalate"
            }
        )
        PlasticType.objects.get_or_create(
            id=2,
            defaults={
                "code": "HDPE",
                "name": "milk jug",
                "description": "High-Density Polyethylene"
            }
        )
        PlasticType.objects.get_or_create(
            id=3,
            defaults={
                "code": "PVC",
                "name": "shampoo bottle",
                "description": "Polyvinyl Chloride"
            }
        )
        PlasticType.objects.get_or_create(
            id=4,
            defaults={
                "code": "LDPE",
                "name": "Plastic Bag",
                "description": "Low-Density Polyethylene"
            }
        )
        PlasticType.objects.get_or_create(
            id=5,
            defaults={
                "code": "PP",
                "name": "yogurt cup",
                "description": "Polypropylene"
            }
        )
        PlasticType.objects.get_or_create(
            id=6,
            defaults={
                "code": "PS",
                "name": "foam cup",
                "description": "Polystyrene"
            }
        )

    # Auto-populate Collection Centers
    if not CollectionCenter.objects.exists():
        CollectionCenter.objects.get_or_create(
            id=1,
            defaults={
                "name": "Downtown Recycling Hub",
                "city": "Mumbai",
                "state": "Maharashtra",
                "address": "123 Main St",
                "contact": "9876543210"
            }
        )

        CollectionCenter.objects.get_or_create(
            id=2,
            defaults={
                "name": "Northside Eco Center",
                "city": "Mumbai",
                "state": "Maharashtra",
                "address": "456 North Ave",
                "contact": "9876543211"
            }
        )

    plastic_types = PlasticType.objects.all()
    collection_centers = CollectionCenter.objects.all()

    if request.method == "POST":
        try:
            # 1. Pull the IDs from the form submission
            p_id = request.POST.get("plastic_type_id")
            c_id = request.POST.get("center_id")
            
            # 2. Check if a center wasn't selected or database is empty
            if not c_id:
                messages.error(request, "Please select a valid Collection Center.")
                return redirect(request.path)
                
            # 3. Fallback: If your database somehow lost its records, auto-create a fallback center
            if not CollectionCenter.objects.exists():
                CollectionCenter.objects.get_or_create(id=1, defaults={"name": "Downtown Recycling"})
                c_id = 1 # Force look up the entry we just made
            
            # 4. Safely pull objects from database
            plastic_type = PlasticType.objects.get(id=p_id)
            
            try:
                center = CollectionCenter.objects.get(id=c_id)
            except CollectionCenter.DoesNotExist:
                # If the exact ID isn't found, fall back to the first available center in your database
                center = CollectionCenter.objects.first()
                if not center:
                    raise Exception("No Collection Centers exist in the database at all. Please create one.")

            # 5. Create the database record submission safely
            WasteSubmission.objects.create(
                plastic_type=plastic_type,
                collection_center=center,
                submitter_name=request.POST.get("submitter_name"),
                submitter_email=request.POST.get("submitter_email"),
                submitter_phone=request.POST.get("phone_number"),
                weight_kg=float(request.POST.get("weight_kg") or 0)
            )
            
            messages.success(request, "Waste submitted successfully!")
            return redirect('dashboard')
            
        except Exception as e:
            messages.error(request, f"Error saving data: {e}")
    return render(
        request,
        "submit.html",
        {
            "plastic_types": plastic_types,
            "collection_centers": collection_centers,
        },
    )
def dashboard(request):
    """Data analytics dashboard"""
    submissions = WasteSubmission.objects.all().order_by('-submitted_at')[:10]
    
    plastic_stats = {}
    for s in WasteSubmission.objects.all():
        code = s.plastic_type.code if s.plastic_type else "Unknown"
        plastic_stats[code] = plastic_stats.get(code, 0) + float(s.weight_kg or 0)
        
    centers = CollectionCenter.objects.all()
    
    # ─── CRITICAL CAPITALIZATION FIX HERE ───
    from .models import DataMiningReport  # <-- Make sure the 'M' is capitalized!
    reports = DataMiningReport.objects.all().order_by('-id')[:5]
    
    context = {
        'submissions': submissions,
        'plastic_stats': json.dumps(plastic_stats),
        'centers': centers,
        'reports': reports,  
    }
    return render(request, 'dashboard.html', context)
def centers_view(request):
    """Collection centers map"""
    centers = CollectionCenter.objects.filter(is_active=True)
    return render(request, 'centers.html', {'centers': centers})


def reports_view(request):
    """Data mining reports"""
    reports = DataMiningReport.objects.all().order_by('-created_at')
    return render(request, 'reports.html', {'reports': reports})


def track_view(request):
    """Track submission"""
    submission = None
    if request.method == 'POST':
        tracking_id = request.POST.get('tracking_id')
        try:
            submission = WasteSubmission.objects.get(id=tracking_id)
        except WasteSubmission.DoesNotExist:
            messages.error(request, 'No submission found with that ID.')
    return render(request, 'track.html', {'submission': submission})


# --- API Endpoints ---

def api_stats(request):
    """API: dashboard statistics"""
    submissions = WasteSubmission.objects.all()
    total_weight = sum(s.weight_kg for s in submissions)
    by_type = {}
    for s in submissions:
        code = s.plastic_type.code
        by_type[code] = round(by_type.get(code, 0) + s.weight_kg, 2)

    monthly = {}
    for s in submissions:
        key = s.submitted_at.strftime('%b %Y')
        monthly[key] = round(monthly.get(key, 0) + s.weight_kg, 2)

    status_count = {}
    for s in submissions:
        status_count[s.status] = status_count.get(s.status, 0) + 1

    return JsonResponse({
        'total_submissions': submissions.count(),
        'total_weight_kg': round(total_weight, 2),
        'co2_saved_kg': round(total_weight * 2.5, 2),
        'energy_saved_kwh': round(total_weight * 5.8, 2),
        'trees_equivalent': round(total_weight * 0.1, 2),
        'by_plastic_type': by_type,
        'monthly_trend': monthly,
        'status_breakdown': status_count,
        'active_centers': CollectionCenter.objects.filter(is_active=True).count(),
    })


def api_centers(request):
    """API: list collection centers"""
    centers = CollectionCenter.objects.filter(is_active=True)
    data = [{
        'id': c.id,
        'name': c.name,
        'city': c.city,
        'state': c.state,
        'address': c.address,
        'contact': c.contact,
        'capacity_kg': c.capacity_kg,
        'lat': c.latitude,
        'lng': c.longitude,
    } for c in centers]
    return JsonResponse({'centers': data})


@csrf_exempt
@require_http_methods(["POST"])
def api_submit(request):
    """API: submit waste"""
    try:
        data = json.loads(request.body)
        plastic_type = PlasticType.objects.get(code=data['plastic_type'])
        center = CollectionCenter.objects.get(id=data['center_id'])
        submission = WasteSubmission.objects.create(
            submitter_name=data['name'],
            submitter_email=data['email'],
            submitter_phone=data.get('phone', ''),
            plastic_type=plastic_type,
            weight_kg=float(data['weight']),
            collection_center=center,
            description=data.get('description', ''),
        )
        return JsonResponse({
            'success': True,
            'tracking_id': submission.id,
            'points_earned': submission.points_earned,
            'message': f'Successfully submitted! Tracking ID: #{submission.id}'
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


def api_mining(request):
    """API: data mining insights"""
    submissions = list(WasteSubmission.objects.select_related('plastic_type', 'collection_center').all())
    # Pattern analysis
    type_freq = {}
    center_freq = {}
    for s in submissions:
        type_freq[s.plastic_type.code] = type_freq.get(s.plastic_type.code, 0) + 1
        center_freq[s.collection_center.city] = center_freq.get(s.collection_center.city, 0) + 1

    top_type = max(type_freq, key=type_freq.get) if type_freq else 'N/A'
    top_city = max(center_freq, key=center_freq.get) if center_freq else 'N/A'
    avg_weight = (sum(s.weight_kg for s in submissions) / len(submissions)) if submissions else 0

    insights = [
        {
            'title': 'Most Common Plastic Type',
            'value': top_type,
            'description': f'{type_freq.get(top_type, 0)} submissions',
            'trend': 'up',
            'category': 'Pattern Mining'
        },
        {
            'title': 'Top Contributing City',
            'value': top_city,
            'description': f'{center_freq.get(top_city, 0)} submissions',
            'trend': 'up',
            'category': 'Geographic Analysis'
        },
        {
            'title': 'Average Waste Weight',
            'value': f'{round(avg_weight, 2)} kg',
            'description': 'Per submission average',
            'trend': 'stable',
            'category': 'Statistical Analysis'
        },
        {
            'title': 'Recycling Rate',
            'value': f"{round((WasteSubmission.objects.filter(status='recycled').count() / max(len(submissions), 1)) * 100, 1)}%",
            'description': 'Of total submissions recycled',
            'trend': 'up',
            'category': 'Efficiency Metrics'
        },
    ]
    return JsonResponse({'insights': insights, 'total_analyzed': len(submissions)})

    from django.shortcuts import render
def analytics_view(request):
    # Retrieve groupings using standard values dictionary querying
    data_query = WasteSubmission.objects.values('plastic_type').annotate(
        total_weight=Sum('weight_kg'),
        count=Count('id')
    )
    
    labels = []
    weights = []
    
    for item in data_query:
        # Check if plastic_type field directly holds an integer ID or relation
        raw_type = item['plastic_type']
        
        # If it's a primary key ID, let's look up its text label name dynamically
        try:
            from .models import PlasticType
            pt_obj = PlasticType.objects.get(id=raw_type)
            label_name = pt_obj.name
        except:
            # Fallback placeholder label text if relation retrieval fails
            label_name = f"Type {raw_type}" if raw_type else "Uncategorized"
            
        labels.append(label_name)
        weights.append(float(item['total_weight'] or 0))
    
    context = {
        'labels': labels,
        'weights': weights,
    }
    return render(request, 'analytics.html', context)
