# You need to customize the path of the materials
# 你需要自己复制资源路径
# 1.导入必要的库并做实例化
import pygame,random,time
pygame.init()
pygame.key.set_repeat(1,1)
# 2.设置窗口参数
bg_width = 400  # 设置窗口宽度
bg_height = 700 # 设置窗口高度
running = True
# 3.设置窗口大小
sc = pygame.display.set_mode((bg_width,bg_height))
# 4.加载图片
bg = pygame.image.load("C:\\mxcmaterials\\飞机大战-bg-6495b162-e6cc-4921-86b2-347c7886383c.png")
pygame.mixer.music.load("C:\\mxcmaterials\\飞机大战-bgm-3fb8a304-cf74-4343-8a80-04f369f2e374.wav")
# 重复播放背景音乐
pygame.mixer.music.play(-1)
# 设置音量，0.0-1.0之间，0.0是静音，1.0是最大声音
pygame.mixer.music.set_volume(0.1)
# 3.6 加载音效
bullet_sound = pygame.mixer.Sound("C:\\mxcmaterials\\飞机大战-bullet-a3696130-2db3-4038-87ef-e5e1b1de9821.wav")
# 设置音效音量
bullet_sound.set_volume(0.3)

###### 4.5 添加战机和敌机击毁的音效
ed = pygame.mixer.Sound("C:\\mxcmaterials\\飞机大战-enemy_D-fbf76277-1523-4d18-84ac-f09acad3f89f.wav") # 敌机被摧毁的音效
ed.set_volume(0.3)
hd = pygame.mixer.Sound("C:\\mxcmaterials\\飞机大战-hero_D-38080960-a048-49b8-80d3-21bc477dfd3f.wav")
hd.set_volume(0.3)
# 5.5 大型敌机音效
big_enemy_flying = pygame.mixer.Sound("C:\\mxcmaterials\\飞机大战-bigE_f-1b67ee77-a427-4932-a5f6-b2785ffb9e03.wav")
big_enemy_flying.set_volume(0.3)
big_enemy_Ds=pygame.mixer.Sound("C:\\mxcmaterials\\飞机大战-bigE_D-63870e30-83d5-42f0-b351-9baabb472d40.wav")
big_enemy_Ds.set_volume(0.3)
# 拓展 空中补给音效
supply_falling_sound = pygame.mixer.Sound("C:\\mxcmaterials\\飞机大战-supply-ae2bfabc-e270-4a53-8758-0fbd79a3ba1f.wav")
supply_falling_sound.set_volume(0.3)
# 定义主战机类
class HeroPlane( ):
    def __init__(self ): # 构造函数
        #载入生存和坠毁图片
        
        self.image = pygame.image.load("C:\\mxcmaterials\\飞机大战-hero_1-6f8059af-7855-4db9-a8bf-895e61ef4adb.png")
        # 知识进阶：1.两种造型
        self.image1 = pygame.image.load("C:\\mxcmaterials\\飞机大战-hero_1-6f8059af-7855-4db9-a8bf-895e61ef4adb.png")
        self.image2 = pygame.image.load("C:\\mxcmaterials\\飞机大战-hero_2-5ecbfeaa-57c1-4474-9cd8-6dd692e6f6e5.png")
        # 2.设置形态之间转换的开关
        self.switch_image = False # 交换器开关关闭
        self.down_image = pygame.image.load("C:\\mxcmaterials\\飞机大战-hero_D-872c6d71-4075-4385-91a8-7b022d98f0a9.png")
        # 获取自身的矩形对象，方便的存储和操作矩形区域
        self.rect = self.image.get_rect()
        # 初始化位置
        self.rect.left = 150 # 矩形左边的x坐标
        self.rect.top = 500  # 矩形顶部的y坐标
        # 初始化移动速度
        self.speed = 3
        self.active = True # 是否存活
    def moveUp(self):
        # 矩形顶部的y坐标
        if self.rect.top>0:
            self.rect.top -= self.speed
        else:
            self.rect.top = 0
    def moveDown(self):
        # 矩形底部的y坐标
        # 为了效果更好 所以让它距离底端60
        if self.rect.bottom < bg_height-60:
            self.rect.top += self.speed
        else:
            self.rect.bottom = bg_height-60
    def moveLeft(self):
        # 矩形左边的x坐标
        if self.rect.left > 0:
            self.rect.left -= self.speed
        else:
            self.rect.left = 0
    def moveRight(self):
        # 矩形右边的x坐标
        if self.rect.right < bg_width:
            self.rect.left += self.speed
        else:
            self.rect.right = bg_width
