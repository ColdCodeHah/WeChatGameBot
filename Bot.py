import datetime
import random
import re
import time

from wxpy import *
import WeChatBot.SqlUser as SUser
import WeChatBot.SqlChengYu as SChengYu
from WeChatBot.DownMusic import Music
from WeChatBot.PicChengYu import PicChengyu
import threading

# 实例化，并登录微信

weixinqun=input('请输入机器人要接入的群名称：')

bot = Bot()

# 查找到要使用机器人来聊天的好友

my_friend0 = ensure_one(bot.search(weixinqun))
# my_friend1 = ensure_one(bot.search(u'大家庭'))
# my_friend2 = ensure_one(bot.search(u'伍零玖'))

# frind=bot.friends().search('雨雨')[0]

# tuling = Tuling(api_key='b93070f7cb7544588fa615cb8e264821')
# xiaoi = XiaoI('iiR9blobkej3', 'OtuLQuwCN2b9kgalFSvs')

chengyujielong=False#成语接龙是否开始
caishuzi=False #猜数字是否开始
shuzi=0   #猜数字的答案
caishuziCount=0   #本轮猜数的次数
caishuzimoney=0   #本轮猜数字奖池金额
startWord='三生三世十里桃花情之所契如铃合欢幸而有你此生不换天涯何处无方才何必单恋一枝花'
startCY=''
zhemo=['你指挥你的奴隶{0}去搬砖，一口气搬了200斤，为你赚取3金币','你的奴隶{0}去山西挖煤，为你赚取5金币','你的奴隶{0}搬砖的时候摔倒了，你支付了医药费3金币','你的奴隶{0}搬砖的时候和别人打了一架，你赔了5金币',
       '你指挥你的奴隶{0}去街头卖唱，动人的歌声吸引了很多听众为你赚取3金币','你使唤你的奴隶{0}去乞讨，为你讨到5金币','你指挥你的奴隶{0}去街头卖唱，结果一人听了心脏病突发你赔了3金币','你使唤你的奴隶{0}去乞讨，结果被路人抢劫，损失5金币']
taohao=['你帮你的主人{0}洗脚，主人一高兴，赏了你3金币','天气太热，你帮你的主人{0}打扇，主人给了你5金币','你帮你主人{0}洗脚，结果装的是开水，主人给了你最爱吃的大嘴巴子，并罚3金币','你帮你主人{0}打扇，结果主人感冒了，一气之下罚了你5金币',
        '你帮你主人{0}拖地，拖得一尘不染，主人一高兴给了你3金币','你为你主人{0}做饭，饭菜正合口味主人奖励你5金币','你帮你主人{0}拖地，结果地太滑主人摔倒罚了你3金币','你为你主人{0}做饭，结果主人食物中毒住院损失5金币']
anfu1=['你赏给你的奴隶{0}一块骨头，奴隶吃了后一口气搬了200斤砖为你赚取','你给你的奴隶{0}买了瓶可乐，奴隶一高兴将私房钱给了你']
anfu2=['你赏给你的奴隶{0}一块骨头，结果卡着了喉咙，送往医院医治了','你给你的奴隶{0}买了瓶可乐，结果因为可乐过期奴隶食物中毒抢救了']
picChengyAnswer=''#看图认成语的答案
picChengyStart=False#看图猜成语是否开始
naojjzwStart=False#脑筋急转弯是否开始
naojjzwAnswer=''#脑筋急转弯的答案
caizimiStart=False#猜字谜是否开始
caizimiAnswer=''#猜字谜答案
yizhandaodiStart=False#一站到底游戏是否开始
yizhandaodiAnswer=''#一站到底答案
yizhandaodiTime=None#一站到底结束时间
yizhandaodiPerson=''#发起一站到底的人
yizhandaodiIsBack=False#一站到底是否回答

