from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from .models import Report
from .forms import ReportForm
from django.contrib.auth import logout


def home(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('garbage:admin_dashboard')
        else:
            return redirect('garbage:upload_report')
    else:
        return redirect('login')


@login_required
def upload_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        if form.is_valid() and latitude and longitude:
            report = form.save(commit=False)
            report.user = request.user
            try:
                report.latitude = float(latitude)
                report.longitude = float(longitude)
            except ValueError:
                messages.error(request, "Invalid location coordinates.")
                return render(request, 'garbage/upload.html', {'form': form})

            report.save()
            messages.success(request, "Garbage report submitted successfully.")
            if request.user.is_staff:
                return redirect('garbage:admin_dashboard')  # admin users
            else:
                return redirect('garbage:upload_report')  # regular users

        else:
            messages.error(request, "Please upload an image and allow location access.")
            messages.error(request, "Please correct the errors in the form.")
    else:
        form = ReportForm()

    removed_reports = Report.objects.filter(user=request.user, status='removed', notified=False)
    context = {'form': form, 'removed_reports': removed_reports}
    return render(request, 'garbage/upload.html', context)


def is_admin(user):
    return user.is_staff


@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    reports = Report.objects.all().order_by('-created_at')
    return render(request, 'garbage/admin_dashboard.html', {'reports': reports})


@login_required
@user_passes_test(is_admin)
def remove_report(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    if report.status != 'removed':
        report.status = 'removed'
        report.notified = False
        report.save()
        messages.success(request, f"Report #{report.id} marked as removed.")
    else:
        messages.warning(request, f"Report #{report.id} is already marked as removed.")

    return redirect('garbage:admin_dashboard')


@login_required
@require_POST
@csrf_protect
def acknowledge_notification(request, report_id):
    report = get_object_or_404(Report, id=report_id, user=request.user)
    report.notified = True
    report.save()
    return JsonResponse({'success': True})



def logout_view(request):
    logout(request)
    return redirect('login')
    



