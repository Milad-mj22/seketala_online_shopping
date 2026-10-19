import json
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .forms import ComplaintForm

logger = logging.getLogger(__name__)


@csrf_exempt
@require_POST
def submit_complaint(request):
    """
    دریافت شکایت به صورت AJAX (JSON).
    پاسخ: JSON با success / message / complaint_id
    """
    try:
        if request.content_type == 'application/json':
            data = json.loads(request.body.decode('utf-8'))
        else:
            data = request.POST.dict()

        form = ComplaintForm(data)

        if not form.is_valid():
            # برگردوندن خطاها به فارسی
            errors = {}
            for field, errs in form.errors.items():
                errors[field] = errs[0] if errs else ''
            return JsonResponse({
                'success': False,
                'message': 'اطلاعات نامعتبر است.',
                'errors': errors,
            }, status=400)

        complaint = form.save(commit=False)

        # IP
        xff = request.META.get('HTTP_X_FORWARDED_FOR')
        complaint.ip_address = (
            xff.split(',')[0].strip() if xff else request.META.get('REMOTE_ADDR')
        )
        complaint.user_agent = request.META.get('HTTP_USER_AGENT', '')[:1000]
        complaint.status = 'new'
        complaint.save()

        logger.info(f'✅ Complaint #{complaint.id} saved from {complaint.ip_address}')

        return JsonResponse({
            'success': True,
            'message': 'شکایت شما با موفقیت ثبت شد. تا ۴۸ ساعت آینده با شما تماس می‌گیریم.',
            'complaint_id': complaint.id,
        }, status=201)

    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'داده‌های ارسالی معتبر نیست.',
        }, status=400)
    except Exception as e:
        logger.exception('Complaint submit error')
        return JsonResponse({
            'success': False,
            'message': f'خطا در ثبت شکایت: {str(e)}',
        }, status=500)