# 2.1 设计敌战机
class Enemy():
    def __init__(self ):
        #载入生存和坠毁图片
        self.image = pygame.image.load("C:\\mxcmaterials\\飞机大战-enemy-45722412-8891-4d4b-8f1c-4395735489c4.png")
        self.down_image = pygame.image.load("C:\\mxcmaterials\\飞机大战-enemy_D-1081edba-70ec-4d8a-959c-6737cd333b50.png")
        # 获取自身的矩形对象，方便的存储和操作矩形区域
        self.rect = self.image.get_rect()
        # 初始化位置
        self.rect.left = random.randint(0,bg_width-57) # 矩形左边的x坐标
        self.rect.top = random.randint(-5*bg_height,-43)  # 矩形顶部的y坐标
        # 初始化移动速度
        self.speed = 1
        self.active=True # 是否存活 
    # 设计移动的方法
    def move(self):
        if self.rect.top<bg_height:
            self.rect.top+=self.speed
        else:
            self.reset() # 一旦到达底部，使用重置方法回到顶部，进行新的降落
    # 重置
    def reset(self):
        self.active=True # 状态：生存
        self.rect.left=random.randint(0,bg_width-57) # 宽度和高度范围内随机下落
        self.rect.top=random.randint(-5*bg_height,100)
# 5.1 设计大敌机类
class BigEnemy( ):
    energy = 10 # 能量值
    def __init__(self ): # 构造函数，存储属性
        # 大敌机不是一颗子弹就能击毁，需要设置能量值
        self.energy = BigEnemy.energy
        # 载入生存和坠毁图片
        self.image = pygame.image.load("C:\\mxcmaterials\\飞机大战-bigE-dc03e9bf-e813-47a6-8329-211741a2ac6d.png")
        self.down_image = pygame.image.load("C:\\mxcmaterials\\飞机大战-bigE_D-f16260ad-d3bc-4dbe-8fe3-1fb1a22daf4f.png")
        self.rect = self.image.get_rect( ) # 获取矩形对象
        self.rect.left = random.randint(0,bg_width-169) # 左侧的x
        self.rect.top = random.randint((-5)*bg_height,-258)# 顶部的y
        self.speed = 1 # 移动速度
        #大敌机的初始生存状态应该是False
        self.active = False
    def move(self):
        if self.rect.top<bg_height:
            self.rect.top +=self.speed
        else:
            self.reset()
    # 重置敌机
    def reset(self):
        self.active = False # 状态：关闭
        self.rect.left = random.randint(0,bg_width-85)
        self.rect.top = random.randint((-5)*bg_height,-258)
# 定义子弹类

class Bullet():
    def __init__(self,left,top):
        self.image=pygame.image.load("C:\\mxcmaterials\\飞机大战-bullet-2dbf0897-0d23-46cd-9622-1b9f342a4c16.png")
        self.rect=self.image.get_rect() # 获取矩形对象
        self.rect.left=left # 左侧x
        self.rect.top=top   # 顶部y
        self.speed=5        # 移动的速度
        self.active=False   # 状态：关闭
    # 子弹移动
    def move(self):
        self.rect.top-=self.speed
        if self.rect.top<0:
            self.active=False
    def reset(self,left,top):
        self.active=True
        self.rect.left=left
        self.rect.top=top   
# 空中补给类
class Bullet_Supply( ):
    def __init__(self):
        self.image = pygame.image.load("C:\\mxcmaterials\\飞机大战-supply-ee2ea981-dbf0-4db6-8a10-32e018e38a18.png")
        self.rect = self.image.get_rect()
        self.speed = 3
        self.rect.left = random.randint(0,bg_width-58)
        self.rect.top = random.randint(-5*bg_height,-88)
        self.active = False
        self.mask=pygame.mask.from_surface(self.image)
    def move(self):
        if self.rect.top<bg_height:
            self.rect.top += self.speed
        else:
            self.active = False
    def reset(self):
        self.active = True
        self.rect.left = random.randint(0,bg_width-58)
        self.rect.top = random.randint(-5*bg_height,-88)

