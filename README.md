# WeChatGameBot
简单好玩的微信游戏机器人（使用wxpy）
这个软件使用了wxpy支持库

dist里有使用PyInstaller打包好的程序，运行输入群名然后扫描登录就一切OK了，具体的游戏说明在下面：


        bakcStr='[注册]注册账号，进行游戏，但不准注销\n'
        bakcStr+='[查询]显示你的账号信息\n'
        bakcStr+='[资产排行][身价排行]查询资产、身价排行\n'
        bakcStr+='[转账+数字+@昵称]进行转账操作\n'
        bakcStr+='[猜数字]开始猜数字游戏，回复[我猜+数字]答题\n'
        bakcStr+='[成语接龙]开始成语接龙游戏，回复[我接+成语]答题\n'
        bakcStr+='[看图认成语]进行看图片认成语游戏，回复[我认+成语]答题\n'
        bakcStr+='[脑筋急转弯]进行脑筋急转弯答题游戏，回复[我答+答案]答题\n'
        bakcStr+='[字谜]进行猜字谜游戏，回复[我打+谜底]答题\n'
        bakcStr+='[一站到底]进行一站到底抢答题目游戏，回复[我选+选项]答题\n'
        bakcStr+='[点歌+歌名]点歌功能\n'
        bakcStr+='\n以下为好友买卖奴隶游戏功能菜单：\n'
        bakcStr+='[奴隶]查询自己名下的奴隶名单[主人]查询自己的主人[买@昵称]将某人买回名下做奴隶[赎身]花费金币赎身'
        bakcStr+='[打工+工作+@昵称]指挥奴隶去打工，如：打工挖煤@张三'
        bakcStr+='[逃跑][折磨][讨好][造反][安抚][抢劫]'
