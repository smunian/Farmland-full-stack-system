
from django.db import models
from django.utils import timezone
from dateutil.relativedelta import relativedelta


# Create your models here.
class User_info(models.Model):
    username = models.CharField(max_length=32, primary_key=True, default='')
    password = models.CharField(max_length=512, default='')  # 注意：在实际应用中应该使用更安全的密码处理方式
    email = models.EmailField(max_length=32, default='')


class agriculture_info(models.Model):  # 农田信息表
    name = models.CharField(max_length=32, primary_key=True, default='')
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    user_info = models.ForeignKey(User_info, on_delete=models.CASCADE, related_name='agriculture_infos', default='')


class device(models.Model):  # 硬件数据表
    device_id = models.CharField(max_length=32, primary_key=True, default='')  # 设备id
    device_name = models.CharField(max_length=32, default='')  # 设备名
    device_location = models.CharField(max_length=32, default='')  # 设备位置
    device_state = models.BooleanField(default='')  # 是否在线，移除了不必要的 max_length
    device_creation_date = models.DateTimeField(auto_now_add=True)
    last_online = models.DateTimeField(default='', null=True)
    # 确保 agriculture_info 是 AgricultureInfo 模型的引用
    agriculture_info = models.ForeignKey(agriculture_info, on_delete=models.CASCADE, related_name='device_info',
                                         default='')


class device_history(models.Model):
    device = models.ForeignKey(device, on_delete=models.CASCADE, related_name='history', default='')
    device_online = models.DateTimeField(null=True)  # 在线时间
    device_offline = models.DateTimeField(null=True, blank=True)  # 离线时间
    duration = models.IntegerField(null=True, blank=True, help_text="在线时长（分钟）")


class SensorMonitor_info(models.Model):  # 硬件传感器数据表
    # uuid=models.CharField(max_length=32, primary_key=True, default='')
    record_time = models.DateTimeField(primary_key=True, auto_now=True)  # 获取时间
    temperature = models.FloatField(default='')  # 温度
    humidity = models.FloatField(default='')  # 湿度
    co2 = models.FloatField(default='')  # 二氧化碳
    luminance = models.FloatField(default='')  # 光照度
    soi_humidity = models.FloatField(default='')  # 土壤湿度
    device_info = models.ForeignKey(device, on_delete=models.CASCADE, related_name='sensor_monitor_info',
                                    default='')  # 设备信息关联


class IrrigationCycle(models.Model):
    CYCLE_CHOICES = (
        ('D', 'Daily'),
        ('W', 'Weekly'),
        ('M', 'Monthly'),
        ('Y', 'Yearly'),
    )
    name = models.CharField(max_length=1, choices=CYCLE_CHOICES)


class IrrigationSchedule(models.Model):
    device = models.ForeignKey(device, on_delete=models.CASCADE, related_name='irrigation_schedules')
    start_time = models.TimeField()
    duration = models.IntegerField()
    cycle = models.CharField(max_length=10,
                             choices=[('day', 'Day'), ('week', 'Week'), ('month', 'Month'), ('year', 'Year'), ])
    next_execution_date = models.DateField(null=True, blank=True)
    is_enabled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.device.name} - {self.cycle} - {self.start_time}"

    def calculate_next_execution_date(self):
        if self.is_enabled:
            if self.cycle == 'day':
                return self.next_execution_date + relativedelta(days=1)
            elif self.cycle == 'week':
                return self.next_execution_date + relativedelta(weeks=1)
            elif self.cycle == 'month':
                return self.next_execution_date + relativedelta(months=1)
            elif self.cycle == 'year':
                return self.next_execution_date + relativedelta(years=1)
        return None  # 如果灌溉计划被禁用，则返回None

    def save(self, *args, **kwargs):
        if not self.next_execution_date:
            self.next_execution_date = timezone.now().date()
        self.next_execution_date = self.calculate_next_execution_date() if self.is_enabled else None
        super().save(*args, **kwargs)
# class api_irrigationschedule_info(models.Model):
#     SCHEDULE_TYPE_CHOICES = (
#         ('每天定时', '每天定时'),
#         ('每周定时', '每周定时'),
#         ('每月定时', '每月定时'),
#         ('每年定时', '每年定时'),
#     )
#     schedule_type = models.CharField(max_length=50, choices=SCHEDULE_TYPE_CHOICES)
#     valve_control = models.CharField(max_length=10, choices=(('开启', '开启'), ('关闭', '关闭')))
#     start_time = models.CharField(max_length=50)
#     duration = models.CharField(max_length=50)
#
#
# class ThresholdIrrigation(models.Model):
#     VALVE_CONTROL_CHOICES = (
#         ('开启', '开启'),
#         ('关闭', '关闭'),
#     )
#     TEMPERATURE_THRESHOLD_CHOICES = (
#         ('大于', '大于'),
#         ('小于', '小于'),
#     )
#     HUMIDITY_THRESHOLD_CHOICES = TEMPERATURE_THRESHOLD_CHOICES
#     CO2_THRESHOLD_CHOICES = TEMPERATURE_THRESHOLD_CHOICES
#     LIGHT_THRESHOLD_CHOICES = TEMPERATURE_THRESHOLD_CHOICES
#     SOIL_MOISTURE_THRESHOLD_CHOICES = TEMPERATURE_THRESHOLD_CHOICES
#
#     id = models.AutoField(primary_key=True)
#     valve_control = models.CharField(max_length=10, choices=VALVE_CONTROL_CHOICES)
#     valve_hold_time = models.IntegerField()
#     temperature_threshold = models.CharField(max_length=10, choices=TEMPERATURE_THRESHOLD_CHOICES)
#     temperature_value = models.FloatField()
#     humidity_threshold = models.CharField(max_length=10, choices=HUMIDITY_THRESHOLD_CHOICES)
#     humidity_value = models.FloatField()
#     co2_threshold = models.CharField(max_length=10, choices=CO2_THRESHOLD_CHOICES)
#     co2_value = models.FloatField()
#     light_threshold = models.CharField(max_length=10, choices=LIGHT_THRESHOLD_CHOICES)
#     light_value = models.FloatField()
#     soil_moisture_threshold = models.CharField(max_length=10, choices=SOIL_MOISTURE_THRESHOLD_CHOICES)
#     soil_moisture_value = models.FloatField()
