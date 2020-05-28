# lmyAutoCheckIn
蓝墨云班课自动签到
基于 [SurelySomeday/lmyAutoCheckIn](https://github.com/SurelySomeday/lmyAutoCheckIn) 项目的修改

改动如下：
- 稍微优化一下代码
- 调高写在代码里的版本号，3.1.x因为太老有可能成为特征，现在只有login接口仍然是和3.1.x版本号，那个接口在高版本签名规则好像改了
- 仅保留签到功能
- 修改签到服务器地址，原来的不能用了
- 签到轮训机制优化

## 食用说明
### 下载源码
```bash
git clone --depth=1 https://github.com/hunshcn/lmyAutoCheckIn
```
### 修改config.json
#### 全局参数

| 参数 | 备注 |
| ----  | ---- |
| username | 用户名 |
| password | 密码 |
| device_code | 设备随机码，示例配置里给了一个，我随便手敲的，建议自己随机一个，长度按照给的来就行 |
| sleep_time | 轮询间隔，默认30秒，不建议调快，会触发检测 |
| dingding | 用以通知的钉钉机器人token，如果不知道是什么请放空 |
| lat | 经度 |
| lng | 纬度 经纬度可以放空，教师端显示未获取位置|
| class | 课程数组 |

#### 课程参数

| 参数 | 备注 |
| ----  | ---- |
| location | 经纬度，默认使用全局参数，如果不需要课程特定位置请不要添加此key |
| days | List[int] 每周几检测这个课程 |
| start | 如果符合days参数，几点几分开始检测，24小时制，格式：[hour, minute] |
| end | 如果符合days参数，几点几分结束检测，24小时制，格式：[hour, minute] |

#### 示例配置
初级
```json
{
    "username": "",
    "password": "",
    "lat": "",
    "lng": "",
    "device_code": "9d9a8yra_3rrs_ooe0_3jdo_eaej0393jvox",
    "class":[
        {
            "id": "83196437-1234-1234-1234-123456789012",
            "days": [4],
            "start": [9,0],
            "end": [9,20]
        },
        {
            "id": "83196437-1234-1234-1234-123456789012",
            "days": [3],
            "start": [7,55],
            "end": [8,2]
        }
    ]
}
```

高级
```json
{
    "username": "",
    "password": "",
    "lat": "",
    "lng": "",
    "dingding": "yourtokenhere",
    "sleep_time": 30,
    "device_code": "9d9a8yra_3rrs_ooe0_3jdo_eaej0393jvox",
    "class":[
        {
            "id": "83196437-1234-1234-1234-123456789012",
            "days": [4],
            "start": [9,0],
            "end": [9,20],
            "location": {"lat": 29.1234, "lng": 119.1234}
        }
    ]
}
```
这个是每周四、9:00~9:20每隔30秒检测一次，发送位置信息(29.1234, 119.1234)，签到成功后发送钉钉提醒

### 注意
间隔快了可能会受到提醒短信，但是好像也没什么事就是了...

同一时刻多门课同时签到暂不支持，也不打算支持，有需要请自行pr

device_code随便敲是为了过于明显的特征，同样的可能也有ua，如果要改自己代码里改一下