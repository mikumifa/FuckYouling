
# 友邻优课 题目爬虫

外刊时文 2023 题库

> 由于爬单一题库, 不需要破解sign
>
> 不过还是破解了

## Data
course_data里面是题库
couse_data_temp.csv里面有具体的详细信息
## Sign

下面是各种地方来的各种和sign有关代码

<details> 
<summary>下拉</summary> 

```
    public String l(String str) {
        return s.a("buildversion=23102601&timestamp=" + str + "&salt=183846cdf0cA3ba5");
    }

```

```
public class s {
    public static String a(String str) {
        char[] cArr = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f'};
        try {
            byte[] bytes = str.getBytes();
            MessageDigest messageDigest = MessageDigest.getInstance("MD5");
            messageDigest.update(bytes);
            byte[] digest = messageDigest.digest();
            char[] cArr2 = new char[digest.length * 2];
            int i2 = 0;
            for (byte b2 : digest) {
                int i3 = i2 + 1;
                cArr2[i2] = cArr[(b2 >>> 4) & 15];
                i2 = i3 + 1;
                cArr2[i3] = cArr[b2 & Ascii.SI];
            }
            return new String(cArr2);
        } catch (Exception e2) {
            e2.printStackTrace();
            return null;
        }
    }
}
```

```
        Map<String, Object> hashMap = new HashMap<>();
            if (a2 instanceof t) {
                int i2 = 0;
                while (true) {
                    t tVar = (t) a2;
                    if (i2 >= tVar.size()) {
                        break;
                    }
                    hashMap.put(tVar.a(i2), tVar.b(i2));
                    i2++;
                }
                hashMap.toString();
            } else {
                i.f fVar = new i.f();
                a2.writeTo(fVar);
                hashMap = z.b(fVar.d0());
            }
            k2 = m(hashMap);

```

```

    public String m(Map<String, Object> map) {
        int i2;
        try {
            String[] strArr = (String[]) map.keySet().toArray(new String[0]);
            Arrays.sort(strArr);
            StringBuilder sb = new StringBuilder();
            int length = strArr.length;
            while (i2 < length) {
                String str = strArr[i2];
                if (map.get(str) instanceof String) {
                    String str2 = (String) map.get(str);
                    if (str2.contains("[")) {
                        i2 = str2.contains("]") ? i2 + 1 : 0;
                    }
                    if (str2.contains("{") && str2.contains("}")) {
                    }
                }
                if (map.get(str) != null && !"".equals(map.get(str)) && !(map.get(str) instanceof ArrayList) && !n(map.get(str))) {
                    sb.append(str);
                    sb.append(ContainerUtils.KEY_VALUE_DELIMITER);
                    sb.append(map.get(str));
                    sb.append(ContainerUtils.FIELD_DELIMITER);
                }
            }
            sb.append("timestamp");
            sb.append(ContainerUtils.KEY_VALUE_DELIMITER);
            sb.append(this.f11807f);
            sb.append(ContainerUtils.FIELD_DELIMITER);
            String c2 = com.zhuomogroup.ylyk.utils.k.c();
            if (r.b(c2)) {
                sb.append("userid");
                sb.append(ContainerUtils.KEY_VALUE_DELIMITER);
                sb.append(c2);
                sb.append(ContainerUtils.FIELD_DELIMITER);
            }
            sb.append("salt");
            sb.append(ContainerUtils.KEY_VALUE_DELIMITER);
            sb.append("$KJSD&)2TSz8M$oF");
            return s.a(sb.toString());
        } catch (Exception e2) {
            CrashReport.postCatchedException(e2);
            com.blankj.utilcode.util.p.j(">>>>>>>>>>>>>>>exception:" + e2.toString());
            return "";
        }
    }
}
```

```
function getSign505(data, timestamp) {
  // 505强校验:body对象的参数拼接成字符串+salt的值,进行 md5
  // 客户端校验能通过
  // 但是H5端加了个buildVersion参与校验,导致校验不通过
  // 目前来说,大部分接口都是不走该校验方式,不确定哪个接口走 505 校验
  // 2022年06月17日  讲userid拼进去
  let sign = ''
  const salt = '$KJSD&)2TSz8M$oF'
  if (!data) data = {}
  // if (appUser && appUser.userId) data.userid = appUser.userId
  // data.timestamp = timestamp
  let keys = Object.keys(data)
  // 排序
  keys = keys.sort()
  // 排除空字段
  keys = keys.filter(key => {
    const value = data[key]
    const type = typeof value
    const isNotObj = type !== 'object' || !(type instanceof Date)
    return isNotObj && value != null && value !== ''
  })
  keys.forEach(key => {
    let value = data[key]
    if (value instanceof Date) value = JSON.stringify(value).replace(/"+/g, '')
    sign += `${key}=${value}&`
  })
  // console.log(
  //   `${sign}timestamp=${timestamp}${appUser && appUser.userId ? `&userid=${appUser.userId}` : ''}&salt=${salt}`,
  //   ';;;;;'
  // )
  sign = md5(
    `${sign}timestamp=${timestamp}${appUser && appUser.userId ? `&userid=${appUser.userId}` : ''}&salt=${salt}`
  )
  // sign = md5(`${sign}salt=${salt}`)
  return { sign505: sign }
}

```

```
export function getHeaderUser(data, options) {
  if (data && options) {
    // 为 data 计算 uuid
    if (options.uuid && data.uuid) {
      data.uuid = uuidv4()
    }
  }
  const buildVersion = parseInt(appUser.buildVersion) || new Date().toFormattedString('yyMMdd01') // 默认值
  const timestamp = parseInt(new Date().getTime() / 1000)
  // sign.type/: 1 仅验证时间戳；2 验证请求参数
  const type = pageArgs.args().signType || 1
  const sign = getSign({ buildVersion, timestamp, data, type })
  return {
    ...(appUser.userId ? { userId: appUser.userId } : {}), // 匿名页面没有用户参数
    ...{ accountId: appUser.appName || 'default' }, // 平台标识
    version: appUser.version,
    token: appUser.token,
    channel: appUser.channel,
    buildVersion, // ios 需要的参数
    timestamp,
    deviceId: appUser.deviceId,
    anonymousId: appUser.anonymousId || getCookie('anonymousId'),
    ...sign
  }
}
```
</details>

Sign签名是` buildversion=23102601&timestamp=" + str + "&salt=183846cdf0cA3ba5`

Sign505是 请求体参数加上时间戳和用户ID和salt

>  请求问题题目不需要sign505
>
> sign的buildversion是写死的
