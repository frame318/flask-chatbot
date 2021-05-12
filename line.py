from config import *
import requests
import json


def Question(text, intent, reply_token, id, req):  # สอบถามปัญหา
    if text == 'สอบถามปัญหาอีกครั้ง':
        text_message = TextSendMessage(text='สอบถามได้เลยคะ')
        line_bot_api.reply_message(reply_token, text_message)
        line_bot_api.link_rich_menu_to_user(id, 'richmenu-72a16f5b0c0fcfd3fa814be8edc1b616')
    else:
        text_message = TextSendMessage(text='สวัสดี')
        text_message2 = TextSendMessage(
            text='care you  เป็นหุ่นยนต์ถามตอบเกี่ยวกับให้บริการ เรื่องการเลื่อนนัด คำแนะนำทั่วไปสำหรับผู้ป่วย และ ผู้ดูแล ที่ได้มารับบริการโรงพยาบาลจิตเวชขอนแก่นราชนครินทร์ ')
        flex_message = FlexSendMessage(
            alt_text='hello',
            contents={
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "md",
                    "contents": [
                        {
                            "type": "button",
                            "style": "secondary",
                            "action": {
                                "type": "message",
                                "label": "การเลื่อนนัด",
                                "text": "การเลื่อนนัด"
                            }
                        },
                        {
                            "type": "button",
                            "style": "secondary",
                            "action": {
                                "type": "message",
                                "label": "การกินยา",
                                "text": "การกินยา"
                            }
                        },
                        {
                            "type": "button",
                            "style": "secondary",
                            "action": {
                                "type": "message",
                                "label": "คลินิกนอกเวลา",
                                "text": "คลินิกนอกเวลา"
                            }
                        },
                        {
                            "type": "button",
                            "style": "secondary",
                            "action": {
                                "type": "message",
                                "label": "Covid 19",
                                "text": "Covid 19"
                            }
                        },

                    ]
                }
            }
        )
        line_bot_api.reply_message(reply_token, [text_message, text_message2, flex_message])
        line_bot_api.link_rich_menu_to_user(id, 'richmenu-72a16f5b0c0fcfd3fa814be8edc1b616')


def Menu(text, intent, reply_token, id):  # เมนู
    if intent == 'Menu':
        confirm_template_message = TemplateSendMessage(
            alt_text='Confirm template',
            template=ConfirmTemplate(
                text='ต้องการหยุดการสนทนา',
                actions=[
                    MessageAction(
                        label='ใช่',
                        text='ใช่'
                    ),
                    MessageAction(
                        label='ไม่ใช่',
                        text='สอบถามปัญหาอีกครั้ง'
                    )
                ]
            )
        )
        line_bot_api.reply_message(reply_token, confirm_template_message)
    if intent == 'Menu - yes':
        line_bot_api.unlink_rich_menu_from_user(id)


def Reminder(text, intent, reply_token, id):
    if text == 'เตือนความจำ':
        buttons_template_message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                thumbnail_image_url='https://sv1.picz.in.th/images/2020/10/13/OIyNvV.jpg',
                title='เตือนความจำ',
                text='ช่วยสำหรับจดจำวันนัดหมาย',
                actions=[
                    URIAction(
                        label='เตือนความจำ',
                        uri='https://liff.line.me/1654982439-PGQy8pvw/remindergeturl'
                    ),
                    MessageAction(
                        label='ดูบันทึกเตือนความจำ',
                        text='ดูบันทึกเตือนความจำ'
                    ),
                ]
            )
        )
        line_bot_api.reply_message(reply_token, buttons_template_message)
    if text == 'ดูบันทึกเตือนความจำ':

        conn = sqlite3.connect('user.db')
        c = conn.cursor()
        c.execute("SELECT * FROM reminders WHERE id_user == '{}'".format(id))
        all_product = c.fetchall()

        if all_product == []:
            text_message = TextSendMessage(text='คุณยังไม่มีบันทึกเตือนความจำ')
            line_bot_api.reply_message(reply_token, text_message)
        else:
            for i in all_product:
                service_1 = i[2]
                service_2 = i[3]
                service_3 = i[4]
                service_4 = i[5]
                reminder = i[6]
                date = i[7]
                time = i[8]
            if service_1 == 1:
                txt1 = '✅ ไปตามนัดพบแพทย์'
            else:
                txt1 = '❌ ไปตามนัดพบแพทย์'
            if service_2 == 1:
                txt2 = '✅ ไปตามนัดรับยาเดิม'
            else:
                txt2 = '❌ ไปตามนัดรับยาเดิม'
            if service_3 == 1:
                txt3 = '✅ ไปตามนัดเข้ากลุ่มบำบัด'
            else:
                txt3 = '❌ ไปตามนัดเข้ากลุ่มบำบัด'
            if service_4 == 1:
                txt4 = '✅ ขอคำปรึกษาปัญหาครอบครัว'
            else:
                txt4 = '❌ ขอคำปรึกษาปัญหาครอบครัว'

            text_message = TextSendMessage(
                text='{}\n{}\n{}\n{}\nวันที่ : {}\nเวลา : {}\nหมายเหตุอื่นๆ : {}'.format(txt1, txt2, txt3, txt4, date,
                                                                                         time, reminder))
            line_bot_api.reply_message(reply_token, text_message)


