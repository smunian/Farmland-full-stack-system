from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password, make_password
from agriculture.serializers import *
from mqtt_service.apps import *

from api import models


#   水阀状态和开启时间和保存模型


# 定时灌溉模型
class GuangaiModels:
    water_status = 0,
    water_keeplive = 0,
    temperature_is_valid = 1
    temperature_relation = 0
    temperature_value = 0
    humidity_is_valid = 1
    humidity_releation = 0
    humidity_value = 0
    co2_is_valid = 0
    co2_relation = 0
    co2_value = 0
    lumination_is_valid = 1
    lumination_relation = 0
    lumination_value = 0
    soil_humidity_is_valid = 0
    soil_humidity_relation = 0
    soil_humidity_value = 0


guangai = GuangaiModels()
a = 0
id_parm = 0


# 网页登入界面接口逻辑
# Create your views here.
def web_login(req):
    if req.method == 'GET':
        return render(req, 'login.html')
    if req.method == 'POST':
        name = req.POST.get('username')
        pwd = req.POST.get('pwd')
        if name == "" or pwd == "":
            return render(req, 'login.html', {'err': '账户密码为空'})
        data = models.User_info.objects.filter(username=name).first()
        if not data or not data.password:
            return render(req, 'login.html', {'err': '账户不存在或密码为空'})
        if pwd != data.password:
            return render(req, 'login.html', {'err': '密码错误'})
        if name != 'fjcpc':
            return render(req, 'login.html', {'err': '该用户不为管理员用户'})

        return redirect('index')  # 登录成功后重定向到首页或其他指定页面
    return HttpResponse('请求方式错误')
        # return HttpResponse('请求方式错误')
        # data = {'message': '请求成功',
        #         'code': '200'
        #         }
        # return JsonResponse(data, status=200)


#   添加用户
def add(req):
    if req.method == 'GET':
        return render(req, 'add.html')
    name = req.POST.get('user')
    pwd = req.POST.get('pwd')
    models.User_info.objects.create(username=name, password=pwd)
    return redirect('index')


#   更新用户
def updata(req, nid):
    if req.method == 'GET':
        name = models.User_info.objects.filter(username=nid).first()
        return render(req, 'updata.html', {'name': name})
    user = req.POST.get('username')
    pwd = req.POST.get('password')
    models.User_info.objects.filter(id=nid).update(username=user, password=pwd)
    return redirect('index')


#   删除用户
def delete(req):
    nid = req.GET.get('nid')
    models.User_info.objects.filter(id=nid).delete()
    return redirect('index')


#   登入页面
def index(req):
    user_list = models.User_info.objects.all()
    return render(req, 'index.html', {'list': user_list})


# 显示数据
def datedisplay(req, param):
    city_ids = {
        '北京': {1, 18, 49, 78, 109, 139, 170, 200, 231, 262, 292, 323, 353},
        '厦门': {2, 19, 50, 79, 110, 140, 171, 201, 232, 263, 293, 324, 354},
        '福州': {3, 20, 51, 80, 111, 141, 172, 202, 233, 264, 294, 325, 355},
        '泉州': {4, 21, 52, 81, 112, 142, 173, 203, 234, 265, 295, 326, 356},
    }
    if param in city_ids:
        date_list = []
        ids = city_ids[param]
        for i in ids:
            date = models.SensorMonitor_info.objects.get(i)
            date_table = {
                'time': date.record_time,
                'temperature': date.temperature,
                'humidity': date.humidity,
                'co2': date.co2,
                'luminance': date.luminance,
                'soi_humidity': date.soi_humidity
            }
            date_list.append(date_table)
        return render(req, 'datedisplay.html', {'list': date_list})


# 没选择地区时调用
def datadisplay_no_param(req):
    date_list = ""
    return render(req, 'datedisplay.html', {'list': date_list})


# 显示农田
def farmland(req):
    farmland_list = models.agriculture_info.objects.all()
    return render(req, 'farmland.html', {'list': farmland_list})


# 删除农田
def farmland_delete(req):
    farmland_name = req.GET.get('farmland_name')
    models.agriculture_info.objects.filter(name=farmland_name).delete()
    return redirect('farmland')


# 增加农田
def farmland_add(req):
    if req.method == 'GET':
        return render(req, 'farmland_add.html')
    farmland = req.POST.get('farmland')
    models.agriculture_info.objects.create(name=farmland)
    return redirect('farmland')


