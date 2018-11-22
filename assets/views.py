from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from . import models
from . import asset_handler

# Create your views here.

@csrf_exempt
def report(request):
    """
    通过csrf_exempt装饰器，跳过django的csrf安全机制，让post的数据被接受，但是这又带来新的安全问题。
    可以通过客户端，使用自定义的认证的token，进行身份认证。这部分请工作，请根据实际情况自己进行。
    :param request:
    :return:
    """
    if request.method == "POST":
        asset_data = request.POST.get('asset_data')
        data = json.loads(asset_data)

        #各种数据检查， 请仔细添加和完善！
        if not data:
            return HttpResponse("没有数据!")
        if not issubclass(dict, type(data)):
            return HttpResponse("数据必须为字典格式!")

        # 是否携带关键的sn号
        sn = data.get('sn', None)
        if sn:
            # 进入审批流程
            # 首先判断是否在上线资产中存在该SN
            asset_obj = models.Asset.objects.filter(sn=sn)
            if asset_obj:
                #进入已上线资产的数据更新流程
                pass
                return HttpResponse("资产数据已经更新!")
            else:         #如果上线资产中没有，那么说明书未来审批资产， 进入新资产待审批区，更新或者创建资产.
                obj = asset_handler.NewAsset(request, data)
                response = obj.add_to_new_asset_zone()
                return HttpResponse(response)
        else:
            return HttpResponse("没有资产SN序列号,请检查数据!")
        #print(asset_data)
        #return HttpResponse("成功收到数据！")

from django.shortcuts import get_object_or_404

def index(request):
    assets = models.Asset.objects.all()
    return render(request, 'assets/index.html', locals())

# def dashboard(request):
#     total = models.Asset.objects.count()
#     upline = models.Asset.objects.filter(status=0).count()
#     offline = models.Asset.objects.filter(status=1).count()
#     unknown = models.Asset.objects.filter(status=2).count()
#     breakdown = models.Asset.objects.filter(status=3).count()
#     backup = models.Asset.objects.filter(status=4).count()
#     up_rate = round(upline/total*100)
#     o_rate = round(offline/total*100)
#     un_rate = round(unknown/total*100)
#     bd_rate = round(breakdown/total*100)
#     bu_rate = round(backup/total*100)
#     server_number = models.Server.objects.count()
#     networkdevice_number = models.NetworkDevice.objects.count()
#     storagedevice_number = models.SecurityDevice.objects.count()
#     securitydevice_number = models.SecurityDevice.objects.count()
#     software_number = models.Software.objects.count()
#
#     return render(request, 'assets/dashboard2.html', locals())


def dashboard(request):
    total = models.Asset.objects.count()
    upline = models.Asset.objects.filter(status=0).count()
    offline = models.Asset.objects.filter(status=1).count()
    unknown = models.Asset.objects.filter(status=2).count()
    breakdown = models.Asset.objects.filter(status=3).count()
    backup = models.Asset.objects.filter(status=4).count()
    up_rate = round(upline/total*100)
    o_rate = round(offline/total*100)
    un_rate = round(unknown/total*100)
    bd_rate = round(breakdown/total*100)
    bu_rate = round(backup/total*100)
    server_number = models.Server.objects.count()
    networkdevice_number = models.NetworkDevice.objects.count()
    storagedevice_number = models.StorageDevice.objects.count()
    securitydevice_number = models.SecurityDevice.objects.count()
    software_number = models.Software.objects.count()

    return render(request, 'assets/dashboard.html', locals())

def detail(request, asset_id):
    """
    以显示服务器类型资产详细为例，安全设备，存储设备，网络设备等参照比例
    :param request:
    :param asset_id:
    :return:
    """

    asset = get_object_or_404(models.Asset, id=asset_id)
    return render(request, 'assets/detail.html', locals())