def Drug(text, intent, reply_token, id):
    if text == 'รู้เรื่องยา':  # รู้เรื่องยา
        carousel_template_message = TemplateSendMessage(
            alt_text='Carousel template',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://sv1.picz.in.th/images/2020/10/13/OIyt22.jpg',
                        title='ควรรู้เกี่ยวกับยาจิตเวช',
                        text='สาระน่ารู้ควรรู้เกี่ยวกับยาจิตเวช',
                        actions=[
                            URIAction(
                                label='ข้อควรรู้เกี่ยวกับยาจิตเวช',
                                uri='https://www.manarom.com/blog/psychiatric_medications.html'
                            ),
                            MessageAction(
                                label='วิดิโอน่ารู้เกี่ยวกับยาจิตเวช',
                                text='วิดิโอน่ารู้เกี่ยวกับยาจิตเวช'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://sv1.picz.in.th/images/2020/10/13/OIycG9.jpg',
                        title='RDU รู้เรื่องยา',
                        text='แอปพลิเคชันสำหรับใช้ดูข้อมูลฉลากยาเสริม',
                        actions=[
                            URIAction(
                                label='IOS',
                                uri='https://apps.apple.com/th/app/rdu-%E0%B8%A3-%E0%B9%80%E0%B8%A3-%E0%B8%AD%E0%B8%87%E0%B8%A2%E0%B8%B2/id1286704705?l=th'
                            ),
                            URIAction(
                                label='Android',
                                uri='https://play.google.com/store/apps/details?id=com.uhosnet&hl=th'
                            )
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(reply_token, carousel_template_message)
    if text == 'วิดิโอน่ารู้เกี่ยวกับยาจิตเวช':
        carousel_template_message = TemplateSendMessage(
            alt_text='Carousel template',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://sv1.picz.in.th/images/2020/10/13/OIyfBQ.png',
                        title='ทำความเข้าใจ "ยาจิตเวช"',
                        text='ปัญหาการใช้ ผลข้างเคียง',
                        actions=[
                            MessageAction(
                                label='ดูวิดิโอ',
                                text='วิดิโอน่ารู้เกี่ยวกับยาจิตเวช-1'
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://sv1.picz.in.th/images/2020/10/13/OIyk8n.png',
                        title='คำถามยอดฮิตยาจิตเวช',
                        text='คำถามยอดฮิตยาจิตเวช',
                        actions=[
                            MessageAction(
                                label='ดูวิดิโอ',
                                text='วิดิโอน่ารู้เกี่ยวกับยาจิตเวช-2'
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://sv1.picz.in.th/images/2020/10/13/OIy97g.png',
                        title='การใช้ยากับผู้ป่วยด้านจิตเวช',
                        text='การใช้ยากับผู้ป่วยด้านจิตเวช',
                        actions=[
                            MessageAction(
                                label='ดูวิดิโอ',
                                text='วิดิโอน่ารู้เกี่ยวกับยาจิตเวช-3'
                            ),
                        ]
                    ),
                ]
            )
        )
        line_bot_api.reply_message(reply_token, carousel_template_message)
    if text == 'วิดิโอน่ารู้เกี่ยวกับยาจิตเวช-1':
        text_message = TextSendMessage(text='https://www.youtube.com/watch?v=gQ5uqTLTtjY')
        line_bot_api.reply_message(reply_token, text_message)
    if text == 'วิดิโอน่ารู้เกี่ยวกับยาจิตเวช-2':
        text_message = TextSendMessage(text='https://www.youtube.com/watch?v=S9uO_ABmkU8')
        line_bot_api.reply_message(reply_token, text_message)
    if text == 'วิดิโอน่ารู้เกี่ยวกับยาจิตเวช-3':
        text_message = TextSendMessage(text='https://www.youtube.com/watch?v=bFBUmYF193E')
        line_bot_api.reply_message(reply_token, text_message)


def Knowledge(text, intent, reply_token, id):
    if text == 'เกร็ดความรู้':
        buttons_template_message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                thumbnail_image_url='https://sv1.picz.in.th/images/2020/10/13/OIywF1.png',
                title='เกร็ดความรู้',
                text='สาระน่ารู้',
                actions=[
                    MessageAction(
                        label='การดูแลผู้ป่วยจิตเวช',
                        text='การดูแลผู้ป่วยจิตเวช'
                    ),
                    MessageAction(
                        label='การดูแลผู้ป่วยซึมเศร้า',
                        text='การดูแลผู้ป่วยซึมเศร้า'
                    ),
                    MessageAction(
                        label='การจัดการความเครียด',
                        text='การจัดการความเครียด'
                    ),
                    MessageAction(
                        label='เฝ้าระวังความเสี่ยง',
                        text='การเฝ้าระวังความเสี่ยงฆ่าตัวตาย'
                    ),
                ]
            )
        )
        line_bot_api.reply_message(reply_token, buttons_template_message)
    if text == 'การดูแลผู้ป่วยจิตเวช':  # การดูแลผู้ป่วยจิตเวช
        flex_message = FlexSendMessage(
            alt_text='hello',
            contents={
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "md",
                    "contents": [
                        {
                            "type": "button",
                            "style": "secondary",
                            "action": {
                                "type": "message",
                                "label": "7 สัญญาณเตือน ผู้ป่วยจิตเวชยา",
                                "text": "7 สัญญาณเตือน ผู้ป่วยจิตเวชยาเสพติดก่อความรุนแรง"
                            }
                        },
                        {
                            "type": "button",
                            "style": "secondary",
                            "action": {
                                "type": "message",
                                "label": "โรคจิตเภท",
                                "text": "โรคจิตเภท"
                            }
                        },
                        {
                            "type": "button",
                            "style": "secondary",
                            "action": {
                                "type": "message",
                                "label": "4 วิธี ดูแผู้ป่วยจิตเภท",
                                "text": "4 วิธี ดูแผู้ป่วยจิตเภท"
                            }
                        },
                        {
                            "type": "button",
                            "style": "secondary",
                            "action": {
                                "type": "message",
                                "label": "การช่วยเหลือเบื้องต้นผู้มีอาการ",
                                "text": "การช่วยเหลือเบื้องต้นผู้มีอาการโรคจิต"
                            }
                        },

                    ]
                }
            }
        )
        line_bot_api.reply_message(reply_token, flex_message)
    if text == '7 สัญญาณเตือน ผู้ป่วยจิตเวชยาเสพติดก่อความรุนแรง':  # การดูแลผู้ป่วยจิตเวช
        image_message = ImageSendMessage(
            original_content_url='https://sv1.picz.in.th/images/2021/02/09/o9m9Fz.jpg',
            preview_image_url='https://sv1.picz.in.th/images/2021/02/09/o9m9Fz.jpg'
        )
        line_bot_api.reply_message(reply_token, image_message)
    if text == 'โรคจิตเภท':  # การดูแลผู้ป่วยจิตเวช
        image_message = ImageSendMessage(
            original_content_url='https://sv1.picz.in.th/images/2021/02/09/o9mPgn.jpg',
            preview_image_url='https://sv1.picz.in.th/images/2021/02/09/o9mPgn.jpg'
        )
        line_bot_api.reply_message(reply_token, image_message)
    if text == '4 วิธี ดูแผู้ป่วยจิตเภท':  # การดูแลผู้ป่วยจิตเวช
        image_message = ImageSendMessage(
            original_content_url='https://sv1.picz.in.th/images/2020/10/13/OIy4lN.jpg',
            preview_image_url='https://sv1.picz.in.th/images/2020/10/13/OIy4lN.jpg'
        )
        line_bot_api.reply_message(reply_token, image_message)
    if text == 'การช่วยเหลือเบื้องต้นผู้มีอาการโรคจิต':  # การดูแลผู้ป่วยจิตเวช
        image_message = ImageSendMessage(
            original_content_url='https://sv1.picz.in.th/images/2021/02/09/o9yLnS.jpg',
            preview_image_url='https://sv1.picz.in.th/images/2021/02/09/o9yLnS.jpg'
        )
        line_bot_api.reply_message(reply_token, image_message)

    if text == 'การดูแลผู้ป่วยซึมเศร้า':  # การดูแลผู้ป่วยจิตเวช
        flex_message = FlexSendMessage(
            alt_text='hello',
            contents={
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "md",
                    "contents": [
                        {
                            "type": "button",
                            "style": "secondary",
                            "action": {
                                "type": "message",
                                "label": "คุณเป็นโรคซึมเศร้าหรือไม่",
                                "text": "คุณเป็นโรคซึมเศร้าหรือไม่"
                            }
                        },
                        {
                            "type": "button",
                            "style": "secondary",
                            "action": {
                                "type": "message",
                                "label": "จะทำอย่างไรเมื่อเป็นโรคซึมเศร้า",
                                "text": "จะทำอย่างไรเมื่อเป็นโรคซึมเศร้า"
                            }
                        },
                        {
                            "type": "button",
                            "style": "secondary",
                            "action": {
                                "type": "message",
                                "label": "คนใกล้ชิด-สามารถช่วยได้",
                                "text": "โรคซึมเศร้า-เพื่อน-ครอบครัว-คนใกล้ชิด-สามารถช่วยได้"
                            }
                        },
                    ]
                }
            }
        )
        line_bot_api.reply_message(reply_token, flex_message)
    if text == 'คุณเป็นโรคซึมเศร้าหรือไม่':  # การดูแลผู้ป่วยจิตเวช
        image_message = ImageSendMessage(
            original_content_url='https://sv1.picz.in.th/images/2021/02/09/o9yyKg.jpg',
            preview_image_url='https://sv1.picz.in.th/images/2021/02/09/o9yyKg.jpg'
        )
        line_bot_api.reply_message(reply_token, image_message)
    if text == 'จะทำอย่างไรเมื่อเป็นโรคซึมเศร้า':  # การดูแลผู้ป่วยจิตเวช
        image_message = ImageSendMessage(
            original_content_url='https://sv1.picz.in.th/images/2021/02/09/o9FKnI.jpg',
            preview_image_url='https://sv1.picz.in.th/images/2021/02/09/o9FKnI.jpg'
        )
        line_bot_api.reply_message(reply_token, image_message)
    if text == 'โรคซึมเศร้า-เพื่อน-ครอบครัว-คนใกล้ชิด-สามารถช่วยได้':  # การดูแลผู้ป่วยจิตเวช
        image_message = ImageSendMessage(
            original_content_url='https://sv1.picz.in.th/images/2021/02/09/o9FgZt.jpg',
            preview_image_url='https://sv1.picz.in.th/images/2021/02/09/o9FgZt.jpg'
        )
        line_bot_api.reply_message(reply_token, image_message)

    if text == 'การจัดการความเครียด':  # การดูแลผู้ป่วยจิตเวช
        flex_message = FlexSendMessage(
            alt_text='hello',
            contents={
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "md",
                    "contents": [
                        {
                            "type": "button",
                            "style": "secondary",
                            "action": {
                                "type": "message",
                                "label": "การจัดการความเครียด",
                                "text": "วิธีการจัดการความเครียด"
                            }
                        },
                        {
                            "type": "button",
                            "style": "secondary",
                            "action": {
                                "type": "message",
                                "label": "3 ขั้นตอนฝึกสมาธิ คลายเครียด",
                                "text": "3 ขั้นตอนฝึกสมาธิ คลายเครียด"
                            }
                        },
                        {
                            "type": "button",
                            "style": "secondary",
                            "action": {
                                "type": "message",
                                "label": "7 วิธีฟื้นฟูใจตัวเอง",
                                "text": "7 วิธีฟื้นฟูใจตัวเองจากการโดนนอกใจ"
                            }
                        },
                        {
                            "type": "button",
                            "style": "secondary",
                            "action": {
                                "type": "message",
                                "label": "10 วิธีปฏิบัติเพื่อช่วยคลายเครียด",
                                "text": "10 วิธีปฏิบัติเพื่อช่วยคลายเครียดในการทำงาน"
                            }
                        },
                        {
                            "type": "button",
                            "style": "secondary",
                            "action": {
                                "type": "message",
                                "label": "ขั้นตอนการฝึกสติ",
                                "text": "ขั้นตอนการฝึกสติ"
                            }
                        },
                        {
                            "type": "button",
                            "style": "secondary",
                            "action": {
                                "type": "message",
                                "label": "การปฐมพยาบาลด้านสุขภาพจิต",
                                "text": "การปฐมพยาบาลด้านสุขภาพจิต 1 รับ 4 ให้"
                            }
                        },
                    ]
                }
            }
        )
        line_bot_api.reply_message(reply_token, flex_message)
    if text == 'วิธีการจัดการความเครียด':  # การดูแลผู้ป่วยจิตเวช
        image_message = ImageSendMessage(
            original_content_url='https://sv1.picz.in.th/images/2021/02/09/o9IjfR.jpg',
            preview_image_url='https://sv1.picz.in.th/images/2021/02/09/o9IjfR.jpg'
        )
        line_bot_api.reply_message(reply_token, image_message)
    if text == '3 ขั้นตอนฝึกสมาธิ คลายเครียด':  # การดูแลผู้ป่วยจิตเวช
        image_message = ImageSendMessage(
            original_content_url='https://sv1.picz.in.th/images/2021/02/09/oTduwf.jpg',
            preview_image_url='https://sv1.picz.in.th/images/2021/02/09/oTduwf.jpg'
        )
        line_bot_api.reply_message(reply_token, image_message)
    if text == '7 วิธีฟื้นฟูใจตัวเองจากการโดนนอกใจ':  # การดูแลผู้ป่วยจิตเวช
        image_message = ImageSendMessage(
            original_content_url='https://sv1.picz.in.th/images/2021/02/09/oT0t69.jpg',
            preview_image_url='https://sv1.picz.in.th/images/2021/02/09/oT0t69.jpg'
        )
        line_bot_api.reply_message(reply_token, image_message)
    if text == '10 วิธีปฏิบัติเพื่อช่วยคลายเครียดในการทำงาน':  # การดูแลผู้ป่วยจิตเวช
        image_message = ImageSendMessage(
            original_content_url='https://sv1.picz.in.th/images/2021/02/09/oT7Tpl.jpg',
            preview_image_url='https://sv1.picz.in.th/images/2021/02/09/oT7Tpl.jpg'
        )
        line_bot_api.reply_message(reply_token, image_message)
    if text == 'ขั้นตอนการฝึกสติ':  # การดูแลผู้ป่วยจิตเวช
        image_message = ImageSendMessage(
            original_content_url='https://sv1.picz.in.th/images/2021/02/09/oTSjfe.jpg',
            preview_image_url='https://sv1.picz.in.th/images/2021/02/09/oTSjfe.jpg'
        )
        line_bot_api.reply_message(reply_token, image_message)
    if text == 'การปฐมพยาบาลด้านสุขภาพจิต 1 รับ 4 ให้':  # การดูแลผู้ป่วยจิตเวช
        image_message = ImageSendMessage(
            original_content_url='https://sv1.picz.in.th/images/2021/02/09/oTSsuN.jpg',
            preview_image_url='https://sv1.picz.in.th/images/2021/02/09/oTSsuN.jpg'
        )
        line_bot_api.reply_message(reply_token, image_message)

    if text == 'การเฝ้าระวังความเสี่ยงฆ่าตัวตาย':  # การดูแลผู้ป่วยจิตเวช
        flex_message = FlexSendMessage(
            alt_text='hello',
            contents={
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "md",
                    "contents": [
                        {
                            "type": "button",
                            "style": "secondary",
                            "action": {
                                "type": "message",
                                "label": "5 สัญญาณเตือนเสี่ยงฆ่าตัวตาย",
                                "text": "5 สัญญาณเตือนเสี่ยงฆ่าตัวตาย"
                            }
                        },
                        {
                            "type": "button",
                            "style": "secondary",
                            "action": {
                                "type": "message",
                                "label": "รังแกกัน ไม่ใช่เรื่องล้อเล่น",
                                "text": "กลั่นแกล้ง/รังแกกัน ไม่ใช่เรื่องล้อเล่น"
                            }
                        },
                        {
                            "type": "button",
                            "style": "secondary",
                            "action": {
                                "type": "message",
                                "label": "10 สัญญานเตือนเสี่ยงฆ่าตัวตาย",
                                "text": "10 สัญญานเตือนเสี่ยงฆ่าตัวตาย"
                            }
                        },
                        {
                            "type": "button",
                            "style": "secondary",
                            "action": {
                                "type": "message",
                                "label": "5อย่า3ควรเมื่อเห็นคนทำร้ายตัวเอง",
                                "text": "5อย่า3ควรเมื่อเห็นคนทำร้ายตัวเอง"
                            }
                        },

                    ]
                }
            }
        )
        line_bot_api.reply_message(reply_token, flex_message)
    if text == '5 สัญญาณเตือนเสี่ยงฆ่าตัวตาย':  # การดูแลผู้ป่วยจิตเวช
        image_message = ImageSendMessage(
            original_content_url='https://sv1.picz.in.th/images/2021/02/09/oTYNLP.jpg',
            preview_image_url='https://sv1.picz.in.th/images/2021/02/09/oTYNLP.jpg'
        )
        line_bot_api.reply_message(reply_token, image_message)
    if text == 'กลั่นแกล้ง/รังแกกัน ไม่ใช่เรื่องล้อเล่น':  # การดูแลผู้ป่วยจิตเวช
        image_message = ImageSendMessage(
            original_content_url='https://sv1.picz.in.th/images/2021/02/09/oTYhEe.jpg',
            preview_image_url='https://sv1.picz.in.th/images/2021/02/09/oTYhEe.jpg'
        )
        line_bot_api.reply_message(reply_token, image_message)
    if text == '10 สัญญานเตือนเสี่ยงฆ่าตัวตาย':  # การดูแลผู้ป่วยจิตเวช
        image_message = ImageSendMessage(
            original_content_url='https://sv1.picz.in.th/images/2021/02/09/oTYqx1.jpg',
            preview_image_url='https://sv1.picz.in.th/images/2021/02/09/oTYqx1.jpg'
        )
        line_bot_api.reply_message(reply_token, image_message)
    if text == '5อย่า3ควรเมื่อเห็นคนทำร้ายตัวเอง':  # การดูแลผู้ป่วยจิตเวช
        image_message = ImageSendMessage(
            original_content_url='https://sv1.picz.in.th/images/2021/02/09/oTYjAJ.jpg',
            preview_image_url='https://sv1.picz.in.th/images/2021/02/09/oTYjAJ.jpg'
        )
        line_bot_api.reply_message(reply_token, image_message)
    # if text == '5 วิธีจัดการความเครียด': #การดูแลผู้ป่วยจิตเวช
    #     image_message = ImageSendMessage(
    #         original_content_url= 'https://sv1.picz.in.th/images/2020/10/26/bTpU39.jpg',
    #         preview_image_url='https://sv1.picz.in.th/images/2020/10/26/bTpU39.jpg'
    #     )
    #     line_bot_api.reply_message(reply_token, image_message)
    # if text == 'การดูแลผู้ป่วยจิตเวช': #การดูแลผู้ป่วยจิตเวช
    #     image_message = ImageSendMessage(
    #         original_content_url= 'https://sv1.picz.in.th/images/2020/10/13/OIy4lN.jpg',
    #         preview_image_url='https://sv1.picz.in.th/images/2020/10/13/OIy4lN.jpg'
    #     )
    #     line_bot_api.reply_message(reply_token, image_message)
    # if text == 'อยากเลิกเหล้า เราช่วยได้': #อยากเลิกเหล้า เราช่วยได้
    #     image_message = ImageSendMessage(
    #         original_content_url='https://sv1.picz.in.th/images/2020/10/13/OIyhqS.jpg',
    #         preview_image_url='https://sv1.picz.in.th/images/2020/10/13/OIyhqS.jpg'
    #     )
    #     line_bot_api.reply_message(reply_token, image_message)

    # if text == 'วิดิโอน่ารู้': #
    #     carousel_template_message = TemplateSendMessage(
    #         alt_text='Carousel template',
    #         template=CarouselTemplate(
    #             columns=[
    #                 CarouselColumn(
    #                     thumbnail_image_url= 'https://sv1.picz.in.th/images/2020/10/13/OIy0cl.png',
    #                     title='เกร็ดความรู้คู่สุขภาพ',
    #                     text='วิธีการรับมือกับอาการของโรคซึมเศร้า',
    #                     actions=[
    #                         MessageAction(
    #                             label='ดูวิดิโอ',
    #                             text='วิดิโอน่ารู้-1'
    #                         ),
    #                     ]
    #                 ),
    #                 CarouselColumn(
    #                     thumbnail_image_url='https://sv1.picz.in.th/images/2020/10/13/OIy72k.png',
    #                     title='หายใจคลายเครียด',
    #                     text='การจัดการความเครียดด้วยตนเอง',
    #                     actions=[
    #                         MessageAction(
    #                             label='ดูวิดิโอ',
    #                             text='วิดิโอน่ารู้-2'
    #                         ),
    #                     ]
    #                 ),
    #                 CarouselColumn(
    #                     thumbnail_image_url='https://sv1.picz.in.th/images/2020/10/13/OIySyv.png',
    #                     title='การจัดการความเครียด',
    #                     text='การผ่อนคลายกล้ามเนื้อ',
    #                     actions=[
    #                         MessageAction(
    #                             label='ดูวิดิโอ',
    #                             text='วิดิโอน่ารู้-3'
    #                         ),
    #                     ]
    #                 ),
    #                 CarouselColumn(
    #                     thumbnail_image_url='https://sv1.picz.in.th/images/2020/10/13/OIyzTE.png',
    #                     title='โปรเจค "น้ำ"',
    #                     text='โปรเจค "น้ำ" โดย กรมสุขภาพจิต',
    #                     actions=[
    #                         MessageAction(
    #                             label='ดูวิดิโอ',
    #                             text='วิดิโอน่ารู้-4'
    #                         ),
    #                     ]
    #                 ),
    #             ]
    #         )
    #     )
    #     line_bot_api.reply_message(reply_token, carousel_template_message)
    #
    # if text == 'วิดิโอน่ารู้-1':
    #     text_message = TextSendMessage(text='https://www.youtube.com/watch?v=8S9k80Hn4rs')
    #     line_bot_api.reply_message(reply_token, text_message)
    # if text == 'วิดิโอน่ารู้-2':
    #     text_message = TextSendMessage(text='https://www.youtube.com/watch?v=D-ozvjPlVy4')
    #     line_bot_api.reply_message(reply_token, text_message)
    # if text == 'วิดิโอน่ารู้-3':
    #     text_message = TextSendMessage(text='https://www.youtube.com/watch?v=kOLNFOKSDnk')
    #     line_bot_api.reply_message(reply_token, text_message)
    # if text == 'วิดิโอน่ารู้-4':
    #     text_message = TextSendMessage(text='https://www.youtube.com/watch?v=WC3VaxiHY9g')
    #     line_bot_api.reply_message(reply_token, text_message)


