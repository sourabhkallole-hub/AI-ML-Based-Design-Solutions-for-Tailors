from django.shortcuts import render
from app.models import Register
from app.models import Contact
from app.models import PredictHistory
from app.models import AdminMaster, Design, DesignSteps, Bookings
from django.http import JsonResponse, HttpResponse, Http404
import pandas as pd
import joblib
import os
# import numpy as np
import googlemaps
# import datetime
from django.conf import settings
import json
from django.utils.timezone import localtime
from collections import Counter, defaultdict


def openLogin(request):
    return render(request, "admin/admin_login.html", {})

def adminHistory(request):
    return render(request, "admin/admin_history.html", {})

def adminReport(request):
    return render(request, "admin/admin_users.html", {})

def adminContact(request):
    return render(request, "admin/admin_contact.html", {})

def adminProfile(request):
    return render(request, "admin/admin_profile.html", {})

def tailorProfile(request):
    return render(request, "tailor/tailor_profile.html", {})

def adminDesign(request):
    return render(request, "admin/admin_design.html", {})

def adminDesignDetails(request):
    if request.POST["action"] == "add":

        Design.objects.create(
            de_name=request.POST["selDesignType"],
            de_image=request.FILES["filePhoto"],
        )

    elif request.POST["action"] == "getData":
        data = Design.objects.filter(de_status="0").values()
        data = list(data)
        values = JsonResponse(data, safe=False)
        return values

    elif request.POST["action"] == "update":
        data = Design.objects.filter(de_id=request.POST["id"]).update(
            de_name=request.POST["selDesignType1"],
            de_image=request.FILES["filePhoto1"],
        )

    elif request.POST["action"] == "delete":
        data = Design.objects.filter(de_id=request.POST["id"]).update(
            de_status="1"
        )

    return HttpResponse()

def adminDesignDetailsCreate(request):
    action = request.POST.get("action")

    if action == "add":
        DesignSteps.objects.create(
            ar_de_id=request.POST.get("id", ""),
            ar_name=request.POST.get("txtName1", ""),
            ar_image=request.FILES.get("filePhoto1"),
            ar_description=request.POST.get("txtDescription1", ""),
        )
        return HttpResponse()

    elif action == "getData":
        data = list(DesignSteps.objects.filter(ar_de_id = request.POST['id'], ar_status="0").values())
        return JsonResponse(data, safe=False)

    elif action == "update":
        obj = DesignSteps.objects.filter(ar_id=request.POST.get("id")).first()
        if obj:
            if request.POST.get("selDesignType1"):
                obj.ar_name = request.POST["selDesignType1"]
            if "filePhoto1" in request.FILES:
                obj.ar_image = request.FILES["filePhoto1"]
            if request.POST.get("txtDescription1"):
                obj.ar_description = request.POST["txtDescription1"]
            obj.save()
        return HttpResponse()

    elif action == "delete":
        DesignSteps.objects.filter(ar_id=request.POST.get("id")).update(ar_status="1")
        return HttpResponse()

    return HttpResponse()

def adminProfileDetails(request):
    dataValue = AdminMaster.objects.filter(
            ad_email=request.session["email"]
        ).values()
    data = list(dataValue)
    return JsonResponse(data, safe=False)

def adminUpdateProfileDetails(request):
    data = AdminMaster.objects.filter(ad_email=request.session["email"]).update(
        ad_name=request.POST["txtName"],
        ad_mobile=request.POST["txtMobile"],
        ad_password=request.POST["txtPassword"],
    )

    return HttpResponse();

def update_status(request):
    Bookings.objects.filter(bk_id=request.POST["id"]).update(
        status=request.POST["selStatus"],
    )
    
    return HttpResponse()

