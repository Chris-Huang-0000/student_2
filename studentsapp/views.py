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

def post(request):
    if request.method == "POST":
        mess = request.POST['username']
        print(f"mess={mess}")
    else:
        mess = "表單資料尚未送出!"
    return render(request,"post.html",{"mess":mess})


def post1(request): #新增資料到資料庫，不做驗證
    if request.method == "POST":
        uname = request.POST['name']
        usex = request.POST['sex']
        ubirthday = request.POST['birthday']
        uemail = request.POST['email']
        uphone = request.POST['phone']
        uaddress = request.POST['address']
        addinfo = student.objects.create(name=uname,sex=usex,birthday=ubirthday,email=uemail,phone=uphone,address=uaddress)
        addinfo.save()
        return redirect(reverse(index))
    else:
        message = "請輸入資料(資料不做驗證)"
    return render(request,"post1.html",{"message":message})


from studentsapp.form import PostForm
def postform(request):
    if request.method == "POST":
        postform = PostForm(request.POST)
        if postform.is_valid():
            uname = postform.cleaned_data["name"]
            print(uname)
        else:
            print("驗證錯誤")
    else:
        print("沒有輸入資料")
        postform = PostForm()
    return render(request,"postform.html",locals())


def post2(request):
    if request.method == "POST":
        postform = PostForm(request.POST)
        if postform.is_valid():
            uname = postform.cleaned_data["name"]
            usex = postform.cleaned_data["sex"]
            ubirthday = postform.cleaned_data["birthday"]
            uemail = postform.cleaned_data["email"]
            uphone = postform.cleaned_data["phone"]
            uaddress = postform.cleaned_data["address"]
            addinfo = student.objects.create(name=uname,sex=usex,birthday=ubirthday,email=uemail,phone=uphone,address=uaddress)
            addinfo.save()
            print("已儲存!")
            return redirect(reverse(index))
        else:
            print(postform.errors) #postform.errors抓住錯誤訊息
            message = "驗證錯誤，請重新輸入"
    else:
        message = "姓名、性別、生日必須輸入"
        postform = PostForm()
    return render(request,"post2.html",{"message":message,"postform":postform})


def delete(request,id=None):
    if id != None:
        if request.method == "GET":
            userid = id
        try:
            unit = student.objects.get(id=userid)
            unit.delete()
            return redirect(reverse(index))
        except:
            message = "讀取錯誤"
    
            return render(request,"delete.html",{"message":message})


def edit(request,id,mode=None):
    if mode == "edit":
        unit = student.objects.get(id=id)
        unit.name = request.GET['new_name']
        unit.sex = request.GET['new_sex']
        unit.birthday = request.GET['new_birthday']
        unit.email = request.GET['new_email']
        unit.phone = request.GET['new_phone']
        unit.address = request.GET['new_address']
        unit.save()
        # message = "已修改..."
        return redirect(reverse(index))
    else:
        try:
            unit = student.objects.get(id=id)
        except:
            message = "此 id 不存在"
        
        # 如果要傳送的變數，時而有值;時而沒值的情況，採用locals()方式傳送變數會比較好
        return render(request,"edit.html",locals())
    

def edit2(request,id=None,mode=None):
    if mode == "load":
        unit = student.objects.get(id=id)
        return render(request,"edit2.html",locals())
    elif mode == "save":
        unit = student.objects.get(id=id)
        unit.name = request.POST['new_name']
        unit.sex = request.POST['new_sex']
        unit.birthday = request.POST['new_birthday']
        unit.email = request.POST['new_email']
        unit.phone = request.POST['new_phone']
        unit.address = request.POST['new_address']
        unit.save()
        return redirect(reverse(index))