def AssessmentForm(text, intent, reply_token, id):
    if text == 'แบบประเมิน':
        buttons_template_message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                thumbnail_image_url='https://sv1.picz.in.th/images/2020/10/13/OIyTgW.png',
                title='โรงพยาบาลจิตเวชขอนแก่นราชนครินทร์',
                text='แบบประเมิน',
                actions=[
                    URIAction(
                        label='แบบประเมินความเครียด',
                        uri='https://liff.line.me/1654982439-PGQy8pvw/st5'
                    ),
                    # URIAction(
                    #     label='แบบคัดกรองการฆ่าตัวตาย',
                    #     uri='https://liff.line.me/1654982439-PGQy8pvw/sui9'
                    # ),
                    URIAction(
                        label='แบบประเมินการฆ่าตัวตาย',
                        uri='https://liff.line.me/1654982439-PGQy8pvw/Q8'
                    ),
                    URIAction(
                        label='แบบประเมินโรคซึมเศร้า',
                        uri='https://liff.line.me/1654982439-PGQy8pvw/Q9'
                    ),

                ]
            )
        )
        line_bot_api.reply_message(reply_token, buttons_template_message)


def Public_relations(text, intent, reply_token, id):
    if text == 'ติดต่อ ประชาสัมพันธ์':  # ประชาสัมพันธ์ ติดต่อเรา
        buttons_template_message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                thumbnail_image_url='https://sv1.picz.in.th/images/2020/10/13/OIyZlD.jpg',
                title='โรงพยาบาลจิตเวชขอนแก่นราชนครินทร์',
                text='169 ถนน ชาตะผดุง ตำบลในเมือง อำเภอเมืองขอนแก่น ขอนแก่น 40000',
                actions=[
                    MessageAction(
                        label='เบอร์โทรติดต่อ',
                        text='เบอร์โทรติดต่อ'
                    ),
                    MessageAction(
                        label='location',
                        text='location'
                    ),
                    URIAction(
                        label='เว็บไซต์',
                        uri='http://www.jvkk.go.th:8080/web_jvkk_th/'
                    ),
                    MessageAction(
                        label='Email',
                        text='Email'
                    )
                ]
            )
        )
        line_bot_api.reply_message(reply_token, buttons_template_message)
    if text == 'เบอร์โทรติดต่อ':
        text_message = TextSendMessage(text='โทรศัพท์ : 043209999')
        line_bot_api.reply_message(reply_token, text_message)
    if text == 'location':
        location_message = LocationSendMessage(
            title='โรงพยาบาลจิตเวชขอนแก่นราชนครินทร์',
            address='169 ถนน ชาตะผดุง ตำบลในเมือง อำเภอเมืองขอนแก่น ขอนแก่น 40000',
            latitude=16.4257186,
            longitude=102.8489639
        )
        line_bot_api.reply_message(reply_token, location_message)
    if text == 'Email':
        text_message = TextSendMessage(text='Email : careyou.jvkk@gmail.com')
        line_bot_api.reply_message(reply_token, text_message)