# 显示定时灌溉
def Valve(req):
    valve_list = models.api_irrigationschedule_info.objects.all()
    return render(req, 'Valve.html', {'list': valve_list})


# 显示阈值灌溉
def threshold(req):
    threshold_list = models.ThresholdIrrigation.objects.all()
    print(threshold_list)
    return render(req, 'threshold.html', {'list': threshold_list})


# 前后分离后端接口
def api_login(req):
    if req.method == 'POST':
        # 使用 request.POST.get 获取表单数据
        user = req.POST.get('username')
        pwd = req.POST.get('password')
        print(user)
        print(pwd)
        # 根据用户名获取 User_info 实例
        try:
            user_info = User_info.objects.get(username=user)
        except models.User_info.DoesNotExist:
            # 如果用户不存在，返回用户名不存在的错误信息
            return JsonResponse({"code": "401", "message": "用户名不存在"}, status=401)

        # 使用 Django 的 check_password 函数来验证密码
        if pwd == user_info.password:
            # 如果密码验证成功
            login_result = {"code": "200", "message": "登录成功"}
        else:
            # 如果密码验证失败，返回密码错误的错误信息
            login_result = {"code": "401", "message": "密码错误"}

        return JsonResponse(login_result, safe=False)
    else:
        # 如果不是 POST 请求，返回错误
        return JsonResponse({"code": "400", "message": "Invalid request"}, status=400)


def add_user(request):
    if request.method == 'POST':
        # 使用 request.POST.get 获取表单数据
        name = request.POST.get('name')
        pwd = request.POST.get('pwd')

        # 创建 User_info 实例，同时设置密码
        if name and pwd:  # 确保 name 和 pwd 不为空
            # 使用 make_password 创建密码哈希
            password_hash = make_password(pwd)

            # 创建用户实例并保存到数据库
            user = User_info.objects.create(
                username=name,
                password=password_hash  # 存储密码哈希而不是明文密码
            )

            return JsonResponse({"message": "OK"}, status=200)
        else:
            return JsonResponse({"message": "Name and password are required"}, status=400)

    else:
        return JsonResponse({"message": "Invalid request"}, status=400)


def device_data(request):
    device_id = request.GET.get('device_id')
    sensor_info = SensorMonitor_info.objects.filter(device_info_id=device_id)
    sensordata = SensorMonitor_infoSerializer(sensor_info, many=True)
    return JsonResponse(sensordata.data, safe=False)


def device_info(request):
    return


def agriculture_info(request):
    return


#   app的登入界面接口
def login(req):
    if req.method == 'POST' and req.content_type == 'application/json':
        data = json.loads(req.body)
        name = data["user"]
        pwd = data['pwd']
        # data = models.User_info.objects.filter(username=name).first()
        data = models.User_info.objects.filter(username=name).first()
        if data is None:
            return HttpResponse("用户未注册")
        if pwd == data.password:
            return HttpResponse("登入成功")
    return HttpResponse("用户或者密码错误")


#   忘记密码接口
def forgot_password(req):
    if req.method == 'POST' and req.content_type == 'application/json':
        data = json.loads(req.body)
        username = data["user"]
        password = data['pwd']
        is_data = models.User_info.objects.filter(username=username)
        if not is_data.exists():
            return JsonResponse({'error': '该账号不存在'}, status=400)
        models.User_info.objects.filter(username=username).update(password=password)
        return HttpResponse("修改成功")
    else:
        return JsonResponse({'error': '无效的请求方法'}, status=400)


# 显示地点接口
def text_select(req):
    global id_parm
    if req.GET.get('id') is not None:
        temp = int(req.GET.get('id'))
        if temp != 0:
            id_parm = temp - 1
    name = models.agriculture_info.objects.order_by('name')
    name_list = {
        'name': name[id_parm].name
    }
    return JsonResponse(name_list)


# 传感器数据接口
def cgq(req):
    global a
    if req.GET.get('id') is not None:
        temp = int(req.GET.get('id'))
        if temp != 0:
            a = temp - 1
        data = models.SensorMonitor_info.objects.order_by('record_time').last()
    data_dict = {
        'record_time': data.record_time.strftime('%Y-%m-%d'),
        'temperature': data.temperature,
        'humidity': data.humidity,
        'co2': data.co2,
        'luminance': data.luminance,
        'soi_humidity': data.soi_humidity
    }
    # 将数据转换为JSON格式
    # 返回JSON响应
    return JsonResponse(data_dict)