def get_booking_details(request, bk_id: int):
    try:
        b = Bookings.objects.get(pk=bk_id)
    except Bookings.DoesNotExist:
        raise Http404("Booking not found or inactive")

    ph = PredictHistory.objects.filter(ph_id=b.ph_id, ph_status="0").first()
    d = Design.objects.filter(de_id=b.de_id, de_status="0").first()
    steps_qs = DesignSteps.objects.filter(ar_de_id=str(b.de_id), ar_status="0").order_by("ar_id")

    booking_payload = {
        "user_email": b.user_email,
        "de_name": b.de_name,
        "booking_date": localtime(b.created_at).strftime("%d-%m-%Y") if b.created_at else b.booking_date.strftime("%d-%m-%Y"),
        "booking_time": localtime(b.created_at).strftime("%I:%M %p") if b.created_at else b.booking_time.strftime("%I:%M %p"),
        "status": b.status,
    }

    ph_payload = None
    if ph:
        ph_payload = {
            "ph_age": ph.ph_age,
            "ph_gender": ph.ph_gender,
            "ph_height_cm": ph.ph_height_cm,
            "ph_chest_cm": ph.ph_chest_cm,
            "ph_waist_cm": ph.ph_waist_cm,
            "ph_hips_cm": ph.ph_hips_cm,
            "ph_shoulder_cm": ph.ph_shoulder_cm,
            "ph_occasion": ph.ph_occasion,
            "ph_predicted_outfit": ph.ph_predicted_outfit,
            "ph_created_by": ph.ph_created_by,
        }

    design_payload = {}
    if d:
        design_payload = {
            "de_name": d.de_name,
            "de_status": d.de_status,
            "de_image": str(d.de_image) if getattr(d, "de_image", None) else "",
        }

    steps_payload = []
    for s in steps_qs:
        steps_payload.append({
            "ar_name": s.ar_name,
            "ar_description": s.ar_description,
            "ar_status": s.ar_status,
            "ar_image": str(s.ar_image) if getattr(s, "ar_image", None) else "",
        })

    return JsonResponse({
        "booking": booking_payload,
        "predict_history": ph_payload,
        "design": design_payload,
        "steps": steps_payload,
    })

def getDesigns(request):
    dataValue = Design.objects.filter(de_status = "0", de_name = request.POST['res']).values()
    data = list(dataValue)
    return JsonResponse(data, safe=False)

def save_selected_designs(request):
    try:
        user_email = request.session.get("web_email")
        if not user_email:
            return JsonResponse({"status": "error", "message": "User not logged in"}, status=401)

        data = json.loads(request.body.decode("utf-8"))
        selections = data.get("selections", [])
        history_id = data.get("history_id")

        if not history_id:
            return JsonResponse({"status": "error", "message": "history_id is required"}, status=400)

        saved = []
        for sel in selections:
            booking = Bookings.objects.create(
                de_id=sel.get("de_id"),
                de_name=sel.get("de_name"),
                user_email=user_email,
                ph_id=history_id
            )
            saved.append({
                "bk_id": booking.bk_id,
                "de_id": booking.de_id,
                "de_name": booking.de_name,
                "user_email": booking.user_email,
                "ph_id": booking.ph_id,
                "booking_date": str(booking.booking_date),
                "booking_time": str(booking.booking_time),
            })

        return JsonResponse({"status": "success", "saved": saved}, status=201)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)

def adminLogout(request):
    if "email" in request.session:
        del request.session["email"]
    return render(request, "admin/admin_login.html")


def loginAdmin(request):
    if AdminMaster.objects.filter(
        ad_email=request.POST["txtEmail"], ad_password=request.POST["txtPassword"]
    ).count():
        dataValue = AdminMaster.objects.filter(
            ad_email=request.POST["txtEmail"]
        ).values()
        data = list(dataValue)
        dictValue = data[0]
        request.session["email"] = dictValue["ad_email"]
        request.session["role"] = dictValue["ad_role"]
        request.session["name"] = dictValue["ad_name"]
        return HttpResponse(dictValue["ad_role"])
    else:
        return HttpResponse("10")


def logoutAdmin(request):
    request.session.delete()
    return render(request, "index.html", {})


# admin details
def adminMaster(request):
    return render(request, "admin/admin_master.html", {})


def adminDetails(request):
    if request.POST["action"] == "add":
        if (
            AdminMaster.objects.filter(
                ad_mobile=request.POST["txtMobileNo"],
                ad_email=request.POST["txtEmail"],
                ad_status=0,
            ).count()
            == 0
        ):
            AdminMaster.objects.create(
                ad_name=request.POST["txtName"],
                ad_mobile=request.POST["txtMobileNo"],
                ad_email=request.POST["txtEmail"],
                ad_password=request.POST["txtPassword"],
                ad_role=request.POST["selRole"],
            )
        else:
            return HttpResponse("10")

    elif request.POST["action"] == "getData":
        data = AdminMaster.objects.filter(ad_status="0").values()
        data = list(data)
        values = JsonResponse(data, safe=False)
        return values

    elif request.POST["action"] == "update":
        data = AdminMaster.objects.filter(ad_id=request.POST["id"]).update(
            ad_name=request.POST["txtName1"],
            ad_mobile=request.POST["txtMobileNo1"],
            ad_email=request.POST["txtEmail1"],
        )

    elif request.POST["action"] == "delete":
        data = AdminMaster.objects.filter(ad_id=request.POST["id"]).update(
            ad_status="1"
        )

    return HttpResponse()

def adminHistoryDetails(request):
    if request.POST["action"] == "getData":
        data = PredictHistory.objects.filter(ph_status="0").values()
        data = list(data)
        values = JsonResponse(data, safe=False)
        return values

    return HttpResponse()

