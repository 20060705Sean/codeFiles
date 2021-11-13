import pygame
pygame.init()
red = (255,0,0)
blue = (0,0,255)
w,h = size = 480,360
screen = pygame.display.set_mode(size)
pygame.display.set_caption("遮罩")
clock = pygame.time.Clock()
i=0

# 创建大的圆环
radius1 = 50
width1,height1 = 2*radius1,2*radius1
hollow_circle = pygame.Surface((width1,height1),pygame.SRCALPHA)
pos = width1//2,height1//2
rect1 = hollow_circle.get_rect(center=(w//2,h//2))
pygame.draw.circle(hollow_circle,red,pos,radius1,10)
mask1 = pygame.mask.from_surface(hollow_circle) #获取圆环的Mask
# 创建小的实心圆
radius2 = 10
width2,height2 = 2 * radius2,2 * radius2
solid_circle = pygame.Surface((width2,height2),pygame.SRCALPHA)
pos = width2//2,height2//2
rect2 = solid_circle.get_rect(center=(w//2,h//2))
pygame.draw.circle(solid_circle,blue,pos,radius2)
mask2 = pygame.mask.from_surface(solid_circle)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    screen.fill((255,255,255))

    mpos = pygame.mouse.get_pos()
    rect2.center = mpos

    offset = rect2.x - rect1.x, rect2.y - rect1.y
    p = mask1.overlap(mask2, offset)  #检测两个Mask有没有碰撞
    #这种检测法图像的透明区域不在碰撞检测范围内
    #没有碰撞返回None，有碰撞返回碰撞的坐标(相对于mask1的坐标)
    #返回值：【mask1中碰撞区域左上角的坐标,而且这个坐标是相对于mask1图像左上角的】
    screen.blit(hollow_circle, rect1)
    screen.blit(solid_circle, rect2)
    print(i,p)
    i+=1
    clock.tick(60)
    pygame.display.update()