#   农田数据接口
def agriculture_list(req):
    data_obj = models.agriculture_info.objects.all()
    data = [models.agriculture_info.objects.count()]
    a = 0
    for i in data_obj:
        a += 1
        data_string = {
            'id': a,
            'name': i.name
        }
        data.append(data_string)
    return JsonResponse(data, safe=False)


class WateModels:
    def __init__(self):
        self.status = 0
        self.day = 1
        self.start_time = 0
        self.keep_time = 0


wate = WateModels()


#   水阀状态获取
def water_status(req):
    zt = req.GET.get('status')
    device = req.GET.get('id')
    if zt == 'true':
        mqtt_clinet.is_open(a=1, device=device)
    else:
        mqtt_clinet.is_open(a=0, device=device)
    print(device)
    return HttpResponse('OK')


#   定时灌溉接口
def wate_time(req):
    if req.method == 'GET':
        data_dict = {
            'day': wate.day,
            'start_time': wate.start_time,
            'keep_time': wate.keep_time,
        }
        return JsonResponse(data_dict)
    if req.method == 'POST' and req.content_type == 'application/json':
        data = json.loads(req.body)
        wate.day = data['day']
        wate.start_time = data['start_time']
        wate.keep_time = data['keep_time']
        return HttpResponse('OK')


# 定时灌溉阈值接口
def guangai_time(req):
    if req.method == 'GET':
        data_dict = {
            'water_status': guangai.water_status,
            'water_keeplive': guangai.water_keeplive,
            'temperature_is_valid': guangai.temperature_is_valid,
            'temperature_relation': guangai.temperature_relation,
            'temperature_value': guangai.temperature_value,
            'humidity_is_valid': guangai.humidity_is_valid,
            'humidity_releation': guangai.humidity_releation,
            'humidity_value': guangai.humidity_value,
            'co2_is_valid': guangai.co2_is_valid,
            'co2_relation': guangai.co2_relation,
            'co2_value': guangai.co2_value,
            'lumination_is_valid': guangai.lumination_is_valid,
            'lumination_relation': guangai.lumination_relation,
            'lumination_value': guangai.lumination_value,
            'soil_humidity_is_valid': guangai.soil_humidity_is_valid,
            'soil_humidity_relation': guangai.soil_humidity_relation,
            'soil_humidity_value': guangai.soil_humidity_value
        }
        return JsonResponse(data_dict)
    if req.method == 'POST' and req.content_type == 'application/json':
        data = json.loads(req.body)
        guangai.water_status = data['water_status']
        guangai.water_keeplive = data['water_keeplive']
        guangai.temperature_is_valid = data['temperature_is_valid']
        guangai.temperature_relation = data['temperature_relation']
        guangai.temperature_value = data['temperature_value']
        guangai.humidity_is_valid = data['humidity_is_valid']
        guangai.humidity_releation = data['humidity_releation']
        guangai.humidity_value = data['humidity_value']
        guangai.co2_is_valid = data['co2_is_valid']
        guangai.co2_relation = data['co2_relation']
        guangai.co2_value = data['co2_value'],
        guangai.lumination_is_valid = data['lumination_is_valid']
        guangai.lumination_relation = data['lumination_relation']
        guangai.lumination_value = data['lumination_value']
        guangai.soil_humidity_is_valid = data['soil_humidity_is_valid']
        guangai.soil_humidity_relation = data['soil_humidity_relation']
        guangai.soil_humidity_value = data['soil_humidity_value']
        return HttpResponse('OK')


#   历史数据接口
def histry_data(req):
    global list_data
    data_list = []
    data_test = req.GET.get('day')
    if data_test == '0':
        list_data = models.SensorMonitor_info.objects.order_by('-record_time')[:7]
    if data_test == '1':
        list_data = models.SensorMonitor_info.objects.order_by('-record_time')[:6]
    if data_test == '2':
        list_data = models.SensorMonitor_info.objects.order_by('-record_time')[:12]
    for i in list_data:
        data = {
            'temperature': i.temperature,
            'humidity': i.humidity,
            'co2': i.co2,
            'luminance': i.luminance,
            'soi_humidity': i.soi_humidity
        }
        data_list.append(data)
    return JsonResponse(data_list, safe=False)