def adminHistoryIndividualDetails(request):
    if request.POST["action"] == "getData":
        data = PredictHistory.objects.filter(ph_status="0", ph_created_by=request.POST['email']).values()
        data = list(data)
        values = JsonResponse(data, safe=False)
        return values

    return HttpResponse()

def adminUserDetails(request):
    if request.POST["action"] == "getData":
        data = Register.objects.filter(rg_status="0").values()
        data = list(data)
        values = JsonResponse(data, safe=False)
        return values

    return HttpResponse()

def adminContactDetails(request):
    if request.POST["action"] == "getData":
        data = Contact.objects.filter(co_status="0").values()
        data = list(data)
        values = JsonResponse(data, safe=False)
        return values

    return HttpResponse()

def webIndex(request):
    web_email = request.session.get("web_email")
    return render(request, "web/index.html", {"web_email": web_email})

def about(request):
    web_email = request.session.get("web_email")
    return render(request, "web/about.html", {"web_email": web_email})

def contact(request):
    web_email = request.session.get("web_email")
    return render(request, "web/contact.html", {"web_email": web_email})


def loginUser(request):
    return render(request, "web/login.html", {})

def register(request):
    return render(request, "web/register.html", {})

def profile(request):
    return render(request, "web/profile.html", {})

def my_bookings(request):
    return render(request, "web/my_bookings.html", {})


def tailor_bookings(request):
    return render(request, "tailor/tailor_bookings.html", {})


def get_bookings(request):
    try:
        user_email = request.session.get("web_email")
        if not user_email:
            return JsonResponse({"error": "User not logged in"}, status=401)

        bookings = Bookings.objects.filter(user_email=user_email).order_by('-booking_date', '-booking_time')

        data = []
        for b in bookings:
            data.append({
                "de_name": b.de_name,
                "booking_date": b.booking_date.strftime("%d-%m-%Y"),
                "booking_time": b.booking_time.strftime("%I:%M %p"),
                "status": b.status,
            })
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    

def get_tailor_bookings(request):
    try:
        bookings = Bookings.objects.all().order_by('-booking_date', '-booking_time')
        data = []
        for b in bookings:
            data.append({
                "bk_id": b.bk_id,
                "de_name": b.de_name,
                "user_email": b.user_email,  # include user email
                "booking_date": b.booking_date.strftime("%d-%m-%Y"),
                "booking_time": b.booking_time.strftime("%I:%M %p"),
                "status": b.status,
            })
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def webLogin(request):
    if Register.objects.filter(
        rg_email=request.POST["txtEmail"],
        rg_password=request.POST["txtPassword"],
    ).count():
        request.session["web_email"] = request.POST["txtEmail"]
        return HttpResponse("1")
    else:
        return HttpResponse("0")

def webLogout(request):
    del request.session["web_email"]
    return render(request, "web/index.html")

def newRegister(request):
    if Register.objects.filter(
        rg_email=request.POST["txtEmail"], rg_mobile=request.POST["txtMobileNo"]
    ).count():
        return HttpResponse("10")
    else:
        lclID = Register.objects.count()
        status = "0"
        lclNewID = lclID + 1

        Register.objects.create(
            rg_id=lclNewID,
            rg_name=request.POST["txtName"],
            rg_mobile=request.POST["txtMobileNo"],
            rg_email=request.POST["txtEmail"],
            rg_password=request.POST["txtPassword"],
        )

        return HttpResponse("0")

def saveContact(request):
    lclID = Contact.objects.count()
    status = "0"
    lclNewID = lclID + 1

    Contact.objects.create(
        co_id=lclNewID,
        co_name=request.POST["txtName"],
        co_email=request.POST["txtEmail"],
        co_mobile=request.POST["txtMobileNo"],
        co_subject=request.POST["txtSubject"],
        co_message=request.POST["txtMessage"],
        co_status=status,
    )

    return HttpResponse()
gmaps = googlemaps.Client(key='AIzaSyDdzOoBadUjbHkFwrSRtuhFs40wB1yy_ho')

CSV_PATH = os.path.join(settings.BASE_DIR, "static", "fashion_recommendation_dataset_balanced.csv")
_TRIPLE_MAP = {}
_PAIR_MAP = {}
_SINGLE_MAP = {}
_CSV_LOADED = False