@bot.register(chats=my_friend0,except_self=False)
# @bot.register(chats=my_friend1,except_self=False)
# @bot.register(chats=my_friend2,except_self=False)
def reply_my_friend(msg):
    global weixinqun
    global my_friend0
    global my_friend1
    global chengyujielong
    global startWord
    global startCY
    global caishuzi
    global shuzi
    global caishuziCount
    global caishuzimoney
    global zhemo
    global taohao
    global anfu1
    global anfu2
    global picChengyAnswer
    global picChengyStart
    global naojjzwAnswer
    global naojjzwStart
    global caizimiAnswer
    global caizimiStart
    global yizhandaodiStart
    global yizhandaodiAnswer
    global yizhandaodiTime
    global yizhandaodiPerson
    global yizhandaodiIsBack
    bakcStr=''
    name=msg.member.name
    qun=msg.chat.name
    print(msg.member.name+'：'+msg.text)

    if msg.text=='注册':
        try:
            info=SUser.UserSelect(name)
        except Exception as e:
            print(e)
        if info==None or len(info)<=0:
            SUser.UserInsert(name,qun)
            bakcStr='注册成功，初始金币100枚'
        else:
            bakcStr='你注册过了，不要重复注册'

    elif msg.text=='查询':
        ulchaxun=SUser.UserSelect(name)
        if ulchaxun==None or len(ulchaxun)==0:
            bakcStr='你没有注册'
        else:
            bakcStr='剩余金币：'+str(ulchaxun[2])+'枚'
            if ulchaxun[2]<=10:
                bakcStr+='，金币不足了，请联系群主。'
            if ulchaxun[3]!=0:
                ul1=SUser.UserSelect1(ulchaxun[3])
                bakcStr+='，你的主人：'+ul1[1]
            bakcStr+='，你的身价：'+str(ulchaxun[4])

    elif '转账' in msg.text and '@' in msg.text:
        ul=SUser.UserSelect(name)#查询自己信息
        if ul==None or len(ul)==0:
            bakcStr='你没有注册，转什么账'
        else:
            at=msg.text.index('@')
            try:
                money=int(msg.text[2:at])
                p=msg.text[at+1:len(msg.text)-1].replace(' ','')
                ulzhuan=SUser.UserSelect(p)
                if ulzhuan==None or len(ulzhuan)==0:
                    bakcStr='接收你转账的人不存在'
                else:
                    if money >0:
                        SUser.UserUpdateBalance(name,-money)
                        SUser.UserUpdateBalance(ulzhuan[1],money)
                        bakcStr='转账给 {0} {1} 金币成功'.format(p,money)
                    else:
                        bakcStr='你转账的金币还能更少点吗？'
            except:
                bakcStr='转账失败'

    elif msg.text=='猜数字':
        ulcaishuzi=SUser.UserSelect(name)
        if ulcaishuzi==None or len(ulcaishuzi)==0:
            bakcStr='你还没有注册'
        else:
            if ulcaishuzi[2]<=0:
                bakcStr='你金币不足了！'
            else:
                caishuzi=True
                shuzi=random.randint(1,200)
                caishuziCount=0
                caishuzimoney=0
                bakcStr='猜数字游戏开始啦，1-200之间，回复“我猜数值”'

    elif "我猜" in msg.text:
        try:
            if caishuzi==False:
               bakcStr='猜数字游戏还未开始！'
            else:
                ulwocai=SUser.UserSelect(name)
                if ulwocai==None or len(ulwocai)==0:
                    bakcStr='你还没有注册，不准猜！'
                else:
                    if ulwocai[2]<=caishuziCount:
                        bakcStr='你金币不足，不准猜！'
                    else:
                        num=re.sub('\D','',msg.text).replace(' ','')
                        if num==None or type(int(num))!=int:
                            return
                        if int(num)<shuzi:
                            caishuziCount+=1
                            SUser.UserUpdateBalance(name,-caishuziCount)
                            caishuzimoney+=caishuziCount
                            bakcStr='你猜的数字比答案小'+'，金币扣'+str(caishuziCount)+'枚'
                        elif int(num)>shuzi:
                            caishuziCount+=1
                            SUser.UserUpdateBalance(name,-caishuziCount)
                            caishuzimoney+=caishuziCount
                            bakcStr='你猜的数字比答案大'+'，金币扣'+str(caishuziCount)+'枚'
                        else:
                            SUser.UserUpdateBalance(name,40)
                            bakcStr='你猜对啦！答案为'+str(shuzi)+'，奖励金币40枚'
                            caishuzi=False
        except:
            pass

    elif msg.text=='奴隶':
        ulnuli=SUser.UserSelect(name)
        if ulnuli==None or len(ulnuli)==0:
            bakcStr='你还没有注册'
        else:
            ulnuli2=SUser.UserSelect2(ulnuli[0])
            if ulnuli2==None or len(ulnuli2)==0:
                bakcStr='你还没有奴隶'
            else:
                bakcStr='你的奴隶：\n'
                for r in ulnuli2:
                    sj=str(r[4])
                    n=r[1]
                    bakcStr+=r[1]+'，身价：'+str(r[4])
                    if r[5]!=None and r[5]!='':
                        worktime=datetime.datetime.strptime(r[5],'%Y-%m-%d %H:%M:%S')
                        nowTime=datetime.datetime.now()
                        if worktime>=nowTime:
                            bakcStr+=' 正在{0}'.format(r[6])
                    bakcStr+='\n'

    elif '买' in msg.text:
        atmai=msg.text.index('@')
        if atmai==1:
            p=msg.text[2:len(msg.text)-1].replace(' ','')
            ulmai=SUser.UserSelect(p)
            if ulmai==None or len(ulmai)==0:
                bakcStr='你要买的奴隶不存在'
            else:
                reBoss=ulmai[3] #原主人
                ulmaim=SUser.UserSelect(name)
                if ulmaim==None or len(ulmaim)==0:
                    bakcStr='你还没有注册'
                else:
                    if p in name:
                        bakcStr='你不能买自己'
                    elif ulmai[0]==ulmaim[3]:
                        bakcStr=p+'是你的主人，不能买'
                    elif ulmai[3]==ulmaim[0]:
                        bakcStr=p+'已经是你的奴隶了'
                    elif ulmaim[2]<ulmai[4]:
                        bakcStr='余额不足，买不起'
                    else:
                        cost=0
                        if ulmai[5]!=None and ulmai[5]!='':
                            worktime=datetime.datetime.strptime(ulmai[5],'%Y-%m-%d %H:%M:%S')
                            nowTime=datetime.datetime.now()
                            if worktime>=nowTime:
                                cost=ulmai[4]+int(ulmaim[4]/10)
                                bakcStr='你要买的奴隶正在'+ulmai[6]+'，你多花费了'+str(int(ulmaim[4]/10))+'金币，'
                            else:
                                cost=ulmai[4]
                        else:
                            cost=ulmai[4]
                        SUser.UserUpdateBalance(name,-cost) #花费金币
                        SUser.UserUpdateBoss(ulmaim[0],ulmai[1])  #易主
                        SUser.UserUpdateMoney(ulmai[4]+50,ulmai[1])#买一次  身价+50
                        if reBoss!=0:
                            ulremai=SUser.UserSelect1(reBoss)#查询原主人信息
                            SUser.UserUpdateBalance(ulremai[1],cost) #原主人获得金币
                        bakcStr+='你共花了'+str(cost)+'金币把'+p+'买回来了，可以尽情折磨啦'

    elif msg.text=='赎身':
        ulshushen=SUser.UserSelect(name)#查询自己信息
        if ulshushen==None or len(ulshushen)==0:
            bakcStr='你还没有注册'
        else:
            if ulshushen[2]<ulshushen[4]:
                bakcStr='你金币不够，赎不了身'
            else:
                bossulshushen=SUser.UserSelect1(ulshushen[3]) #查询主人信息
                if bossulshushen==None or len(bossulshushen)==0:
                    bakcStr='你还没有主人呢，可怜...'
                else:
                    cost=0
                    if ulshushen[5]!=None and ulshushen[5]!='':
                        worktime=datetime.datetime.strptime(ulshushen[5],'%Y-%m-%d %H:%M:%S')
                        nowTime=datetime.datetime.now()
                        if worktime>=nowTime:
                            cost=ulshushen[4]+int(ulshushen[4]/10)
                            bakcStr='因为你正在'+ulshushen[6]+'，你多花费了'+str(int(ulshushen[4]/10))+'金币，'
                        else:
                            cost=ulshushen[4]
                    else:
                        cost=ulshushen[4]
                    SUser.UserUpdateBalance(name,-cost)
                    SUser.UserUpdateBalance(bossulshushen[1],cost) #把钱交给主人
                    SUser.UserUpdateMoney(ulshushen[4]+50,name)  #修改身价  自由身 身价1
                    SUser.UserUpdateBoss(0,name) #易主  自由身
                    bakcStr='你共花了'+str(cost)+'金币把自己从主人那赎回来，现在你是自由身啦'

    elif msg.text=='逃跑':
        ultaopao=SUser.UserSelect(name)#查询自己信息
        if ultaopao==None or len(ultaopao)==0:
            bakcStr='你还没有注册'
        else:
            bossultaopao=SUser.UserSelect1(ultaopao[3]) #查询主人信息
            if bossultaopao==None or len(bossultaopao)==0:
                bakcStr='你还没有主人呢，不用逃跑'
            else:
                m=int(ultaopao[4]/10)
                if ultaopao[2]<=m:
                    bakcStr='你金币不足，跑不脱！'
                else:
                    jilv=random.randint(1,9)
                    if jilv==5:#1/10逃跑成功
                        SUser.UserUpdateMoney(1,name)  #修改身价  自由身 身价1
                        SUser.UserUpdateBoss(0,name) #易主  自由身
                        bakcStr='哈哈，恭喜！你成功逃离了主人的魔爪，现在自由啦！'
                    else:
                        SUser.UserUpdateBalance(name,-m)
                        SUser.UserUpdateBalance(bossultaopao[1],m)
                        bakcStr='你在逃跑的时候被主人抓回，痛打一顿之后罚款'+str(m)+'金币！'

    elif '折磨' in msg.text:
        ulzhemo=SUser.UserSelect(name)#查询自己信息
        if ulzhemo==None or len(ulzhemo)==0:
            bakcStr='你还没有注册'
        else:
            at=msg.text.index('@')
            if at==2:
                p=msg.text[3:len(msg.text)-1]
                ulnuli=SUser.UserSelect(p)
                if ulnuli==None or len(ulnuli)==0:
                    bakcStr='你要折磨的奴隶不存在'
                else:
                    if ulnuli[3]!=ulzhemo[0]:
                        bakcStr='你要折磨的人不是你的奴隶'
                    else:
                        ind=random.randint(0,7)
                        if ind==0:
                            SUser.UserUpdateBalance(name,3)
                        elif ind==1:
                            SUser.UserUpdateBalance(name,5)
                        elif ind==2:
                            SUser.UserUpdateBalance(name,-3)
                        elif ind==3:
                            SUser.UserUpdateBalance(name,-5)
                        elif ind==4:
                            SUser.UserUpdateBalance(name,3)
                        elif ind==5:
                            SUser.UserUpdateBalance(name,5)
                        elif ind==6:
                            SUser.UserUpdateBalance(name,-3)
                        elif ind==7:
                            SUser.UserUpdateBalance(name,-5)
                        bakcStr=zhemo[ind].format(ulnuli[1])

    elif msg.text=='讨好':
        ultaohao=SUser.UserSelect(name)#查询自己信息
        if ultaohao==None or len(ultaohao)==0:
            bakcStr='你还没有注册'
        else:
            bossul=SUser.UserSelect1(ultaohao[3]) #查询主人信息
            if bossul==None or len(bossul)==0:
                bakcStr='你还没有主人呢，找不到人讨好'
            else:
                ind=random.randint(0,7)
                if ind==0:
                    SUser.UserUpdateBalance(name,3)
                elif ind==1:
                    SUser.UserUpdateBalance(name,5)
                elif ind==2:
                    SUser.UserUpdateBalance(name,-3)
                elif ind==3:
                    SUser.UserUpdateBalance(name,-5)
                if ind==4:
                    SUser.UserUpdateBalance(name,3)
                elif ind==5:
                    SUser.UserUpdateBalance(name,5)
                elif ind==6:
                    SUser.UserUpdateBalance(name,-3)
                elif ind==7:
                    SUser.UserUpdateBalance(name,-5)
                bakcStr=taohao[ind].format(bossul[1])

    elif msg.text=='主人':
        ulzhurenm=SUser.UserSelect(name)#查询自己信息
        if ulzhurenm==None or len(ulzhurenm)==0:
            bakcStr='你还没有注册'
        else:
            ulzr=SUser.UserSelect1(ulzhurenm[3])
            if ulzr==None or len(ulzr)==0:
                bakcStr='你没有主人哦，你是自由的'
            else:
                bakcStr='你的主人是'+ulzr[1]

    elif '抢劫' in msg.text or '打劫' in msg.text:
        ul=SUser.UserSelect(name)#查询自己信息
        if ul==None or len(ul)==0:
            bakcStr='你还没有注册'
        else:
            at=msg.text.index('@')
            if at==2:
                p=msg.text[3:len(msg.text)-1]
                ind=random.randint(0,2)
                m=random.randint(1,5)
                if ind==0:
                    SUser.UserUpdateBalance(p,-m)
                    SUser.UserUpdateBalance(name,m)
                    bakcStr='抢劫'+p+'成功，抢到'+str(m)+'金币'
                else:
                    SUser.UserUpdateBalance(name,-m)
                    bakcStr='你抢劫'+p+'的时候被警察叔叔抓住，送进监狱并罚款'+str(m)+'金币'

    elif msg.text=='造反':
        ul=SUser.UserSelect(name)#查询自己信息
        if ul==None or len(ul)==0:
            bakcStr='你还没有注册，请先注册'
        else:
            ulzr=SUser.UserSelect1(ul[3])
            if ulzr==None or len(ulzr)==0:
                bakcStr='你没有主人，造毛线反'
            else:
                ind=random.randint(0,50)
                if ind==25:
                    SUser.UserUpdateMoney(ul[4]+50,name)  #修改身价
                    SUser.UserUpdateBoss(0,name) #易主  自由身
                    bakcStr='经过不断地抗争，终于造反成功！你已经逃离了主人的魔爪！'
                else:
                    if ul[5]!=None and ul[5]!='':
                        worktime=datetime.datetime.strptime(ul[5],'%Y-%m-%d %H:%M:%S')
                        nowTime=datetime.datetime.now()
                        if worktime>=nowTime:
                            SUser.UserUpdateBalance(name,-8)
                            SUser.UserUpdateBalance(ulzr[1],8)
                            bakcStr='你正在'+ul[6]+'，造反的时候被包工头暴揍一顿并罚金币8'
                        else:
                            SUser.UserUpdateBalance(name,-5)
                            SUser.UserUpdateBalance(ulzr[1],5)
                            bakcStr='你鼓动其他奴隶和你一起造反，结果造反当晚被其他奴隶出卖，被主人吊起打了三天三夜，并罚金币5！'

    elif '安抚' in msg.text:
        ulzhemo=SUser.UserSelect(name)#查询自己信息
        if ulzhemo==None or len(ulzhemo)==0:
            bakcStr='你还没有注册'
        else:
            at=msg.text.index('@')
            if at==2:
                p=msg.text[3:len(msg.text)-1]
                ulnuli=SUser.UserSelect(p)
                if ulnuli==None or len(ulnuli)==0:
                    bakcStr='你要安抚的奴隶不存在'
                else:
                    if ulnuli[3]!=ulzhemo[0]:
                        bakcStr='你要安抚的人不是你的奴隶'
                    else:
                        ind=random.randint(1,5)
                        ind1=random.randint(0,1)
                        ind2=random.randint(0,1)
                        if ind1==0:
                            bakcStr=anfu1[ind2].format(p)+str(ind)+'金币'
                            SUser.UserUpdateBalance(name,ind)
                        else:
                            bakcStr=anfu2[ind2].format(p)+str(ind)+'金币'
                            SUser.UserUpdateBalance(name,-ind)
    elif '打工' in msg.text:
        ul=SUser.UserSelect(name)#查询自己信息
        if ul==None or len(ul)==0:
            bakcStr='你还没有注册'
        else:
            at=msg.text.index('@')
            if at>2:
                work=msg.text[2:at]
                p=msg.text[at+1:len(msg.text)-1]
                ulnuli=SUser.UserSelect(p)
                if ulnuli==None or len(ulnuli)==0:
                    bakcStr='你要安排去打工的奴隶不存在'
                else:
                    if ulnuli[3]!=ul[0]:
                        bakcStr='你要安排去打工的人{0}不是你的奴隶'.format(ulnuli[1])
                    else:
                        canWork=False
                        if ulnuli[5]!=None and ulnuli[5]!='':
                            worktime=datetime.datetime.strptime(ulnuli[5],'%Y-%m-%d %H:%M:%S')
                            nowTime=datetime.datetime.now()
                            if worktime>=nowTime:
                                bakcStr='你的奴隶{0}正在拼命{1}，你不要太狠了'.format(ulnuli[1],ulnuli[6])
                                canWork=False
                            else:
                                canWork=True
                        else:
                            canWork=True
                        if canWork:
                            now = datetime.datetime.now()
                            delta = datetime.timedelta(hours=1)
                            wktime = now + delta
                            strwktime=wktime.strftime('%Y-%m-%d %H:%M:%S')
                            SUser.UserUpdateWork(ulnuli[1],strwktime,work)
                            SUser.UserUpdateFlag(ulnuli[1],0)#修改通知标识
                            bakcStr='你已经使唤你的奴隶{0}去{1}了，1小时后就可以给你带回工资啦'.format(ulnuli[1],work)

    elif msg.text=='成语接龙':
        ul=SUser.UserSelect(name)#查询自己信息
        if ul==None or len(ul)==0:
            bakcStr='你还没有注册，请先注册'
        else:
            index=random.randint(0,23)
            colCY=SChengYu.ChengYuSelectLike(startWord[index])
            if colCY==None or len(colCY)<=0:
                bakcStr='在准备开始成语接龙的时候，系统没有准备好初始成语，失败了，请重新试试吧'
                chengyujielong=False
            else:
                index=random.randint(0,len(colCY)-1)
                startCY=colCY[index]
                startCY=str(startCY).replace(' ','')
                bakcStr='成语接龙开始啦，我出 '+startCY+' 请回复 我接成语'
                chengyujielong=True

    elif '我接' in msg.text:
        ul=SUser.UserSelect(name)#查询自己信息
        if ul==None or len(ul)==0:
            bakcStr='你都没有注册，不准接'
        else:
            if not chengyujielong:
                bakcStr='成语接龙没有开始，请发送 成语接龙 开始游戏'
            else:
                if ul[2]<5:
                    bakcStr='金币不足，拒绝参加！'
                else:
                    answer=msg.text[2:len(msg.text)].replace(' ','')
                    if not answer[0]==startCY[len(startCY)-1]:
                        bakcStr='我认为你接错了，上交金币3'
                        SUser.UserUpdateBalance(name,-3)
                    else:
                        colCY=SChengYu.ChengYuSelectLike(answer)
                        if not len(colCY)>0:
                            bakcStr='我认为你接错了，上交金币3'
                            SUser.UserUpdateBalance(name,-3)
                        else:
                            colCY=SChengYu.ChengYuSelectLike(answer[len(answer)-1])
                            enableCol=[]
                            for item in colCY:
                                if item[0]==answer[len(answer)-1]:
                                    enableCol.append(item)
                            if not len(enableCol)>0:
                                bakcStr='你牛鼻，我居然也有词穷的时候，你yin了！奖励金币40'
                                SUser.UserUpdateBalance(name,40)
                                chengyujielong=False
                            else:
                                startCY=enableCol[random.randint(0,len(enableCol)-1)].replace(' ','').replace('\t','').replace('\n','')
                                bakcStr='算你对，赏你3金币。我接'+startCY
                                SUser.UserUpdateBalance(name,3)

    elif msg.text=='看图认成语':
        PY=PicChengyu()
        list=PY.GetPicAndCY()
        if list==None or len(list)<=0:
            bakcStr='生成图片失败了，再试一下吧'
        else:
            current=list[random.randint(0,len(list)-1)]
            if not PY.DownLoadPic(current[0]):
                bakcStr='生成图片失败了，再试一下吧'
            else:
                picChengyAnswer=current[1]
                msg.reply('@img@caichengyu.jpg')
                bakcStr='请看图片，发送 我认成语'
                picChengyStart=True

    elif '我认' in msg.text:
        ul=SUser.UserSelect(name)#查询自己信息
        if ul==None or len(ul)==0:
            bakcStr='你都没有注册，不准认'
        else:
            if not picChengyStart:
                bakcStr='看图认成语没有开始，请发送 看图认成语 开始游戏'
            else:
                if ul[2]<5:
                    bakcStr='金币不足，拒绝参加！'
                else:
                    answer=msg.text[2:len(msg.text)]
                    if answer!=picChengyAnswer:
                        bakcStr='你认错了！上交5金币！'
                        SUser.UserUpdateBalance(name,-5)
                    else:
                        bakcStr='牛鼻，你答对了，赏你5金币！'
                        SUser.UserUpdateBalance(name,5)
                        picChengyStart=False

    elif '点歌' in msg.text:
        ul=SUser.UserSelect(name)#查询自己信息
        if ul==None or len(ul)==0:
            bakcStr='你注都没有注册，不准点歌'
        else:
            songs=msg.text[2:len(msg.text)]
            if len(songs)>0:
                msg.reply('@'+name+'  请骚等，正在从百度、酷狗、酷我、QQ等各大网站盗取音乐《{0}》'.format(songs))
                mus=Music()
                if mus.GetMusic(songs):
                    msg.reply(mus.musicPath)
                else:
                    msg.reply('@'+name+'  盗取失败...')

    elif msg.text=='脑筋急转弯':
        ul=SUser.UserSelect(name)#查询自己信息
        if ul==None or len(ul)==0:
            bakcStr='你注都没有注册，还敢玩脑筋急转弯？'
        else:
            list=SChengYu.NaojjzwSelect()
            if list==None or len(list)<=0:
                bakcStr='生成脑筋急转弯题失败了，请再试一下吧'
            else:
                ind=random.randint(0,len(list)-1)
                bakcStr=list[ind][0]
                naojjzwAnswer=list[ind][1]
                naojjzwStart=True
                msg.reply('@'+name+'  出题如下，请发送 我答+答案 答题')

    elif '我答' in msg.text:
        ul=SUser.UserSelect(name)#查询自己信息
        if ul==None or len(ul)==0:
            bakcStr='你没有注册，你这个智商还敢答题？'
        else:
            if naojjzwStart==False:
                bakcStr='脑筋急转弯没有开始'
            elif ul[2]<5:
                bakcStr='金币不足，拒绝参加！'
            else:
                answer=msg.text[2:len(msg.text)]
                answer=answer.replace(' ','')
                count=0
                for s in answer:
                    if s not in naojjzwAnswer:
                        count+=1
                if count!=0 and len(naojjzwAnswer)/count>=5:#不得低于标准答案的1/5
                    bakcStr='答错！不解释！上交5金币'
                    SUser.UserUpdateBalance(name,-5)
                elif count!=0 and len(naojjzwAnswer)/count<3:#容错 1/3
                    bakcStr='答错！不解释！上交5金币'
                    SUser.UserUpdateBalance(name,-5)
                else:
                    bakcStr='好吧，算你牛鼻，赏你5金币'
                    SUser.UserUpdateBalance(name,5)
                    naojjzwStart=False

    elif msg.text=='字谜':
        ul=SUser.UserSelect(name)#查询自己信息
        if ul==None or len(ul)==0:
            bakcStr='你注都没有注册，不准玩！'
        else:
            row=[]
            ind=random.randint(1,4259)
            for i in range(0,3):
                row=SChengYu.ZimiSelect(ind)
                if row!=None and len(row)>0:
                    break
            if row==None or len(row)<=0:
                bakcStr='生成谜语失败，请重试一下吧'
            else:
                caizimiAnswer=row[1]
                bakcStr='字谜开始，发送 我打+谜底\n'+row[0]
                caizimiStart=True

    elif '我打' in msg.text:
        ul=SUser.UserSelect(name)#查询自己信息
        if ul==None or len(ul)==0:
            bakcStr='你没有注册，你这个智商还敢答题？'
        else:
            if caizimiStart==False:
                bakcStr='猜字谜游戏没有开始'
            elif ul[2]<5:
                bakcStr='金币不足，拒绝参加！'
            else:
                answer=msg.text[2:len(msg.text)].replace(' ','')
                if answer==caizimiAnswer:
                    bakcStr='好吧，算你对！金币+5'
                    SUser.UserUpdateBalance(name,5)
                    caizimiStart=False
                else:
                    bakcStr='答错！金币-5'
                    SUser.UserUpdateBalance(name,-5)

    elif msg.text=='一站到底':
        ul=SUser.UserSelect(name)#查询自己信息
        if ul==None or len(ul)==0:
            bakcStr='你注都没有注册，不准玩！'
        else:
            if ul[2]<5:
                bakcStr='金币不足，拒绝参加！'
            else:
                row=[]
                ind=random.randint(1,4991)
                row=SChengYu.YizhandaodiSelect(ind)
                if row!=None and len(row)>0:
                    yizhandaodiAnswer=row[1]
                    yizhandaodiPerson=name
                    now = datetime.datetime.now()
                    delta = datetime.timedelta(seconds=12)
                    yizhandaodiTime=now + delta
                    yizhandaodiIsBack=False
                    bakcStr='游戏开始啦，请发送 我选+答案 答题\n\n'
                    bakcStr+=row[0]+'\n\n'
                    bakcStr+='倒计时12s后还未答题，扣5金币！你只有一次机会！'
                    yizhandaodiStart=True
                    t=threading.Thread(target=runYizhandaodi,args=(2,))
                    t.start()

    elif '我选' in msg.text:
        ul=SUser.UserSelect(name)#查询自己信息
        if ul==None or len(ul)==0:
            bakcStr='你都没有注册，选个铲铲！'
        else:
            if yizhandaodiStart==False:
                bakcStr='一站到底游戏没有开始'
            elif ul[2]<5:
                bakcStr='金币不足，拒绝参加！'
            else:
                answer=msg.text[2:len(msg.text)].replace(' ','')
                answer=answer.upper()
                if answer==yizhandaodiAnswer:
                    bakcStr='好吧，算你对！金币+5'
                    SUser.UserUpdateBalance(name,5)
                    yizhandaodiStart=False
                    yizhandaodiIsBack=True
                else:
                    bakcStr='答错！金币-5'
                    SUser.UserUpdateBalance(name,-5)
                    yizhandaodiStart=False
                    yizhandaodiIsBack=True


    elif msg.text=='资产排行':
        list=SUser.UserSelectPaiHang(qun,'balance')
        if list!=None and len(list)>0:
            bakcStr='资产排行榜：\n'
            for row in list:
                bakcStr+=row[1]+' 金币：'+str(row[2])+'\n'

    elif msg.text=='身价排行':
        list=SUser.UserSelectPaiHang(qun,'money')
        if list!=None and len(list)>0:
            bakcStr='身价排行榜：\n'
            for row in list:
                bakcStr+=row[1]+' 身价：'+str(row[4])+'\n'

    elif msg.text=='菜单':
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




    if not bakcStr=='':
        msg.reply('@'+name+'  '+bakcStr)




