from django.shortcuts import render,redirect
from django.urls import reverse
from studentsapp.models import student
from django.db.models import Q
from django.core.paginator import Paginator #Paginator 分頁設定套件 
from django.http import HttpResponse, JsonResponse
from django.forms.models import model_to_dict

# Create your views here.
def listone(request):
    try:
        unit = student.objects.get(address = '南韓釜山')
    except:
        errormessage = '(讀取錯誤!)'
    return render(request,'listone.html',locals())

def listall(request):
    students = student.objects.all().order_by('-id')
    return render(request,'listall.html',locals())

def index(request):
    if 'site_search' in request.GET:
        site_search = request.GET['site_search'].strip()
        
        #__contains:比對一個欄位取出包含一個關鍵字的資料
        # students = student.objects.filter(name__contains=site_search)
        
        # 比對多個欄位取出包含一個關鍵字的資料
        # students = student.objects.filter(
        #     Q(name__contains=site_search)|
        #     Q(birthday__contains=site_search)|
        #     Q(email__contains=site_search)|
        #     Q(phone__contains=site_search)|
        #     Q(address__contains=site_search)
        #     )

        # 比對多個欄位取出包含多個關鍵字的資料
        keywords = site_search.split()
        print(keywords)
        q_object = Q()
        for keyword in keywords:
            q_object.add(Q(name__contains=keyword),Q.OR)
            q_object.add(Q(birthday__contains=keyword),Q.OR)
            q_object.add(Q(email__contains=keyword),Q.OR)
            q_object.add(Q(phone__contains=keyword),Q.OR)
            q_object.add(Q(address__contains=keyword),Q.OR)
        students = student.objects.filter(q_object)

        
    else:
        students = student.objects.all().order_by('id')

    paginator = Paginator(students,1)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num) #根據取得page_num，得到對應頁數的資料
    #page_obj : 包含該頁資料的物件
    # page_obj.object_list : 該頁的資料
    # page_obj.has_previous,page_obj.has_next : 判斷是否有上一頁或下一頁
    # page_obj.previous_page_number,page_obj.next_page_number : 上一頁或下一頁
    # page_obj.number : 目前的頁碼
    # pagenator.num_pages : 總頁數


    return render(request,'index.html',locals())
