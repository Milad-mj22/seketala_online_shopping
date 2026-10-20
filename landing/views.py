from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def landing(request):
    return render(request, 'landing/landing.html')



import os
import json
import base64
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import openai
from pathlib import Path

# تنظیم OpenAI
openai.api_key = settings.OPENAI_API_KEY

@csrf_exempt  # فقط برای تست، در production از @csrf_protect استفاده کن
def voice_assistant(request):
    """
    دریافت متن از کاربر، ارسال به OpenAI، دریافت جواب،
    تبدیل به صدا با TTS و برگردوندن audio_url
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'فقط متد POST پشتیبانی میشه'}, status=405)

    try:
        data = json.loads(request.body)
        user_text = data.get('text', '').strip()

        if not user_text:
            return JsonResponse({'error': 'متن وارد نشده'}, status=400)

        # ===== 1. ارسال به OpenAI =====
        # شما می‌تونید از سیستم‌پرامپت مناسب برای رستوران استفاده کنید
        system_prompt = """
        شما یک دستیار هوشمند برای رستوران فست‌فود «سکه طلا» هستید.
        وظیفه شما کمک به مشتریان برای ثبت سفارش، پاسخ به سوالات درباره منو،
        قیمت‌ها و زمان تحویل است.
        منوی رستوران شامل:
        - برگر طلایی: ۲۵۰,۰۰۰ تومان
        - پیتزا مخصوص: ۳۸۰,۰۰۰ تومان
        - ساندویچ مرغ: ۱۹۰,۰۰۰ تومان
        - سیب‌زمینی ویژه: ۱۲۰,۰۰۰ تومان
        - نوشابه: ۳۰,۰۰۰ تومان
        
        زمان تحویل: زیر ۲۰ دقیقه
        آدرس: تهران، خیابان ولیعصر، پلاک ۴۵
        تلفن: ۰۲۱-۱۲۳۴۵۶۷۸
        
        لطفاً به فارسی و با لحن دوستانه پاسخ بده.
        اگر کاربر سفارش داد، لیست سفارش‌ها رو جمع‌بندی کن و قیمت کل رو محاسبه کن.
        """

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # یا "gpt-4"
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_text}
            ],
            temperature=0.7,
            max_tokens=500
        )

        reply_text = response.choices[0].message.content

        # ===== 2. تبدیل متن به صدا با OpenAI TTS =====
        try:
            # OpenAI TTS (نسخه جدید)
            from openai import OpenAI
            client = OpenAI(api_key=settings.OPENAI_API_KEY)
            
            speech_response = client.audio.speech.create(
                model="tts-1",
                voice="nova",  # گزینه‌های: alloy, echo, fable, onyx, nova, shimmer
                input=reply_text,
                speed=1.0
            )

            # ذخیره فایل صوتی
            audio_filename = f"voice_response_{hash(reply_text)}.mp3"
            audio_path = Path('media') / 'audio' / audio_filename
            audio_path.parent.mkdir(parents=True, exist_ok=True)
            
            # ذخیره فایل
            with open(audio_path, 'wb') as f:
                f.write(speech_response.content)
            
            audio_url = f"/media/audio/{audio_filename}"

        except Exception as tts_error:
            print(f"TTS Error: {tts_error}")
            audio_url = None

        # ===== 3. برگردوندن جواب =====
        return JsonResponse({
            'reply': reply_text,
            'audio_url': audio_url,
        })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON نامعتبر'}, status=400)
    except Exception as e:
        print(f"Error: {e}")
        return JsonResponse({'error': str(e)}, status=500)
    




from django.shortcuts import redirect
import hashlib

def verify(request):
    res_code = request.POST.get("ResCode", "")
    order_id = request.POST.get("SaleOrderId", "")
    verify_sale_reference_id = request.POST.get("SaleReferenceId", "")

    token = hashlib.md5(
        f"MnuyyytAAAmnd77++{order_id}".encode()
    ).hexdigest()

    url = (
        f"http://foodsoftonline.ir/py_behp_vrfy.php"
        f"?f1={res_code}"
        f"&f2={order_id}"
        f"&f3={verify_sale_reference_id}"
        f"&f4={token}"
    )

    return redirect(url)




from django.http import HttpResponse
import hashlib


def mellat_gateway(request):
    authority = request.GET.get("auth", "")
    token = request.GET.get("token", "")
    received_hash = request.GET.get("hsh", "")

    expected_hash = hashlib.md5(
        f"{token}{authority}GHUdjjjsSfg89++tytr".encode()
    ).hexdigest()

    if received_hash != expected_hash:
        return HttpResponse(
            """
            <div style="width:500px;margin:auto;background:red;color:white;
                        font-size:22px;text-align:center;margin-top:80px;
                        height:50px;line-height:50px;">
                در انتقال به درگاه پرداخت مشکلی بوجود آمد-5001
            </div>
            <div style="width:200px;margin:auto;">
                <button onclick="window.history.go(-2);return false;"
                        style="width:200px;height:50px;margin-top:20px;">
                    بازگشت
                </button>
            </div>
            """
        )

    return HttpResponse(f"""
    <form id="myform"
          action="https://bpm.shaparak.ir/pgwchannel/startpay.mellat"
          method="POST">
        <input type="hidden" name="RefId" value="{authority}">
    </form>

    <script>
        document.getElementById("myform").submit();
    </script>
    """)







from django.http import HttpResponse
import hashlib


def top_gateway(request):
    token = request.GET.get("token", "")
    hsh = request.GET.get("hsh", "")

    expected_hash = hashlib.md5(
        f"{token}GHUdjjjsSfg89++tytr".encode("utf-8")
    ).hexdigest()

    if hsh != expected_hash:
        return HttpResponse("""
            <div style="width:500px;margin:auto;background:red;color:white;
                        font-size:22px;text-align:center;margin-top:80px;
                        height:50px;line-height:50px;">
                در انتقال به درگاه پرداخت مشکلی بوجود آمد - 5001
            </div>
        """)

    return HttpResponse(f"""
    <form id="paymentForm"
          action="https://top.shaparak.ir/Payment/Index"
          method="POST">

        <input type="hidden" name="Token" value="{token}">

    </form>

    <script>
        document.getElementById("paymentForm").submit();
    </script>
    """)




from django.shortcuts import redirect
import hashlib


def top_callback(request):
    status = request.POST.get("status", "")
    token = request.POST.get("Token", "")
    rrn = request.POST.get("RRN", "")

    sign = hashlib.md5(
        f"MnuyyytAAAmnd77++{token}".encode()
    ).hexdigest()

    return redirect(
        f"http://foodsoftonline.ir/py_behp_vrfy.php"
        f"?f1={status}"
        f"&f2={token}"
        f"&f3={rrn}"
        f"&f4={sign}"
    )




from django.http import HttpResponse
from django.views.decorators.http import require_GET

@require_GET
def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow: /admin/",  # مسیر ادمین را مسدود کنید
        "Disallow: /private/", # هر مسیر خصوصی دیگری
        f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")