def _load_csv_rules():
    global _CSV_LOADED, _TRIPLE_MAP, _PAIR_MAP, _SINGLE_MAP
    if _CSV_LOADED:
        return
    if not os.path.exists(CSV_PATH):
        _CSV_LOADED = True
        return
    df = pd.read_csv(CSV_PATH, dtype=str).fillna("")
    df["gender_n"] = df["gender"].str.strip().str.lower()
    df["occasion_n"] = df["occasion"].str.strip().str.lower()
    df["style_n"] = df["style_preference"].str.strip().str.lower()
    df["outfit_n"] = df["recommended_outfit"].str.strip()
    triple_counters = defaultdict(Counter)
    pair_counters = defaultdict(Counter)
    single_counters = defaultdict(Counter)
    for _, row in df.iterrows():
        g = row["gender_n"] or "unknown"
        o = row["occasion_n"] or "any"
        s = row["style_n"] or "any"
        outfit = row["outfit_n"] or ""
        if outfit:
            triple_counters[(g, o, s)][outfit] += 1
            pair_counters[("gender", g, "occasion", o)][outfit] += 1
            pair_counters[("gender", g, "style", s)][outfit] += 1
            pair_counters[("occasion", o, "style", s)][outfit] += 1
            single_counters[("gender", g)][outfit] += 1
            single_counters[("occasion", o)][outfit] += 1
            single_counters[("style", s)][outfit] += 1
    _TRIPLE_MAP = {k: c.most_common(1)[0][0] for k, c in triple_counters.items()}
    _PAIR_MAP = {k: c.most_common(1)[0][0] for k, c in pair_counters.items()}
    _SINGLE_MAP = {k: c.most_common(1)[0][0] for k, c in single_counters.items()}
    _CSV_LOADED = True

def _predict_from_csv_only(gender, occasion, style_pref):
    _load_csv_rules()
    g = (gender or "unknown").strip().lower()
    o = (occasion or "any").strip().lower()
    s = (style_pref or "any").strip().lower()
    outfit = _TRIPLE_MAP.get((g, o, s))
    if outfit:
        return outfit
    for pk in [("gender", g, "occasion", o), ("gender", g, "style", s), ("occasion", o, "style", s)]:
        val = _PAIR_MAP.get(pk)
        if val:
            return val
    for sk in [("gender", g), ("occasion", o), ("style", s)]:
        val = _SINGLE_MAP.get(sk)
        if val:
            return val
    return None

def predict(request):
    print("========== PREDICT CALLED ==========")
    print(request.POST)
    print("====================================")
    
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=405)
    try:
        static_dir = os.path.join(settings. BASE_DIR, "static")
        model = joblib.load(os.path.join(static_dir, "fashion_rf_model.pkl"))
        print("Model Loaded")
        le_outfit = joblib.load(os.path.join(static_dir, "recommended_outfit_encoder.pkl"))
        print("Encoder Loaded")
        def getf(k, cast=float, req=True):
            v = request.POST.get(k, "").strip()
            if v == "" and req:
                raise ValueError(f"Missing required field: {k}")
            return cast(v) if v != "" else None
        print("=" * 50)
        print("POST DATA:", request.POST)
        print("age =", request.POST.get("age"))
        print("gender =", request.POST.get("gender"))
        print("occasion =", request.POST.get("occasion"))
        print("style_preference =", request.POST.get("style_preference"))
        print("height_cm =", request.POST.get("height_cm"))
        print("chest_cm =", request.POST.get("chest_cm"))
        print("waist_cm =", request.POST.get("waist_cm"))
        print("hips_cm =", request.POST.get("hips_cm"))
        print("shoulder_cm =", request.POST.get("shoulder_cm"))
        print("=" * 50)

        age = int(round(getf("age")))
        gender = request.POST.get("gender", "").strip()
        occasion = request.POST.get("occasion", "").strip()
        style_pref = request.POST.get("style_preference", "").strip() or "Casual"
        if not gender or not occasion:
            return JsonResponse({"error": "gender and occasion are required."}, status=400)
        outfit = _predict_from_csv_only(gender=gender, occasion=occasion, style_pref=style_pref)
        if not outfit:
            return JsonResponse({"error": "No matching outfit found in CSV."}, status=404)
        created_by = request.session.get("web_email") or getattr(getattr(request, "user", None), "email", "") or ""
        rec = PredictHistory.objects.create(
            ph_age=age,
            ph_gender=gender,
            ph_height_cm=request.POST.get("height_cm", ""),
            ph_chest_cm=request.POST.get("chest_cm", ""),
            ph_waist_cm=request.POST.get("waist_cm", ""),
            ph_hips_cm=request.POST.get("hips_cm", ""),
            ph_shoulder_cm=request.POST.get("shoulder_cm", ""),
            ph_occasion=occasion,
            ph_predicted_outfit=outfit,
            ph_created_by=created_by,
            ph_status="0"
        )
        return JsonResponse({"predicted_outfit": outfit, "history_id": rec.ph_id})
    except ValueError as ve:
        print("========== VALUE ERROR ==========")
        print(ve)
        print("=================================")
        return JsonResponse({"error": str(ve)}, status=400)
    except Exception as e:
        import traceback
        print("========== FULL ERROR ==========")
        traceback.print_exc()
        print("================================")
        print("Prediction Error:", e)
        return JsonResponse({"error": "Prediction failed."}, status=500)