from django import forms

class PostForm(forms.Form):
    name = forms.CharField(max_length=20,initial="",label="姓名") #沒設label屬性，輸出的表單物件會以指派的變數名稱當作label
    sex = forms.CharField(max_length=2,initial="M",label="性別")
    birthday = forms.DateField(label="生日")
    email = forms.EmailField(max_length=100,initial="",required=False,label="郵件信箱")
    phone = forms.CharField(max_length=50,initial="",required=False,label="電話")
    address = forms.CharField(max_length=255,initial="",required=False,label="地址")