def runCheck(tick):
    while True:
        list=SUser.UserSelectAll()
        if list!=None and len(list)>0:
            for row in list:
                if row[5]!=None and row[5]!='':
                    worktime=datetime.datetime.strptime(row[5],'%Y-%m-%d %H:%M:%S')
                    nowTime=datetime.datetime.now()
                    if (nowTime-worktime).seconds>=0 and (nowTime-worktime).seconds<=20:
                        ulzr=SUser.UserSelect1(row[3])
                        if ulzr!=None and len(ulzr)>0 and row[7]==0:
                            money=int(row[4]/10)
                            msg='@{0} 你的奴隶{1}{2}回来啦！并交给了你所有的工资{3}'.format(ulzr[1],row[1],row[6],money)
                            SUser.UserUpdateFlag(row[1],1)#修改通知标识
                            SUser.UserUpdateBalance(ulzr[1],money)
                            if row[8]==weixinqun:
                                my_friend0.send(msg)
                            # elif row[8]=='大家庭':
                            #     my_friend1.send(msg)
                            # elif row[8]=='伍零玖':
                            #     my_friend2.send(msg)
        time.sleep(tick)

def runYizhandaodi(tick):
    global yizhandaodiIsBack
    global yizhandaodiTime
    global yizhandaodiPerson
    global yizhandaodiStart
    while yizhandaodiIsBack==False:
        nowTime=datetime.datetime.now()
        if nowTime>yizhandaodiTime:
            SUser.UserUpdateBalance(yizhandaodiPerson,-5)
            yizhandaodiIsBack=True
            yizhandaodiStart=False
            row=SUser.UserSelect(yizhandaodiPerson)
            if row!=None and len(row)>0:
                if row[8]=='机器人':
                    my_friend0.send('@'+yizhandaodiPerson+' 一站到底倒计时结束，扣5金币')
                # elif row[8]=='大家庭':
                #     my_friend1.send('@'+yizhandaodiPerson+' 一站到底倒计时结束，扣5金币')
                # elif row[8]=='伍零玖':
                #     my_friend2.send('@'+yizhandaodiPerson+' 一站到底倒计时结束，扣5金币')
        time.sleep(tick)

t=threading.Thread(target=runCheck,args=(5,))
t.start()
embed()