# 实例化对象:对象=类名()
hero=HeroPlane()
# 实例化敌战机群
enemies=[]
for a in range(15): # 15架
    enemy=Enemy()   # 实例化对象
    enemies.append(enemy) # 添加至列表中
# 3.1 子弹初始化
bullet_list=[] # 存储子弹
b_index=0  # 第一颗子弹
for b_index in range(8): # 取出一枚子弹
    bullet=Bullet(hero.rect.midtop[0],hero.rect.midtop[1]) # 实例化，子弹应该是由主战机发射的
    bullet_list.append(bullet)
# 3.3 实现连续发射，设定定时器
# 1.自定义发射子弹事件
SHOOT_TIME = pygame.USEREVENT + 1
# 2.每隔一定的时间发送一次定义的事件（单位为毫秒）
pygame.time.set_timer(SHOOT_TIME,200)
# 4.3 添加分数显示
#1.创建分数变量及实例化字体对象
score = 0  # 存储分数的初始值
# 1.实例化字体对象           字体     字号 加粗
font = pygame.font.SysFont("simhei.ttf",28,True)

#5.2 自定义大敌机出现事件
BIG_ENEMY_TIME=pygame.USEREVENT+2 # 自定义的第2个事件
# 设置大敌机出现定时器
pygame.time.set_timer(BIG_ENEMY_TIME,10000)
# 实例化大敌机
big_enemy = BigEnemy()
bullet_supply=Bullet_Supply()
super_bullet=False
SUPPLY_TIME=pygame.USEREVENT+3
pygame.time.set_timer(SUPPLY_TIME,7000)
SUPER_BULLET_TIME=pygame.USEREVENT+4
while running:
    # 子弹发射开关
    shoot = False
    sc.blit(bg,(0,0))
    sc.blit(hero.image,(hero.rect.left,hero.rect.top)) # 将战机展示在窗口上
    # 绘制多个敌战机
    for each in enemies: # 遍历敌机组，每次取出一架敌机
        each.move()      # 移动
        sc.blit(each.image,(each.rect.left,each.rect.top)) # 将敌机展示在窗口上
    # 5.4 绘制大敌机
    if big_enemy.active ==True: # 大敌机==被激活
        big_enemy.move()  # 大敌机移动的方法
        sc.blit(big_enemy.image,(big_enemy.rect.left,big_enemy.rect.top)) # 出现在窗口上
        # 5.6 大敌机飞行声音__start__
        if -400 < big_enemy.rect.top < bg_height:
            big_enemy_flying.play(-1) # 播放音效
        else:
            big_enemy_flying.stop()   # 停止播放
        # 大敌机飞行声音__end__
    # 3.2 发射子弹
    for b in bullet_list: # 遍历子弹列表
        if b.active==True:  # 子弹被激活
            b.move()          # 每次取出一枚进行移动
            sc.blit(b.image,(b.rect.left,b.rect.top)) # 贴在窗口上
            # 4.1 敌机与子弹的碰撞检测        子弹   敌机列表  False不会删除冲突子弹 
            enemy_hit = pygame.sprite.spritecollide(b,enemies,False)
            #击中敌机，子弹消除
            if enemy_hit : # 如果击中了敌机组：
                b.active = False  # 当前子弹就失效了
                #遍历被击中的敌机列表，展示击毁效果，并且重置被击中的敌机
                for e in enemy_hit: # 遍历敌机组
                    sc.blit(e.down_image,(e.rect.left,e.rect.top))
                    e.reset()
                    score+=100  # 击中一架敌机，分数就会+100
                    ed.play() # 被摧毁的音效
            enemy_big_hit = pygame.sprite.collide_mask(b,big_enemy)
            if enemy_big_hit:
                b.active = False
                big_enemy.energy-=1
                if big_enemy.energy==0:
                    big_enemy.active=False
                    big_enemy_flying.stop()
                    big_enemy_Ds.play()
                    sc.blit(big_enemy.down_image,(big_enemy.rect.left,big_enemy.rect.top))
                    pygame.display.update()
                    big_enemy.reset()
                    score+=1000
                    big_enemy.energy=10
    pygame.display.update()
    # 获取电脑事件
    for event in pygame.event.get():
        if event.type==pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                hero.moveUp()
            elif event.key==pygame.K_DOWN or event.key == pygame.K_s:
                hero.moveDown()
            elif event.key==pygame.K_LEFT or event.key == pygame.K_a:
                hero.moveLeft()
            elif event.key==pygame.K_RIGHT or event.key == pygame.K_d:
                hero.moveRight()    
        # 3.4 射击事件的监听
        elif event.type == SHOOT_TIME:
            shoot = True # 发射子弹的开关被开启了
            hero.switch_image=not hero.switch_image  # 发射子弹时需要切换形态
        # 5.3 实现大敌机事件的监听
        elif event.type==BIG_ENEMY_TIME:
            big_enemy.active=True # 大敌机被激活了
        elif event.type==SUPPLY_TIME:
            bullet_supply.reset()
        elif event.type==SUPER_BULLET_TIME:
            super_bullet = False
        elif event.type==pygame.QUIT:
            pygame.quit()
            break
    if bullet_supply.active==True:
        bullet_supply.move()
        sc.blit(bullet_supply.image,(bullet_supply.rect.left,bullet_supply.rect.left))
        if pygame.sprite.collide_mask(bullet_supply,hero):
            b_index = 0
            super_bullet = True
            pygame.time.set_timer(SUPER_BULLET_TIME,3*1000)
            bullet_supply.active=False
    # 5.4 -1.绘制黑色血槽
    pygame.draw.line(sc,(0,0,0),
    (big_enemy.rect.left,big_enemy.rect.top-5),
    (big_enemy.rect.right,big_enemy.rect.top-5),2)
    # 5.4 -2 定义变量energy_remain，保存此时剩余血量的比例
    energy_remain=big_enemy.energy/BigEnemy.energy
    # # 5.4 -3.绘制上层血量，比例大于0.2，显示绿色，低于0.2，显示红色
    if energy_remain>0.2:
        energy_color=(0,255,0)
    else:
        energy_color=(255,0,0)
    # # 5.4 -4 绘制上层血量
    pygame.draw.line(sc,energy_color,
    (big_enemy.rect.left,big_enemy.rect.top-5),
    (big_enemy.rect.left+big_enemy.rect.width*energy_remain,big_enemy.rect.top-5),5)
    if shoot ==True: # 子弹被开启
        bullet_sound.play() # 播放子弹音效
        if super_bullet==True:
            bullet_list[b_index].reset(hero.rect.centerx-33,hero.rect.centery)
            bullet_list[b_index+1].reset(hero.rect.centerx+33,hero.rect.centery)
            b_index=(b_index+2)%8
        else:
            bullet_list[b_index].reset(hero.rect.midtop[0],hero.rect.midtop[1]) # 到达顶部要去重置
            b_index = (b_index+1)%8
        if event.type==pygame.QUIT:
            pygame.display.quit()
            exit()
    # 3.交换后的效果展示
    if hero.switch_image==True:
        sc.blit(hero.image1,(hero.rect.left,hero.rect.top))
    else:
        sc.blit(hero.image2,(hero.rect.left,hero.rect.top))
    # 4.4 分数显示
    # 2.渲染字体
    score_text = font.render("SCORE:%d"%score,True,(255,255,255))
    # 3.绘制在窗口上
    sc.blit(score_text,(10,10))
    # 4.2 检测英雄机与敌机的碰撞             战机   敌机列表     像素遮罩检测
    hero_hit=pygame.sprite.spritecollide(hero,enemies,False,pygame.sprite.collide_mask)
    hero_hit_big = pygame.sprite.collide_mask(hero,big_enemy)
    if hero_hit or hero_hit_big:
        big_enemy_flying.stop()
        hd.play()
        sc.blit(hero.down_image,(hero.rect.left,hero.rect.top))
        running=False # 主战机一旦被摧毁，游戏结束
    #知识进阶-step3--end--
    pygame.display.update()
#拓展练习
sc.blit(bg,(0,0))
# 1.实例化字体对象
font = pygame.font.SysFont("simhei.ttf",28)
# 2.渲染字体
over_text1 = font.render("GAME OVER",True,(255,255,255))
over_text2 = font.render("SCORE:%d"%score,True,(255,255,255))
# 3.绘制在窗口上
sc.blit(over_text1,(100,150))
sc.blit(over_text2,(100,250))
# 刷新
pygame.display.update()
time.sleep(5)
pygame.quit()