def reply(text, intent, reply_token, id, req):
    if intent == 'Question - sticker':
        text_message = TextSendMessage(text='ก่อนจะคุยกันเรามาวัดอุณหภูมิใจกันไหมคะ')
        confirm_template_message = TemplateSendMessage(
            alt_text='Confirm template',
            template=ConfirmTemplate(
                text='วัดอุณหภูมิใจ',
                actions=[
                    MessageAction(
                        label='ทำ',
                        text='ทำ'
                    ),
                    MessageAction(
                        label='ไม่ทำ',
                        text='สอบถามปัญหาอีกครั้ง'
                    )
                ]
            )
        )
        line_bot_api.reply_message(reply_token, [text_message, confirm_template_message])
    if intent == 'Question - sticker - yes':
        imagemap_message = ImagemapSendMessage(
            base_url='',
            alt_text='this is an imagemap',
            base_size=BaseSize(height=600, width=1040),
            actions=[
                {
                    "type": "message",
                    "area": {
                        "x": 125,
                        "y": 169,
                        "width": 154,
                        "height": 187
                    },
                    "text": "1"
                },
                {
                    "type": "message",
                    "area": {
                        "x": 292,
                        "y": 166,
                        "width": 138,
                        "height": 190
                    },
                    "text": "2"
                },
                {
                    "type": "message",
                    "area": {
                        "x": 449,
                        "y": 164,
                        "width": 153,
                        "height": 196
                    },
                    "text": "3"
                },
                {
                    "type": "message",
                    "area": {
                        "x": 612,
                        "y": 164,
                        "width": 137,
                        "height": 195
                    },
                    "text": "4"
                },
                {
                    "type": "message",
                    "area": {
                        "x": 767,
                        "y": 167,
                        "width": 144,
                        "height": 194
                    },
                    "text": "5"
                },
                {
                    "type": "message",
                    "area": {
                        "x": 111,
                        "y": 372,
                        "width": 146,
                        "height": 210
                    },
                    "text": "6"
                },
                {
                    "type": "message",
                    "area": {
                        "x": 273,
                        "y": 375,
                        "width": 148,
                        "height": 208
                    },
                    "text": "7"
                },
                {
                    "type": "message",
                    "area": {
                        "x": 439,
                        "y": 367,
                        "width": 148,
                        "height": 214
                    },
                    "text": "8"
                },
                {
                    "type": "message",
                    "area": {
                        "x": 603,
                        "y": 375,
                        "width": 151,
                        "height": 208
                    },
                    "text": "9"
                },
                {
                    "type": "message",
                    "area": {
                        "x": 776,
                        "y": 374,
                        "width": 146,
                        "height": 209
                    },
                    "text": "10"
                }
            ]
        )
        line_bot_api.reply_message(reply_token, imagemap_message)
    if intent == 'Question - sticker - yes - 1':
        num = int(req["queryResult"]["outputContexts"][0]["parameters"]['number.original'])
        if num >= 8:
            text_message = TextSendMessage(text='ระดับ 8-10 คะแนนดีมากคะ')
            flex_message = FlexSendMessage(
                alt_text='hello',
                contents={
                    "type": "bubble",
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "md",
                        "contents": [
                            {
                                "type": "button",
                                "style": "secondary",
                                "action": {
                                    "type": "message",
                                    "label": "การเลื่อนนัด",
                                    "text": "การเลื่อนนัด"
                                }
                            },
                            {
                                "type": "button",
                                "style": "secondary",
                                "action": {
                                    "type": "message",
                                    "label": "การกินยา",
                                    "text": "การกินยา"
                                }
                            },
                            {
                                "type": "button",
                                "style": "secondary",
                                "action": {
                                    "type": "message",
                                    "label": "คลินิกนอกเวลา",
                                    "text": "คลินิกนอกเวลา"
                                }
                            },
                            {
                                "type": "button",
                                "style": "secondary",
                                "action": {
                                    "type": "message",
                                    "label": "อื่นๆ",
                                    "text": "อื่นๆ"
                                }
                            },

                        ]
                    }
                }
            )
            text_message2 = TextSendMessage(text='สอบถามอะไรคะ')
            line_bot_api.reply_message(reply_token, [text_message, text_message2, flex_message])

        if num >= 5 and num < 8:
            text_message = TextSendMessage(text='ระดับ 5-7 คะแนนใช้ได้คะ')
            text_message2 = TextSendMessage(
                text='ถ้าคุณมีความเครียดแนะนำให้ฝึกสติ ตาม link ฝึกหายใจคลายเครียด กรมสุขภาพจิต https://www.youtube.com/watch?v=D-ozvjPlVy4 ')
            text_message3 = TextSendMessage(
                text='เทคนิคการจัดการความเครียดด้วยตนเอง กรมสุขภาพจิต https://www.youtube.com/watch?v=kOLNFOKSDnk')
            line_bot_api.reply_message(reply_token, [text_message, text_message2, text_message3])
        if num < 5:
            text_message = TextSendMessage(text='ระดับ1-4 คะแนนไม่ค่อยดีคะ')
            text_message2 = TextSendMessage(
                text='ถ้าไม่สบายใจแนะนำให้ปรึกษาเจ้าหน้าที่ รพ. ที่เบอร์ 043-237151 และ1323  ได้คะ')
            line_bot_api.reply_message(reply_token, [text_message, text_message2])

    if intent == 'Q1 - 1 - 1 - 1' or intent == 'Q1 - 1 - 1 - 2 - 1':
        confirm_template_message = TemplateSendMessage(
            alt_text='Confirm template',
            template=ConfirmTemplate(
                text='ยาพอกินไหม',
                actions=[
                    MessageAction(
                        label='พอ',
                        text='พอ'
                    ),
                    MessageAction(
                        label='ไม่พอ',
                        text='ไม่พอ'
                    )
                ]
            )
        )
        line_bot_api.reply_message(reply_token, confirm_template_message)

    if intent == 'Q1 - 1 - 1 - 1 - yes - 1' or intent == 'Q1 - 1 - 1 - 1 - no - 1' or intent == 'Q1 - 1 - 1 - 2 - 1 - yes - 1' or intent == 'Q1 - 1 - 1 - 2 - 1 - no - 1':
        text_message = TextSendMessage(text='จองคิวออนไลน์ได้ตาม link : http://122.154.130.61/que_online/')
        text_message2 = TextSendMessage(text='หรือโทรสอบถามข้อมูลที่ งานเวชระเบียน 043-209999 ต่อ 63101 ในเวลาราชการ ')
        confirm_template_message = TemplateSendMessage(
            alt_text='Confirm template',
            template=ConfirmTemplate(
                text='มีอะไรคุยอีกกันต่ออีกไหม ',
                actions=[
                    MessageAction(
                        label='มี',
                        text='สอบถามปัญหาอีกครั้ง'
                    ),
                    MessageAction(
                        label='ไม่มี',
                        text='เมนูหลัก'
                    )
                ]
            )
        )
        line_bot_api.reply_message(reply_token, [text_message, text_message2, confirm_template_message])
    if intent == 'Q1 - 2 - 1':
        text_message = TextSendMessage(text='ขออภัยค่ะ  อยากให้ลองโทรใหม่อีกครั้ง หรือ โทรไปที หมายเลข 1323')
        confirm_template_message = TemplateSendMessage(
            alt_text='Confirm template',
            template=ConfirmTemplate(
                text='มีอะไรคุยอีกกันต่ออีกไหม ',
                actions=[
                    MessageAction(
                        label='มี',
                        text='สอบถามปัญหาอีกครั้ง'
                    ),
                    MessageAction(
                        label='ไม่มี',
                        text='เมนูหลัก'
                    )
                ]
            )
        )
        line_bot_api.reply_message(reply_token, [text_message, confirm_template_message])

    if intent == 'Q2':
        confirm_template_message = TemplateSendMessage(
            alt_text='Confirm template',
            template=ConfirmTemplate(
                text='ตอนนี้ กินยาอยู่ไหม ',
                actions=[
                    MessageAction(
                        label='กิน',
                        text='กิน'
                    ),
                    MessageAction(
                        label='ไม่กิน',
                        text='ไม่กิน'
                    )
                ]
            )
        )
        line_bot_api.reply_message(reply_token, confirm_template_message)
    if intent == 'Q2 - yes - 2 - 1':
        text_message = TextSendMessage(text='ขออภัยค่ะ  อยากให้ลองโทรใหม่อีกครั้ง หรือ โทรไปที หมายเลข 1323')
        confirm_template_message = TemplateSendMessage(
            alt_text='Confirm template',
            template=ConfirmTemplate(
                text='มีอะไรคุยอีกกันต่ออีกไหม ',
                actions=[
                    MessageAction(
                        label='มี',
                        text='สอบถามปัญหาอีกครั้ง'
                    ),
                    MessageAction(
                        label='ไม่มี',
                        text='เมนูหลัก'
                    )
                ]
            )
        )
        line_bot_api.reply_message(reply_token, [text_message, confirm_template_message])

    if intent == 'Q2 - yes - 1 - 1':
        text_message = TextSendMessage(text='คราวหน้าที่มาพบหมอ ให้ถามหมอเรื่องการปรับยาด้วยนะคะ')
        confirm_template_message = TemplateSendMessage(
            alt_text='Confirm template',
            template=ConfirmTemplate(
                text='มีอะไรคุยอีกกันต่ออีกไหม ',
                actions=[
                    MessageAction(
                        label='มี',
                        text='สอบถามปัญหาอีกครั้ง'
                    ),
                    MessageAction(
                        label='ไม่มี',
                        text='เมนูหลัก'
                    )
                ]
            )
        )
        line_bot_api.reply_message(reply_token, [text_message, confirm_template_message])

    if intent == 'Q2 - no - 1 - 1':
        text_message = TextSendMessage(text='คราวหน้าที่มาพบหมอ ให้ถามหมอเรื่องการปรับยาด้วยนะคะ')
        confirm_template_message = TemplateSendMessage(
            alt_text='Confirm template',
            template=ConfirmTemplate(
                text='มีอะไรคุยอีกกันต่ออีกไหม ',
                actions=[
                    MessageAction(
                        label='มี',
                        text='สอบถามปัญหาอีกครั้ง'
                    ),
                    MessageAction(
                        label='ไม่มี',
                        text='เมนูหลัก'
                    )
                ]
            )
        )
        line_bot_api.reply_message(reply_token, [text_message, confirm_template_message])

    if intent == 'Q2 - no - 2 - 1':
        text_message = TextSendMessage(text='ขออภัยค่ะ  อยากให้ลองโทรใหม่อีกครั้ง หรือ โทรไปที หมายเลข 1323')
        confirm_template_message = TemplateSendMessage(
            alt_text='Confirm template',
            template=ConfirmTemplate(
                text='มีอะไรคุยอีกกันต่ออีกไหม ',
                actions=[
                    MessageAction(
                        label='มี',
                        text='สอบถามปัญหาอีกครั้ง'
                    ),
                    MessageAction(
                        label='ไม่มี',
                        text='เมนูหลัก'
                    )
                ]
            )
        )
        line_bot_api.reply_message(reply_token, [text_message, confirm_template_message])

    if intent == 'Q3 - 1':
        text_message = TextSendMessage(text='ลงทะเบียนในระบบออนไลน์ตาม QR cord นี้คะ')
        imagemap_message = ImagemapSendMessage(
            base_url='https://sv1.picz.in.th/images/2020/10/13/OIyiBJ.png?_ignored=',
            alt_text='this is an imagemap',
            base_size=BaseSize(height=966, width=1040),
            actions=[
                URIImagemapAction(
                    link_uri='http://onelink.to/tf6v9h',
                    area=ImagemapArea(
                        x=27, y=20, width=990, height=946
                    )
                ),
            ]
        )
        line_bot_api.reply_message(reply_token, [text_message, imagemap_message])

    if intent == 'test':
        data = requests.get('https://covid19.th-stat.com/api/open/today')
        json_data = json.loads(data.text)

        Confirmed = json_data['Confirmed']  # ติดเชื้อสะสม
        Recovered = json_data['Recovered']  # หายแล้ว
        Hospitalized = json_data['Hospitalized']  # รักษาอยู่ใน รพ.
        Deaths = json_data['Deaths']  # เสียชีวิต
        NewConfirmed = json_data['NewConfirmed']  # บวกเพิ่ม

        text_message = TextSendMessage(
            text='ติดเชื้อสะสม = {} คน(+เพิ่ม{})\nหายแล้ว = {} คน\nรักษาอยู่ใน รพ. = {} คน\nเสียชีวิต = {} คน'.format(
                Confirmed, NewConfirmed, Recovered, Hospitalized, Deaths))
        line_bot_api.reply_message(reply_token, text_message)
#     if intent == 'Default Fallback Intent':
#
#         print('Default Fallback Intent')
