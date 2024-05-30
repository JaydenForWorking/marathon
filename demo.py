from PIL import Image, ImageDraw, ImageFont


def makingCertificate(text_to_add):

    # 打开图像文件
    image_path = '证书模板.jpg'
    image = Image.open(image_path)

    # 确保图像是 RGB 模式，以便支持彩色文本
    if image.mode != 'RGB':
        image = image.convert('RGB')



    # 创建一个可以在图片上绘图的对象
    draw = ImageDraw.Draw(image)


    # # 指定字体和大小
    # font_path = 'arial.ttf'  # 需要一个字体文件
    # font_size = 24
    # font = ImageFont.truetype(font_path, font_size)

    # 指定中文字体和大小
    # font_path = 'simHei.ttf'  # 这里假设你有一个名为simsun的字体文件，它支持中文
    font_path = 'fonts/方正粗宋简体.ttf'
    font_size = 12
    font = ImageFont.truetype(font_path, font_size)

    # # 要添加到图像上的文本
    # text_to_add = {
    #     '参赛号码': '12345',
    #     '姓名': '张三',
    #     '项目': '5KM',
    #     '成绩': '1:30:23',
    #     '平均配速': '5：37'
    # }

    # # 文本的位置
    # positions = {
    #     '参赛号码': (320, 400),
    #     '姓名': (300, 530),
    #     '项目': (300, 650),
    #     '成绩': (430, 800),
    # }
    # 文本的位置
    positions = {
        '参赛号码': (120, 110),
        '姓名': (110, 140),
        '项目': (100, 165),
        '成绩': (100, 190),
        '平均配速': (120, 220)
    }

    # 添加文本到图像
    for key, value in text_to_add.items():
        position = positions[key]
        draw.text(position, value, font=font, fill=(0, 0, 0))

    # 保存修改后的图像
    output_path = 'certificate_with_text.jpg'
    image.save(output_path)

    return output_path
