# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-07 08:54
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asset_type', models.CharField(choices=[('server', '服务器'), ('networkdevice', '网络设备'), ('storagedevice', '存储设备'), ('securitydevice', '安全设备'), ('software', '软件资产')], default='server', max_length=64, verbose_name='资产类型')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='资产名称')),
                ('sn', models.CharField(max_length=128, unique=True, verbose_name='资产序列号')),
                ('status', models.SmallIntegerField(choices=[(0, '在线'), (1, '下线'), (2, '未知'), (3, '故障'), (4, '备用')], default=0, verbose_name='设备状态')),
                ('manage_ip', models.GenericIPAddressField(blank=True, null=True, verbose_name='管理IP')),
                ('purchase_day', models.DateField(blank=True, null=True, verbose_name='购买日期')),
                ('expire_day', models.DateField(blank=True, null=True, verbose_name='过保日期')),
                ('price', models.FloatField(blank=True, null=True, verbose_name='价格')),
                ('memo', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('c_time', models.DateTimeField(auto_now_add=True, verbose_name='批准日期')),
                ('m_time', models.DateTimeField(auto_now=True, verbose_name='更新日期')),
                ('admin', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='admin', to=settings.AUTH_USER_MODEL, verbose_name='资产管理员')),
                ('approved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='approved_by', to=settings.AUTH_USER_MODEL, verbose_name='批准人')),
            ],
            options={
                'ordering': ['-c_time'],
                'verbose_name_plural': '资产总表',
                'verbose_name': '资产总表',
            },
        ),
        migrations.CreateModel(
            name='BusinessUnit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='业务线')),
                ('memo', models.CharField(blank=True, max_length=64, null=True, verbose_name='备注')),
                ('parent_unit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parent_level', to='assets.BusinessUnit')),
            ],
            options={
                'verbose_name_plural': '业务线',
                'verbose_name': '业务线',
            },
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sn', models.CharField(max_length=128, unique=True, verbose_name='合同号')),
                ('name', models.CharField(max_length=64, verbose_name='合同名称')),
                ('memo', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('price', models.IntegerField(verbose_name='合同金额')),
                ('detail', models.TextField(blank=True, null=True, verbose_name='合同详细')),
                ('start_day', models.DateField(blank=True, null=True, verbose_name='开始日期')),
                ('end_day', models.DateField(blank=True, null=True, verbose_name='失效日期')),
                ('license_num', models.IntegerField(blank=True, null=True, verbose_name='license数量')),
                ('c_day', models.DateField(auto_now_add=True, verbose_name='创建日期')),
                ('m_day', models.DateField(auto_now=True, verbose_name='修改日期')),
            ],
            options={
                'verbose_name_plural': '合同',
                'verbose_name': '合同',
            },
        ),
        migrations.CreateModel(
            name='CPU',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cpu_model', models.CharField(blank=True, default=True, max_length=128, verbose_name='CPU型号')),
                ('cpu_count', models.PositiveSmallIntegerField(default=1, verbose_name='物理CPU个数')),
                ('cpu_core_count', models.PositiveSmallIntegerField(default=1, verbose_name='CPU核数')),
                ('asset', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='assets.Asset')),
            ],
            options={
                'verbose_name_plural': 'CPU',
                'verbose_name': 'CPU',
            },
        ),
        migrations.CreateModel(
            name='Disk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sn', models.CharField(max_length=128, verbose_name='硬盘SN号')),
                ('slot', models.CharField(blank=True, max_length=64, null=True, verbose_name='所在插槽位')),
                ('model', models.CharField(blank=True, max_length=128, null=True, verbose_name='磁盘型号')),
                ('manufacturer', models.CharField(blank=True, max_length=128, null=True, verbose_name='磁盘制造商')),
                ('capacity', models.FloatField(blank=True, null=True, verbose_name='磁盘容量(GB)')),
                ('interface_type', models.CharField(choices=[('SATA', 'SATA'), ('SAS', 'SAS'), ('SCSI', 'SCSI'), ('unknown', 'unknown')], default='unknown', max_length=16, verbose_name='接口类型')),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Asset')),
            ],
            options={
                'verbose_name_plural': '硬盘',
                'verbose_name': '硬盘',
            },
        ),
        migrations.CreateModel(
            name='EventLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='事件名称')),
                ('event_type', models.SmallIntegerField(choices=[(0, '其他'), (1, '硬件变更'), (2, '新增配件'), (3, '设备上线'), (4, '设备上线'), (5, '定期维护'), (6, '业务上线/更新/变更')], default=4, verbose_name='事件类型')),
                ('component', models.CharField(blank=True, max_length=256, null=True, verbose_name='事件子项')),
                ('datail', models.TextField(verbose_name='事件详情')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='事件时间')),
                ('memo', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('asset', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='assets.Asset')),
            ],
            options={
                'verbose_name_plural': '事件记录',
                'verbose_name': '事件记录',
            },
        ),
        migrations.CreateModel(
            name='IDC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='机房名称')),
                ('memo', models.CharField(blank=True, max_length=128, null=True, verbose_name='备注')),
            ],
            options={
                'verbose_name_plural': '机房',
                'verbose_name': '机房',
            },
        ),
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='厂商名称')),
                ('telephone', models.CharField(blank=True, max_length=30, null=True, verbose_name='支持电话')),
                ('memo', models.CharField(blank=True, max_length=128, null=True, verbose_name='备注')),
            ],
            options={
                'verbose_name_plural': '厂商',
                'verbose_name': '厂商',
            },
        ),
        migrations.CreateModel(
            name='NetworkDevice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_asset_type', models.SmallIntegerField(choices=[(0, '路由器'), (1, '交换机'), (2, '负载均衡'), (4, 'VPN设备')], default=0, verbose_name='网络设备类型')),
                ('vlan_ip', models.GenericIPAddressField(blank=True, null=True, verbose_name='VLanIP')),
                ('intranet_ip', models.GenericIPAddressField(blank=True, null=True, verbose_name='内网IP')),
                ('model', models.CharField(blank=True, max_length=128, null=True, verbose_name='网络设备型号')),
                ('firmware', models.CharField(blank=True, max_length=128, null=True, verbose_name='设备固件版本')),
                ('port_num', models.SmallIntegerField(blank=True, null=True, verbose_name='端口个数')),
                ('device_detail', models.TextField(blank=True, null=True, verbose_name='详细配置')),
                ('asset', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='assets.Asset')),
            ],
            options={
                'verbose_name_plural': '网络设备',
                'verbose_name': '网络设备',
            },
        ),
        migrations.CreateModel(
            name='NewAssetApprovalZone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sn', models.CharField(max_length=128, unique=True, verbose_name='资产SN号')),
                ('asset_type', models.CharField(blank=True, choices=[('server', '服务器'), ('networkdevice', '网络设备'), ('storagedevice', '存储设备'), ('securitydevice', '安全设备'), ('IDC', '机房'), ('software', '软件资产')], default='server', max_length=64, null=True, verbose_name='资产类型')),
                ('manufacturer', models.CharField(blank=True, max_length=64, null=True, verbose_name='生产厂商')),
                ('model', models.CharField(blank=True, max_length=128, null=True, verbose_name='型号')),
                ('ram_size', models.PositiveIntegerField(blank=True, null=True, verbose_name='内存大小')),
                ('cpu_model', models.CharField(blank=True, max_length=128, null=True, verbose_name='CPU型号')),
                ('cpu_count', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('cpu_core_count', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('os_distribution', models.CharField(blank=True, max_length=64, null=True)),
                ('os_type', models.CharField(blank=True, max_length=64, null=True)),
                ('os_release', models.CharField(blank=True, max_length=64, null=True)),
                ('data', models.TextField(verbose_name='资产数据')),
                ('c_time', models.DateTimeField(auto_now_add=True, verbose_name='汇报日期')),
                ('m_time', models.DateTimeField(auto_now=True, verbose_name='数据更新日期')),
                ('approved', models.BooleanField(default=False, verbose_name='是否批准')),
            ],
            options={
                'ordering': ['-c_time'],
                'verbose_name_plural': '新上线待批准资产',
                'verbose_name': '新上线待批准资产',
            },
        ),
        migrations.CreateModel(
            name='NIC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=64, null=True, verbose_name='网卡名称')),
                ('model', models.CharField(max_length=128, verbose_name='网卡型号')),
                ('mac', models.CharField(max_length=64, verbose_name='MAC地址')),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True, verbose_name='IP地址')),
                ('net_mask', models.CharField(blank=True, max_length=64, null=True, verbose_name='掩码')),
                ('bonding', models.CharField(blank=True, max_length=64, null=True, verbose_name='绑定地址')),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Asset')),
            ],
            options={
                'verbose_name_plural': '网卡',
                'verbose_name': '网卡',
            },
        ),
        migrations.CreateModel(
            name='RAM',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sn', models.CharField(blank=True, max_length=128, null=True, verbose_name='SN号')),
                ('model', models.CharField(blank=True, max_length=128, null=True, verbose_name='内存型号')),
                ('manufacturer', models.CharField(blank=True, max_length=128, null=True, verbose_name='内存制造商')),
                ('slot', models.CharField(max_length=64, verbose_name='插槽')),
                ('capacity', models.IntegerField(blank=True, null=True, verbose_name='内存大小(GB)')),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Asset')),
            ],
            options={
                'verbose_name_plural': '内存',
                'verbose_name': '内存',
            },
        ),
        migrations.CreateModel(
            name='SecurityDevice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_asset_type', models.SmallIntegerField(choices=[(0, '防火墙'), (1, '入侵检测设备'), (2, '互联网网关'), (4, '运维审计系统')], default=0, verbose_name='安全设备类型')),
                ('asset', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='assets.Asset')),
            ],
            options={
                'verbose_name_plural': '安全设备',
                'verbose_name': '安全设备',
            },
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_asset_type', models.SmallIntegerField(choices=[(0, 'PC服务器'), (1, '刀片机'), (2, '小型机')], default=0, verbose_name='服务器类型')),
                ('created_by', models.CharField(choices=[('auto', '自动添加'), ('manual', '手工录入')], default='auto', max_length=32, verbose_name='添加方式')),
                ('model', models.CharField(blank=True, max_length=128, null=True, verbose_name='服务器型号')),
                ('raid_type', models.CharField(blank=True, max_length=512, null=True, verbose_name='Raid类型')),
                ('os_type', models.CharField(blank=True, max_length=64, null=True, verbose_name='操作系统类型')),
                ('os_distribution', models.CharField(blank=True, max_length=64, null=True, verbose_name='发行版本')),
                ('os_release', models.CharField(blank=True, max_length=64, null=True, verbose_name='操作系统版本')),
                ('asset', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='assets.Asset')),
                ('hosted_on', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hosted_on_server', to='assets.Server', verbose_name='宿主机')),
            ],
            options={
                'verbose_name_plural': '服务器',
                'verbose_name': '服务器',
            },
        ),
        migrations.CreateModel(
            name='Software',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_asset_type', models.SmallIntegerField(choices=[(0, '操作系统'), (1, '办公/开放软件'), (2, '业务软件')], default=0, verbose_name='软件类型')),
                ('license_num', models.IntegerField(default=1, verbose_name='授权数量')),
                ('version', models.CharField(help_text='例如: Centos release 6.7 (Final)', max_length=64, unique=True, verbose_name='软件/系统版本')),
            ],
            options={
                'verbose_name_plural': '软件系统',
                'verbose_name': '软件/系统',
            },
        ),
        migrations.CreateModel(
            name='StorageDevice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_asset_type', models.SmallIntegerField(choices=[(0, '磁盘阵列'), (1, '网络存储器'), (2, '磁带库'), (4, '磁带机')], default=0, verbose_name='存储设备类型')),
                ('asset', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='assets.Asset')),
            ],
            options={
                'verbose_name_plural': '存储设备',
                'verbose_name': '存储设备',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True, verbose_name='标签名')),
                ('c_day', models.DateField(auto_now_add=True, verbose_name='创建日期')),
            ],
            options={
                'verbose_name_plural': '标签',
                'verbose_name': '标签',
            },
        ),
        migrations.AddField(
            model_name='eventlog',
            name='new_asset',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='assets.NewAssetApprovalZone'),
        ),
        migrations.AddField(
            model_name='eventlog',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='事件执行人'),
        ),
        migrations.AddField(
            model_name='asset',
            name='business_unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='assets.BusinessUnit', verbose_name='所属业务线'),
        ),
        migrations.AddField(
            model_name='asset',
            name='contract',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='assets.Contract', verbose_name='合同'),
        ),
        migrations.AddField(
            model_name='asset',
            name='idc',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='assets.IDC', verbose_name='所在机房'),
        ),
        migrations.AddField(
            model_name='asset',
            name='manufacturer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='assets.Manufacturer', verbose_name='制造商'),
        ),
        migrations.AddField(
            model_name='asset',
            name='tags',
            field=models.ManyToManyField(blank=True, to='assets.Tag', verbose_name='标签'),
        ),
        migrations.AlterUniqueTogether(
            name='ram',
            unique_together=set([('asset', 'slot')]),
        ),
        migrations.AlterUniqueTogether(
            name='nic',
            unique_together=set([('asset', 'model', 'mac')]),
        ),
        migrations.AlterUniqueTogether(
            name='disk',
            unique_together=set([('asset', 'sn')]),
        ),
    ]
